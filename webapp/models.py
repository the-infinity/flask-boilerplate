# encoding: utf-8

"""
Copyright (c) 2012 - 2016, Ernesto Ruge
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from sqlalchemy.ext.declarative import declarative_base
from webapp import db
from flask_security import UserMixin, RoleMixin

Base = declarative_base()

roles_users = db.Table('roles_users',
  db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
  db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class User(db.Model, UserMixin):
  __tablename__ = 'user'

  id = db.Column(db.Integer, primary_key=True)
  sex = db.Column(db.Integer())
  firstname = db.Column(db.String(255))
  lastname = db.Column(db.String(255))
  
  email = db.Column(db.String(255))
  
  roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

class Example1(db.Model):
  __tablename__ = 'example1'
  id = db.Column(db.Integer(), primary_key=True)
  
  created = db.Column(db.DateTime())
  updated = db.Column(db.DateTime())
  active = db.Column(db.Integer())
  
  name = db.Column(db.Text())
  descr = db.Column(db.Text())
  
  example2s = db.relationship("Example2", backref="Example1", lazy='dynamic')
  
  def __init__(self):
    pass

  def __repr__(self):
    return '<Example1 %r>' % self.name

  
class Example2(db.Model):
  __tablename__ = 'example2'
  id = db.Column(db.Integer(), primary_key=True)
  
  example1_id = db.Column(db.Integer, db.ForeignKey('example1.id'))
  
  def __init__(self):
    pass

  def __repr__(self):
    return '<Example2 %r>' % self.name

