from flask_app import app
from flask import render_template, redirect, request,session
from flask_app.models.user import User
from flask_app.models.song import Song

@app.route('/create/song', methods = ['POST'])
def create_song():
    if 'user_id' not in session:
        return redirect ('/dashboard')
    if not Song.song_validator(request.form):
        return redirect('/dashboard')
    data = {
        "song_name":request.form['song_name'],
        "artist_name":request.form['artist_name'],
        "description":request.form['description'],
        "genre":request.form['genre'],
        "user_id":session["user_id"]
    }
    Song.add_song(data)
    return redirect('/dashboard')

@app.route('/destroy/song/<int:id>')
def destroy_song(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id':id
    }
    Song.destroy_song(data)
    return redirect('/dashboard')

@app.route('/edit/song/<int:id>')
def get_to_edit_page(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id,
        "user_id":session['user_id']
    }
    user_data = {
        "id":session["user_id"]
    }
    return render_template('edit.html', users = User.show_single_user(user_data),song = Song.show_single_song(data))

@app.route('/edit_song', methods = ['POST'])
def edit_song():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Song.song_validator(request.form):
        return redirect('/dashboard')
    data = {
        "id": request.form['id'], 
        "song_name":request.form['song_name'],
        "artist_name":request.form['artist_name'],
        "description":request.form['description'],
        "genre":request.form['genre']
    }
    Song.edit_song(data)
    return redirect('/dashboard')