from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name)
app.secret_key = 'your_secret_key'

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messaging_system.db'
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Initialize Flask-SocketIO
socketio = SocketIO(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        login_user(user)
        flash('Login successful!', 'success')
    else:
        flash('Login failed. Please check your credentials.', 'error')

    return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    flash('Registration successful!', 'success')
    return redirect(url_for('login'))

@socketio.on('message')
def handle_message(data):
    message = data['message']
    username = data['username']
    emit('message', {'username': username, 'message': message}, broadcast=True)

if __name__ == '__main__':
    app.run(debug=True)
