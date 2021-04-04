from flask import Flask
from flask import make_response, jsonify
from flask import render_template, url_for, request, redirect, flash
from flask_login import LoginManager
from flask_login import login_required, current_user, login_user, logout_user
from flask_restful import Api
from werkzeug.security import generate_password_hash, check_password_hash

from data import db_session
from data import folders_resource, notes_resource
from data import users_resource
from data.email_engine import send_login_and_password, send_account_deleted, send_password_changed
from data.folder import Folder
from data.momentjs import momentjs
from data.note import Note
from data.user import User
from functions.update_last_change_date import update_last_change_date

app = Flask(__name__)
api = Api(app)
app.secret_key = "aspddmngmnvcmnjsnuiqrioperjmxvnzxbvoiafwqfoewirn"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)

app.jinja_env.globals['momentjs'] = momentjs

db_session.global_init("db/notepad.db")
api.add_resource(users_resource.UsersListResource, '/api/users')
api.add_resource(users_resource.UserResource, '/api/users/<int:user_id>')

api.add_resource(folders_resource.FolderResource, '/api/folders/<int:folder_id>')
api.add_resource(folders_resource.FoldersListResource, '/api/folders')

# only for dev
api.add_resource(notes_resource.NotesListResource, '/api/notes')
api.add_resource(notes_resource.NoteResource, '/api/notes/<int:note_id>')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def home():
    folders_ = []
    if current_user.is_authenticated:
        folders_ = current_user.folders
    return render_template('home.html', folders=folders_, user=current_user)


@app.route('/<folder_id>', methods=['POST', 'GET'])
@login_required
def folders(folder_id):
    if not folder_id.isdigit():
        return redirect(url_for('home'))

    if request.method == 'GET':
        query = ''
    else:
        query = request.form.get('search-note')
    acc_folders = current_user.folders
    session = db_session.create_session()
    notes = session.query(Note).filter(Note.folder_id == folder_id) \
        .filter(Note.header.like('%' + query.lower() + '%')).all()

    empty = ''
    if not notes:
        empty = "В этой папке нет ни одной заметки..."
    return render_template('folders.html', folders=acc_folders, notes=notes,
                           current_folder=session.query(Folder).filter(Folder.id == folder_id).first(),
                           empty=empty,
                           user=current_user, query=query)


@app.route('/add_note/<folder_id>', methods=['POST', 'GET'])
@login_required
def add_note(folder_id):
    session = db_session.create_session()
    if request.method == 'GET':
        return render_template('add_note.html', user=current_user)

    header, text = request.form.get('note-name').lower(), request.form.get('note-text')

    tags_d = {'important': 'важное', 'education': 'учеба',
              'work': 'работа', 'fun': 'развлечения', 'thoughts': 'мысли'}
    tags = ' '.join([tags_d[i] for i in tags_d.keys() if request.form.get(i)])
    if not tags:
        tags = ''
    new_note = Note(header=header, text=text, folder_id=folder_id, tags=tags)

    session.add(new_note)
    session.commit()

    update_last_change_date()
    return redirect('/' + folder_id)


@app.route('/del/<folder_id>/<note_id>')
@login_required
def del_note(folder_id, note_id):
    session = db_session.create_session()
    to = 'manage_folders'
    if int(note_id) != -1:
        [session.delete(note) for note in
         session.query(Note).filter(Note.id == note_id).all()]
        session.commit()
        to = str(folder_id)
    else:
        folder = session.query(Folder).filter(Folder.id == folder_id).first()
        session.delete(folder)
        [session.delete(note) for note in session.query(Note).filter(Note.folder_id == folder_id).all()]
        session.commit()

    update_last_change_date()
    return redirect('/' + to)


@app.route('/edit/<note_id>', methods=['POST', 'GET'])
@login_required
def edit_note(note_id):
    session = db_session.create_session()
    founded_note = session.query(Note).filter(Note.id == note_id).first()
    if request.method == 'GET':
        return render_template('edit_note.html', note=founded_note, user=current_user)

    new_header = request.form.get('note-name').lower()
    new_text = request.form.get('note-text')
    tags_d = {'important': 'важное', 'education': 'учеба', 'work': 'работа', 'fun': 'развлечения', 'thoughts': 'мысли'}
    new_tags = ' '.join([tags_d[i] for i in tags_d.keys() if request.form.get(i)])
    founded_note.header = new_header
    founded_note.text = new_text
    founded_note.tags = new_tags
    update_last_change_date()
    session.commit()

    return redirect('/' + str(founded_note.folder_id))


@app.route('/settings')
@login_required
def settings():
    acc_folders_ = current_user.folders
    notes_cnt = sum([len(folder.notes) for folder in acc_folders_])
    folders_cnt = len(acc_folders_)

    return render_template('settings.html', notes_cnt=notes_cnt, folders_cnt=folders_cnt,
                           user=current_user)


@app.route('/manage_folders', methods=['POST', 'GET'])
@login_required
def manage_folders():
    if request.method == 'GET':
        query = ''
    else:
        query = request.form.get('search-folder')
    session = db_session.create_session()
    acc_folders = session.query(Folder).filter(Folder.user_id == current_user.id) \
        .filter(Folder.name.like('%' + query.lower() + '%')).all()

    return render_template('manage_folders.html', folders=acc_folders, user=current_user, query=query)


@app.route('/create_folder', methods=['POST', 'GET'])
@login_required
def create_folder():
    if request.method == 'GET':
        return render_template('create_folder.html', user=current_user)

    session = db_session.create_session()
    folder_name = request.form.get('folder-name').lower()
    new_folder = Folder(name=folder_name, user_id=current_user.id)
    session.add(new_folder)
    session.commit()
    update_last_change_date()
    return redirect('/' + str(new_folder.id))


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    session = db_session.create_session()
    if current_user.is_authenticated:
        return redirect('/')
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        user = session.query(User).filter_by(login=login).first()
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
                    session = db_session.create_session()
                    session.add(new_user)
                    session.commit()
                    login_user(new_user)
                    send_login_and_password(email, login, password)
                    return redirect('/')
                except Exception:
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
    session = db_session.create_session()
    user = session.query(User).get(current_user.id)
    user.name = request.form.get('name')
    user.surname = request.form.get('surname')
    user.sex = request.form.get('sex')
    user.country = request.form.get('country')
    user.city = request.form.get('city')
    user.phone = request.form.get('phone')
    session.commit()
    return redirect('/profile')


@app.route('/delete_profile')
@login_required
def delete_profile():
    session = db_session.create_session()
    user = session.query(User).get(current_user.id)
    session.delete(user)

    send_account_deleted(user.email, user.login)
    session.commit()
    return redirect('/')


@app.route('/change_password', methods=['POST', 'GET'])
@login_required
def change_password():
    if request.method == 'GET':
        return render_template('change_password.html', user=current_user)
    session = db_session.create_session()
    user = session.query(User).get(current_user.id)

    if check_password_hash(user.password, request.form.get('password')):
        send_password_changed(user.email, user.login, request.form.get('new-password'))
        user.password = generate_password_hash(request.form.get('new-password'))
        session.commit()
        return redirect('/')
    else:
        flash('Неверный пароль!')

    return render_template('change_password.html', user=current_user)


@app.route('/about')
def about():
    return render_template('about.html', user=current_user)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(401)
def unauthorized(error):
    return redirect('/login')


def main():
    app.run()


# __name__ = run
if __name__ == '__main__':
    main()
