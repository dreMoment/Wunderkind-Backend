# app/config.py
import os


#Below is my personal db
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://wunderkind_user:toor1234@192.168.1.38:3307/wunderkind'

#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://grossm_virtual_teacher2:PnUzaZmnsZ2ir1gHpxVFneBl@mysql.inf.ethz.ch/grossm_virtual_teacher2'
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://grossm_virtual_teacher2:PnUzaZmnsZ2ir1gHpxVFneBl@mysql.inf.ethz.ch/3306'


SECRET_KEY = 'secretkey'
JWT_SECRET_KEY = 'jwt-secret-key'
JWT_ACCESS_TOKEN_EXPIRES = False
