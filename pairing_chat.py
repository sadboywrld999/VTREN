from flask import Flask, render_template, request, redirect, url_for, flash
import random

app = Flask(__name)
app.secret_key = 'your_secret_key'

# Store users who are looking for pairings
users_waiting_for_pairing = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/request_pairing', methods=['POST'])
def request_pairing():
    user_id = request.form['user_id']

    if user_id not in users_waiting_for_pairing:
        users_waiting_for_pairing.append(user_id)
        flash('Request for pairing submitted!', 'success')
    else:
        flash('You are already in the queue for pairing.', 'warning')

    return redirect(url_for('home'))

@app.route('/find_pair', methods=['POST'])
def find_pair():
    user_id = request.form['user_id']

    if user_id in users_waiting_for_pairing:
        users_waiting_for_pairing.remove(user_id)
        random.shuffle(users_waiting_for_pairing)  # Shuffle for randomness
        if users_waiting_for_pairing:
            paired_user = users_waiting_for_pairing.pop()
            flash(f'You are now paired with {paired_user}.', 'success')
        else:
            flash('No users available for pairing at the moment. Please wait.', 'info')
    else:
        flash('You are not in the pairing queue.', 'warning')

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
