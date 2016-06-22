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

from flask.ext.wtf import Form
from wtforms import validators
from models import *
from wtforms import SubmitField, TextField, SelectField, FileField, TextAreaField
from webapp import app, db
import util


class ComplaintForm(Form):
  text = TextField(
    label=u'Vorname',
    validators=[validators.Length(min=1,max=255)],
    description='Text')
  email = TextField(
    label=u'E-Mail',
    validators=[validators.Length(max=255), validators.Email(message=u'Bitte geben Sie eine korrekte Mailadresse an.')],
    description='Ihre E-Mail-Adresse')
  text_area = TextAreaField(
    label='TextArea',
    validators=[],
    description='TextArea')
  select_field = SelectField(
    label=u'Anrede',
    validators=[validators.Length(max=255), validators.AnyOf(['1', '2'], u'')],
    choices=[('1', '1'), ('2', '2'), ('0', '-')])
  submit = SubmitField(
    label=u'Nachricht senden')
