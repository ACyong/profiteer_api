
# Gino基础使用
```python
增
await CompanyNoticeModel.create(title='ss')

改
c = await CompanyNoticeModel.query.gino.first()
await c.update(title='11').apply()

await CompanyNoticeModel.update.values(title='sdfsd').where(CompanyNoticeModel.title=='11').gino.all()


查
await CompanyNoticeModel.query.gino.first()
await CompanyNoticeModel.query.gino.all()
await CompanyNoticeModel.get(1)
await CompanyNoticeModel.query.where(CompanyNoticeModel.title=='sdfsd').gino.all()

query = CompanyNoticeModel.query.where(CompanyNoticeModel.title='sdfsd')
await query.where(CompanyNoticeModel.id==1).gino.all()


选择字段
await CompanyNoticeModel.select('title').gino.first()
await CompanyNoticeModel.select('title').gino.all()

生成器
await CompanyNoticeModel.query.gino.iterate()

删
await CompanyNoticeModel.delete.where(CompanyNoticeModel.title=='ss').gino.all()
await CompanyNoticeModel.delete.gino.all() == await CompanyNoticeModel.delete.gino.first()

c = await CompanyNoticeModel.query.gino.first()
await c.delete()

事务
async with db.transaction():

排序
await CompanyNoticeModel.query.order_by(CompanyNoticeModel.id).gino.first()
await CompanyNoticeModel.query.order_by(CompanyNoticeModel.id.desc()).gino.first()

distinct
await CompanyNoticeModel.query.distinct(CompanyNoticeModel.title).order_by(CompanyNoticeModel.title,CompanyNoticeModel.id.desc()).gino.all()
await CompanyNoticeModel.query.distinct(CompanyNoticeModel.title).gino.all()


join
from sqlalchemy.sql import join, outerjoin
j = join(CompanyNoticeModel, CompanyAccountModel, CompanyNoticeModel.company_account_id==CompanyAccountModel.id)
n = await CompanyNoticeModel.query.select_from(j).gino.all()


count
setattr(CompanyNoticeModel, 'count', func.count(CompanyNoticeModel.id).label('count'))
await CompanyNoticeModel.select('count').gino.all()


alise
setattr(CompanyNoticeModel, 'label', CompanyNoticeModel.id.label('id_'))
await CompanyNoticeModel.select('label').gino.all()


subquery
from sqlalchemy.sql import select
nn = select([CompanyAccountModel.id])
await CompanyNoticeModel.query.where(CompanyNoticeModel.company_account_id==nn).gino.all()

group_by
await CompanyNoticeModel.select('title').group_by(CompanyNoticeModel.title).gino.all()


limit/offset
await CompanyNoticeModel.query.limit(10).offset(2).gino.all()
```