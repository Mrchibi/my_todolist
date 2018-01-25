#-*- coding=UTF-8 -*-

from __future__ import unicode_literals
from flask_wtf import Form
from wtforms import RadioField, SubmitField, StringField,PasswordField
from wtforms.validators import DataRequired, Length

class TodoListForm(Form):
    title = StringField('标题', validators=[DataRequired(), Length(1, 64)])
    status = RadioField('是否完成', validators=[DataRequired()],  choices=[("1", '是'),("0",'否')])
    submit = SubmitField('ADD')

class LoginForm(Form):
    username = StringField('用户名',validators=[DataRequired(),Length(1,24)])
    password = PasswordField('密码',validators=[DataRequired(),Length(1,24)])
    submit = SubmitField('登录')
    