# -*- coding:utf-8 -*-
import os
from configparser import ConfigParser

try:
    CONFIG_PATH = os.environ.get('PROFITEER_API_CONFIG_PATH')
except Exception:
    raise ValueError


config = ConfigParser()
config.read(CONFIG_PATH)

# ENV
ENV = config["ENV"]
CURRENT_ENV = ENV.get("CURRENT_ENV")


# gevent 配置
GEVENT = config["GEVENT"]
GEVENT_POOL_SIZE = int(GEVENT.get("GEVENT_POOL_SIZE", "20"))


# PG
PG = config["PG"]
PG_POOL_SIZE = int(PG.get("PG_POOL_SIZE", "20"))
PG_MAX_OVER = int(PG.get("PG_MAX_OVER", "10"))
PG_POOL_RECYCLE = int(PG.get("PG_POOL_RECYCLE", "3600"))
PG_POOL_TIMEOUT = int(PG.get("PG_POOL_TIMEOUT", "500"))
PG_URI = PG.get("PG_URI")


# MongoDB
MONGO = config["MONGO"]
MONGO_POOL_SIZE = MONGO.get("MONGO_POOL_SIZE")
MONGO_TIMEOUT = MONGO.get("MONGO_TIMEOUT")
MONGO_CONNECT_TIMEOUT = MONGO.get("MONGO_CONNECT_TIMEOUT")
MONGO_URI = MONGO.get("MONGO_MAIN_URI")


# Redis
REDIS = config["REDIS"]
REDIS_POOL_SIZE = REDIS.get("REDIS_POOL_SIZE")
REDIS_TIMEOUT = REDIS.get("REDIS_TIMEOUT")
REDIS_CONNECT_TIMEOUT = REDIS.get("REDIS_CONNECT_TIMEOUT")
REDIS_URI = REDIS.get("REDIS_URI")


# user PRC
RPC = config["RPC"]
USER_RPC_SERVERS = RPC.get("USER_RPC_SERVERS").split(',')
