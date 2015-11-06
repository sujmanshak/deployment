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


import  os, sys
import xml.etree.ElementTree as ET
from utils import INFO, WARNING, ERROR, FATAL,DEBUG, SET_DEBUG

deploymentmessage = ""

def setmessage(txt):
    deploymentmessage = txt
    
def getmessage():
    if len(deploymentmessage) > 0:
        return deploymentmessage
    else:
        return "Unknown internal error"
    
def writedeploymentfile (config, filespec, hostcount):
    setmessage("")
    if config == "":
        ERROR("no XML to write as deployment file.")
        return False
    x = updatehostcount(config,hostcount)
    if x is None: return False
    
    try:
        fid = open(filespec ,"w")
        DEBUG("writing deployment file " + filespec)
        result = fid.write(x)
        fid.close()
        return True
    except Exception as e:
        setmessage("INTERNAL ERROR CAN'T WRITE FILE: " + str(e))
        ERROR("INTERNAL ERROR CAN'T WRITE FILE: " + str(e))
        return False



def updatehostcount(config,hostcount):
    setmessage("")
    DEBUG("update host count to " + str(hostcount) + " on deployment file " + config)
    try:
        xml = ET.fromstring(config)
    except Exception as e:
        setmessage("Invalid deployment file. Cannot parse XML.")
        ERROR("Invalid deployment file. Cannot parse XML.")
        return None
        
    cluster = xml.find('cluster')
    DEBUG("Cluster: " + str(cluster))
    if cluster is None:
        setmessage("Invalid deployment file. No <cluster> element.")
        ERROR("Invalid deployment file. No <cluster> element.")
        return None
    
    if ('hostcount' in cluster.attrib):
        cluster.attrib['hostcount'] = str(hostcount)
    else:
        # Add hostcount
        cluster.attrib['hostcount'] = hostcount
    return ET.tostring(xml)
        
        

def testit(f):
    fid = open(f,"r")
    result = fid.read()
    fid.close()
    writedeploymentfile(result,'test.xml',3)
