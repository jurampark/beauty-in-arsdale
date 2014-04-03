from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
interest = Table('interest', post_meta,
    Column('key', Integer, primary_key=True, nullable=False),
    Column('user_key', Integer),
    Column('product_key', Integer),
    Column('set_key', Integer),
    Column('is_set', Boolean, default=ColumnDefault(False)),
    Column('created_time', DateTime, default=ColumnDefault(<sqlalchemy.sql.functions.now at 0x3614fd0; now>)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['interest'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['interest'].drop()
