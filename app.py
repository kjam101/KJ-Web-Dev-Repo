from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import jsonify


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Feedback model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    feedback_text = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Contact model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/link')
def link():
    return render_template('link.html')

@app.route('/examples')
def examples():
    return render_template('examples.html')

@app.route('/studies')
def studies():
    return render_template('studies.html')

@app.route('/tips')
def tips():
    return render_template('tips.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Invalid or missing JSON data'}), 400

        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        if not all([name, email, subject, message]):
            return jsonify({'error': 'Missing fields'}), 400

        new_contact = Contact(name=name, email=email, subject=subject, message=message)
        db.session.add(new_contact)
        db.session.commit()

        return jsonify({'message': 'Contact info received'}), 200

    return render_template('contact.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        rating = request.form.get('rating')
        comment = request.form.get('comment')

        if not rating and not comment:
            return render_template('feedback.html', error="Please provide a rating or comment.")

        new_feedback = Feedback(rating=rating, feedback_text=comment)
        db.session.add(new_feedback)
        db.session.commit()

        return render_template('feedback.html', success="Thank you for your feedback!")

    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(debug=True)