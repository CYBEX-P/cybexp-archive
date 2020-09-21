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



S_SUCCESS = 0
S_NOT_SUPPORTED = 1
S_ERROR = 2

def parsemain(typtag, orgid, timezone, data):
    """
    returns
    -------
    state: 
        returns errors codes of success codes.
    raw(tahoe.Raw):
        return the raw tahow object if successful. else is None
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
            return S_NOT_SUPPORTED, raw

        return S_SUCCESS, raw
    except:
        logging.error("\nproc.archive.parsemain -- " + str(typtag), exc_info=True)
        return S_ERROR, None