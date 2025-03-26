from flask import request, Flask, render_template, url_for, redirect, abort
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
    articles = Article.query.order_by(Article.date.desc()).all() # Будут выводиться все статьи из БД в хронологическом порядке desc нужно для того, чтобы более новые статьи отображались выше
    return render_template("posts.html", articles = articles) # сможем рабоать в шаблоне со списком статей по ключевому слову articles


# для кнопки подробнее, чтобы можно было полноценно открыть статью
@app.route('/posts/<int:id>') # ind:id чтобы в заголовке указывался номер статьи 
def post_detail(id):
    article = Article.query.get(id) 
    if not article:
        abort(404) # вернем 404 если статья не найдена
    return render_template("post_detail.html", article = article) 


# # обработчик для кнопки удалить и дополнить
# @app.route('/posts/<int:id>/del') # ind:id чтобы в заголовке указывался номер статьи 
# def post_detail(id):
#     article = Article.query.get_or_404(id) # если статья будет не найдена, то будет вызвана ошибка 404
#     try:
#         db.session.delete(article)
#         db.session.commit()
#         return redirect('/posts')
#     except:
#         return "При удалении возникла ошибка( "
#     return render_template("post_detail.html", article = article) 


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
            return redirect('/posts')# если успешное добавление статьи то идет переадресация на страницу со всеми статьями
        except:
            return "При добавлении статьи произошла ошибка:"
    else:
        return render_template("create_article.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug = True)
