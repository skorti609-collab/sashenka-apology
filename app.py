from flask import Flask, render_template, request, redirect, url_for, session
from datetime import date

app = Flask(__name__)
app.secret_key = 'change-this-to-a-long-random-secret-key'

MIN_DATE = date(2026, 11, 26)
MAX_DATE = date(2026, 12, 5)
PLACES = {'kfc': 'KFC', 'mcdonalds': "McDonald's", 'sushi': 'Суши домой'}

@app.get('/')
def index():
    return render_template('index.html', min_date=MIN_DATE.isoformat(), max_date=MAX_DATE.isoformat())

@app.post('/choose-date')
def choose_date():
    raw_date = request.form.get('date', '')
    try:
        chosen = date.fromisoformat(raw_date)
    except ValueError:
        return redirect(url_for('index'))
    if not MIN_DATE <= chosen <= MAX_DATE:
        return redirect(url_for('index'))
    session['chosen_date'] = chosen.strftime('%d.%m.%Y')
    return redirect(url_for('place'))

@app.route('/place', methods=['GET', 'POST'])
def place():
    if 'chosen_date' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        choice = request.form.get('place', '')
        if choice not in PLACES:
            return redirect(url_for('place'))
        session['chosen_place'] = PLACES[choice]
        return redirect(url_for('thanks'))
    return render_template('place.html', chosen_date=session['chosen_date'])

@app.get('/thanks')
def thanks():
    if 'chosen_date' not in session or 'chosen_place' not in session:
        return redirect(url_for('index'))
    return render_template('thanks.html', chosen_date=session['chosen_date'], chosen_place=session['chosen_place'])

@app.get('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
