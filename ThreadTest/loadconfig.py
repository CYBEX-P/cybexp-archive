import gridfs
import json
import logging
import os
import pdb
import pymongo
import sys

import tahoe

default = {
    "archive" : { 
        "mongo_url" : "mongodb://localhost:27017/",
        "archive_db" : "tahoe_db",
        "archive_coll": "instance",
        "tahoe_db": "tahoe_db",
        "tahoe_coll": "tahoe_coll"
    },
    "cache" : {
        "mongo_url" : "mongodb://localhost:27017/",
        "cache_db" : "cache_db",
        "cache_coll": "file_entries"
    }
}


def get_config(filename='config.json'):
    """Read config from file `config.json`."""
  
    try:
        #this_dir = os.path.dirname(__file__)
        #filename = os.path.join(this_dir, filename)
        with open(filename, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        config = default
        logging.warning("No config file found, using default config")
    except json.decoder.JSONDecodeError:
        logging.error("Bad configuration file!", exc_info=True)
        sys.exit(1) # 1 = error in linux

    for k, v in default.items():
        if k not in config:
            config[k] = v

    return config


def get_archiveconfig(filename='config.json'):
    """Configuration of Identity Backend."""
  
    config = get_config(filename)
    archiveconfig = config['archive']
    for k, v in default['archive'].items():
        if k not in archiveconfig:
            archiveconfig[k] = v
    return archiveconfig
      

def get_apiconfig(filename='config.json'):
    """Configuration of API."""
    
    config = get_config(filename)
    apiconfig = config['api']
    
    for k, v in default['api'].items():
        if k not in apiconfig:
            apiconfig[k] = v
    return apiconfig
        

def get_identity_backend(filename='config.json'):
    archiveconfig = get_archiveconfig(filename)
    mongo_url = archiveconfig['mongo_url']
    dbname = archiveconfig['identity_db']
    collname = archiveconfig['identity_coll']
    backend = tahoe.identity.IdentityBackend(mongo_url, dbname, collname)
    return backend


def get_report_backend(filename='config.json'):
    archiveconfig = get_archiveconfig(filename)
    mongo_url = archiveconfig['mongo_url']
    dbname = archiveconfig['report_db']
    collname = archiveconfig['report_coll']
    backend = tahoe.MongoBackend(mongo_url, dbname, collname)
    return backend


def get_tahoe_backend(filename='config.json'):
    archiveconfig = get_archiveconfig(filename)
    mongo_url = archiveconfig['mongo_url']
    dbname = archiveconfig['tahoe_db']
    collname = archiveconfig['tahoe_coll']
    backend = tahoe.MongoBackend(mongo_url, dbname, collname)
    return backend

get_archive_backend = get_tahoe_backend

##def get_archive_backend(filename='config.json'):
##    archiveconfig = get_archiveconfig(filename)
##    mongo_url = archiveconfig['mongo_url']
##    dbname = archiveconfig['archive_db']
##    collname = archiveconfig['archive_coll']
##    backend = tahoe.MongoBackend(mongo_url, dbname, collname)
##    return backend

def get_cacheconfig(filename='config.json'):
    """Configuration of Identity Backend."""
  
    config = get_config(filename)
    archiveconfig = config['cache']
    for k, v in default['cache'].items():
        if k not in archiveconfig:
            archiveconfig[k] = v
    return archiveconfig


def get_cache_db(filename='config.json'):
    cacheconfig = get_cacheconfig(filename)
    mongo_url = cacheconfig['mongo_url']
    dbname = cacheconfig['cache_db']
    collname = cacheconfig['cache_coll']
    
    client = pymongo.MongoClient(mongo_url, connect=False)
    db = client.get_database(dbname)
    coll = db.get_collection(collname)
    fs = gridfs.GridFS(db)

    return coll, fs
























