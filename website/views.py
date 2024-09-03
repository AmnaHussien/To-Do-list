from flask_login import login_required, current_user
from . import db
from flask import Blueprint, render_template,request
from .models import task


views = Blueprint('views', __name__)

@login_required
@views.route('/', methods=['POST', 'GET'])
def home():
    if request.method == ['POST']:
        task = request.form.get('task')
        if len(task) < 1:
            return "Task Is Too Short!"
        else:
            new_task = task(content=task, user_id=current_user, is_complete=False, due_date=datetime.utcnow)
            db.sessio.add(new_task)
            db.session.commit()
            return("Task added Successfully!")
    return render_template('home.html', user=current_user)
@views.route('/delete_task/<int:id>', methods=['POST', 'GET'])
def delete_task(id):
    #check if user is logged in

    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        task_to_delete = task.query.get_or_404(id)
        if task_to_delete:
            if task_to_delete.user_id != current_user.id:
                abort(403)
            else:
                db.session.remove(task_to_delete)
                db.session.commit()
                return " Task deleted successfully "
        #return redirect(url_for('home.html'))
@views.route('/update/<int:id>', methods=['PUT'])
def update_task(id):
    task_id = task.query.get_or_400(id)
    if request.method =='POST':
        task_id.content = request.form['content']
        if content == NULL or not content:
            return "conent is required"
        elif len(content) > 50:
            return "Error the content is too long"
        task_id.description = request.form['description']
        if description == NULL or not description:
            return "Description is required"
        task_id.due_date = request.form['due_date']
        if due_date == NULL or not due_date:
            return "Due date is required"
        elif not validate_date(due_date):
            return "Due date format is not validate"
        db.session.commit()
        return "Task updated successfully" # i need to use try and except****
    else:
        return render_template('home.html')
#this route accept id as parameter
