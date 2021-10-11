from flask_app import app
import os
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from flask import flash,session
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_bcrypt import Bcrypt

from flask_app import ALLOWED_EXTENSIONS

bcrypt = Bcrypt(app)

class User():
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.picture = data['picture']
        self.fav_genre = data['fav_genre']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('songs').query_db(query)

        users = []

        for user in results:
            users.append(cls(user))
        print(user)
        return users

    @classmethod
    def show_single_user(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('songs').query_db(query,data)
        user = cls(results[0])
        print(user)
        return user
    
    @classmethod
    def add_user(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(hashed_pw)s);"
        return connectToMySQL('songs').query_db(query,data)

    @staticmethod
    def user_validator(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 3:
            flash("First name needs to be at least 2 character.")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name needs to be at least 2 character.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Email is invalid!")
            is_valid = False
        if len(data['password'])  < 8:
            flash('Password must be at least 8 characters.')
            is_valid = False
        if len(data['verify_password'])  < 8:
            flash('Verify password must be at least 8 characters.')
            is_valid = False
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('songs').query_db(query,data)
        if len(results) != 0:
            flash("Email already exists.Please try logging in.")
            is_valid = False
        if data['password'] != data['verify_password']:
            flash("Passwords must match")
            is_valid = False
        if data['picture'] == '':
            data['picture'] == 'default_profile_pic.jpeg'
        return is_valid
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('songs').query_db(query,data)
        if len(results) < 1:
            return False 
        return cls(results[0])
    
    @classmethod
    def edit_user(cls,data):
        query = "UPDATE users SET first_name = %(first_name)s,last_name = %(last_name)s,email = %(email)s,password = %(password)s, fav_genre = %(fav_genre)s,picture = %(picture)s WHERE id = %(id)s;"
        results = connectToMySQL('songs').query_db(query,data)
        print(results)
        return results

    @classmethod
    def destroy_user(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        results = connectToMySQL('songs').query_db(query,data)
        print(results)
        return results

    @classmethod
    def user_validator2(cls,data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 3:
            flash("First name needs to be at least 2 character.")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name needs to be at least 2 character.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Email is invalid!")
            is_valid = False
        if len(data['password'] or ['verify_password']) == 0:
            flash('Passwords must be filled out.')
            is_valid = False
        query2 = "SELECT * FROM users WHERE id = %(id)s;"
        results2 = connectToMySQL('songs').query_db(query2,data)
        user2 = cls(results2[0])
        print(user2)
        if data['email'] != session['user_email']:
            query = "SELECT * FROM users WHERE email = %(email)s;"
            results = connectToMySQL('songs').query_db(query,data)  
            if len(results) != 0:
                flash("Email already in use. Please try a different email")
                is_valid = False
        if data['password'] != data['verify_password']:
            flash("Passwords must match")
            is_valid = False
        EXT = {'.jpeg','.jpg','.png'}
        root_ext = os.path.splitext(data['picture'])
        if root_ext[1] not in EXT:
            flash('File type must be jpg, jpeg, or png')
            is_valid = False
        return is_valid