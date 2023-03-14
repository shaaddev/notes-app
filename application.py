from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)
application.app_context().push()


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100))
    note = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@application.route('/')
def index():
    # show all notes
    note_list = Note.query.all()
    return render_template('index.html', note_list=note_list)

@application.route('/', methods=['POST'])
def add_note():
    # add new note
    subject = request.form.get('subject')
    note = request.form.get('note')

    new_note = Note(subject=subject, note=note, complete=False)

    db.session.add(new_note)
    db.session.commit()
    return redirect(url_for('index'))

@application.route('/edit/<int:note_id>')
def edit_note(note_id):
    # edit note
    note = Note.query.filter_by(id=note_id)
    db.session.commit()
    return render_template('edit.html')
    

@application.route('/delete/<int:note_id>')
def delete_note(note_id):
    # delete note
    note = Note.query.filter_by(id=note_id).first()
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('index'))




if __name__ == '__main__':
    db.create_all()

    application.run(debug=True)