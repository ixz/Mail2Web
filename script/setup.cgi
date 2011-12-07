#!/usr/bin/python
# -*- coding: UTF-8 -*-

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
#   Setup script for reading and writting the config file
#-----------------------------------------------------------------------------

import cgi, sys, os
from string import Template
from ConfigReader import ConfigReader

def main(argv):
    print "Content-Type: text/html;charset=utf-8\n"
    print ""    
    
    cfg=ConfigReader()

    form=cgi.FieldStorage()    
    if form:
        # user has submitted form, so we store in the config file
        if form.has_key('pophost'):
            cfg.host=form.getvalue('pophost')
        if form.has_key('popport'):
            cfg.port=form.getvalue('popport')
        if form.has_key('popusername'):
            cfg.username=form.getvalue('popusername')
        if form.has_key('popuserpass'):
            cfg.userpass=form.getvalue('popuserpass')
        if form.has_key('ssl'):
            cfg.ssl=form.getvalue('ssl')
        if form.has_key('delmsg'):
            cfg.delmsg=form.getvalue('delmsg')
        if form.has_key('popsentfrom'):
            cfg.sentfrom=form.getvalue('popsentfrom')
        cfg.write('./mail2web.conf')
        print "Ok"
    else:
        # Display settings as HTML page.

        # Get template for setup.html
        f=open('../templates/setup.tmpl','r')
        template=Template(f.read())
        f.close()

        # Read config file
        cfg.read('./mail2web.conf')

        # Set values in template and display as HTML
        d=dict()
        d["POPHOST"]=cfg.host
        d["POPPORT"]=str(cfg.port)
        d["POPUSER"]=cfg.username
        d["POPPASS"]=cfg.userpass
        d["POPSENTFROM"]=cfg.sentfrom
        if cfg.ssl==True:
            d["SSLTRUE"]='checked="checked"'
            d["SSLFALSE"]=''
        else:
            d["SSLTRUE"]=''
            d["SSLFALSE"]='checked="checked"'
        if cfg.delmsg==True:
            d["DELMSGTRUE"]='checked="checked"'
            d["DELMSGFALSE"]=''
        else:
            d["DELMSGTRUE"]=''
            d["DELMSGFALSE"]='checked="checked"'
        
        print template.safe_substitute(d)    

if __name__ == '__main__':
    main(sys.argv)
    
