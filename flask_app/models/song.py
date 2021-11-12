from logging import NullHandler
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
import os
import lyricsgenius
from flask import flash

class Song():
    def __init__(self,data):
        self.id = data['id']
        self.song_name = data['song_name']
        self.artist_name = data['artist_name']
        self.genre = data['genre']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM songs;"
        results = connectToMySQL('songs').query_db(query)
        
        songs = []

        for song in results:
            songs.append(cls(song))
        print(song)
        return songs

    @classmethod
    def get_all_with_users(cls):
        query = "SELECT * FROM songs LEFT JOIN users ON songs.user_id = users.id ORDER BY songs.id DESC;"
        results = connectToMySQL('songs').query_db(query)
        list = []

        for object in results:
            poster_data = {
                "id" : object['users.id'],
                "first_name": object['first_name'],
                "last_name": object['last_name'],
                "email":object['email'],
                "password":object['password'],
                "picture":object['picture'],
                "fav_genre":object['fav_genre'],
                "created_at": object["users.created_at"],
                "updated_at": object["users.updated_at"],
                "user_id":object['user_id']
            }
            t = cls(object)
            t.creator = User(poster_data)
            list.append(t)
        return list

    @classmethod
    def add_song(cls,data):
        query = "INSERT INTO songs (song_name,artist_name,description,genre,user_id) VALUES(%(song_name)s,%(artist_name)s,%(description)s,%(genre)s,%(user_id)s);"
        results = connectToMySQL('songs').query_db(query,data)
        print(results)
        return results

    @classmethod
    def destroy_song(cls,data):
        query = "DELETE FROM songs WHERE id = %(id)s;"
        results = connectToMySQL('songs').query_db(query,data)
        print(results)
        return results
    
    @classmethod
    def show_user_fav_songs(cls,data):
        query = "SELECT * FROM songs WHERE user_id = %(id)s;"
        results = connectToMySQL('songs').query_db(query,data)

        songs = []

        for song in results:
            songs.append(cls(song))
        print(songs)
        return songs

    @classmethod
    def edit_song(cls,data):
        query = "UPDATE songs SET song_name = %(song_name)s, artist_name = %(artist_name)s, description = %(description)s, genre = %(genre)s WHERE id = %(id)s"
        return connectToMySQL('songs').query_db(query,data)

    @classmethod
    def show_single_song(cls,data):
        query = "SELECT * FROM songs WHERE id = %(id)s;"
        results = connectToMySQL('songs').query_db(query,data)

        song = cls(results[0])
        print(song)
        return song

    @classmethod
    def get_songs_api(cls,data):
        query = "SELECT * FROM songs WHERE id = %(id)s"
        results = connectToMySQL('songs').query_db(query,data)
        songs = cls(results[0])
        genius = lyricsgenius.Genius(os.environ.get('API_KEY'))
        artist = genius.search_artist(songs.artist_name, max_songs = 0)
        song = genius.search_song(songs.song_name, artist.name)
        print(song.lyrics)
        return song.lyrics
    
    @classmethod
    def api_validator(cls,data):
        query = "SELECT * FROM songs WHERE id = %(id)s"
        results = connectToMySQL('songs').query_db(query,data)
        songs = cls(results[0])
        genius = lyricsgenius.Genius(os.environ.get('API_KEY'))
        artist = genius.search_artist(songs.artist_name, max_songs = 0)
        song = genius.search_song(songs.song_name, artist.name)
        is_valid = True
        if song == None:
            flash('The song lyrics do not exist. Please check the spelling. If the spelling is correct, then we apologize for the song not being in the database.', category = 'error')
            is_valid = False
        return is_valid

    @staticmethod
    def song_validator(song):
        is_valid = True
        if len(song['song_name']) == 0:
            flash("Song title must be filled out",category = 'message')
            is_valid = False
        if len(song['artist_name']) == 0:
            flash("Artist name must be filled out",category = 'message')
            is_valid = False
        if len(song['description']) == 0:
            flash("Why do you like this song? Please fill it out.", category = 'message')
            is_valid = False
        return is_valid 

    