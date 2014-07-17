#!/usr/bin/env python

import datetime

t1 = datetime.datetime.now()

import os
import sys
import time
import re
import shutil

from CLI import *

def BuildList(dir, ext): # Take a directory and expected file extension as arguments, then build a dictionary with filenames as the keys and update times as their values
    temp = {}
    ex = ["index.htm", "Archive.htm"]
    for each in os.listdir(dir):
        if (each.endswith(ext) == True) and (str(ex).find(each) == -1):
            mtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(os.stat(dir+"/"+each).st_mtime))
            temp[re.sub("(\.txt)|(\.htm)", "", each.replace("-", " "))] = mtime
    return temp

if (len(sys.argv) > 1):
    if (sys.argv[1] == "-a"):
        Interface(str(sys.argv[2:]).lstrip("['").rstrip("']").replace("', '", " "), BuildList)
    else:
        print ("Invalid command entered, please try again or use the \"-a\" parameter to enter First Crack's Authoring mode.")

def ExtractFilename(filename):
    return filename.split(",")[0].lstrip("[")+".htm"
def toXML(string):
    if (re.search("[\s\w](\&[^#8220;|^#8221;])[\s\w]", string) != None):
        string = string.replace("&", "&#38;")
    return string.replace("<", "&lt;").replace(">", "&gt;")
def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)
update = []
def SyncDirectories(canonical, uncanonical, canonical_path, ttype, uncanonical_path, dtype): # Check for existence in the uncanonical_path directory
    for each in canonical:
        if ((re.search("^[0-9]{4}$", each) == None) and (re.search("([a-zA-Z][0-9]{4})", each) == None)):
            try:
                uncanonical[each]
                if (canonical[each] != uncanonical[each]):
                    update.append(each)
            except:
                if (ttype == ".htm"):
                    os.remove(canonical_path+"/"+each.replace(" ", "-")+ttype)
                update.append(each)
        elif (re.search("[0-9]{0}[0-9]{4}[0-9]{0}", each).group(0) == str(date.today().year)):
            update.append(each)
        else: # Collections by month and year not of the current year, i.e. May2012.htm
            pass
def Migrate(file_name, mod_time):
    file_descriptor = open("Content/"+file_name, "r")
    article_content = file_descriptor.readline()

    if (article_content.startswith("# [") == True):
        article_type = "linkpost"
        article_content = article_content.lstrip("# ").replace(") #", "")
        article_content = article_content.split("]")
        article_title = article_content[0].lstrip("[")
        article_url = article_content[1].lstrip("(").rstrip(")")
    else:
        article_type = "original"
        article_title = article_content.replace("# ", "").replace(" #", "")
        article_url = file_name.replace(".txt", ".htm")
        article_content = file_descriptor.readline()

    article_content = file_descriptor.read()

    file_descriptor.close()
    file_descriptor = open("Content/"+file_name, "w")
    file_descriptor.write("""Type: %s\nTitle: %s\nLink: %s\nPubdate: %s\nAuthor: %s\n\n%s""" % (article_type, article_title.strip(), article_url.strip(), mod_time, "Zac Szewczyk", article_content.strip()))

    file_descriptor.close()
    os.utime("Content/"+file_name, ((time.mktime(time.strptime(mod_time, "%Y/%m/%d %H:%M:%S"))), (time.mktime(time.strptime(mod_time, "%Y/%m/%d %H:%M:%S")))))

cRecent = BuildList("Content", ".txt")
sRecent = BuildList("Structure", ".htm")

if (len(cRecent) > len(sRecent)):
    SyncDirectories(cRecent, sRecent, "Content", ".txt", "Structure", ".htm")
else:
    SyncDirectories(sRecent, cRecent, "Structure", ".htm", "Content", ".txt") #Delete any files bearing the same name in Structure that don't exist in Content

files = []
for w in sorted(cRecent, key=cRecent.get, reverse=True):
    files.append("[%s, %s]" % (w, cRecent[w]))

# Open index.htm and Archive.htm, clear the contents, and reopen in Append mode. Also open Template.htm and associate all three with file descriptors.
index_fd = open("Structure/index.htm", "w").close()
index_fd = open("Structure/index.htm", "a")
archive_fd = open("Structure/Archive.htm", "w").close()
archive_fd = open("Structure/Archive.htm", "a")
template_fd = open("Structure/System/Template.htm", "r")

# Create first half of structure file, up to the point where content is required.
content = template_fd.read()
if (os.getcwd().split("/")[-1] == "Beta"):
    content = content.replace("<!--BETA-->", """<meta name="robots" content="noindex">""")
content = content.split("<!--Divider-->")

content.append(content[0])

# Write the beginning of Archive.htm
archive_fd.write(content[0].replace("Zac J. Szewczyk", "All Articles").replace("<body id=\"BODYID\">", "<body id=\"Archive\">").replace("""<a id="remote_archive_link" href="http://zacjszewczyk.com/Structure/Archive.htm">Post Archives</a>""", """<a id="remote_archive_link" href="http://zacjszewczyk.com/Structure/Archive.htm">Post Archives</a>\n</li>\n<li><a href=\"2012.htm\">2012 Archives</a>\n</li>\n<li>\n<a href=\"2013.htm\">2013 Archives</a>\n</li>\n<li>\n<a href=\"2014.htm\">2014 Archives</a>"""))

# Open Main_feed.xml, clear the file, and open it again in append mode.
feed_fd = open("Main_feed.xml", "w").close()
feed_fd = open("Main_feed.xml", "a")
today = datetime.datetime.now()
feed_fd.write("""\
<?xml version='1.0' encoding='ISO-8859-1' ?>
<rss version="2.0" xmlns:sy="http://purl.org/rss/1.0/modules/syndication/" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
    <title>Zac J. Szewczyk</title>
    <link>http://zacjszewczyk.com</link>
    <description></description>
    <language>en-us</language>
    <atom:link href="http://zacjszewczyk.com/rss" rel="self" type="application/rss+xml" />
    <lastBuildDate>%s EST</lastBuildDate>
    <ttl>5</ttl>
    <generator>First Crack</generator>""" % (today.strftime("%a, %d %b %Y %H:%M:%S")))

# Define a dictionary for converting three letter month names to their full counterpart
months = {"01" : "January", "02" : "February", "03" : "March", "04" : "April", "05" : "May", "06" : "June", "07" : "July", "08" : "August", "09" : "September", "10" : "October", "11" : "November", "12" : "December"}
name_to_number = {"Jan" : "01", "Feb" : "02", "Mar" : "03", "Apr" : "04", "May" : "05", "Jun" : "06", "Jul" : "07", "Aug": "08", "Sep" : "09", "Oct" : "10", "Nov" : "11", "Dec" : "12"}
year_list = {"2012" : [], "2013" : [], "2014" : [], "2015" : [], "2016" : [], "2017" : [], "2018" : [], "2019" : [], "2020" : []}

file_idx = 0 # Index of file currently being processed. 0 is the first file, 1 is the second, etc.

for position, each in enumerate(files):
    if (position == 0):
        next = None
        previous = files[position+1]
    elif (position < len(files)-1):
        next = files[position-1]
        previous = files[position+1]
    elif (position == len(files)-1):
        next = files[position-1]
        previous = None
    else:
        print ("Error")

    cname = each.split(",")[0].lstrip("[")+".txt" # Define a variable for the content file's name
    sname = each.split(",")[0].lstrip("[").replace(" ", "-")+".htm" # Define a variable for the structure file's name

    # Create a variable for the "Permalink"--formerly "Read More..."--link
    read_more = "<a class=\"read_more_link\" href=\"%s\">&#9449;</a>" % (sname.replace("&", "&amp;"))

    if open("Content/"+cname, "r").readline().startswith("Type:") == False:
        Migrate(cname, each.split(",")[1].rstrip("]").strip())

    with open("Content/"+cname, "r") as fd:
        atype = fd.readline().replace("Type: ", "").strip()
        title = fd.readline().replace("Title: ", "").strip()
        link = fd.readline().replace("Link: ", "").strip()
        pubdate = fd.readline().replace("Pubdate: ", "").strip()
        author = fd.readline().replace("Author: ", "")

        fd.readline()

        structure_fd = open("Structure/"+sname, "w")
        structure_fd.close()
        structure_fd = open("Structure/"+sname, "a")
        structure_fd.write(content[-1].replace("Zac J. Szewczyk", title+" - Zac J. Szewczyk").replace("BODYID", cname.replace(" ", "").replace(".txt", ""))+"<article>\n")
        
        types = ["", "", ""]
        active = ""
        iter_count = 0
        for line in iter(fd.readline, ""):
            if (re.match("(\[>[0-9]+\])", line) != None):
                types.append("<div class=\"footnote\">,,</div>")
            elif (re.match(">|\s{4}", line) != None):
                if ((types[-1] == "<blockquote>,,</blockquote>") or (types[-2] == "<blockquote>,,</blockquote>") or (types[-3] == "<blockquote>,,</blockquote>") or (types[-1] == "<bqt>,,</bqt>") or (types[-2] == "<bqt>,,</bqt>") or (types[-3] == "<bqt>,,</bqt>")):
                    types.append("<bqt>,,</bqt>")
                else:
                    types.append("<blockquote>,,</blockquote>")
            elif (re.match("\*\s", line) != None):
                line = line.replace("* ", "")
                if ((types[-1] == "<ul>,,</ul>") or (types[-2] == "<ul>,,</ul>") or (types[-3] == "<ul>,,</ul>") or (types[-1] == "<li>,,</li>") or (types[-2] == "<li>,,</li>") or (types[-3] == "<li>,,</li>")):
                    types.append("<li>,,</li>")
                else:
                    types.append("<ul>,,</ul>")
            elif (re.match("[0-9]+", line) != None):
                line = re.sub("[0-9]+\.\s", "", line)
                if ((types[-1] == "<ol>,,</ol>") or (types[-2] == "<ol>,,</ol>") or (types[-3] == "<ol>,,</ol>")):
                    types.append("<li>,,</li>")
                else:
                    types.append("<ol>,,</ol>")
            elif (re.match("[a-zA-Z_\[\*\"]", line) != None):
                types.append("<p>,,</p>")
            else: 
                types.append("<blank>,,</blank>")

            if (len(types) == 4):
                types.pop(0)

            current = types[-1]
            second = types[-2]
            third = types[-3]

            # line = line.replace("&", "&#38;")
            if (re.search("(\&)", line) != None):
                line = line.replace("&", "&#38;")

            if (re.match("---", line) != None): # Parse <hr /> elements
                line = line.replace("---", "<hr />")

            if (re.search("(--)", line)): # Parse emdashes
                line = line.replace("--", "&#160;&#8212;&#160;")

            for each in re.findall("([\s\<\>\\\*\/\[\.\-\(]+\"[\w\%\#\\*<\>]+)", line): # Parse double-quote quotations
                ftxt = each.replace("\"", "&#8220;", 1)
                line = line.replace(each, ftxt)
            for each in re.findall("(\w+\.?\"[\s\)\]\<\>\.\*\-\,])", line):
                ftxt = each.replace("\"", "&#8221;", 1)
                line = line.replace(each, ftxt)

            for each in re.findall("(\w+'[\w+|\s+])", line): # Parse single-quote quotations
                ftxt = each.replace("\'", "&#8217;")
                line = line.replace(each, ftxt)
            for each in re.findall("([\s\(]'\w+)", line):
                ftxt = each.replace("\'", "&#8216;", 1)
                line = line.replace(each, ftxt)

            if re.search("(#){4}\s[\s\w\:\[\]\&\#\+\=\!\$\%\|\;\*\?\(\,\)\/\.\-\_\'\"]+\s(#){4}", line): # Parse <h4> elements
                header_id = line.replace("#### ", "", 1).replace(" ####", "", 1).replace(" ", "").replace("&#8220;", "").replace("&#8221;", "").replace("&#8217;", "").replace("&#8216;", "").replace("&#8217;", "")
                header_id = re.sub("[^a-zA-Z0-9_\s]", "", header_id)
                line = line.replace("#### ", "<h4 id=\""+header_id.strip()+"\">", 1).replace(" ####", "</h4>", 1)

            if re.search("(#){3}\s[\s\w\:\[\]\&\#\+\=\!\$\%\|\;\*\?\(\,\)\/\.\-\_\'\"]+\s(#){3}", line): # Parse <h3> elements
                header_id = line.replace("### ", "", 1).replace(" ###", "", 1).replace(" ", "").replace("&#8220;", "").replace("&#8221;", "").replace("&#8217;", "").replace("&#8216;", "").replace("&#8217;", "")
                header_id = re.sub("[^a-zA-Z0-9_\s]", "", header_id)
                line = line.replace("###", "<h3 id=\""+header_id.strip()+"\">", 1).replace("###", "</h3>", 1)

            if re.search("(#){2}\s[\s\w\:\[\]\&\#\+\=\!\$\%\|\;\*\?\(\,\)\/\.\-\_\'\"]+\s(#){2}", line): # Parse <h2> elements
                header_id = line.replace("## ", "", 1).replace(" ##", "", 1).replace(" ", "").replace("&#8220;", "").replace("&#8221;", "").replace("&#8217;", "").replace("&#8216;", "").replace("&#8217;", "")
                header_id = re.sub("[^a-zA-Z0-9_\s]", "", header_id)
                line = line.replace("## ", "<h2 id=\""+header_id.strip()+"\">", 1).replace(" ##", "</h2>", 1)

            if re.search("(#){1}\s[\s\w\:\[\]\&\#\+\=\!\$\%\|\;\*\?\(\,\)\/\.\-\_\'\"]+\s(#){1}", line): # Parse <h1> elements
                header_id = line.replace("# ", "", 1).replace(" #", "", 1).replace(" ", "").replace("&#8220;", "").replace("&#8221;", "").replace("&#8217;", "").replace("&#8216;", "").replace("&#8217;", "")
                header_id = re.sub("[^a-zA-Z0-9_\s]", "", header_id)
                line = line.replace("# ", "<h1 id=\""+header_id.strip()+"\">", 1).replace(" #", "</h1>", 1)

            for each in re.findall("\*{1}[\w:\"\.\+'\s\.|#\\&=,\$\!\?\;\-\[\]]+\*{1}", line):
                if (cname == "Yahoo to Acquire Tumblr.txt"):
                    ftxt = each.replace("*", "<em>", 1).replace("*", "</em>> ", 1)
                else:
                    ftxt = each.replace("*", "<em>", 1).replace("*", "</em>", 1)
                line = line.replace(each, ftxt)

            for each in re.findall("(\!\[[\w\@\s\"'\|\<\>\.\#?\*\;\%\+\=!\,-:$&]+\]\(['\(\)\#\;?\@\%\w\&:\,\./\~\s\"\!\#\=\+-]+\))", line): # Parse images
                desc = each.split("]")[0].lstrip("![")
                url = each.split("]")[1].split(" ")[0].lstrip("(")
                alt = each.split("]")[1].split(" &#8220;")[1].rstrip("&#8221;)")
                line = line.replace(each, "<div class=\"image\"><img src=\""+url+"\" alt=\""+alt+"\" title=\""+title+"\"></div>")

            for each in re.findall("(\[[\w\@\s\"'\|\<\>\.\#?\*\;\%\+\=!\,-:$&]*\]\(['\(\)\#\;?\@\%\w\&:\,\./\~\!\#\=\+-]*\))", line): # Parse links
                desc = each.split("]")[0].lstrip("[")
                url = each.split("]")[1].lstrip("(").replace(")", "", 1).replace("&", "&amp;")
                if (url.endswith(".txt") == True):
                    url = re.sub("\'", "", url).replace(".txt", ".htm").replace(" ", "-").replace("&#8220;", "").replace("&#8221;", "").replace("&#8217;", "").replace("&#8216;", "").replace("&#8217;", "")
                    line = line.replace(each, "<a class=\"local\" href=\""+url.replace(" ", "-")+"\">"+desc+"</a>")
                elif (url == ""):
                    line = line.replace(each, "<a class=\"local\" href=\""+desc.replace("<em>", "").replace("</em>", "").replace(" ", "-")+".htm\">"+desc+"</a>")
                else:
                    line = line.replace(each, "<a href=\""+url+"\">"+desc+"</a>")
            for each in re.findall("(\[[\w\@\s\"'\|\<\>\.\#?\*\;\%\+\=!\,-:$&]*\]\(['\s\(\)\#\;?\@\%\w\&:\,\./\!\#\=\+-]*\)[^\s])", line):
                desc = each.split("]")[0].lstrip("[")
                url = each.split("]")[1].lstrip("(").replace(")", "", 1).replace("&", "&amp;")
                url = url.strip(r"[\.\,\:\;\"\?\&amp;]")
                # if (title == "The Jolla Phone"):
                #     print (url)
                if (url.endswith(".txt") == True):
                    url = url.replace(".txt", ".htm").replace(" ", "-").replace("&#8220;", "").replace("&#8221;", "").replace("&#8217;", "").replace("&#8216;", "").replace("&#8217;", "")
                    line = line.replace(each, "<a class=\"local\" href=\""+url.replace(" ", "-")+"\">"+desc+"</a>")
                else:
                    line = line.replace(each, "<a href=\""+url+"\">"+desc+"</a>")

            # Parse footnotes
            for each in re.findall("(\[\^[0-9]+\])", line):
                mark = each.lstrip("[^").rstrip("]")
                url = """<sup id="fnref"""+mark+""""><a href="#fn"""+mark+"""" rel="footnote">"""+mark+"""</a></sup>"""
                line = line.replace(each, url)

            # Parse single-line comments
            if (re.match("[/]{2}", line) != None):
                line = line.replace("//","<!--")+" -->"

            if (current == "<p>,,</p>"): # If a paragraph
                line = current.replace(",,", line.strip())
            elif (current == "<ul>,,</ul>"): # If an unordered list
                active = "</ul>"
                line = current.split(",,")[0]+"\n<li>"+line.strip()+"</li>"
            elif (current == "<ol>,,</ol>"): # If an ordered list
                active = "</ol>"
                line = current.split(",,")[0]+"\n<li>"+line.strip()+"</li>"
            elif (current == "<li>,,</li>"): # If a list item
                line = current.replace(",,", line.strip())
            elif ((current != "<li>,,</li>") and ((second == "<li>,,</li>") or (second == "<ul>,,</ul>") or (second == "<ol>,,</ol>"))): # If an element following a list item
                line = line.strip()+active+"\n"
                active = ""
            elif (current == "<blockquote>,,</blockquote>"): # If a blockquote
                active = "</blockquote>"
                line = current.split(",,")[0]+"\n<p>"+line.strip().replace("> ", "")+"</p>"
            elif (current == "<bqt>,,</bqt>"): # If the continuation of a blockquote
                line = "<p>"+line.strip().replace("> ", "")+"</p>"
            elif ((current != "<bqt>,,</bqt>") and ((second == "<bqt>,,</bqt>") or (second == "<blockquote>,,</blockquote>"))): # If an element following a blockquote
                # RKLA:SJHFJAKLASGDHJLKASJHDJLKA
                line = line.strip().replace("> ", "")+"</blockquote>\n"
                active = ""
            elif ((current == "<div class=\"footnote\">,,</div>")): # If a footnote
                active = "</div>"
                mark = int(line.split("]")[0].lstrip("[>"))
                if (mark == 1): # If the first footnote
                    line = current.split(",,")[0].replace("div ", "div id=\"fn"+str(mark)+"\" ")+"\n<p>"+line.strip()+"""</p>&#160;&#160;<a class="fn" title="return to article" href="#fnref"""+str(mark)+"""">&#x21a9;</a>"""
                else: # If a later footnote
                    line = "</div>"+current.split(",,")[0]+"<p>"+line.strip()+"</p>"
                    line = line.replace("div ", "div id=\"fn"+str(mark)+"\" ")
            else: # Blank line
                line = line.strip()

            if (iter_count == 0):
                first_paragraph = line
                write_buffer = "<article>\n<h2 class=\"article_title\"><a class=\"%s\" href=\"%s\">%s</a></h2>\n%s\n" % (atype, link, title, first_paragraph)
                feed_buffer = """
        <item>
            <title>%s</title>
            <link>http://zacjszewczyk.com/Structure/%s</link>
            <pubDate>%s EST</pubDate>
            <guid>http://zacjszewczyk.com/Structure/%s</guid>
            <description>\n                %s""" % (toXML(title), sname.replace("&", "&amp;"), time.strftime("%a, %d %b %Y %H:%M:%S%Z", time.strptime(pubdate, "%Y/%m/%d %H:%M:%S")), sname.replace("&", "&amp;"), toXML(first_paragraph.replace("#fn", "http://zacjszewczyk.com/Structure/%s#fn" % (sname)).replace("class=\"local\" href=\"", "href=\"http://zacjszewczyk.com/Structure/")))
                if (file_idx < 25):
                    feed_fd.write(feed_buffer)
                mdate = (datetime.datetime.fromtimestamp(os.path.getmtime("Content/"+cname))).strftime("%a, %d %b %Y %H:%M:%S%Z")
                if ((mdate[5:16].split(" ")[0] == "01") or (mdate[5:16].split(" ")[0] == "21") or (mdate[5:16].split(" ")[0] == "31")):
                    suffix = "st"
                elif ((mdate[5:16].split(" ")[0] == "02") or (mdate[5:16].split(" ")[0] == "22")):
                    suffix = "nd"
                elif ((mdate[5:16].split(" ")[0] == "03") or (mdate[5:16].split(" ")[0] == "23")):
                    suffix = "rd"
                else:
                    suffix = "th"
                if ((cname != "Colophon.txt") and (cname != "Error.txt")):
                    structure_fd.write("\n<p>Published on %s</p>\n" % ((months[name_to_number[mdate[5:16].split(" ")[1]]]+" "+mdate[5:16].split(" ")[0].lstrip("0")+suffix+", "+mdate[5:16].split(" ")[2])))
                structure_fd.write("\n<h2 class=\"article_title\"><a class=\"%s\" href=\"%s\">%s</a></h2>\n%s" % (atype, link, title, line))
            elif (atype == "linkpost" and file_idx < 25):
                write_buffer += "\n"+line
                structure_fd.write("\n"+line)
                if (file_idx < 25):
                    feed_fd.write("\n                "+toXML(line))
            else:
                structure_fd.write("\n"+line)
                if (file_idx < 25):
                    feed_fd.write("\n                "+toXML(line))

            iter_count += 1

        else:
            if (active == "</div>"):
                structure_fd.write("\n"+"""&#160;&#160;<a class="fn" title="return to article" href="#fnref"""+str(mark)+"""">&#x21a9;</a>"""+active)
                if (file_idx < 25):
                    feed_fd.write(toXML("\n"+"""&#160;&#160;<a class="fn" title="return to article" href="#fnref"""+str(mark)+"""">&#x21a9;</a>"""+active))
            elif (active != ""):
                structure_fd.write("\n"+active)
                if (file_idx < 25):
                    feed_fd.write(toXML("\n"+active))
            
            structure_fd.write("\n                    </article>\n")

            if (next == None):
                structure_fd.write(content[1].replace("<!--PREVIOUS-->", """<a href="%s">Previous article</a>""" % (ExtractFilename(previous).replace(" ", "-"))).replace("<!--NEXT-->", "<!--This is the newest article on the site!-->"))
            elif (previous == None):
                structure_fd.write(content[1].replace("<!--PREVIOUS-->", "<!--This is the oldest article on the site!-->").replace("<!--NEXT-->", """<a href="%s">Next article</a>""" % (ExtractFilename(next).replace(" ", "-"))))
            else:
                structure_fd.write(content[1].replace("<!--PREVIOUS-->", """<a href="%s">Previous article</a>""" % (ExtractFilename(previous).replace(" ", "-"))).replace("<!--NEXT-->", """<a href="%s">Next article</a>""" % (ExtractFilename(next).replace(" ", "-"))))

            if (file_idx < 25):
                feed_fd.write("""\n                %s\n            </description>\n        </item>""" % (toXML(read_more.replace("href=\"", "href=\"http://zacjszewczyk.com/Structure/", 1))))
            write_buffer = rreplace(write_buffer, "</p>", "&nbsp;&nbsp;"+read_more+"</p>\n</article>", 1)
            if (cname != "Colophon.txt" and cname != "Error.txt"):
                if (write_buffer.find("#fn") != -1):
                    write_buffer = write_buffer.replace("#fn", "http://zacjszewczyk.com/Structure/%s#fn" % (sname))
                if file_idx == 0: # First article in header
                    content[0] = content[0].replace("<!--FA-->", write_buffer.replace("class=\"read_more_link\"", "class=\"read_more_link\" rel=\"prefetch\""))
                    # feed_fd.write(feed_buffer)
                elif file_idx == 1: # Second article in header
                    content[0] = content[0].replace("<!--SA-->", write_buffer.replace("class=\"read_more_link\"", "class=\"read_more_link\" rel=\"prefetch\""))
                    # feed_fd.write(feed_buffer)
                elif file_idx == 2:
                    index_fd.write(content[0].replace("BODYID", "home"))
                    index_fd.write(write_buffer)
                    # feed_fd.write(feed_buffer)
                elif file_idx < 20: # Article in the main body
                    index_fd.write(write_buffer)
                    # feed_fd.write(feed_buffer)
                else: # Article going to the archive page
                    archive_fd.write(write_buffer)

                    # Append all articles to archive_fd. Change page title to "All Articles". Link to year archives in menu bar
                    # Append articles to year archives according to their year. Change page title to "Articles by Year" Link to month archives in menu bar
                    # Append articles to month archives according to their months. Change page title to "Articles by Month". 
                    # print (pubdate)
                    year_list[pubdate.split("/")[0]].append([pubdate.split("/")[1]+" "+pubdate.split("/")[2].split(" ")[0], title, sname, write_buffer])
            else:
                file_idx -= 1

        if ("structure_fd" in locals()):
            structure_fd.close()

        pubdate = time.mktime(time.strptime(pubdate, "%Y/%m/%d %H:%M:%S"))
        cupdate = os.path.getmtime("Content/"+cname)
        supdate = os.path.getmtime("Structure/"+sname)

        if (pubdate != cupdate):
            # print ("Pubdate != cupdate")
            os.utime("Content/"+cname, (pubdate, pubdate))
            # os.utime("Articles/"+cname, (pubdate, pubdate))
        if (pubdate != supdate):
            os.utime("Structure/"+sname, (pubdate, pubdate))

    file_idx += 1

for year in year_list: # Iterate over each year. "year" is the year, e.g. 2013
    month_list = {"01" : [], "02" : [], "03" : [], "04" : [], "05" : [], "06" : [], "07" : [], "08" : [], "09" : [], "10" : [], "11" : [], "12" : []}
    if year_list[year] != []: # If there was no post for a year, exclude it
        year_fd = open("Structure/"+year+".htm", "w")
        year_fd.write(content[-1].replace("Zac J. Szewczyk", "Articles by Year").replace("id=\"BODYID\"", "id=\"YearArchive\"").replace("""<a id="remote_archive_link" href="http://zacjszewczyk.com/Structure/Archive.htm">Post Archives</a>""", """<a id="remote_archive_link" href="http://zacjszewczyk.com/Structure/Archive.htm">Post Archives</a>\n</li>\n<li><a href=\"#MonthList\">Monthly Archives</a>\n</li>"""))
        year_fd.close()
        year_fd = open("Structure/"+year+".htm", "a")
        
        for item in year_list[year]: # Iterate over each post made during each month, and put them into containers grouped by month. "item" contains all posts made during a year in a tuple of [day year, title, structure file name]
            year_fd.write(item[-1])
            month_list[item[0].split(" ")[0]].append(item[-1])

        year_fd.write("<hr id=\"MonthList\" />")

        for month in sorted(month_list, reverse=True): # Iterate over each month
            # "month" is the month the article was posted in, in a number 01-12:
            if month_list[month] != []: # Exclude months without posts
                month_fd = open("Structure/"+months[month]+year+".htm", "w")
                month_fd.write(content[-1].replace("Zac J. Szewczyk", "Archives by Month").replace("id=\"BODYID\"", "id=\"MonthlyArchive\""))
                month_fd.close()
                month_fd = open("Structure/"+months[month]+year+".htm", "a")
                
                # The string written to year_fd in the line below needs to be appended to the nav bar to give users access to article archives broken up by month.
                year_fd.write("<article class=\"months\">\n<h2><a href=\"%s\">%s</a></h2>\n</article>" % (months[month]+year+".htm", months[month]+" "+year))

                for post in month_list[month]: # List all articles                  
                    # "post" is the title, first paragraph, and link to each article
                    month_fd.write(post)
                month_fd.write(content[1])
                month_fd.close()
        year_fd.write(content[1])
        year_fd.close()

archive_fd.write(content[1])
index_fd.write(content[1])
feed_fd.write("""\n</channel>\n</rss>""")
template_fd.close()
feed_fd.close()
archive_fd.close()
index_fd.close()

t2 = datetime.datetime.now()

print ("Execution time: %s" % (t2-t1))

shutil.copyfile("Main_feed.xml", "../../../Public/Main_feed.xml")