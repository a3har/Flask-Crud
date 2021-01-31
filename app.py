from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from models.POSTGRESmodels import TodoPOSTGRES
from models.MySQLmodels import TodoMySQL
from models.shared import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ostgeism:pZ9a1TCa2Z5kbK4p21XVAgUzOjKB_nwu@kandula.db.elephantsql.com:5432/ostgeism'
app.config['SQLALCHEMY_BINDS'] = {'mysql' : 'mysql://sql12389863:gFQ4HSgFvg@sql12.freemysqlhosting.net:3306/sql12389863'}
db.app = app
db.init_app(app)


@app.route('/POSTGRESQL', methods=['POST', 'GET'])
def postgres_index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = TodoPOSTGRES(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/POSTGRESQL')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = TodoPOSTGRES.query.order_by(TodoPOSTGRES.date_created).all()
        return render_template('POSTGRESQL/index.html', tasks=tasks)


@app.route('/POSTGRESQL/delete/<int:id>')
def postgres_delete(id):
    task_to_delete = TodoPOSTGRES.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/POSTGRESQL')
    except:
        return 'There was a problem deleting that task'

@app.route('/POSTGRESQL/update/<int:id>', methods=['GET', 'POST'])
def postgres_update(id):
    task = TodoPOSTGRES.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/POSTGRESQL')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('POSTGRESQL/update.html', task=task)




######### MYSQL Todo ##########




@app.route('/MySQL', methods=['POST', 'GET'])
def mysql_index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = TodoMySQL(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/MySQL')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = TodoMySQL.query.order_by(TodoMySQL.date_created).all()
        return render_template('MySQL/index.html', tasks=tasks)


@app.route('/MySQL/delete/<int:id>')
def mysql_delete(id):
    task_to_delete = TodoMySQL.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/MySQL')
    except:
        return 'There was a problem deleting that task'

@app.route('/MySQL/update/<int:id>', methods=['GET', 'POST'])
def mysql_update(id):
    task = TodoMySQL.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/MySQL')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('MySQL/update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)
