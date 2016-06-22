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

import datetime, calendar, email.utils, re, urllib, urllib2, json, math, subprocess, socket, sys
from models import *
from webapp import app, db

URL_REGEX = re.compile(
  u"^"
  # protocol identifier
  u"(?:(?:https?|ftp)://)"
  # user:pass authentication
  u"(?:\S+(?::\S*)?@)?"
  u"(?:"
  # IP address exclusion
  # private & local networks
  u"(?!(?:10|127)(?:\.\d{1,3}){3})"
  u"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
  u"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
  # IP address dotted notation octets
  # excludes loopback network 0.0.0.0
  # excludes reserved space >= 224.0.0.0
  # excludes network & broadcast addresses
  # (first & last IP address of each class)
  u"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
  u"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
  u"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
  u"|"
  # host name
  u"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
  # domain name
  u"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
  # TLD identifier
  u"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
  u")"
  # port number
  u"(?::\d{2,5})?"
  # resource path
  u"(?:/\S*)?"
  u"$"
  , re.UNICODE)


# Creates a slug
def slugify(text, delim=u'-'):
  """Generates an ASCII-only slug."""
  result = []
  for word in slugify_re.split(text.lower()):
    word = word.encode('translit/long')
    if word:
      result.append(word)
  return unicode(delim.join(result))

def rfc1123date(value):
  """
  Gibt ein Datum (datetime) im HTTP Head-tauglichen Format (RFC 1123) zurück
  """
  tpl = value.timetuple()
  stamp = calendar.timegm(tpl)
  return email.utils.formatdate(timeval=stamp, localtime=False, usegmt=True)

def expires_date(hours):
  """Date commonly used for Expires response header"""
  dt = datetime.datetime.now() + datetime.timedelta(hours=hours)
  return rfc1123date(dt)

def cache_max_age(hours):
  """String commonly used for Cache-Control response headers"""
  seconds = hours * 60 * 60
  return 'max-age=' + str(seconds)

def obscuremail(mailaddress):
  return mailaddress.replace('@', '__AT__').replace('.', '__DOT__')
app.jinja_env.filters['obscuremail'] = obscuremail

class MyEncoder(json.JSONEncoder):
  def default(self, obj):
    return str(obj)
