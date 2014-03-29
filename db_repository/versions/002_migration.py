from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
django_admin_log = Table('django_admin_log', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('action_time', TIMESTAMP(timezone=True), nullable=False),
    Column('user_id', INTEGER, nullable=False),
    Column('content_type_id', INTEGER),
    Column('object_id', TEXT),
    Column('object_repr', VARCHAR(length=200), nullable=False),
    Column('action_flag', SMALLINT, nullable=False),
    Column('change_message', TEXT, nullable=False),
)

django_content_type = Table('django_content_type', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=100), nullable=False),
    Column('app_label', VARCHAR(length=100), nullable=False),
    Column('model', VARCHAR(length=100), nullable=False),
)

django_session = Table('django_session', pre_meta,
    Column('session_key', VARCHAR(length=40), primary_key=True, nullable=False),
    Column('session_data', TEXT, nullable=False),
    Column('expire_date', TIMESTAMP(timezone=True), nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['django_admin_log'].drop()
    pre_meta.tables['django_content_type'].drop()
    pre_meta.tables['django_session'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['django_admin_log'].create()
    pre_meta.tables['django_content_type'].create()
    pre_meta.tables['django_session'].create()
