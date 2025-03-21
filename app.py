from flask import request, Flask, render_template, url_for, redirect
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) # создание фласк приложения
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True) # p_k для того чтобы айдишник был уникальным
    title = db.Column(db.String(100), nullable = False)
    intro = db.Column(db.String(300), nullable = False) # null для того чтобы нельзя было создать пустое значение
    text = db.Column(db.Text, nullable = True) # Text используется для оптимизации больших текстов
    date = db.Column(db.DateTime, default = datetime.utcnow) # если не будет указана дата, будет использоваться по умолчанию

    def __repr__(self):
        return '<Article %r>' % self.id # когда выбирается объект на основе класса -> объект + id


@app.route('/') # обращаемся к главное странице
@app.route('/home')
def index():
    return render_template("index.html") # подвязываем html файл к странице home


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date).all() # Будут выводиться все статьи из БД в хронологическом порядке 
    return render_template("posts.html", articles = articles) # сможем рабоать в шаблоне со списком статей по ключевому слову articles


@app.route('/create_article', methods=['POST','GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title'] # title прописано в create_article
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title = title, intro = intro, text = text) #Создадим объект на основе класса

        try: # конструкция для обработки ошибок
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')# если успешное добавление статьи то переносим на главнубю страницу
        except:
            return f"При добавлении статьи произошла ошибка: {str(e)}"
    else:
        return render_template("create_article.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug = True)
