from flask import Blueprint,render_template,request,flash, jsonify
from flask_login import login_user, login_required, current_user
from .models import *
from .import db 
import json

views = Blueprint('views',__name__)

@views.route('/',methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        
        
        if len(note) < 1:
            flash('Note is to short',category='error')
        else:
            new_note = Note(data=note,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added',category='success')   
        
    return render_template('home.html',user=current_user)


@views.route('/delete-note',methods=['POST'])
def delete_Note():
    note = json.loads(request.data)
    noteId= note['note']
    
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})
            