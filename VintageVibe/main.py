#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
import datetime
import json
#import simplejson as json
import urllib
import webapp2
import logging
import uuid

from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users


class Greeting(db.Model):
  """Models an individual Guestbook entry with an author, content, and date."""
  author = db.StringProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)


def vintage_vibe_name():
    return "vintage_vibe"
    
def vintageVibeKey(guestbook_name=None):
  """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
  return db.Key.from_path('Guestbook', vintage_vibe_name())


class MainPage(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not(user):
        self.redirect(users.create_login_url(self.request.uri))
        return
  
    guestbook_name=self.request.get('guestbook_name')

    # Ancestor Queries, as shown here, are strongly consistent with the High
    # Replication Datastore. Queries that span entity groups are eventually
    # consistent. If we omitted the ancestor from this query there would be a
    # slight chance that greeting that had just been written would not show up
    # in a query.
    items = db.GqlQuery("SELECT * "
                            "FROM Item "
                            "WHERE ANCESTOR IS :1 AND userId IS :2",
                            guestbook_key(vintage_vibe_name()), user.user_id())

                              
    upload_url = blobstore.create_upload_url('/upload')
    self.response.out.write('<html><body>')

    self.response.out.write("""
    <h1>VintageVibe</h1>
        Welcome %s. Your items are below.""")
        
    for item in items:
        self.response.out.write(
            '<b>%s</b> for %f:' % (item.clothingType,item.price))
        self.response.out.write('<blockquote>%s</blockquote>' %
                              cgi.escape(item.description))
                              
    self.response.out.write("""<a href="/additem">Add an item</a>
    </body></html>""")



class AddItem(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not(user):
        self.redirect(users.create_login_url(self.request.uri))
        return
  
    upload_url = blobstore.create_upload_url('/additem')
    self.response.out.write('<html><body>')

    self.response.out.write("""
    <h1>VintageVibe</h1>
          <form action="%s" method="post" enctype="multipart/form-data">
<p>
Item type:<br>
<input type="text" name="type" size="30">
<p>
Item price:<br>
<input type="number" name="price" size="30">
<p>
Item description:<br>
<textarea name="description" rows="5" cols="30">
</textarea>
</p>
<p>
Please upload photos %s:<br>
<input type="file" name="photos" size="40">
</p>
<div>
<input type="submit" value="Send">
</div>
</form>
</body></html>""" % (upload_url, user.user_id()))

  def post(self):
    user = users.get_current_user()
    if not(user):
        self.redirect(users.create_login_url(self.request.uri))
        return
    upload_url = blobstore.create_upload_url('/additem')
    upload_files = self.get_uploads('photos')  # 'file' is file upload field in the form
    blob_info = upload_files[0]
    self.redirect('/serve/%s' % blob_info.key())


class User(db.Model):
    userId = db.StringProperty()
    userEmail = db.StringProperty()
    location = db.GeoPtProperty()
    #content = db.StringProperty(multiline=True)
    #date = db.DateTimeProperty(auto_now_add=True)
       
class Item(db.Model):
    uuid = db.StringProperty()
    userId = db.StringProperty()
    clothingType = db.StringProperty()
    description = db.StringProperty(multiline=True)
    price = db.FloatProperty()
    
class Photo(db.Model):
    itemId= db.StringProperty()
    photoId = db.StringProperty()
    photo = db.BlobProperty()

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, resource):
    user = users.get_current_user()
    if not(user):
        self.redirect(users.create_login_url(self.request.uri))
        return
    resource = str(urllib.unquote(resource))
    blob_info = blobstore.BlobInfo.get(resource)
    self.send_blob(blob_info)

    
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/additem', AddItem),
                               ('/upload', UploadHandler),
                               ('/serve/([^/]+)?', ServeHandler)],
                              debug=True)
