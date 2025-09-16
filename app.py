from flask import Flask, render_template, redirect, url_for
from gmail_utils import list_unread_emails, mark_email_as_read

app = Flask(__name__)

@app.route('/')
def home():
    try:
        emails = list_unread_emails()
    except Exception as e:
        emails = []
        print(f"Error fetching emails: {e}")
    return render_template('index.html', emails=emails)

@app.route('/mark_read/<email_id>')
def mark_read(email_id):
    try:
        mark_email_as_read(email_id)
    except Exception as e:
        print(f"Error marking email as read: {e}")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
