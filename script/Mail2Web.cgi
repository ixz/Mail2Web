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
#   Mail2Web
#   Reads the configuration file, get mails from POP account and
#   download pictures, create thumbs and start Indexer for creating
#   the web gallery
#
#   Mail2Web.cgi is executed by cronjob
#-----------------------------------------------------------------------------

import cgi
import os, sys, time, shutil
# for POP
import poplib, email, mimetypes
# for indexer
from string import Template

from ConfigReader import ConfigReader
from subprocess import call

#-----------------------------------------------------------------------------
#   Class for connecting to a POP mail account 
#-----------------------------------------------------------------------------
class CPOP:
    __pop_server=None
    def __init__(self):
        return
    # Connect to POP account
    # TODO: test SSL
    def connect(self,username,userpass,host,port=110,ssl=False):
        try:
            if not ssl:
                self.__pop_server=poplib.POP3(host,port)
            else:
                self.__pop_server=poplib.POP3_SSL(host,port)
            self.__pop_server.getwelcome().decode()
            self.__pop_server.user(username).decode()
            self.__pop_server.pass_(userpass).decode()
            return True
        except Exception as val:
            print(str(val))
            return False
    # terminate session
    def quit(self):
        try:
            self.__pop_server.quit().decode()
            self.__pop_server=None
        except Exception as val:
            print(str(val))
    # count messages
    def countMsgs(self):
        try:
            return len(self.__pop_server.list()[1])
        except Exception as val:
            print(str(val))
            return -1
    # get the header of the mail, default: 30 lines 
    def retrieveHeader(self, id, lines=30):
        try:
            msg=self.__pop_server.top(id,lines)
            header=str()
            for i in range(0,lines):
                header+=msg[1][i]+'\n'
            return email.message_from_string(header)
        except Exception as val:
            print(str(val))
            return ''
    # retrieve a message, marks the message as read
    def retrieveMsg(self, id):
        try:
            msg=self.__pop_server.retr(id)
            text=str()
            for t in msg[1]:
                text+=t+'\n'
            return email.message_from_string(text)
        except Exception as val:
            print(str(val))
            return None
    # delete a message
    def deleteMsg(self,id):
        try:
            self.__pop_server.dele(id).decode()
        except Exception as val:
            print(str(val))


#-----------------------------------------------------------------------------
#   Class Indexer
#   Searchs for image files in pics folder
#   Only image files with filename pic_yyyymmdd_HHMMSS
#   Creates gallery page from the images
#   Newest image first
#-----------------------------------------------------------------------------
class Indexer:
    cfg=None
    web_path='..'
    pic_path=''
    template_file=''
    index_file=''
    template=''
    # init, read config 
    def __init__(self):        
        self.cfg=ConfigReader()
        self.cfg.read('./mail2web.conf')
        self.index_file=os.path.join(self.web_path,'index.html')
        self.pic_path=os.path.join(self.web_path,'pics')
        self.template_file=os.path.join(self.web_path,'templates','index.tmpl')
    # extract datetime from image filename
    def GetDateFromFilename(self,filename):
        fname,ext=filename.split('.')
        filename=filename.replace('pic_','').replace('.'+ext,'')
        tt=time.strptime(filename, "%Y%m%d_%H%M%S")
        return tt
    # create index page
    def run(self):
        # open template file
        f=open(self.template_file,'r')    
        self.template=Template(f.read())
        f.close()
        # get all images from pic directory
        files=os.listdir(self.pic_path)
        d=dict()
        if len(files):
            # remove all thumbimage filenames from image list
            thumbs=list()
            for f in files:
                if f[0:3]=='tn_':
                    thumbs.append(f)            
            for f in thumbs:
                files.remove(f)
            # reverse list, so newest file is first
            files.sort(reverse=True)
            # get datetime from filename
            tt=self.GetDateFromFilename(files[0])
            datestring=time.strftime("%d %b %Y %H:%M:%S",tt)
            # set newest image to main date and main image
            d["MAINDATE"]=datestring            
            img=str.format('<img src="{0}" height="50%">', os.path.join('pics',files[0]))
            d["MAINIMAGE"]=img
            # create thumblist
            img='<tr>\n'
            cnt=0
            imgwidth=30
            cols=3      
            for f in files:
                # get datetime from filename
                tt=self.GetDateFromFilename(f)
                datestring=time.strftime("%d %b %Y %H:%M:%S",tt)            
                if cnt % cols == 0:
                    img+='</tr>\n<tr>\n'
                    cnt=0
                img+='<td style="text-align: center; vertical-align: middle; width: 33%;">'
                img+=str.format('{0}<br>\n',datestring)
                img+=str.format('<img src="')
                # check if image has thumbnail, otherwise use original 
                if os.path.exists(os.path.join(self.pic_path,'tn_'+f)):
                    img+=str.format('{0}" ', os.path.join('pics','tn_'+f))
                else:
                    img+=str.format('{0}" ', os.path.join('pics',f))
                img+=str.format('width="{1}%" onclick="displayDate(\'{2}\',\'{0}\')">',os.path.join('pics',f),str(imgwidth),datestring)
                img+='</td>\n'
                cnt+=1                
            img+='</tr>\n'
            # set thumblist
            d["SUBIMAGES"]=img
        # write template to html
        f_index=open(self.index_file,'w')        
        f_index.write(self.template.safe_substitute(d))
        f_index.close()


#-----------------------------------------------------------------------------
#   Mainfunktion    
#-----------------------------------------------------------------------------
def main(argv):
    # no PIL installed on my hoster, but I can use imagemagick convert
    # for genrerating thumbnails
    imagemagick='/usr/local/bin/convert'
    os.chdir(os.path.dirname(argv[-1]))    

    if not os.path.exists('./mail2web.conf'):
        print "Config file not found!"
        sys.exit(0)

    cfg=ConfigReader()
    cfg.read('./mail2web.conf')
    
    username=cfg.username
    userpass=cfg.userpass
    host=cfg.host
    port=cfg.port
    ssl=cfg.ssl
    sentfrom=cfg.sentfrom
    delmsg=cfg.delmsg    

    webpath='..'

    picpath=os.path.join(webpath,'pics')

    tt_string="%a, %d %b %Y %H:%M:%S"

    # connect to POP account
    pop=CPOP()
    try:        
        if pop.connect(username,userpass,host,port,ssl):
            cnt=pop.countMsgs()
            if cnt > 0 :
                for id in range(1,cnt+1):
                    # get mail header
                    mail=pop.retrieveHeader(id,60)
                    match=False
                    # check if mail is from specified sender
                    if sentfrom in mail['From']:                        
                        if mail['Date']:
                            dt_string=mail['Date']
                            if dt_string.count('+'):
                                dt_string=dt_string[:dt_string.find('+')-1]                            
                            tt=time.strptime(dt_string,tt_string)
                        # get complete message
                        mail=pop.retrieveMsg(id)
                        if mail:
                            # check mail parts for images
                            for part in mail.walk():
                                if part.get_content_maintype() == 'multipart':
                                    continue
                                if part.get_content_type() in ['image/jpeg','image/gif','image/png'] :
                                    filename = part.get_filename()                                    
                                    if not filename:
                                        ext = mimetypes.guess_extension(part.get_content_type())
                                        if ext == '.jpe':
                                            ext='.jpg'
                                        if not ext:
                                            # Use a generic bag-of-bits extension
                                            ext = '.bin'                                        
                                    else:
                                        filename,ext=filename.split('.')
                                        ext='.'+ext
                                    # save image file from mail
                                    filename='pic_%04d%02d%02d_%02d%02d%02d%s'%(tt[0],tt[1],tt[2],tt[3],tt[4],tt[5],ext)
                                    file_out=os.path.join(picpath, filename)                                    
                                    tn_file_out=os.path.join(picpath, 'tn_'+filename)
                                    if not os.path.exists(file_out):
                                        fp = open(file_out, 'wb')
                                        fp.write(part.get_payload(decode=True))
                                        fp.close()
                                    if not os.path.exists(tn_file_out):
                                        # create thumbnail
                                        call([imagemagick,file_out,'-resize','128',tn_file_out])                                        
                                    match=True
                            if match:
                                # delete message 
                                if delmsg:
                                    pop.deleteMsg(id)                  
    except Exception as val:
        print(str(val))
    finally:
        pop.quit()

    del pop

    idx=Indexer()
    idx.run()

    del idx
    
    return


if __name__ == '__main__':
    main(sys.argv)
