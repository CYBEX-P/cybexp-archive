from concurrent.futures import ProcessPoolExecutor

import io, time, gridfs, logging, json, copy, random, multiprocessing, os, pdb
from pymongo import MongoClient
from pymongo.errors import CursorNotFound
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from parsemain import parsemain, set_backend
import sys

import loadconfig


_CACHE_COLL = None
_FS = None
_PRIV_KEY_PATH = None


def decrypt_file(file_in, fpriv_name="priv.pem"):
    if isinstance(file_in, bytes):
        file_in = io.BytesIO(file_in)
    private_key = RSA.import_key(open(fpriv_name).read())
    enc_session_key, nonce, tag, ciphertext = [
        file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)
    ]

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)

    return data.decode("utf-8")


def exponential_backoff(n):
    s = min(3600, (2 ** n) + (random.randint(0, 1000) / 1000))
    time.sleep(s)


def archive_one(event):
    global _CACHE_COLL
    global _FS
    global _PRIV_KEY_PATH

    cache_coll = _CACHE_COLL
    fs = _FS
    pkey_fp = _PRIV_KEY_PATH
    
    try:
        try:
            typetag = event["typetag"]
        except KeyError:
            typetag = event["typtag"]
        orgid = event["orgid"]
        #upload_time = event["timestamp"]
        timezone = event["timezone"]

        fid = event["fid"]
        f = fs.get(fid)
        data = str(decrypt_file(f))

        raw = parsemain(typetag, orgid, timezone, data)

        if raw:
            cache_coll.update_one(
                {"_id": event["_id"]},
                {"$set": {"processed": True}, "$addToSet": {"_ref": raw._hash}},
            )
            return True
        else:
            return False
    except gridfs.errors.CorruptGridFile:
        cache_coll.update_one(
            {"_id": event["_id"]},
            {"$set": {"processed": True}, "$set": {"bad_data": True}},
        )
        return False

    except (KeyboardInterrupt, SystemExit):
            raise
        
    except:
        logging.error("proc.archive.archive_one: -- ", exc_info=True)
        return False


def archive(cacheconfig):
    global _CACHE_COLL
    global _FS
    global _PRIV_KEY_PATH
    
    n_failed_attempts = 0
    while True:
        try:
            cache_mongo_url = cacheconfig.pop("mongo_url")
            cache_client = MongoClient(cache_mongo_url, maxPoolSize=1000)
            cache_db = cache_client.get_database(
                cacheconfig.pop("cache_db", "cache_db"))
            cache_coll = cache_db.get_collection(
                cacheconfig.pop("cache_coll", "file_entries"))
            fs = gridfs.GridFS(cache_db)
            private_key_file_path = cacheconfig.pop("private_key", "priv.pem")

            _CACHE_COLL = cache_coll
            _FS = fs
            _PRIV_KEY_PATH = private_key_file_path

##            from parsemain import parsemain  # don't move to top

            break

        except (KeyboardInterrupt, SystemExit):
            raise

        except:
            logging.error(
                "proc.archive.archive 1: Error connecting to database -- ",
                exc_info=True,
            )
            exponential_backoff(n_failed_attempts)
            n_failed_attempts += 1

    while True:
        try:
            cursor = cache_coll.find({"processed": False, "typtag":"unr-honeypot"}).limit(100000)

            with ProcessPoolExecutor(64) as executor:
                success = executor.map(archive_one, cursor)

            any_success = any(success)
    
            if any_success:
                n_failed_attempts = 0
            else:
                n_failed_attempts += 1
            n_failed_attempts = 0

        except CursorNotFound:
            n_failed_attempts += 1

        except (KeyboardInterrupt, SystemExit):
            raise

        except:
            logging.error("proc.archive.archive: ", exc_info=True)
            n_failed_attempts += 1

        exponential_backoff(n_failed_attempts)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.ERROR, format="%(asctime)s %(levelname)s:%(message)s"
    )
    logging.basicConfig(filename = 'archive.log')

    try:
        cacheconfig = loadconfig.get_cacheconfig(sys.argv[1])
        set_backend(sys.argv[1])
    except:
        logging.error(
                "proc.archive.archive: Bad Archive Config -- ",
                exc_info=True,
            )
        sys.exit(1)

        

    archive(copy.deepcopy(cacheconfig))
