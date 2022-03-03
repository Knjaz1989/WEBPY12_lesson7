from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from sqlalchemy.sql import func


app = Flask('my_app')
db_uri = 'postgresql://user1:user1@localhost:5432/webpy12_lesson7'
app.config['SECRET_KEY'] = '46fa7af6ab35c09ecaff3e3d48ee35fc'
app.config.from_mapping(SQLALCHEMY_DATABASE_URI=db_uri)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer, nullable=False)
    user_login = db.Column(db.String(length=40), nullable=False, unique=True, default='')
    first_name = db.Column(db.String(length=30))
    last_name = db.Column(db.String(length=50))
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)

    def __str__(self):
        return f'{self.id}: {self.first_name} {self.last_name}'


class AdvertisementModel(db.Model):

    __tablename__ = 'advertisements'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=50), nullable=False)
    description = db.Column(db.String(length=250))
    publish_date = db.Column(db.DateTime(), default=func.now())
    owner_id = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)

    def __str__(self):
        return f'{self.id}: {self.title}'

    def __repr__(self):
        return f'{self.id}: {self.title}'




