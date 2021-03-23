import sqlalchemy
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from app.funcs import get_accessible_folders, update_last_change_date
from app.models import Note, AppData, Folder, User


@app.route('/')
def home():
    acc_folders = get_accessible_folders()
    return render_template(url_for('home'), folders=acc_folders, user=current_user)


@app.route('/<folder_id>', methods=['POST', 'GET'])
@login_required
def folders(folder_id):
    if not folder_id.isdigit():
        return redirect(url_for('home'))

    if request.method == 'GET':
        query = ''
    else:
        query = request.form.get('search-note')

    acc_folders = get_accessible_folders()

    notes = Note.query.filter(Note.folder_id == folder_id) \
        .filter(Note.header.like('%' + query.lower() + '%')).all()

    empty = ''
    if not notes:
        empty = "В этой папке нет ни одной заметки..."

    return render_template('folders.html', folders=acc_folders, notes=notes,
                           current_folder=Folder.query.filter(Folder.id == folder_id).first(), empty=empty,
                           user=current_user, query=query)


@app.route('/add_note/<folder_id>', methods=['POST', 'GET'])
@login_required
def add_note(folder_id):
    if request.method == 'GET':
        return render_template('add_note.html', user=current_user)

    header, text = request.form.get('note-name').lower(), request.form.get('note-text')

    tags_d = {'important': 'важное', 'education': 'учеба',
              'work': 'работа', 'fun': 'развлечения', 'thoughts': 'мысли'}
    tags = ' '.join([tags_d[i] for i in tags_d.keys() if request.form.get(i)])
    if not tags:
        tags = ''
    new_note = Note(header=header, text=text, folder_id=folder_id, tags=tags)

    db.session.add(new_note)
    db.session.commit()

    update_last_change_date()
    return redirect('/' + folder_id)


@app.route('/del/<folder_id>/<note_id>')
@login_required
def del_note(folder_id, note_id):
    to = 'manage_folders'
    if int(note_id) != -1:
        [db.session.delete(note) for note in
         Note.query.filter(Note.id == note_id).all()]
        db.session.commit()
        to = str(folder_id)
    else:
        folder = Folder.query.filter(Folder.id == folder_id).first()
        db.session.delete(folder)
        [db.session.delete(note) for note in Note.query.filter(Note.folder_id == folder_id).all()]
        db.session.commit()

    update_last_change_date()
    return redirect('/' + to)


@app.route('/edit/<note_id>', methods=['POST', 'GET'])
@login_required
def edit_note(note_id):
    founded_note = Note.query.filter(Note.id == note_id).first()
    if request.method == 'GET':
        return render_template('edit_note.html', note=founded_note, user=current_user)

    new_header = request.form.get('note-name').lower()
    new_text = request.form.get('note-text')
    tags_d = {'important': 'важное', 'education': 'учеба', 'work': 'работа', 'fun': 'развлечения', 'thoughts': 'мысли'}
    new_tags = ' '.join([tags_d[i] for i in tags_d.keys() if request.form.get(i)])
    founded_note.header = new_header
    founded_note.text = new_text
    founded_note.tags = new_tags
    db.session.commit()
    update_last_change_date()
    return redirect('/' + str(founded_note.folder_id))


@app.route('/settings')
@login_required
def settings():
    acc_folders_ = [int(folder.id) for folder in get_accessible_folders()]
    all_notes = Note.query.filter(Note.folder_id.in_(acc_folders_)).all()
    notes_cnt = len(all_notes)
    folders_cnt = len(acc_folders_)
    date = AppData.query.first()
    date = date.last_change_date if date and date.last_change_date else "Изменений не было"

    return render_template('settings.html', last_change_date=date, notes_cnt=notes_cnt, folders_cnt=folders_cnt,
                           user=current_user)


@app.route('/manage_folders', methods=['POST', 'GET'])
@login_required
def manage_folders():
    if request.method == 'GET':
        query = ''
    else:
        query = request.form.get('search-folder')

    acc_folders = Folder.query.filter(Folder.acc_users.contains(current_user.id)) \
        .filter(Folder.name.like('%' + query.lower() + '%')).all()

    return render_template('manage_folders.html', folders=acc_folders, user=current_user, query=query)


@app.route('/create_folder', methods=['POST', 'GET'])
@login_required
def create_folder():
    if request.method == 'GET':
        return render_template('create_folder.html', user=current_user)

    folder_name = request.form.get('folder-name').lower()
    new_folder = Folder(name=folder_name, acc_users=str(current_user.id))
    db.session.add(new_folder)
    db.session.commit()
    update_last_change_date()
    return redirect('/' + str(new_folder.id))


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    if current_user.is_authenticated:
        return redirect('/')
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
        else:
            flash("Логин или пароль неверный!")
    else:
        flash("Введите логин и пароль!")
    return render_template('login.html', user=current_user)


@app.route('/register', methods=['POST', 'GET'])
def register_page():
    if current_user.is_authenticated is False:
        login = request.form.get('login')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        name = request.form.get('name')
        surname = request.form.get('surname')
        if request.method == 'POST':
            if not (login or password or password2):
                flash("Заполните все поля!")
            elif password != password2:
                flash("Пароли не совпадают!")
            else:
                hash_pwd = generate_password_hash(password)
                new_user = User(login=login, password=hash_pwd, name=name, surname=surname, email=email)
                try:

                    db.session.add(new_user)
                    db.session.commit()
                    login_user(new_user)
                    return redirect('/')
                except sqlalchemy.exc.IntegrityError:
                    flash("Аккаунт с такой почтой уже существует!")

        return render_template('register.html', user=current_user)
    return redirect('/')


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout_page():
    logout_user()
    return redirect(url_for('login_page'))


@app.route('/profile')
@login_required
def profile():
    info_lst = {'Телефон': current_user.phone,
                'Страна': current_user.country, 'Город': current_user.city, 'Пол': current_user.sex}

    return render_template('profile.html', user=current_user, info_lst=info_lst)


@app.route('/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    if request.method == 'GET':
        return render_template('edit_profile.html', user=current_user)
    current_user.name = request.form.get('name')
    current_user.surname = request.form.get('surname')
    current_user.sex = request.form.get('sex')
    current_user.country = request.form.get('country')
    current_user.city = request.form.get('city')
    current_user.phone = request.form.get('phone')
    current_user.email = request.form.get('email')
    db.session.commit()
    return redirect('/profile')


@app.route('/about')
def about():
    return render_template('about.html', user=current_user)


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)
    return response

# views
# # Created by Sergey Yaksanov at 27.02.2021
# Copyright © 2020 Yakser. All rights reserved.
