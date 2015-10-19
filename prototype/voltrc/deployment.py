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