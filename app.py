import os
from threading import Thread
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_moment import Moment
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MOVIE_MAIL_SUBJECT_PREFIX'] = '[Movie Pro]'
app.config['MOVIE_MAIL_SENDER'] = 'Movie Admin <movieadmin@example.com>'
app.config['MOVIE_ADMIN'] = os.environ.get('MOVIE_ADMIN')

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


    def __repr__(self):
        return '<User %r>' % self.username

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['MOVIE_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['MOVIE_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def home():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if app.config['MOVIE_ADMIN']:
                send_email(app.config['MOVIE_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('home'))
    return render_template('home.html', form=form, name=session.get('name'),
                           known=session.get('known', False))

@app.route('/about')
def about_us():
    return render_template('about.html')

@app.route('/contact')
def contact_us():
    return render_template('contact.html')

@app.route('/positions')
def positions_available():
    return render_template('positions.html')

@app.route('/create-account')
def create_new_account():
    return render_template('createAccount.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/camera-operators')
def camera_operator_positions():
    return render_template('cameraOperatorsPositions.html')

@app.route('/film-editors')
def film_editing_positions():
    return render_template('filmEditingPositions.html')

@app.route('/film-finance')
def film_finance_positions():
    return render_template('filmFinancePositions.html')

@app.route('/film-music')
def film_music_positions():
    return render_template('filmMusicPositions.html')

@app.route('/film-sound-and-color')
def film_sound_and_color_positions():
    return render_template('filmSoundAndColorPositions.html')

@app.route('/lighting-positions')
def lighting_positions():
    return render_template('lightingPositions.html')

@app.route('/movie-development')
def movie_development_positions():
    return render_template('movieDevelopmentPositions.html')

@app.route('/production-art')
def prodution_art_positions():
    return render_template('productionArtPositions.html')

@app.route('/production-sound')
def prodution_sound_positions():
    return render_template('productionSoundPositions.html')

@app.route('/production-specialty')
def production_speciality_positions():
    return render_template('productionSpecialtyPositions.html')

@app.route('/production-supervisors')
def production_supervisor_positions():
    return render_template('productionSupervisorsPositions.html')

@app.route('/admin/<name>')
def admin_page(name):
    return render_template('admin.html', name=name)

@app.route('/user/<name>')
def user_page(name):
    return render_template('user.html', name=name)

@app.route('/all-projects')
def all_projects():
    return render_template('allProjects.html')

@app.route('/budget')
def budget_page():
    return render_template('budget.html')

@app.route('/current-projects')
def current_projects():
    return render_template('currentProjects.html')

@app.route('/past-projects')
def past_projects():
    return render_template('pastProjects.html')




if __name__ == '__main__':
    app.run(debug=True)