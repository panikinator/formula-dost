from flask import Flask, render_template, request, redirect, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import CheckAnswer, LoginForm, RegistrationForm, NewEqForm,login_required
from eq_lib import check_answer, generate_eq_question
from uuid import uuid4
import os
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/db.sqlite3'
app.config["SECRET_KEY"] = "TcF2PeUu8Urgnf1hUaSSF1Qr_NGzCxhlg01C4o6rfFE62FqyRX7juGkNuhtjfRgw9QAemukv9q0gsnifi4KyJA"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_TYPE"] = "sqlalchemy"
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(days=69)

from models import User, Formula, db

# db = SQLAlchemy(app)
app.config["SESSION_SQLALCHEMY"] = db
Session(app)

if not os.path.exists("data/db.sqlite3"):
        db.create_all()

@app.route("/")
@login_required
def index():
    logged_in = True
    id = session["id"]
    all_eqs = Formula.query.filter_by(user_id=id).all()
    return render_template("index.html",logged_in=logged_in, fs=all_eqs)

@app.route("/view_eq/<eq_id>")
@login_required
def view_eq(eq_id):
    logged_in = True
    eq = Formula.query.filter_by(user_id=session["id"], id=eq_id).first_or_404()
    return render_template("view_eq.html",logged_in=logged_in, eq=eq)

@app.route("/del_eq/<eq_id>")
@login_required
def del_eq(eq_id):
    logged_in = True
    eq = Formula.query.filter_by(user_id=session["id"], id=eq_id).first_or_404()

    db.session.delete(eq)
    db.session.commit()

    flash("Formula Deleted", "success")
    return redirect("/")

@app.route("/practice_eq/<eq_id>")
@login_required
def practice_eq(eq_id):
    logged_in = True
    eq = Formula.query.filter_by(user_id=session["id"], id=eq_id).first_or_404()
    q_uuid = str(uuid4())
    completed_formula, values_dict, answer, choosen_one = generate_eq_question(eq.formula_str)

    session[q_uuid] = (eq_id, completed_formula, values_dict, answer, choosen_one)
    return redirect(f"/q/{q_uuid}")

@app.route("/q/<q_uuid>", methods=["GET", "POST"])
@login_required
def practice_q(q_uuid):
    logged_in = True
    form = CheckAnswer(request.form)
    if q_uuid not in session:
        flash("object not found?", category="warning")
        return redirect("/")
    eq_id, completed_formula, values_dict, answer, choosen_one = session[q_uuid]
    eq = Formula.query.filter_by(user_id=session["id"], id=eq_id).first_or_404()

    if request.method == "POST" and form.validate():
        is_correct = check_answer(answer, form.user_answer.data)
        del session[q_uuid]
        if is_correct:
            flash("Right Answer! mastery++", "success")
            flash(f"Exact Answer: {answer}", "info")

            eq.total_right = eq.total_right + 1
            eq.total_attempts = eq.total_attempts + 1
            db.session.commit()
            return redirect(f"/view_eq/{eq_id}")
        else:
            flash("Wrong Answer! mastery--", "warning")
            flash(f"Exact Answer: {answer}", "info")
            eq.total_wrong = eq.total_wrong + 1
            eq.total_attempts = eq.total_attempts + 1
            db.session.commit()
            return redirect(f"/view_eq/{eq_id}")



    
    return render_template("q.html",logged_in=logged_in, eq=eq, q=completed_formula, values_dict=values_dict, form=form, choosen_one=choosen_one)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration Successful","success")
        flash("use your new credentials to login now","primary")

        return redirect("/login")

    if session.get("id"):
        flash("You are already logged in!", "danger")
        return redirect("/")
    return render_template("register.html",form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user =User.query.filter_by(username=form.username.data).first()
        if not user:
            flash("Incorrect password or username", "danger")
            return redirect(request.url)
        if not check_password_hash(user.password, form.password.data):
            flash("Incorrect password or username", "danger")
            return redirect(request.url)
        session["id"] = user.id
        session.permanent = True
        flash("Login Successful!", "success")
        return redirect("/")

    if session.get("id"):
        flash("You are already logged in!", "danger")
        return redirect("/")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/login")

@app.route("/add_eq", methods=["GET", "POST"])
@login_required
def add_eq():
    logged_in = True
    form = NewEqForm(request.form)
    if request.method == "POST" and form.validate():
        new_formula = Formula(name=form.name.data, formula_str=form.formula_str.data, description=form.description.data, user_id=session["id"])
        db.session.add(new_formula)
        db.session.commit()
        flash("New Formula added successfully", "success")
        return redirect("/")
    return render_template("add_eq.html",form=form,logged_in=logged_in)


if __name__ == "__main__":
    
    app.run(host="0.0.0.0", debug=True)