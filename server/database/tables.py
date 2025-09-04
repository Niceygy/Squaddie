from sqlalchemy import BOOLEAN, Column, Integer, String, JSON
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
    progress_data = Column(JSON)
    password_hash = Column(String(44))