from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
auth_group = Table('auth_group', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String, nullable=False),
)

auth_group_permissions = Table('auth_group_permissions', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('group_id', Integer, nullable=False),
    Column('permission_id', Integer, nullable=False),
)

auth_permission = Table('auth_permission', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String, nullable=False),
    Column('content_type_id', Integer, nullable=False),
    Column('codename', String, nullable=False),
)

auth_user = Table('auth_user', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('password', String, nullable=False),
    Column('last_login', DateTime, nullable=False),
    Column('is_superuser', Boolean, nullable=False),
    Column('username', String, nullable=False),
    Column('first_name', String, nullable=False),
    Column('last_name', String, nullable=False),
    Column('email', String, nullable=False),
    Column('is_staff', Boolean, nullable=False),
    Column('is_active', Boolean, nullable=False),
    Column('date_joined', DateTime, nullable=False),
)

auth_user_groups = Table('auth_user_groups', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer, nullable=False),
    Column('group_id', Integer, nullable=False),
)

auth_user_user_permissions = Table('auth_user_user_permissions', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer, nullable=False),
    Column('permission_id', Integer, nullable=False),
)

django_admin_log = Table('django_admin_log', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('action_time', DateTime, nullable=False),
    Column('user_id', Integer, nullable=False),
    Column('content_type_id', Integer),
    Column('object_id', Text),
    Column('object_repr', String, nullable=False),
    Column('action_flag', SmallInteger, nullable=False),
    Column('change_message', Text, nullable=False),
)

django_content_type = Table('django_content_type', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String, nullable=False),
    Column('app_label', String, nullable=False),
    Column('model', String, nullable=False),
)

django_session = Table('django_session', pre_meta,
    Column('session_key', String, primary_key=True, nullable=False),
    Column('session_data', Text, nullable=False),
    Column('expire_date', DateTime, nullable=False),
)

polls_choice = Table('polls_choice', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('poll_id', Integer, nullable=False),
    Column('choice_text', String, nullable=False),
    Column('votes', Integer, nullable=False),
)

polls_poll = Table('polls_poll', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('question', String, nullable=False),
    Column('pub_date', DateTime, nullable=False),
)

products = Table('products', post_meta,
    Column('key', Integer, primary_key=True, nullable=False),
    Column('product_name', String, nullable=False),
    Column('product_id', Integer, nullable=False),
    Column('product_type', String(length=2)),
    Column('product_desc', String),
    Column('product_big_img', String(length=255)),
    Column('product_small_img', String(length=255)),
    Column('video_review_url', String(length=255)),
    Column('blog_review_list_id', Integer),
    Column('product_brand', String(length=255)),
    Column('product_capacity', Integer),
    Column('product_price', Integer),
    Column('product_fit_for', String(length=1)),
    Column('product_color', String(length=10)),
    Column('product_color_rgb', String(length=10)),
    Column('product_get_it_beauty_rank', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['auth_group'].drop()
    pre_meta.tables['auth_group_permissions'].drop()
    pre_meta.tables['auth_permission'].drop()
    pre_meta.tables['auth_user'].drop()
    pre_meta.tables['auth_user_groups'].drop()
    pre_meta.tables['auth_user_user_permissions'].drop()
    pre_meta.tables['django_admin_log'].drop()
    pre_meta.tables['django_content_type'].drop()
    pre_meta.tables['django_session'].drop()
    pre_meta.tables['polls_choice'].drop()
    pre_meta.tables['polls_poll'].drop()
    post_meta.tables['products'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['auth_group'].create()
    pre_meta.tables['auth_group_permissions'].create()
    pre_meta.tables['auth_permission'].create()
    pre_meta.tables['auth_user'].create()
    pre_meta.tables['auth_user_groups'].create()
    pre_meta.tables['auth_user_user_permissions'].create()
    pre_meta.tables['django_admin_log'].create()
    pre_meta.tables['django_content_type'].create()
    pre_meta.tables['django_session'].create()
    pre_meta.tables['polls_choice'].create()
    pre_meta.tables['polls_poll'].create()
    post_meta.tables['products'].drop()
