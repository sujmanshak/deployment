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


import urllib2
import urllib
import json
import time
import sys
#import pdb
from utils import INFO, WARNING, ERROR, FATAL,DEBUG, SET_DEBUG, STREAM, UTILPRINT

class dbclass:
    hostname = ""
    status = 0
    
class configclass:
    hoststring = ""
    deployment = ""
    action = ""
    args = ""
class stateclass:
    server = {}
    msg = {}
    cluster = 0
    
hoststring = ""
deployment = ""
settings = configclass()
state = stateclass()

def resolveServerId(s):
    svr = s
    if svr == "": svr = "localhost"
    if svr.find(":") < 0: svr = svr + ":8000"
    DEBUG("Reolve Server  as [" + svr + "]")
    return svr

def checkJsonStatus(j):
    data = ""
    status = -1
    
    try:
        data = json.loads(j)
    except:
        WARNING("can't read JSON")
    
    try:
        if ("status" in data): status = int(data["status"])
    except:
        WARNING("can't parse status")

    return status

def checkJsonData(j, field):
    data = ""
    status = -1
    retval = ""
    
    DEBUG("Json string " + j)
    try:
        data = json.loads(j)
    except:
        WARNING("can't read JSON")
        return retval
    
    if ("data" in data):
        d = data["data"]
        if (field in d): 
            retval = d[field]
        else:
            DEBUG("no field " + field + " in data")
    else:
        WARNING("No data in JSON")
    
    return retval

def checkErrorMsg(s):
    if s in state.msg:
        return state.msg[s]
    return ""

def printErrorMsg(s):
    t = checkErrorMsg(s)
    if len(t) > 0: print t
    
def initServer(s):
    global settings, state
    # Get current status of server

    DEBUG("init server [" + s + "]")
    svr = resolveServerId(s)
    url = "http://" + svr + "/WEBRC?request=init"
    try:
    	r = urllib2.urlopen(url)
    except Exception, e:
    	ERROR(" Cannot reach server " + s + " " + e.message)
    	raise
    	return False     	
    jdata = r.read()
    status = checkJsonStatus(jdata)
    state.server[s] = status
    
    # If this is the first server, and no deployment file is defined,
    # load the deployment file, etc.
    # Validate anything but create or add (join, recover...)
    #print "DEBUG INIT(), Deployment: " + checkJsonData(jdata,"deployment")
    if s == settings.hoststring.split(",")[0]:
        DEBUG("This is the first server in the list [" + s + "]. Parsing data.")
        if settings.deployment == "":
            settings.deployment = retval = checkJsonData(jdata,"deployment")

    if status == 1 or status == 2:
        ERROR("a database is already running on server " + s)
        return False
    #else:
    #   DEBUG("status is " + str(status))
    return True

def prepServer(s):
    global settings,state
    
    svr = resolveServerId(s)
    
    # Set the hosts and deployment (as necessary)
    data = {}
    data["hoststring"] = settings.hoststring
    data["deployment"] = settings.deployment
    data["args"] = settings.args
    jdata =json.dumps(data)
    urldata = urllib.urlencode({"data": jdata})
    url = "http://" + svr + "/WEBRC?request=set&" + urldata
    DEBUG("Prep server url: " + url)
    try:
    	r = urllib2.urlopen(url)
    except Exception, e:
    	ERROR(" Cannot reach server " + s + " " + e.message)
    	raise
    	return False     	
    jdata = r.read()
    status = checkJsonStatus(jdata)
    state.server[s] = status
    state.msg[s] = checkJsonData(jdata,"msg")
    
    
    if status > -1: return True
    return False
        
def startServer(s):
    global settings,state

    svr = resolveServerId(s)
    url = "http://" + svr + "/WEBRC?request=" + settings.action
    DEBUG("URL TO START: [" + url + "]")
    try:
    	r = urllib2.urlopen(url)
    except Exception, e:
    	ERROR(" Cannot reach server " + s + " " + e.message)
    	raise
    	return False     	
    jdata = r.read()
    status = checkJsonStatus(jdata)
    state.server[s] = status
    state.msg[s] = checkJsonData(jdata,"msg")
    
    # Check for error messages

    if status == 2 or status == 1: return True
        
    return False
    
def pingServer(s):
    global state
    svr = resolveServerId(s)
    url = "http://" + svr + "/WEBRC?request=ping"
    r = urllib2.urlopen(url)
    jdata = r.read()
    status = checkJsonStatus(jdata)
    state.server[s] = status
    state.msg[s] = checkJsonData(jdata,"msg")

    if status == 2:
        UTILPRINT( "Database is running!")
        return False
    if status == 3:
        UTILPRINT( "Database has stopped!")
        return False
    if status == 3:
        UTILPRINT( "Database has failed!")
        return False
    return True
    
def checkCliFlag(flag):
    if flag == "replica": return False
    if flag == "deployment": return True
    if flag == "d": return True
    if flag == "debug": return False

    ERROR("unknown argument " + flag)
    exit()

def parseCli(conf):
    global settings
    flags = []
    flagargs = []
    arguments = []
    currentflag = ""
    flagargument = False
    i = 0
    for a in sys.argv:
        i = i + 1
        if i == 1: continue  # skip the script name
        if a[0:1] == "-":
            if flagargument:
                ERROR("expecting value for argument " + currentflag)
                exit()
            fl = ""
            flarg = ""
            if a[0:2] == "--":
                fl = a[2:]
                p = fl.find("=")
                if p < 0: p = fl.find(":")
                if p >= 0:
                    flarg = fl[p+1:]
                    fl = fl[0:p]
            else:
                fl = a[1:]
                if len(fl) > 1:
                    flarg = fl[1:]
                    fl = fl[0:1]
            # Check if flag is valid and/or needs arguments
            if checkCliFlag(fl):
                if flarg == "":
                    currentflag = fl
                    flagargument = True
                else:
                    flags.append(fl)
                    flagargs.append(flarg)
            else:
                flags.append(fl)
                flagargs.append(flarg)
                
        else:
            # Catch arguments
            if flagargument:
                flags.append(currentflag)
                flagargs.append(a)
                flagargument = False
                currentflag = ""
            else:
                if len(conf.action) == 0:
                    conf.action = a
                else:
                    arguments.append(a)
        
    DEBUG("Flags: " + str(len(flags)))
    DEBUG("Args: " + str(len(arguments)))
    
    for i in range(0, len(flags)):         
        if flags[i] == "deployment" or flags[i] == "d":
            try:
                deploy = ""
                with open(flagargs[i],"r") as df:
                    for line in df:
                        # Compress the deployment
                        if len(deploy) > 0: deploy = deploy + "\n"
                        deploy = deploy + line.strip()
                conf.deployment = deploy
            except Exception, e:
                ERROR("cannot read deployment file.\n" + str(e))
                exit()
        if flags[i] == "replica" or flags[i] == "r":
            conf.args = conf.args + " --replica"
        if flags[i] == "debug":
            SET_DEBUG(True)

                
    t = ",".join(arguments)
    t = t.replace(" ","")
    while t.find(",,") >=0: t = t.replace(",,",",")
    settings.hoststring = t

######  Parse CLI


parseCli(settings)

DEBUG("Settings: " + "\n" \
    + settings.hoststring  + "\n" \
    + settings.deployment + "\n" \
    + settings.action  + "\n" \
    + settings.args )


data = {}
data["hoststring"]  = settings.hoststring
data["deployment"]  = settings.deployment

#jdata =json.dumps(data)
#print  "JSON data: " + jdata
#urldata = urllib.urlencode({"data": jdata})
#print  "Encoded JSON data: " + urldata


###### init, load, and start all servers

#exit()

servers = settings.hoststring.split(",")
serverstate = {}
minstate = 0
maxstate = 0
    
for h in servers: 
    if not initServer(h): 
        printErrorMsg(h)
        exit()
for h in servers: 
    if not prepServer(h): 
        printErrorMsg(h)
        exit()
for h in servers: 
    if not startServer(h): 
        printErrorMsg(h)
        exit()
    serverstate["h"] = 1

started = False

#print "Database is starting",
STREAM( "Database is starting")

trigger = 0
while not started:
    time.sleep(1)
    trigger = trigger + 1
    if trigger % 3 == 0: 
        STREAM( ".")
    for h in servers:
        if not pingServer(h): started = True


    
