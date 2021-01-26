# -*- coding: utf-8 -*-
import argparse
import asyncio
import logging
from datetime import datetime

import tornado
from tornado.web import Application, access_log

from apps.urls import urls
from config.config import CURRENT_ENV
from libs.pg.client import set_up_db
from libs.rpc.set_up import set_up_rpc_timer

access_logger = logging.getLogger('tornado.access')
access_logger.setLevel(logging.INFO)


def make_app(model):
    debug = False if CURRENT_ENV == "Product" else True
    return Application(
        urls.get(model), log_function=log_func, debug=debug
    )


def log_func(handler):
    if handler.get_status() < 400:
        log_method = access_log.info
    elif handler.get_status() < 500:
        log_method = access_log.warning
    else:
        log_method = access_log.error
    request_time = 1000.0 * handler.request.request_time()
    msg = "%s %d %s %s (%s) %s %s %.2fms" % (
        datetime.now(), handler.get_status(), handler.request.method,
        handler.request.uri, handler.request.remote_ip,
        handler.request.headers.get("User-Agent") or '',
        handler.request.arguments, request_time)
    log_method(msg)


parser = argparse.ArgumentParser()
parser.add_argument('-H', '--host', help="server listen host")
parser.add_argument('-P', '--port', type=int, help="server listen port")
parser.add_argument('-M', '--model', type=str, help="server model")


if __name__ == "__main__":
    args = parser.parse_args()
    if not args.host or not args.port or not args.model:
        raise Exception("please enter host and port and model")
    asyncio.ensure_future(set_up_db())
    app = make_app(args.model)
    set_up_rpc_timer()
    app.listen(args.port, args.host, xheaders=True)
    tornado.ioloop.IOLoop.current().start()
