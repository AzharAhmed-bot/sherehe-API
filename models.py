from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin




metadata= MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db=SQLAlchemy()



class Users(db.Model,SerializerMixin):
    __tablename__='users'

    id=db.Column(db.Integer() ,primary_key=True)
    name=db.Column(db.String(), unique=True)
    password=db.Column(db.String())
    amount=db.Column(db.Integer(), default=0)
    paid=db.Column(db.Boolean, default=False)

    


