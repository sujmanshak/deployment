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

import sys
global_debug_flag = False
global_stream_flag = False

def UTILPRINT(txt):
    global global_stream_flag
    if global_stream_flag: 
        print    # clear print line
        SET_STREAM(False)
    print (txt)

def STREAM(txt):
    SET_STREAM(True)
    sys.stdout.write(txt)
    sys.stdout.flush()
    
            
def INFO(txt):
    UTILPRINT( "INFO: " + txt)

def WARNING(txt):
    UTILPRINT(  "WARNING: " + txt)

def ERROR(txt):
    UTILPRINT(  "ERROR: " + txt)

def FATAL(txt):
    UTILPRINT(  "FATAL: " + txt)
    exit()

def DEBUG(txt):
    global global_debug_flag
    if global_debug_flag: UTILPRINT(  "DEBUG: " + txt)

def SET_DEBUG(flag):
    global global_debug_flag
    if flag:
        global_debug_flag = True
    else:
        global_debug_flag  = False
        
def SET_STREAM(flag):
    global global_stream_flag
    if flag:
        global_stream_flag = True
    else:
        global_stream_flag  = False
    

def CHECK_DEBUG():
    global global_debug_flag
    if global_debug_flag:
        UTILPRINT(  "Debug flag is true!")
    else:
        UTILPRINT(  "Debug flag is False!")
	
