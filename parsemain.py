import logging
import pdb
import loadconfig

from tahoe import Instance, Raw, MongoBackend

if __name__ == "__main__":
    _BACKEND = loadconfig.get_tahoe_backend()
    Instance._backend = _BACKEND

def set_backend(config_loc):
    _BACKEND = loadconfig.get_tahoe_backend(config_loc)
    Instance._backend = _BACKEND

def parsemain(typtag, orgid, timezone, data):
    """
    This function takes the provided parameters and passes them to be made into a raw
    TAHOE instance that holds the tags and data.
    ----------
    typtag: String
        tag that indicates the type of data
        Example: a typetag can be labeled a tahoe 'attribute'
    orgid: String
        name of the source or organizations
    timezone: String
        the indiciated timezone
    data: Dictionary or Large list of Strings
        the raw unprocessed data
    

    """
    try:
        raw_sub_type = {
            "unr-honeypot": "unr_honeypot",
        }.get(typtag, None)
        if raw_sub_type:
            raw = Raw(raw_sub_type, data, orgid, timezone)
        else:
            raw = None
            logging.warning(
                "\nproc.archive.parsemain -- Unknown typtag : " + str(typtag)
            )
        return raw
    except:
        logging.error("\nproc.archive.parsemain -- " + str(typtag), exc_info=True)
