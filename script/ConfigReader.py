#!/usr/bin/python

#-----------------------------------------------------------------------------
#   Copyright 2011 ixz
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
#   Class for reading a config file
#-----------------------------------------------------------------------------

import os, sys, time
import ConfigParser, base64

class ConfigReader:
    # init class members
    host=''
    username=''
    userpass=''
    port=110
    ssl=False
    sentfrom=''
    delmsg=False
    path='.'
    # initialization
    def __init__(self):
        try:
            pass
        except Exception as val:
            print(str(val))
    # write the configuration to file
    def write(self,filename=None):
        try:
            # use default config filename
            if not filename:
                filename='./mail2web.conf'
            config = ConfigParser.RawConfigParser()
            config.add_section('POP')
            config.set('POP', 'HOST', self.host)
            config.set('POP', 'USERNAME', self.username)
            # simple 'encryption' for password. Not safe at all! :-)
            # TODO: use better encryption
            config.set('POP', 'USERPASS', base64.b64encode(self.userpass))
            config.set('POP', 'FROM', self.sentfrom)
            config.set('POP', 'PORT', self.port)
            config.set('POP', 'SSL', self.ssl)            
            config.set('POP', 'DELMSG', self.delmsg)
            with open(filename, 'wb') as configfile:
                config.write(configfile)
            del config
        except Exception as val:
            print(str(val))
    # read the configuration from a file
    def read(self,filename):
        try:
            config = ConfigParser.RawConfigParser()
            config.read(filename)
            self.host=config.get('POP', 'HOST')
            self.username=config.get('POP', 'USERNAME')
            self.userpass=base64.b64decode(config.get('POP', 'USERPASS'))
            self.port=config.getint('POP', 'PORT')
            self.ssl=config.getboolean('POP', 'SSL')
            self.sentfrom=config.get('POP', 'FROM')
            self.delmsg=config.getboolean('POP', 'DELMSG')
            del config
        except Exception as val:
            print(str(val))    

if __name__ == '__main__':
    pass
