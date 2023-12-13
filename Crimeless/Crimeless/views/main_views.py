from flask import Flask, Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from src.models import Question
from src.models import Answer
from src.models import User
from app import db

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():

    return render_template('index.html')

@bp.route('/about')
def about():

    return render_template('about.html')
@bp.route('/post/')
def post():
    question_list = Question.query.order_by(Question.create_date.desc())
    return redirect(url_for('question.post'))

@bp.route('/graph/')
def graph():

    return redirect(url_for('graph.bar'))