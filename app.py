from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)

bootstrap = Bootstrap(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def home():
    return render_template ('home.html')

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