from flask import Blueprint, request, render_template, redirect, url_for, current_app
from .models import Skill, Client
from app.admin.forms import UpdateTagForm
from .forms import ContactForm, MessageForm

from . import public

@public.route('/', methods=['POST','GET'])
def index():
    skills = Skill.get_all()
    if request.method == 'GET':
        current_app.logger.info('mostrando inicio de session')
        return render_template('home.html',skills=skills)
    else:
        id_= request.form['options']
        skill = Skill.get_by_id(id_)
        form = UpdateTagForm(id_hidden=skill.id)
        return render_template('public/skill_pg.html',skill=skill, form=form)


@public.route('/message/')
def message():
    form = MessageForm()
    return render_template('public/message_form.html', form=form)

