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

from wtforms.validators import DataRequired, IPAddress, ValidationError, Optional, Regexp
from flask_inputs import Inputs
import socket


class Validation(object):
    """"Validation Class"""
    @staticmethod
    def port_validation(form, field):
        """Port Validation """
        response_result = {'status': 1}
        if ":" in field.data:
            count = field.data.count(":")
            if count > 1:
                raise ValidationError('Invalid value')
            array = field.data.split(":")
            if len(array) == 2:
                try:
                    socket.inet_pton(socket.AF_INET, array[0])
                except AttributeError:
                    try:
                        socket.inet_aton(array[0])
                    except socket.error:
                        raise ValidationError('Invalid IP address')
                    return array[0].count('.') == 3
                except socket.error:
                    raise ValidationError('Invalid IP address')
                try:
                    val = int(array[1])
                    if val < 1 or val >= 65535:
                        raise ValidationError('Port must be greater than 1 and less than 65535')
                except ValueError as err:
                    msg = err.message
                    if msg is 'Port must be greater than 1 and less than 65535':
                        raise ValidationError('Port must be greater than 1 and less than 65535')
                    else:
                        raise ValidationError('Value must be positive.')
            else:
                raise ValidationError('Invalid value')
        else:
            try:
                val = int(field.data)
                if val < 1 or val > 65536:
                    raise ValidationError('Port must be greater than 1 and less than 65535')
            except ValueError as err:
                msg = err.message
                if msg is 'Port must be greater than 1 and less than 65535':
                    raise ValidationError('Port must be greater than 1 and less than 65535')
                else:
                    raise ValidationError('Value must be positive.')


class ServerInputs(Inputs):
    """
    Validation class for inputs
    """
    json = {
        'name': [
            DataRequired('Name is required.'),
            Regexp('^[a-zA-Z0-9_.]+$', 0, 'Only alphabets, numbers, _ and . are allowed.')
        ],
        'hostname': [
            DataRequired('Hostname is required.'),
            Regexp('^[a-zA-Z0-9_.]+$', 0, 'Only alphabets, numbers, _ and . are allowed.')
        ],
        'enabled': [
            Optional(),
        ],
        'admin-listener': [
            Optional(),
            Validation.port_validation
        ],
        'internal-listener': [
            Optional(),
            Validation.port_validation
        ],
        'http-listener': [
            Optional(),
            Validation.port_validation
        ],
        'zookeeper-listener': [
            Optional(),
            Validation.port_validation
        ],
        'replication-listener': [
            Optional(),
            Validation.port_validation
        ],
        'client-listener': [
            Optional(),
            Validation.port_validation
        ],
        'internal-interface': [
            Optional(),
            IPAddress('Invalid IP address.')
        ],
        'external-interface': [
            Optional(),
            IPAddress('Invalid IP address.')
        ],
        'public-interface': [
            Optional(),
            IPAddress('Invalid IP address.')
        ],
    }
