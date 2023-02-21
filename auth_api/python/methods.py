# These functions need to be implemented
import pymysql
import hashlib
import os
import jwt
import json

from dotenv import load_dotenv

#loading env vars
load_dotenv()
class Token:

    def generate_token(self, username, password):
        db = Database()
        sec = Sec()
        conexion = db.connect()
        valid_user = sec.validate_user(username, password, conexion)
        print('USERS')
        print(valid_user)
        if(len(valid_user)==1):
            return sec.to_jwt({'role': valid_user[0][3]})
        else:
            return 'Error 203: Incorrect username or password'

class Restricted:

    def access_data(self, authorization):
        try:
            data = jwt.decode(authorization, os.environ.get("SECRET"), algorithms=["HS256"])
            if( 'role' in data ):
                print(data)
                #Validate if role exist
                return 'You are under protected data'
            else: 
                print(data)
                return 'Token error'
        except Exception as e:
            return 'Token error'

class Database:
    def connect(self):
        return pymysql.connect(
            host=os.environ.get("HOST_DB"),
            user=os.environ.get("USER_DB"), 
            password=os.environ.get("PASSWORD_DB"), 
            db=os.environ.get("NAME_DB")
            )

class Sec:
    def hashing(self, pw, salt):
        return hashlib.sha512((pw+salt).encode('utf-8')).hexdigest()

    def validate_user(self, username, password, conexion):
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM users")
                users = cursor.fetchall()

                return self.usr_map(username, password, users)
        except Exception as e:
            print(e)

            
    def usr_map(self, username, password, users):
        return list (
            filter(
                lambda user: 
                    username == user[0] 
                    and 
                    self.hashing(password, user[2]) == user[1] 
                ,
                users
            )
        )

    def to_jwt(self, data):
        return jwt.encode(data, os.environ.get("SECRET"), algorithm="HS256")