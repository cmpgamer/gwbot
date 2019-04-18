import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, MetaData
 
metadata = MetaData()

ApiKeys = Table(
    'ApiKeys', metadata,
    Column('id', Integer, primary_key=True),
    Column('discord_id', Text, nullable=False),
    Column('gw2_api_key', Text, nullable=False)
)






#
# class Builds(Base):
#     __tablename__ = 'builds'
#     id = Column(Integer, primary_key=True)
#     discord_server = Column(Text, nullable=False)
#     time = Column(Text, nullable=False)
#     profession = Column(Text, nullable=False)
#     name = Column(Text, nullable=False)
#     description = Column(Text, nullable=False)
#     link = Column(Text, nullable=False)
#
# def connect(user, password, db, host='localhost', port=5432):
#     '''Returns a connection and a metadata object'''
#     # We connect with the help of the PostgreSQL URL
#     # postgresql://federer:[email protected]:5432/tennis
#     url = 'postgresql://{}:{}@{}:{}/{}'
#     url = url.format(user, password, host, port, db)
#
#     # The return value of create_engine() is our connection object
#     con = create_engine(url, client_encoding='utf8')
#
#     return con
#
# # Create an engine that stores data in the local directory's
# # sqlalchemy_example.database file.
# engine = connect('bot_account', 'password', 'bot')
#
# # Create all tables in the engine. This is equivalent to "Create Table"
# # statements in raw SQL.
# Base.metadata.create_all(engine)
#
# Session = sessionmaker()
# Session.configure(bind=engine)
