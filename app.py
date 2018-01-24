#-*- coding:UTF-8 -*-

from __future__ import unicode_literals

from flask import (Flask,render_template,session,redirect,url_for,
                   request,flash,abort)
from forms import TodoListForm
from flask_bootstrap import Bootstrap#初始化Flask-bootstrap，把程序实例传入构造方法进行初始化
from ext import db
from models import TodoList


SECRET_KEY = 'this is key'#Session, Cookies以及一些第三方扩展都会用到SECRET_KEY值，
#这是一个比较重要的配置值，应该尽可能设置为一个很难猜到的值，随机值更佳。

app = Flask(__name__)
app.secret_key = SECRET_KEY
bootstrap = Bootstrap(app)

app.config['USERNAME']='admin'
app.config['PASSWORD']='admin'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:123456@localhost/test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def show_todo_list():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    form = TodoListForm()
    if request.method == 'GET':
        todolists = TodoList.query.all()
        return render_template('index.html', todolists=todolists, form=form)
    else:
        if form.validate_on_submit():
            todolist = TodoList(1, form.title.data, form.status.data)
            db.session.add(todolist)
            db.session.commit()
            flash('You have add a new todo list')
        else:
            flash(form.errors)
        return redirect(url_for('show_todo_list'))


@app.route('/delete/<int:id>')
def delete_todo_list(id):
     todolist = TodoList.query.filter_by(id=id).first_or_404()
     db.session.delete(todolist)
     db.session.commit()
     flash('You have delete a todo list')
     return redirect(url_for('show_todo_list'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            flash('Invalid username')
        elif request.form['password'] != app.config['PASSWORD']:
            flash('Invalid password')
        else:
            session['logged_in'] = True
            flash('you have logged in!')
            return redirect(url_for('show_todo_list'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('you have logout!')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
