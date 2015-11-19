"""
This file is part of VoltDB.

Copyright (C) 2008-2015 VoltDB Inc.

This file contains original code and/or modifications of original code.
Any modifications made by VoltDB Inc. are licensed under the following
terms and conditions:

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

from flask import request
import socket


class Validation(object):
    """"Validation Class"""
    def __init__(self):
        pass

    @staticmethod
    def validate_port(listener, listener_type):
        """Port Validation """
        response_result = {'status': 1}
        if ":" in listener:
            count = listener.count(":")
            if count > 1:
                response_result = {'status': -1, 'error': 'Invalid ' + listener_type}
            array = listener.split(":")
            try:
                socket.inet_aton(array[0])
            except socket.error:
                response_result = {'status': -1, 'error': 'Invalid IP address'}
            try:
                val = int(array[1])
                if val < 0:
                    response_result = {'status': -1, 'error': listener_type + ' must be a '
                                                                              'positive number'}
                elif val < 1 or val >= 65535:
                    response_result = {'status': -1, 'error': listener_type + ' must be '
                                                                              'greater than 1 '
                                                                              'and less than 65535'}
            except ValueError:
                response_result = {'status': -1, 'error': listener_type + ' must be a '
                                                                          'positive number'}
        else:
            try:
                val = int(request.json['admin-listener'])
                if val < 0:
                    response_result = {'status': -1, 'error': listener_type + ' must be a '
                                                                              'positive number'}
                elif val < 1 or val > 65536:
                    response_result = {'status': -1, 'error': listener_type + ' must be '
                                                                              'greater than 1 and'
                                                                              ' less than 65535'}
            except ValueError:
                response_result = {'status': -1, 'error': listener_type + ' must be a '
                                                                          'positive number'}
        return response_result

    @staticmethod
    def validate_ports_info(request_info):
        """Validate port and IP addresses"""
        response = {'status': 1}
        if 'admin-listener' in request_info.json:
            if request_info.json['admin-listener'] != "":
                response = Validation.validate_port(request_info.json['admin-listener'],
                                                    'admin-listener')
                if response['status'] == -1:
                    return response

        if 'internal-listener' in request_info.json:
            if request_info.json['internal-listener'] != "":
                response = Validation.validate_port(request_info.json['internal-listener'],
                                                    'internal-listener')
                if response['status'] == -1:
                    return response

        if 'http-listener' in request_info.json:
            if request_info.json['http-listener'] != "":
                response = Validation.validate_port(request_info.json['http-listener'],
                                                    'http-listener')
                if response['status'] == -1:
                    return response

        if 'zookeeper-listener' in request_info.json:
            if request_info.json['zookeeper-listener'] != "":
                response = Validation.validate_port(request_info.json['zookeeper-listener'],
                                                    'zookeeper-listener')
                if response['status'] == -1:
                    return response

        if 'replication-listener' in request_info.json:
            if request_info.json['replication-listener'] != "":
                response = Validation.validate_port(request_info.json['replication-listener'],
                                                    'replication-listener')
                if response['status'] == -1:
                    return response

        if 'client-listener' in request_info.json:
            if request_info.json['client-listener'] != "":
                response = Validation.validate_port(request_info.json['client-listener'],
                                                    'client-listener')
                if response['status'] == -1:
                    return response

        if 'internal-interface' in request_info.json:
            if request_info.json['internal-interface'] != "":
                try:
                    socket.inet_aton(request_info.json['internal-interface'])
                except socket.error:
                    return response

        if 'external-interface' in request_info.json:
            if request_info.json['external-interface'] != "":
                try:
                    socket.inet_aton(request_info.json['external-interface'])
                except socket.error:
                    return response

        if 'public-interface' in request_info.json:
            if request_info.json['public-interface'] != "":
                try:
                    socket.inet_aton(request_info.json['public-interface'])
                except socket.error:
                    return response
        return response
