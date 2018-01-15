#-*- coding:UTF-8 -*-

from __future__ import unicode_literals

import pymysql
from flask import (Flask,render_template,g,session,redirect,url_for,
                   request,flash)

SECRET_KEY = 'this is key'#Session, Cookies以及一些第三方扩展都会用到SECRET_KEY值，
#这是一个比较重要的配置值，应该尽可能设置为一个很难猜到的值，随机值更佳。

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.config['USERNAME']='admin'
app.config['PASSWORD']='admin'





def connect_db():
    """returns a new connection to the database."""
    return pymysql.connect(host='127.0.0.1',
                           user='root',
                           passwd='123456',
                           db='test',
                           charset='utf8')
    
@app.before_request
def before_request():
    """make sure we are connected to the database each request."""
    g.db = connect_db()
    

@app.after_request
def after_request(response):
    """close the database again at the end of the request."""
    g.db.close()
    return response

@app.route('/')
def show_todo_list():
    if not session.get('logged_in'):
        return redirect(url_for('login'))#如果存储的session中logged_in值为False则重定向到login（ url）
    
    sql='select id,user_id,title,status,create_time from todolist'
    with g.db.cursor() as cur:
        cur.execute(sql)
        todo_list = [dict(id=row[0],user_id=row[1],title=row[2],status=bool(row[3]),create_time=row[4]) 
                     for row in cur.fetchall()]
        g.db.commit()
    return render_template('index.html',todo_list=todo_list)

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method =='POST':#若是GET请求则直接渲染登录表单
        if request.form['username'] != app.config['USERNAME']:
            flash('Invalid username')
        elif request.form['password'] !=app.config['PASSWORD']:
            flash('Invalid password')
        else:
            session['logged_in'] = True
            flash('You have logged in!')
            return redirect(url_for('show_todo_list'))
    return render_template('login.html')
    

@app.route('/logout')
def logout():
    session.pop('logged_in',None)#如果会话中有logged_in就删除它
    flash('You have logout!')
    #仅调用flash只是发给客户端一条信息，不负责显示的。
    #显示Flash的信息需要在模板中使用
    #get_flashed_messages()函数获取Flash的信息，并渲染信息。
    return redirect(url_for('login'))








if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)