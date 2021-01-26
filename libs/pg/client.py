# -*- coding: utf-8 -*-
from gino import Gino

from config.config import PG_URI

kwargs = dict(
    min_size=1,
    max_size=20,
    max_queries=1000,
    max_inactive_connection_lifetime=60 * 5,
    echo=False,
)

# 新增数据库时, 在这初始化
CommonDB = Gino()
BiDB = Gino()


async def set_up_db():
    await CommonDB.set_bind(PG_URI, **kwargs)
    await BiDB.set_bind(PG_URI, **kwargs)
