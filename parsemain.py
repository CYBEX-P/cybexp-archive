import logging
import pdb
import loadconfig
from enum import Enum

from tahoe import Instance, Raw, MongoBackend

_BACKEND = None

class ParseState(Enum):
    SUCCESS = 0
    NOT_SUPPORTED = 1
    ERROR = 2

if __name__ == "__main__": # skip execution if imported
    _BACKEND = loadconfig.get_tahoe_backend()
    Instance._backend = _BACKEND

def set_backend(config_loc):
    global _BACKEND
    _BACKEND = loadconfig.get_tahoe_backend(config_loc)
    Instance._backend = _BACKEND




def parsemain(typtag, orgid, timezone, data):
    """
    returns
    -------
    state: 
        returns errors codes or success codes.
    raw(tahoe.Raw):
        return the raw tahoe object if successful. else is None
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
            return ParseState.NOT_SUPPORTED, raw

        return ParseState.SUCCESS, raw
    except:
        logging.error("\nproc.archive.parsemain -- " + str(typtag), exc_info=True)
        return ParseState.ERROR, None

