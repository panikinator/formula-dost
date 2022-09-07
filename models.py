try:
    from __main__ import app
except:
    from main import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Formula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    formula_str = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    total_attempts = db.Column(db.Integer, nullable=False, default=0)
    total_right = db.Column(db.Integer, nullable=False, default=0)
    total_wrong = db.Column(db.Integer, nullable=False, default=0)
