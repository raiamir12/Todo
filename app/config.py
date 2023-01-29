"""Config Database"""
MSSQL = {'host': 'dbhost',
         'user': 'dbuser',
         'passwd': 'dbPwd',
         'db': 'db'}

POSTGRES = {'host': 'localhost',
         'user': 'postgres',
         'passwd': 'postgres',
         'db': 'mydb'}


MSSQL_ONFIG = (f"mssql+pyodbc://{MSSQL['user']}:{MSSQL['passwd']}@{MSSQL['host']}:1433/{ MSSQL['db']}?driver=SQL+Server+Native+Client+10.0")
# POSTGRES_CONFIG =(f"postgresql+psycopg2://{POSTGRES['user']}:{POSTGRES['passwd']}@{POSTGRES['passwd']}/{POSTGRES['db']}")
POSTGRES_CONFIG = "postgresql+psycopg2://{}:{}@{}/{}".format(POSTGRES['user'], POSTGRES['passwd'], POSTGRES['host'], POSTGRES['db'])