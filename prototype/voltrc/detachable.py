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


import subprocess
import threading
import time
from utils import INFO, WARNING, ERROR, FATAL,DEBUG, SET_DEBUG


class processstate:
    
    process = None
    status = 0
    errorcode = 0
    errortext = ""
    errorlog = [""] * 5
    errorlogptr = 0

STATE = processstate()

def subprocreader(p):
  global STATE
  INFO("In subprocess...")
  STATE.status = 1
  while True:
      if p.poll() != None: break
      line = p.stdout.readline().rstrip()
      DEBUG( "subprocess: " + line.rstrip())
      
            # Find when server is up
      if line.find("Server completed initialization") == 0: STATE.status = 2

            # log errors
      if line.find("FATAL") == 0 or line.find("ERROR") == 0: 
        STATE.errorlog[STATE.errorlogptr] = line
        STATE.errorlogptr = STATE.errorlogptr + 1
        if STATE.errorlogptr == 5: STATE.errorlogptr = 0
      
  INFO( "end of process")
  STATE.status = 3
  return
        
def start(action, args, workdir):
    global STATE
    # could also use PYTHONUNBUFFERED
    DEBUG("Starting subprocess: voltdb " +action + args) 
    STATE.process = subprocess.Popen("voltdb " + action  + args, shell=True, cwd=workdir, stdout=subprocess.PIPE)
    STATE.pid = STATE.process.pid
    subthread = threading.Thread(target=subprocreader,args=(STATE.process,))
    subthread.start()
    STATE.status = 1

def stop():
    if STATE.process != None: STATE.process.kill()
    
def ping():
    # check state and return status
    if STATE.process is None: return STATE.status
    if STATE.process.poll() == None: return STATE.status
    DEBUG("ping found old process but no longer running.")
    STATE.status = 3
    return STATE.status
    
def geterrors():
    # return error log
    ptr = STATE.errorlogptr
    retstr = ""
    for i in xrange(0,5):
        if STATE.errorlog[ptr] != "" : retstr = retstr + "\n" + STATE.errorlog[ptr] 
        ptr = ptr + 1
        if ptr == 5: ptr = 0
    return retstr
        
    
#start("create","y","./foo") 
