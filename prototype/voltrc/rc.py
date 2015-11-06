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


import json
import os
import detachable
import deployment
from utils import INFO, WARNING, ERROR, FATAL,DEBUG, SET_DEBUG

# constants
k_status_none = 0
k_status_starting = 1
k_status_running = 2
k_status_stopped = 3
k_status_unknown = 4

# json.dumps(dictionary)
# json.loads(json-string)

class rcconfig:
    
    id = 0
    pid = None
    status = 0
    binroot = ""
    dataroot = ""
    timestamp = 0
    msg = ""
    machine = ""
    human = ""
    data = {}
    ip = ""
    port = ""

dataset = dict()
CONFIG = rcconfig()

def createResponse(s,m,i,t,data):
    d = dict()
    d['id'] = i
    d['timestamp']=t
    d['status']=s
    d['msg']=m
    d['data']=data
    if (len(CONFIG.ip) > 0):
         d['ip'] = CONFIG.ip
    else:
         d['ip'] = 'localhost'
    d['port'] = CONFIG.port
        
    return d

def currentResponse(): 
    return createResponse( \
        CONFIG.status, \
        CONFIG.msg, \
        CONFIG.id, \
        CONFIG.timestamp, \
        CONFIG.data)
    
# Instance definition:
# id: integer
# directory: string
# status: integer
# pid: integer(?)
# deployment: json string
# cluster: comma-separated string
# available actions: comma-separated string

# instance directory:
#   directory name: id{3 digit integer of ID}
#   files:
#       deployment.xml
#       CLUSTER
#       PID

    
def init(data):
    indata = {}
    #DEBUG("INCOMING DATA: " + str(data))
    if (len(data) > 0): indata = json.loads(data)
    #DEBUG("LOADED DATA: " + str(indata))
    if ('ip' in indata) and (CONFIG.ip == ""):
        CONFIG.ip = indata['ip']
        DEBUG("Setting IP to " + CONFIG.ip + " from client." )
        
    instance = findInstance(1)
    if not instance: instance = createInstance(1)
    
    if instance:    
        CONFIG.id = 1
        CONFIG.status = instance.status
        CONFIG.pid = instance.pid
        CONFIG.data = instance.data
    retval = currentResponse()
    return(retval)
    
#############  EXTERNAL PUBLIC ROUTINES #####################

def start(action):
    args = ""
    # find host, write deployment
    hoststring = ""
    if "hoststring" in CONFIG.data: hoststring = CONFIG.data["hoststring"]
    
    hosts = hoststring.split(",")
    hostcount = len(hosts)
    if not deployment.writedeploymentfile( \
                CONFIG.data["deployment"], \
                CONFIG.dataroot + buildinstancedir(CONFIG.id) + "/deployment.xml", \
                hostcount):
        # IF we can't write the deployment file, must fail.
        CONFIG.status = 0
        CONFIG.msg = deployment.getmessage()
        return currentResponse()
        
    
    putTextFile(CONFIG.dataroot + buildinstancedir(CONFIG.id) + "/CLUSTER",hoststring)
        
    action = action.strip().lower()
    if (action == "create") or \
       (action == "recover"):
        if len(hosts) > 1:
            # Add leader
            args = args + " --host=" + hosts[0]
            args = args + " --deployment=deployment.xml"
            
    # start process
    detachable.start(action, args, CONFIG.dataroot + buildinstancedir(1))
    CONFIG.timestamp = CONFIG.timestamp + 1
    CONFIG.status = detachable.STATE.status
    CONFIG.msg = detachable.geterrors()
    putIntFile(CONFIG.dataroot + buildinstancedir(CONFIG.id) + "/STATUS",CONFIG.status)
    return currentResponse()

def stop():
    # stop the current process. This should only be called 
    # because the other nodes of the cluster could not start.
    detachable.kill()
    CONFIG.timestamp = CONFIG.timestamp + 1
    CONFIG.status = detachable.STATE.status
    CONFIG.msg = detachable.geterrors()
    return currentResponse()

def get():
    # for latest status
    return ping()
    # return the current instance
    return currentResponse()
    
def set(data):
    # Cannot set if database is running
    if CONFIG.status == 1 or CONFIG.status == 2: 
        WARNING("Cannot SET while database is starting or running")
        return ping()
        
    # set the specified data (received as JSON)
    d = json.loads(data)
    DEBUG("SET(): " + str(d) )
    hostcount = 1
    if "hoststring" in d:
        CONFIG.data["hoststring"] = d["hoststring"]
        hosts = d["hoststring"].split(",")
        hostcount = len(hosts)
    if "deployment" in d:
        CONFIG.data["deployment"] = d["deployment"]
    if "args" in d:
        CONFIG.data["args"] = d["args"]
        
    # and then return the resulting instance and/or error
    CONFIG.timestamp = CONFIG.timestamp + 1
    return currentResponse()
    
def reset():
    # Cannot reset if database is running
    if CONFIG.status == 1 or CONFIG.status == 2: 
        WARNING("Cannot RESET while database is starting or running")
        return ping()
    # Reset to default settings for deployment etc.
    d = buildinstancedir(CONFIG.id)
    CONFIG.data["hoststring"] = ""
    instance.data["deployment"] =  getDefaultDeployment()
    CONFIG.status = k_status_none
    CONFIG.pid = 0
    # overrite existing deployment file etc. 
    putIntFile(CONFIG.dataroot + instance.dataroot + "/STATUS",instance.status)
    putTextFile(CONFIG.dataroot + instance.dataroot + "/deployment.xml",instance.data["deployment"])
    return ping()
    
    
def ping():
    newstatus = detachable.ping()
    if newstatus != CONFIG.status:
        DEBUG("Ping changing status from " + str(CONFIG.status) + " to " + str(newstatus) )
        CONFIG.status = newstatus
        CONFIG.msg = detachable.geterrors()
        CONFIG.timestamp = CONFIG.timestamp + 1
        putIntFile(CONFIG.dataroot + buildinstancedir(CONFIG.id) + "/STATUS",newstatus)
    return currentResponse()
    
    
#############  INTERNAL  ROUTINES #####################
    
def buildinstancedir(id):
    d = "000" +str(id)
    return("id" + d[len(d)-3:])

def getDefaultDeployment():
    global CONFIG
    deploy = getTextFile(CONFIG.dataroot + "template/deployment.xml")
    if deploy == "": deploy = '<deployment><cluster hostcount="1"/></deployment>'
    return deploy

def createInstance(id):
    global CONFIG
    id = 1        
    
    # set the properties
    instance = rcconfig()
    instance.id = id
    instance.dataroot = buildinstancedir(id)
    instance.status = k_status_none
    instance.pid = 0
    instance.data["deployment"] =  getDefaultDeployment()

    # Now create the necessary objects
    # createDirectory
    try:
        os.mkdir(CONFIG.dataroot + instance.dataroot)
    except Exception as e:
        ERROR("cannot create directory " + CONFIG.dataroot + instance.dataroot)
        return None
    # create status file
    putIntFile(CONFIG.dataroot + instance.dataroot + "/STATUS",instance.status)
    # create deployment file 
    putTextFile(CONFIG.dataroot + instance.dataroot + "/deployment.xml",instance.data["deployment"])
    return instance

def findInstance(id):
    
    # get list of directories
    rcdirs = []
    files = os.listdir(CONFIG.dataroot)
    for f in files:
        if os.path.isdir(f):
            if f[0:2] == "id":
                try:
                    foo = int(f[2:])
                    rcdirs.append(f)
                except:
                    continue
    rcdirs.sort()
    #DEBUG("List of diretories: " + str(rcdirs))

    # create instance list from directories and their contents
    d = buildinstancedir(id)
    if d in rcdirs:
        id = 1
        instance = rcconfig()
        instance.id = id
        instance.dataroot = d

        # get pid and status
        pid = getIntFile(CONFIG.dataroot + d+"/PID")
        status = getIntFile(CONFIG.dataroot + d+"/STATUS")
        if (status < 0): status = k_status_none
        if (pid < 0): pid = 0
        
        instance.status = status
        instance.pid = pid
        
        instance.data["deployment"] =  getTextFile(CONFIG.dataroot + d+"/deployment.xml")
        instance.data["hoststring"] =  getTextFile(CONFIG.dataroot + d+"/CLUSTER")
        return instance
    else:
        return None
    
   

#------------------ File routines ------------------

def getTextFile(f):
    result = ""
    if  not os.path.exists(f):
        DEBUG(f + " not found")
        return result
    try:
        fid = open(f,"r")
        result = fid.read()
        fid.close()
    except Exception as e:
        WARNING(e)
        
    return result

def putTextFile(f,t):
    try:
        fid = open(f,"w")
        fid.write(t)
        fid.close()
    except Exception as e:
        WARNING(e)
        return False
    return True
    
def getJsonFile(f):
    return getTextFile(f)

def putJsonFile(f,t):
    return putTextFile(f)

def getIntFile(f):
    result = -1
    if  not os.path.exists(f):
        DEBUG(f + " not found")
        return result
    try:
        fid = open(f,"r")
        result = int(fid.read())
        fid.close()
    except Exception as e:
        WARNING(e)
        result = -9
        
    return result

def putIntFile(f,i):
    try:
        fid = open(f,"w")
        fid.write(str(i))
        fid.close()
    except Exception as e:
        ERROR(e)
        return False

    return True



    
