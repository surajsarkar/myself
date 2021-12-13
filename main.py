from flask import Flask, render_template, url_for, redirect, request
from flask_wtf.csrf import CSRFProtect
from markupsafe import escape
from datetime import datetime
import smtplib
import os


app = Flask(__name__)


app.secret_key = os.environ.get('GATEKEY')
csrf = CSRFProtect(app)

user_id = os.environ.get('POSTMAN')
receiver = os.environ.get('MAILBOX')
passcode = os.environ.get('GATEPASS')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        form_info = {
            'name': escape(request.form['senders_name']),
            'mail': escape(request.form['senders_email']),
            'message': escape(request.form['message']),
        }
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(user=user_id, password=passcode)
            connection.sendmail(user_id, receiver, f"Subject:Got ya\n\n{form_info['name']}\n\n\n\nMy mail \n {form_info['mail']}\n\n\n\n {form_info['message']}")

        return redirect(url_for('home'))

    return render_template('index.html', presest_year=datetime.now().year)


if __name__ == '__main__':
    app.run(debug=True)



