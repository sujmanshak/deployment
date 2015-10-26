import sys
import os.path

import getopt

import time
import CGIHTTPServer
import BaseHTTPServer
import urllib2
import urlparse
#from html import HTML
import rc
import json

from utils import INFO, WARNING, ERROR, FATAL,DEBUG, SET_DEBUG


################### VARS

PORT = 8000
ASSETS = ["/assets/","/graphics/","/scripts/"]
PROCS = ["/do?","/log?"]
CARDSET = "default"
LOGFILE = "cardsort.log"

IPADDRESS = ""
DATAROOT = "."
BINROOT = "../voltdb"

################### FUNCTIONS
  
def usage():
    print "usage: voltrc [args]"
    print "args:  -d, --data=dir-spec  Root directory for processes"
    print "args:  -debug               Show extra messages"
    print "       -h, --help           This help text"
    print "       -a, --address=host   IP address or host name to use for this server"
    print "       -b, --bin=dir-secp   Directory for VoltDB server executables"
    print "       -p, --port=port-num  Port for VoltDBrc server process"

################### JSON RESPONSE FUNCTIONS

def goodjson(txt):
    return  '{"status":{"code":0,"message":"Success"},"data":{' + \
        txt +  '}}'

def badjson(txt):
    return  '{"status":-1,"msg":"' + txt + '","data":{}}'

################### CLASSES 

    
class Handler (CGIHTTPServer.CGIHTTPRequestHandler):
    cgi_directories = ("/cgi-bin")
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type","text/html")
        s.end_headers()
    def do_GET(s):
        global CARDSET
        # check for assets
        for a in ASSETS:
            if s.path.find(a) == 0:
                print "Getting ASSET ", s.path
                return CGIHTTPServer.CGIHTTPRequestHandler.do_GET(s)

        # check for RC request
        if s.path.find("/WEBRC") == 0:
            #print "Getting WEBRC ", s.path
            return s.do_PROC("WEBRC", s.path)

        # otherwise, it is a file.
        print "Getting file ", s.path
        return s.do_PROC("file", s.path[1:])

    def do_PROC(s,action,args):
        # determine action then do it.
        # current only action is log:
        if (action == "file"):
            data = ""
            if (args=="" or args=="/"): args = "index.html"
            print "Get file: : " + args
            try:
                file = open(args, "r")
                data = file.read()
                file.close()
                s.send_response(200)
                s.send_header("Content-type","text/html")
                s.end_headers()
                s.wfile.write(data)
                return
            except Exception, e:
                ERROR("Cannot read file " + args + " " + str(e))
            
            
        if (action == "WEBRC"):
                # decode arguments
                position = args.find("?")
                query = args[position:]
        
                #print "WEBRC: url path: " + args + "\n" + \
                #    "Query position: " + str(position) + "\n" + \
                #    "Query: " + query

                response = ""
                dbaction = ""
                data = ""
                callback = ""

                try:
                    query = urlparse.parse_qs(urlparse.urlparse(args).query)
                    #print "Got query: " + str(query)
                    if "request" in query: dbaction = query["request"][0]
                    if "data" in query: data = query["data"][0]
                    if "callback" in query: callback = query["callback"][0]

                except Exception, e:
                    print "Failed to parse arguments. " + str(e)
                    s.send_header("Content-type","application/json")
                    s.end_headers()
                    s.wfile.write(badjson("Failed to parse arguments. "))
                    return


                #print "DBG: action is [" + dbaction + "]"
                if (dbaction == "init"):
                    response = json.dumps(rc.get())
                if (dbaction == "ping"):
                    response = json.dumps(rc.ping());
                if (dbaction == "create"):
                    response = json.dumps(rc.start("create"));
                if (dbaction == "recover"):
                    response = json.dumps(rc.start("recover"));
                if (dbaction == "stop"):
                    response = json.dumps(rc.stop());
                if (dbaction == "set"):
                    response = json.dumps(rc.set(data));
                if (dbaction == "get"):
                    response = json.dumps(rc.get(data));
                    


                if (response != ""):
                    s.send_response(200)
                    s.send_header("Content-type","application/json")
                    s.end_headers()
                    if (callback != ""):
                        response = callback + "(" + response + ")"
                    s.wfile.write(response)
                else:
                    s.send_response(200)
                    s.send_header("Content-type","application/json")
                    s.end_headers()
                    s.wfile.write(badjson("Unknown request."))
                    
        return


# Parse CLI

try:
    opts, args = getopt.getopt(sys.argv[1:],"hp:d:b:a:",["help","debug","port=","data=","bin=","address="])
except Exception, e:
    print str(e)
    usage();
    sys.exit()
    
for o,a in opts:
    ofound = False
    if o in ("-h", "--help"):
        usage()
        sys.exit()
    if o in ("-p", "--port"):
        try:
            PORT = int( a )
            ofound = True
        except Exception, e:
            FATAL("bad port number. "+str(e))
    if o in ("-d", "--data"):
        DATAROOT = a
        ofound = True
    if o in ("-b", "--bin"):
        BINROOT = a
        ofound = True
    if o in ("-a", "--address"):
        IPADDRESS = a
        ofound = True
    if o in ("--debug"):
        SET_DEBUG(True)
        ofound = True
    if not ofound:
        ERROR ("Unsupported option " + str(o))
        usage()
        sys.exit()

print "Serving at port", PORT
print "data root", DATAROOT
print "bin root", BINROOT
print "IP address", IPADDRESS

if len(DATAROOT) > 0:
    if DATAROOT[len(DATAROOT) -1:] != "/": DATAROOT = DATAROOT  + "/"
    
print "data root", DATAROOT
    

    
###################### MAIN LOOP

#html = HTML()

# set up HTTP server
httpd = BaseHTTPServer.HTTPServer(("",PORT), Handler)
#print "Serving at port", PORT

# Initialize remote control structures
rc.CONFIG.dataroot = DATAROOT
rc.CONFIG.binroot = BINROOT
rc.CONFIG.ip = IPADDRESS
rc.CONFIG.port = PORT
rc.init("")

         
# Start server processing
httpd.serve_forever()
