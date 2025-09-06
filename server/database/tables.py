from sqlalchemy import BOOLEAN, Column, Integer, String, JSON
from sqlalchemy.ext.mutable import MutableDict
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

class Squads(database.Model):
    __tablename__ = "squads"
    id = Column(Integer, primary_key=True)
    sName = Column(String(100))
    sTag = Column(String(4))
    sOwner = Column(String(50))
    squad_word_hash = Column(String(44))
    
    
class Users(database.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    commander_name = Column(String(50))
    squad_id = Column(Integer)
    progress_data = Column(MutableDict.as_mutable(JSON))
    password_hash = Column(String(44))
    
class Goals(database.Model):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True)
    squad_id = Column(Integer)
    goal_units = Column(String(40))
    progress_data = Column(MutableDict.as_mutable(JSON))
    contributors = Column(Integer)
    
class Contributions(database.Model):
    __tablename__ = "contributions"
    id = Column(Integer, primary_key=True)
    goal_id = Column(Integer)
    squad_id = Column(Integer)
    user_id = Column(Integer)
    units = Column(String(40))
    quantity = Column(Integer)