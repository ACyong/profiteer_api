# -*- coding: utf-8 -*-
import logging
import random
from concurrent.futures.thread import ThreadPoolExecutor

from thriftpy2.transport.base import TTransportException
from tornado.concurrent import run_on_executor

from config.config import CURRENT_ENV
from libs.thrift_connector.connection_pool import ClientPool, ThriftPyCyClient


class BaseRPClient(object):
    NAME = 'BASE RPC'
    THRIFT_SERVICE = None
    RPC_SERVERS = None
    RPC_INDEX = 0
    RPC_CONNS = dict()
    FAIL_ADDRESS = set()
    executor = ThreadPoolExecutor(max_workers=50)

    @classmethod
    def __init_conn(cls, address):
        """真实建立tcp链接，并放入类缓存"""
        if not cls.THRIFT_SERVICE:
            raise Exception("子类必须写明具体服务名称")

        host, port = address.split(":")
        logging.info("{} {} start connect".format(cls.NAME, address))
        pool = ClientPool(cls.THRIFT_SERVICE, host, int(port), connection_class=ThriftPyCyClient, max_conn=1)
        logging.info("{} {} connect success".format(cls.NAME, address))
        cls.RPC_CONNS[address] = pool
        return pool

    @classmethod
    def __get_rpc_client_with_cache(cls, address):
        """从类缓存获取链接，无则新建"""
        if address not in cls.RPC_CONNS:
            if address in cls.FAIL_ADDRESS:
                return cls.get_rpc_client_ignore(address)
            return cls.__init_conn(address)
        return cls.RPC_CONNS[address]

    @classmethod
    def get_rpc_client(cls, index=None):
        """对外暴露接口，调用我获取链接"""
        if not isinstance(cls.RPC_SERVERS, list) or not cls.RPC_SERVERS:
            raise Exception("子类必须写明服务地址列表")

        address = None
        if index is None:
            address = cls.RPC_SERVERS[cls.RPC_INDEX]
            cls.RPC_INDEX = (cls.RPC_INDEX + 1) % len(cls.RPC_SERVERS)
        else:
            if 0 <= index < len(cls.RPC_SERVERS):
                address = cls.RPC_SERVERS[index]
            else:
                raise Exception("请检查rpc client下标参数.")
        return cls.__get_rpc_client_with_cache(address)

    @classmethod
    def reconnect(cls, address):
        logging.info("{} Service reconnect: {}".format(cls.NAME, address))
        try:
            cls.__init_conn(address)
        except Exception as e:
            logging.info("{} Service reconnect: {} fail: {}".format(cls.NAME, address, str(e)))

    @classmethod
    def is_alive(cls, client):
        try:
            resp = client.ping()
            status = resp == 'pong'
        except Exception:
            status = False
        return status

    @classmethod
    @run_on_executor
    def keep_alive(cls):
        cls.FAIL_ADDRESS = set()
        if not cls.RPC_CONNS:
            return
        try:
            for addr, conn in cls.RPC_CONNS.items():
                if not cls.is_alive(conn):
                    try:
                        conn.close()
                    except Exception as e:
                        logging.info("{} Service {} close fail, {}".format(cls.NAME, addr, str(e)))
                    cls.reconnect(addr)
        except Exception:
            # 防止 RPC_CONNS 字典变更引发异常
            pass

    @classmethod
    def get_rpc_client_ignore(cls, address):
        cls.RPC_CONNS.pop(address, None)
        cls.FAIL_ADDRESS.add(address)
        ip = address.split(':')[0]
        if CURRENT_ENV != "Product":
            valid_address = [item for item in cls.RPC_SERVERS if item != address]
        else:
            valid_address = [item for item in cls.RPC_SERVERS if not item.startswith(ip)]
        addr = random.choice(valid_address)
        return cls.__get_rpc_client_with_cache(addr)

    @classmethod
    @run_on_executor
    def execute(cls, func, *args, **kwargs):
        try:
            client = cls.get_rpc_client()
            if not client:
                raise Exception("{} Service is lack of conns".format(cls.NAME))
            return getattr(client, func)(*args, **kwargs)
        except TTransportException:
            address = '{}:{}'.format(client.host, client.port)
            logging.info("{} {} args: {} kwargs: {} retry".format(cls.NAME, func, str(args), str(kwargs)))
            client = cls.get_rpc_client_ignore(address)
            return getattr(client, func)(*args, **kwargs)
