#!/usr/bin/env python

import os
import time
import datetime
from datetime import date
import sys
import re
import ftplib

# Store the menu in a variable so as to provide easy access at any point in time.
menu = """
* To force a single article to rebuild:          -r
* To force all articles to rebuild:              -R
* To upload a specific article:                  -u
* To upload the most recent five articles:       -U
* To re-upload the entire website:               -V
* To upload all back-end files:                  -B
* To display this menu:                          -h
* To exit this mode and return to Update.py:     exit
* To exit this mode and quit the program:        !exit
"""

def InputFile():
    print ("Please enter the name of the file you wish to modify:")
    fname = raw_input("#: ").lstrip("\"").rstrip("\"")
    while (fname.endswith(".txt") != True):
        print ("Please enter a valid file name, including the \".txt\" file extension.")
        fname = str(raw_input("#: ")).lstrip("\"").rstrip("\"")
    return fname

def WaitFor():
    if (len(params != 0)):
        raw_input("Press the \"Enter\" key to continue.")
    else:
        pass

def Interface(params, BuildList):

    if os.path.isfile("settings.txt") != True:
        print ("Please create a \"settings.txt\" file before continuing.")
        print ("""Store this file in the same directory as this script, formatted as such:
Domain: The URL for your website's FTP server.
Username: The FTP server's username.
Passowrd: The FTP server's password""")
        domain = "null"
        username = "null"
        password = "null"
        # sys.exit(0)
    else:
        settings_fd = open("settings.txt", "r")
        domain = settings_fd.readline().strip().lstrip("Domain: ")
        username = settings_fd.readline().strip().lstrip("Username: ")
        password = settings_fd.readline().strip().lstrip("Password: ")
        settings_fd.close()

    cRecent = BuildList("Content", ".txt")
    sRecent = BuildList("Structure", ".htm")

    files = []
    for w in sorted(cRecent, key=cRecent.get, reverse=True):
        files.append("[%s, %s]" % (w, cRecent[w]))

    if (len(params) == 0): # We need input from the user
        print ("""\
Welcome to First Crack's "Authoring" mode.\n
Entering "-h" into the prompt at any point in time will display the menu below.
%s""" % (menu))

    while (True):
        if (len(params) == 0):
            query = raw_input("#: ")
        else:
            query = str(params)

        if (re.search("-r", query) != None):
            i = 1
            for each in files:
                print (str(i)+". "+each.split(",")[0].lstrip("[")+", updated "+each.split(",")[1].rstrip("]"))
                i += 1
            print
                
            fname = InputFile()
            
            os.remove("Structure/"+fname.replace(".txt", ".htm").replace(" ", "-"))
            print ("%s will be rebuilt the next time First Crack is run." % (fname))
        # Rebuild all posts in a similar fashion as rebuilding a single post.
        elif (re.search("-R", query) != None):
            for each in sRecent:
                print (each)
                os.remove("Structure/"+each.replace(" ", "-")+".htm")

            return False
        # Print the menu of valid commands to the terminal.
        if (re.search("-h", query) != None):
            print (menu)
        if (re.search("-u", query) != None):
            print ("Single file upload")
            fname = InputFile().replace(".txt", ".htm").replace(" ", "-")
            ftp = ftplib.FTP(domain)
            ftp.login(username, password)
            ftp.cwd("/")

            if (os.getcwd().split("/")[-1] == "Beta"):
                ftp.cwd("Beta")

            ftp.cwd("Structure")
            ftp.storlines("STOR " + fname, open("Structure/"+fname, "rb"))
            ftp.quit()
            print ("File uploaded")
            return False
        elif (re.search("-U", query) != None):
            # Update the site via FTP
            ftp = ftplib.FTP(domain)
            ftp.login(username, password)
            ftp.cwd("/")
            
            if (os.getcwd().split("/")[-1] == "Beta"):
                ftp.cwd("Beta")

            ftp.storlines("STOR Main_feed.xml", open("Main_feed.xml", "rb"))
            
            ftp.cwd("Structure")
            
            ftp.storlines("STOR index.htm", open("Structure/index.htm", "rb"))
            ftp.storlines("STOR Archive.htm", open("Structure/Archive.htm", "rb"))

            i = 0
            for each in files:
                each = each.split(",")[0].lstrip("[").replace(" ", "-")+".htm"
                if (i < 19):
                    print ("Uploading \"%s\"" % (each))
                    ftp.storlines("STOR " + each, open("Structure/"+each, "rb"))
                    i += 1
                else:
                    break

            ftp.cwd("../Style")
            ftp.storlines("STOR " + "main.css", open("Style/main.css", "rb"))

            ftp.cwd("../Scripts")
            ftp.storlines("STOR main.js", open("Scripts/main.js", "rb"))
            ftp.storlines("STOR jquery.ios-shake.js", open("Scripts/jquery.ios-shake.js", "rb"))

            ftp.quit()
            print ("The site has been updated.")
            sys.exit(0)
        elif (re.search("-V", query) != None):
            # Update the site via FTP
            ftp = ftplib.FTP(domain)
            ftp.login(username, password)
            ftp.cwd("/")
            
            if (os.getcwd().split("/")[-1] == "Beta"):
                ftp.cwd("Beta")

            ftp.storlines("STOR Main_feed.xml", open("Main_feed.xml", "rb"))
            
            ftp.cwd("Structure")
            
            ftp.storlines("STOR index.htm", open("Structure/index.htm", "rb"))
            ftp.storlines("STOR Archive.htm", open("Structure/Archive.htm", "rb"))

            i = 0
            for each in files:
                each = each.split(",")[0].lstrip("[").replace(" ", "-")+".htm"
                if (each.endswith(".htm")):
                    print ("Uploading \"%s\"" % (each))
                    ftp.storlines("STOR " + each, open("Structure/"+each, "rb"))
                    i += 1
                else:
                    break

            ftp.cwd("../Style")
            ftp.storlines("STOR " + "main.css", open("Style/main.css", "rb"))

            ftp.cwd("../Scripts")
            ftp.storlines("STOR main.js", open("Scripts/main.js", "rb"))
            ftp.storlines("STOR jquery.ios-shake.js", open("Scripts/jquery.ios-shake.js", "rb"))
            ftp.quit()
            print ("The entire site has been updated.")
            sys.exit(0)
        elif (re.search("-B", query) != None):
            # Update the site via FTP
            ftp = ftplib.FTP(domain)
            ftp.login(username, password)

            if (os.getcwd().split("/")[-1] == "Beta"):
                ftp.cwd("Beta")

            ftp.cwd("Style")
            ftp.storlines("STOR " + "main.css", open("Style/main.css", "rb"))

            ftp.cwd("../Scripts")
            ftp.storlines("STOR main.js", open("Scripts/main.js", "rb"))
            ftp.storlines("STOR jquery.ios-shake.js", open("Scripts/jquery.ios-shake.js", "rb"))
            ftp.quit()
            print ("The site has been updated.")
            sys.exit(0)
        # Exit the command-line interface and proceed with Update.py.
        if (re.search("exit", query) != None) or (re.search("logout", query) != None):
            return False
        # Exit the command-line interface and prevent Update.py from proceeding.
        elif (re.search("!exit", query) != None):
            sys.exit(0)