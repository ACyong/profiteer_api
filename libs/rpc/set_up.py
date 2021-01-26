# -*- coding: utf-8 -*-
import random

from tornado import ioloop

from libs.rpc.user.sync_client import UserRPClient


RPC_CLIENTS = [UserRPClient, ]
DELAYTIME = 5


def set_up_rpc_timer():
    delay = DELAYTIME + random.randint(1, 3)
    ioloop.PeriodicCallback(_set_up_rpc_timer, delay*100).start()


def _set_up_rpc_timer():
    for client in RPC_CLIENTS:
        client.keep_alive()
