from functools import wraps
from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField, ValidationError
from flask import session, flash, redirect
from eq_lib import check_answer, generate_eq_question



# def set_db(db_get: SQLAlchemy):
#     global db
#     db = db_get

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        
    ])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    username = StringField("Username", [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.Length(min=6),
        validators.DataRequired(),  
    ])

class NewEqForm(Form):
    name = StringField("Formula Name", [validators.Length(min=1, max=25)])
    formula_str = StringField("Formula", [validators.Length(min=3)])
    description = TextAreaField("Formula Description", [validators.Length(min=4)])

    def validate_formula_str(form, field):
        raw_formula = field.data
        try:
            generate_eq_question(raw_formula)
        except:
            raise ValidationError("Invalid Formula entered")


class CheckAnswer(Form):
    user_answer = StringField("Your Answer", [validators.Length(min=1, max=25)])

    def validate_user_answer(form, field):
        try:
            check_answer(1, field.data)
        except:
            raise ValidationError("Invalid Expression entered")


    


        

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'id' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first", "info")
            return redirect("/login")

    return wrap