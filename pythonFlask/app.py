from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
db = SQLAlchemy(app)


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def record_list():
    records = Record.query.all()
    return render_template('record_list.html', records=records)


@app.route('/add/', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_record = Record(title=title, description=description)
        db.session.add(new_record)
        db.session.commit()
        return redirect('/')
    return render_template('add_record.html')


@app.route('/delete/<int:id>/')
def delete_record(id):
    record = Record.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
