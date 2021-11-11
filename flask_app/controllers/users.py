import os
from flask_app import app 
from flask import render_template,redirect,request,flash,session,url_for
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.song import Song
from flask_app import ALLOWED_EXTENSIONS
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/register', methods = ['POST'])
def register_user():
    data = {
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':request.form['password'],
        'verify_password':request.form['verify_password']
    }
    valid = User.user_validator(data)
    if valid:
        hashed_pw = bcrypt.generate_password_hash(request.form['password'])
        data['hashed_pw'] = hashed_pw
        user = User.add_user(data)
        user_email = User.get_by_email(data)
        session['user_email'] = user_email.email
        session['user_picture'] = user_email.picture
        session['user_id'] = user
        print('User logged in.')
    return redirect('/dashboard')
@app.route('/user/login', methods = ['POST'])
def login_user():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid email or password")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid email or password")
        return redirect('/')
    session['user_id'] = user.id
    session['user_email'] =user.email
    session['user_picture'] = user.picture
    print("Successful login")
    return redirect ('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id" : session['user_id'],
        }
    image_file = url_for('static', filename ='profile_pics/')
    return render_template('dashboard.html', all_songs = Song.get_all_with_users(),users = User.show_single_user(data),image_file = image_file)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/users/<int:id>')
def show_user_fav_songs(id):
    if "user_id" not in session:
        return redirect('/logout')
    logged_in_user_data = {
        'id':session['user_id']
    }
    users = {
        "id":id
    }
    image_file = url_for('static', filename ='profile_pics/')
    return render_template("single_user.html",users = User.show_single_user(users), user_logged_in = User.show_single_user(logged_in_user_data),
    all_songs = Song.show_user_fav_songs(users),image_file = image_file)

@app.route('/user/<int:id>')
def show_user_edit_page(id):
    if "user_id" not in session:
        return redirect('/logout')
    image_file = url_for('static', filename ='profile_pics/')
    data = {
        "id":session["user_id"]
    }
    return render_template("edit_profile.html", user = User.show_single_user(data), image_file = image_file)

def allowed_file(profile_pics):
    return '.' in profile_pics and \
        profile_pics.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/edit_user/<int:id>', methods = ['GET','POST'])
def edit_user(id):
    if request.method == 'POST':
        if 'picture' not in request.files:
            flash('No file Part')
            return redirect('/user/<int:id>')
        file = request.files['picture']
        if file.filename =='':
            flash('Please select file')
            return redirect(f'/user/{id}')
        if file and allowed_file(file.filename):
            profile_pics = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],profile_pics))
        data = {
            'id':id,
            'first_name':request.form['first_name'],
            'last_name':request.form['last_name'],
            'email':request.form['email'],
            'password':request.form['password'],
            'verify_password':request.form['verify_password'],
            'fav_genre':request.form['fav_genre'],
            'picture':request.files['picture'].filename
        }
        valid = User.user_validator2(data)
        session['user_picture'] = request.files['picture'].filename
        if not valid:
            return redirect(f'/user/{id}')
        print(valid)
        if valid:
            hashed_pw = bcrypt.generate_password_hash(request.form['password'])
            data['hashed_pw'] = hashed_pw
            user = User.edit_user(data)
            print(user)
            print('User Updated')
            return redirect('/dashboard')
    
@app.route('/destroy/user/<int:id>')
def destroy_user(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    User.destroy_user(data)
    return redirect('/')



    
    
    
