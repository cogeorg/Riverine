#!/usr/bin/env python
# -*- coding: utf-8 -*-

#This python file creates the users.db database. 
#Note: Use only if users.db does not exist!

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('sqlite:///users.db', echo=True)
Base = declarative_base()

class User(Base):
  __tablename__ = "users"

  id = Column('user_id', Integer, primary_key = True)
  username = Column('username', String(50), unique = True, index = True)
  password = Column('password', String(50))
  registered_on = Column('registered_on', DateTime)
  
  def __init__(self, username, password):
    self.username = username
    self.password = password
    self.registered_on = datetime.utcnow()
    
Base.metadata.create_all(engine)
