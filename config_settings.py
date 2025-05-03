import os

class Config:
    SECRET_KEY = '6b90f14df54fcb1b2cfab23123464b147a31a2fce004a15c09a7d94ec1cb33e3'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@localhost:5432/dblogin'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


