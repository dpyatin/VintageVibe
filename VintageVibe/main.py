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

from google.appengine.ext import db
from google.appengine.api import users


class Greeting(db.Model):
  """Models an individual Guestbook entry with an author, content, and date."""
  author = db.StringProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)


def guestbook_key(guestbook_name=None):
  """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
  return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')


class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')

    self.response.out.write("""
    <h1>VintageVibe</h1>
          <form action="http://www.cs.tut.fi/cgi-bin/run/~jkorpela/echo.cgi"
enctype="multipart/form-data" method="post">
<p>
Type some text (if you like):<br>
<input type="text" name="textline" size="30">
</p>
<p>
Please specify a file, or a set of files:<br>
<input type="file" name="datafile" size="40">
</p>
<div>
<input type="submit" value="Send">
</div>
</form>
</body></html>""")

class ShowLocation(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>')
        self.response.out.write("""<h1>VintageVibe</h1>""")
        self.response.out.write("""<p id="demo">Click the button to get your position:</p>
            <p id="latitude"></p>
            <p id="longitude"></p>
            <button onclick="getLocation()">Try It</button>
            <div id="mapholder"></div>
            <script>
            var x=document.getElementById("demo");
            function getLocation()
            {
            if (navigator.geolocation)
            {
            navigator.geolocation.getCurrentPosition(showPosition,showError);
            }
            else{x.innerHTML="Geolocation is not supported by this browser.";}
            }
            
            function showPosition(position)
            {
            var latlon=position.coords.latitude+","+position.coords.longitude;
            document.getElementById("latitude").innerHTML=position.coords.latitude;
            document.getElementById("longitude").innerHTML=position.coords.longitude;
            
            var img_url="http://maps.googleapis.com/maps/api/staticmap?center="
            +latlon+"&zoom=14&size=400x300&markers="+latlon+"&sensor=false";
            document.getElementById("mapholder").innerHTML="<img src='"+img_url+"'>";
            }
            
            function showError(error)
            {
            switch(error.code)
            {
            case error.PERMISSION_DENIED:
            x.innerHTML="User denied the request for Geolocation."
            break;
            case error.POSITION_UNAVAILABLE:
            x.innerHTML="Location information is unavailable."
            break;
            case error.TIMEOUT:
            x.innerHTML="The request to get user location timed out."
            break;
            case error.UNKNOWN_ERROR:
            x.innerHTML="An unknown error occurred."
            break;
            }
            }
            </script>""")
        self.response.out.write('</body></html>')
    
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/showLocation', ShowLocation)],
                              debug=True)
