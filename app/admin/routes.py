from app.public.models import Skill
from app.auth.models import User
from flask import render_template, request,redirect, Blueprint,url_for
from .forms import NewTagForm, UpdateTagForm
from flask_jwt_extended import jwt_required
from app.decorators.unauthorized import admin_required

from . import admin


@admin.route('/tags/')
@jwt_required
@admin_required
def view_tags():
    tags = Skill.query.all()
    return render_template('admin/list_tags.html',tags=tags)

@admin.route('/register_tag/',methods=['POST','GET'])
@jwt_required
@admin_required
def register_tag():
                                
    form = NewTagForm()
    if form.validate_on_submit():
        target = form.target.data
        knowlegd = form.knowlegd.data
        description = form.description.data
        new_tag = Skill(target,knowlegd,description)
        Skill.save(new_tag)    
        return redirect(url_for('public.index'))
    return render_template('admin/new_tag_form.html', form=form)


@admin.route('/delete_tag/<int:id_>/',methods=['GET'])
@jwt_required
@admin_required
def delete_tag(id_):         
    tag = Skill.get_by_id(id_)      
    tag.delete_tag()                 
    return redirect(url_for('public.index'))


@admin.route('/update_tag/',methods=['POST'])
@jwt_required
@admin_required
def update_tag():
    form = UpdateTagForm()       
    if form.validate_on_submit():

        id_ = form.id_hidden.data     
        tag = Skill.get_by_id(id_)      
        new_kn = form.knowlegd.data       
        new_ds = form.description.data
        tag.update_tag(new_kn,new_ds)
        return redirect(url_for('public.index'))

@admin.route('/control_panel/')
@jwt_required
@admin_required
def control_panel():
    users = User.query.all()
    tags = Skill.get_all()
    return render_template('admin/control_panel_admin.html', users = users, tags = tags)
