import yaml
from flask import current_app
from models import db
#MYSQL_URI = 'postgresql://suhas:qwerty@localhost:5432/{}'

#MYSQL_URI = 'mysql+pymysql://root:qwerty@localhost/{}?charset=utf8'
def get_all_tenants():
	with open(r'C:\Users\I354822\PycharmProjects\PoCProject\venv\config\db.yaml') as db_file:

		tenants =  yaml.load(db_file, Loader=yaml.FullLoader)
		return tenants

def prepare_bind(tenant_name,db_url):
	if tenant_name not in current_app.config['SQLALCHEMY_BINDS']:
		current_app.config['SQLALCHEMY_BINDS'][tenant_name] = db_url

	return current_app.config['SQLALCHEMY_BINDS'][tenant_name]


def get_tenant_session(tenant_name):
	if tenant_name not in get_all_tenants():
		return None

	name = get_all_tenants()
	prepare_bind(tenant_name, name[tenant_name][0])
	engine = db.get_engine(current_app, bind=tenant_name)
	session_maker = db.sessionmaker()
	session_maker.configure(bind=engine)
	session = session_maker()
	print(session.new)
	return session
