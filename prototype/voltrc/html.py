# This file is part of VoltDB.

# Copyright (C) 2008-2015 VoltDB Inc.
#
# This file contains original code and/or modifications of original code.
# Any modifications made by VoltDB Inc. are licensed under the following
# terms and conditions:
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


class HTML:

	def encode(self,txt):
		return(txt)
	def decode(self,txt):
		return(txt)

	def header(self,txt):
		output = '<html><head><title>' + self.encode(txt) + '</title>\
<meta charset="utf-8" />\
<meta name="viewport" content="width=device-width, initial-scale=1.0" />\
<link rel="stylesheet" href="/assets/foundation/css/foundation.css" />\
<link rel="stylesheet" href="/assets/font-awesome/css/font-awesome.min.css" />\
<link rel="stylesheet" href="/assets/webserver.css" />\
<script src="/assets/foundation/js/vendor/modernizr.js"></script>\
</head><body>'

		return(output)

	def body(self,txt):
		output = '<div id="main" class="main row">' + \
			txt + '</div>'
		return(output)
	
	def banner(self,txt):
		output = '<div id="banner" class="banner row">\
<div id="logo" class="logo small-2 columns">\
<img src="/graphics/voltdblogo.jpg"/></div>\
<div id="ataglance" class="summary small-8 columns">' + txt + '</div>\
<div id="refresh" class="fa refresh small-2 columns"><span class="fa-repeat"></span></div>\
</div>'
		output = output + '<nav class="row">\
<div class="large-12 columns">\
<ul class="button-group radius even-5">\
<li class="button"><a href="/">Overview</a></li>\
<li class="button"><a href="/administer">Administer</a></li>\
<li class="button"><a href="/configure">Configure</a></li>\
<li class="button"><a href="/performance">Performance</a></li>\
<li class="button"><a href="/sql">SQL Query</a></li>\
</ul>\
</div></nav>'
		return(output)

	def footer(self):
		output = '<script src="/assets/foundation/js/vendor/jquery.js"></script>\
<script src="/assets/foundation/js/foundation.min.js"></script>\
<script>$(document).foundation();</script>\
</body></html>'
		return(output)


"""
div class="row top-bar">
    <div class="small-4 small-offset-4 columns">
      <h2>Profile</h2>
    </div>
    <div class="small-4 columns">
      <a href="#" class="top-bar-button right">Settings</a>
    </div>
  </div>
  <!-- This space is for the app's content -->
  <div class="content"></div>
  <div class="nav">
    <ul>
      <li class="nav-button"><a href="#">Feed</a></li>
      <li class="nav-button"><a href="#">Groups</a></li>
      <li class="nav-button"><a href="#">Goals</a></li>
      <li class="nav-button nav-me"><a href="#">Me</a></li>
    </ul>
  </div>        
"""
