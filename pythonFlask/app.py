from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
db = SQLAlchemy(app)


class Record(db.Model):
    """
    Класс для создания модель записи в базу данных.

    С атрибутами:
        id (int): Уникальный идентификатор записи.
        title (str): Название записи.
        description (str): Описание записи.
        created_at (datetime): Дата и время создания записи.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def record_list():
    """
    Функция для отображения всех записей.

    Возвращает:
        HTML-страницу с списком записей.
    """
    records = Record.query.all()
    return render_template('record_list.html', records=records)


@app.route('/add/', methods=['GET', 'POST'])
def add_record():
    """
    Функция для добавления новой записи.

        Для GET-запроса отображается форма добавления.
        Для POST-запроса обрабатывается форма и создается новая запись.

    Возвращает:
        Перенаправление на главную страницу (после добавления записи)
        или HTML-страница с формой (для GET-запроса).
    """
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
    """
    Функция для удаления записи.

    С атрибутами:
        id (int): Уникальный идентификатор записи.

    Возвращает:
        Перенаправление на главную страницу после удаления записи.
    """
    record = Record.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    """
    Точка входа в приложение Flask.

    Запускает сервер Flask в режиме отладки.
    """
    app.run(debug=True)
