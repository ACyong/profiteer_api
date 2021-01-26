# -*- coding: utf-8 -*-
import os

import thriftpy2

from config.config import USER_RPC_SERVERS
from libs.rpc.base import BaseRPClient


path = os.path.join(
    os.path.dirname(__file__),
    'user.thrift'
)


user_thrift = thriftpy2.load(path, module_name='user_thrift')


class UserRPClient(BaseRPClient):
    THRIFT_SERVICE = user_thrift.UserService
    RPC_SERVERS = USER_RPC_SERVERS

    @classmethod
    async def create_user(cls, user_id, payload):
        """user表中新增记录"""
        user = user_thrift.User(**payload)
        await cls.execute('createUser', user_id, user)
