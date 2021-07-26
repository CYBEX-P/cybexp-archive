import logging
import pdb
import json
import loadconfig

from tahoe import Instance, Raw, MongoBackend

_BACKEND = loadconfig.get_tahoe_backend()
Instance._backend = _BACKEND

def parsemain(typtag, orgid, timezone, data):
    try:
        raw_sub_type = {
            "unr_honeypot": "unr_honeypot",
        }.get(typtag, None)
        if raw_sub_type is None:
            raw_sub_type = typtag
        try:
            _ = json.loads(data)
        except:
            data = json.dumps({'data': data})
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
