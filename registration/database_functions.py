from .models import Database_Info
from django.core.management import call_command
from psycopg2 import connect,extensions
from TrackYourAlumni.settings import DATABASES, DEFAULT_DATABASE_ENGIN,DEFAULT_DATABASE_PASSWORD,DEFAULT_DATABASE_USERNAME,DEFAULT_DATABASE_PORT,DEFAULT_DATABASE_HOST



def db_load():
    db=Database_Info.objects.all()
    for d in db:
        temp={
            'ENGINE':DEFAULT_DATABASE_ENGIN,
            'NAME': d.db_name, 
            'USER': d.db_user, 
            'PASSWORD': d.db_password,
            'HOST': d.db_host, 
            'PORT': d.db_port,
            'CONN_HEALTH_CHECKS': False,'ATOMIC_REQUESTS': False, 'AUTOCOMMIT': True, 'CONN_MAX_AGE': 0,'OPTIONS': {},'TIME_ZONE':None
        }
        DATABASES[d.college_name]=temp
    for keys, value in DATABASES.items():
        print(keys,"--->",value,"\n\n")

def db_migrate(name):
    try:
        call_command('makemigrations')
        call_command('migrate',database=name)
        print("Migrations ran successfully for specific_database!")
        return 0
    except:
        print(Exception,"------Not scusees")
        return 1
    
    
def create_db(name):
    try:
        # TODO: please set unique host,port,user, password for each entry so that on recursive creating db attemp, it can give error on connection.
        connection = connect(host='127.0.0.1',port=5432,user='postgres',password='postgres')
        auto_commit=extensions.ISOLATION_LEVEL_AUTOCOMMIT
        connection.set_isolation_level(auto_commit)
        print(connection)
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE {name}  WITH  ENCODING 'UTF8' LC_COLLATE='en_US.UTF-8' LC_CTYPE='en_US.UTF-8' TEMPLATE template0;")
        print('success')
        return 0
    except:
        print("Db Connection Not success")
        return 1
        
    finally:
        if connection:
            connection.close()

def delete_db(name):
    try:
        # TODO: please set unique host,port,user, password for each entry so that on recursive creating db attemp, it can give error on connection.
        connection = connect(host=DEFAULT_DATABASE_HOST,port=DEFAULT_DATABASE_PORT,user=DEFAULT_DATABASE_USERNAME,password=DEFAULT_DATABASE_PASSWORD)
        auto_commit=extensions.ISOLATION_LEVEL_AUTOCOMMIT
        connection.set_isolation_level(auto_commit)
        print(connection)
        with connection.cursor() as cursor:
            cursor.execute(f"DROP DATABASE {name};")
        print('success')
        return 0
    except:
        print("Db Connection Not success")
        return 1
        
    finally:
        if connection:
            connection.close()
            
    
def db_store(temp):
    db_info={
            'ENGINE': DEFAULT_DATABASE_ENGIN,
            'NAME': temp.db_name, 
            'USER': temp.db_user, 
            'PASSWORD': temp.db_password,
            'HOST': temp.db_host, 
            'PORT': temp.db_port,
            'CONN_HEALTH_CHECKS': False,'ATOMIC_REQUESTS': False, 'AUTOCOMMIT': True, 'CONN_MAX_AGE': 0,'OPTIONS': {},'TIME_ZONE':None
        }

    print(db_info,"-----database in formation",temp.college_name,"----colege name")
    DATABASES[temp.college_name]=db_info
    temp=db_migrate(temp.college_name)
    return temp