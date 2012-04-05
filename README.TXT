Mail2Web - v0.1.0.2
*******************

Mail2Web is a server side script, to create a web gallery
from images, that where sent by mail.
It connects to a POP mail account, checks if there are mails
from a specific sender and downloads attached images, if there
are any. A index file (HTML) is generated displaying a simple
web gallery of the downloaded images.

Tested on Apache/2.2.17 (FreeBSD), mod_hcgi/0.9.3 

Requirements:
HTTP Server with Python support and ImageMagick

Check in scripts if the shebang matchs your server location of python.
Also check if the imagemagick path in main function in Mail2Web.cgi
matches your ImageMagick installation.  

Installation:
- Create a folder where you want to install Mail2Web
- Copy all files of package to your folder
- Set permissions:
	* Set chmod of subfolders to 755
	* Set chmod of all scripts to 700
	* Set chmod of all templates to 600
	
Setup Mail2Web:
Start the setup script. To do so, go to
http://www.yourdomain.com/mail2web/script/setup.cgi
Enter your data and press Ok.
Attention: At the moment everyone has access to your setup script, so 
change permission on Setup.cgi to 600 when you're done or delete it.
You should check permission on mail2web.conf in the script folder. 
Set it to 600 if it is not yet.

Create cronjob for running the Mail2Web.cgi script.

*     *     *   *    *        command to be executed
-     -     -   -    -
|     |     |   |    |
|     |     |   |    +----- day of week (0 - 6) (Sunday=0)
|     |     |   +------- month (1 - 12)
|     |     +--------- day of        month (1 - 31)
|     +----------- hour (0 - 23)
+------------- min (0 - 59) 

e.g. every 5 minutes:
*/5	*	*	*	*	/home/<...>/mail2web/script/Mail2Web.cgi

Every day at 00:00:
0	0	*	*	*	/home/<...>/mail2web/script/Mail2Web.cgi

Hourly at xx:20:
20	*	*	*	*	/home/<...>/mail2web/script/Mail2Web.cgi

Wait for mails from sender and the script run, then check the index page on    
http://www.yourdomain.com/mail2web

Fixed:
- Deactivated error messages in connection and quit method. 

TODO:
- Better security and permission:
	* Login before Setup
	* Use better encryption for password in config file.
- Unknown issues ;-) 
 



 