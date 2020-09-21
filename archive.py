

import io, time, gridfs, logging, json, copy, random, multiprocessing, os, pdb
from pymongo import MongoClient
from pymongo.errors import CursorNotFound
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import sys
from pathlib import Path
import argparse

import parsemain
from parsemain import parsemain
import loadconfig


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


def archive_one(event, cache_coll, fs, pkey_fp, parsemain):
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

        state, raw = parsemain(typetag, orgid, timezone, data)

        if state == parsemain.S_SUCCESS:
            cache_coll.update_one(
                {"_id": event["_id"]},
                {"$set": {"processed": True}, "$addToSet": {"_ref": raw._hash}, {"$unset": {"special":1, "state":1}}},
            )
            return True
        elif state == parsemain.S_NOT_SUPPORTED:
            cache_coll.update_one(
                {"_id": event["_id"]},
                {"$set": {"processed": False}, "$set": {"state": "typetag_not_supported", "special": True}},
            )
            return False
        elif state == parsemain.S_ERROR:
            cache_coll.update_one(
                {"_id": event["_id"]},
                {"$set": {"processed": False}, "$set": {"state": "server_error", "special": True}},
            )
            return False
        return False # catch all
    except gridfs.errors.CorruptGridFile:
        cache_coll.update_one(
            {"_id": event["_id"]},
            {"$set": {"processed": False}, "$set": {"state": "bad_data", "special": True}},
        )
        return False

    except (KeyboardInterrupt, SystemExit):
            raise
        
    except:
        logging.error("proc.archive.archive_one: -- ", exc_info=True)
        return False


def archive(cacheconfig, force_process=False, exec_once=False):
    n_failed_attempts = 0
    while True:
        try:
            cache_mongo_url = cacheconfig.pop("mongo_url")
            cache_client = MongoClient(cache_mongo_url)
            cache_db = cache_client.get_database(
                cacheconfig.pop("cache_db", "cache_db"))
            cache_coll = cache_db.get_collection(
                cacheconfig.pop("cache_coll", "file_entries"))
            fs = gridfs.GridFS(cache_db)
            private_key_file_path = cacheconfig.pop("private_key", "priv.pem")
            

            from parsemain import parsemain  # don't move to top

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
            if force_process:
                query = {"processed": False, "special": False}
            else:
                query = {"processed": False}
            cursor = cache_coll.find(query).limit(10000)
            #cursor = cache_coll.find({"processed": False,"typtag":"unr-honeypot"}).limit(120)
            any_success = False
            for e in cursor:
                s = archive_one(e, cache_coll, fs, private_key_file_path, parsemain)
                any_success = any_success or s

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

        if exec_once:
            break


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "config_file",
        metavar="config-file",
        help="filename of JSON file containing configuration. [config.json]",
        default="config.json",
    )
    parser.add_argument(
        "--config-file",
        help="filename of JSON file containing array of configs to run. Disables connection to databse and live update.",
        default=None,
    )

    parser.add_argument(
        '-f',
        '--force-process',
        help='Force process all unprocessed data, includes previously unsuported data.',
        action='store_true',
        default=False)
    parser.add_argument(
        '-o',
        '--run-once',
        help='Do not loop undefinatelly throught the database, just do it once and exit.',
        action='store_true',
        default=False)

    args = parser.parse_args()
    
    conf_path = Path(args.config_file).resolve()
    if not conf_path.is_file():
            parser.error("{} does not exist or is not a file".format(conf_path))


    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s %(levelname)s:%(message)s"
    )  # filename = 'archive.log',

    try:
        cacheconfig = loadconfig.get_cacheconfig(conf_path)
        parsemain.set_backend(conf_path)
    except:
        logging.error(
                "proc.archive.archive: Bad Archive Config -- ",
                exc_info=True,
            )
        sys.exit(1)

        

    archive(copy.deepcopy(cacheconfig), args.force_process, args.run_once)





# TODO
# index "special" field in DB

