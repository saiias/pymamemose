#! /usr/bin/env python
# -*- coding: utf-8 -*-

import BaseHTTPServer as bts
import subprocess
import urlparse
import os
import json
import codecs
import urllib2
import re

HOME_DIR = os.environ["HOME"]

try:
    SETTING=json.load(open(HOME_DIR+'/.pymamemose.json'))
except IOError,(errno,strerrno):
    print "Don't exist ~/.pymamemose.json"
    SETTING={"DOCUMENT_ROOT":"~/Dropbox/memo","RECENT_NUM":5,"PORT":8000,"REST_PATTERN":".rst","IGNORE_FILE":""}
    
DOCUMENT_ROOT =os.path.expanduser(SETTING["DOCUMENT_ROOT"]) if SETTING.has_key("DOCUMENT_ROOT") else "~/Dropbox/memo"
RECENT_NUM =SETTING["RECENT_NUM"] if SETTING.has_key("RECENT_NUM") else 5
PORT = SETTING["PORT"] if SETTING.has_key("PORT") else 8000
REST_PATTERN  =SETTING["REST_PATTERN"] if SETTING.has_key("REST_PATTERN") else  ".rst"
IGNORE_FILE =SETTING["IGNORE_FILE"] if SETTING.has_key("IGNORE_FILE") else ""

class GetHandler(bts.BaseHTTPRequestHandler):    
    def do_GET(self):
        if self.path == '/favicon.ico':
            self.send_error(404)
        else:
            parsed_path = urlparse.urlparse(self.path)
            self.send_response(200)
            self.send_header("Content-type","text/html") 
            res = Pymamemose(parsed_path)
            self.end_headers()
            self.wfile.write(res.make_html())        
            return


class Pymamemose():
    def __init__(self,parsed_path):
        self.parsed_path=parsed_path
        self.restpatobj =re.compile(REST_PATTERN)
        self.ignoreobj = re.compile(IGNORE_FILE)
        
    def make_html(self):
        path = DOCUMENT_ROOT+self.parsed_path.path
        query=urllib2.unquote(self.parsed_path.query)
        if path == DOCUMENT_ROOT + "/search":            
            res = self.req_search(path,query)            
        elif os.path.isdir(path):
            res = self.req_index(path,query)
        elif os.path.isfile(path):
            res = self.req_file(path,query)
        else:
            print "failture"

        return res

    def header_html(self,title,path,q=""):
        html = """<!DOCTYPE HTML>
<html>
<head>
<meta charset="UTF-8">
<title> %s </title>
"""%(title)
        html+="""
<style type="text/css">
<!--
body {
    margin: auto;
    padding: 0 2em;
    max-width: 80%;
    border-left: 1px solid black;
    border-right: 1px solid black;
    font-size: 100%;
    line-height: 140%;
}
pre {
    border: 1px solid #090909;
    background-color: #f8f8f8;
    padding: 0.5em;
    margin: 0.5em 1em;
}
code {
    border: 1px solid #cccccc;
    background-color: #f8f8f8;
    padding: 2px 0.5em;
    margin: 0 0.5em;
}
a {
    text-decoration: none;
}
a:link, a:visited, a:hover {
    color: #4444cc;
}
a:hover {
    text-decoration: underline;
}
h1, h2, h3 {
    font-weight: bold;
    color: #2f4f4f;
}
h1 {
    font-size: 200%;
    line-height: 100%;
    margin: 1em 0;
    border-bottom: 1px solid #2f4f4f;
}
h2 {
    font-size: 175%;
    line-height: 100%;
    margin: 1em 0;
    padding-left: 0.5em;
    border-left: 0.5em solid #2f4f4f;
}
h3 {
    font-size: 150%;
    line-height: 100%;
    margin: 1em 0;
}
h4, h5 {
    font-weight: bold;
    color: #000000;
    margin: 1em 0 0.5em;
}
h4 { font-size: 125% }
h5 { font-size: 100% }
p {
    margin: 0.7em 1em;
    text-indent: 1em;
}
div.footnotes {
    padding-top: 1em;
    color: #090909;
}
div#header {
    margin-top: 1em;
    padding-bottom: 1em;
    border-bottom: 1px dotted black;
}
div#header > form {
    display: float;
    float: right;
    text-align: right;
}
a.filename {
    color: #666666;
a}
footer {
    border-top: 1px dotted black;
    padding: 0.5em;
    font-size: 80%;
    text-align: right;
    margin: 5em 0 1em;
}
blockquote {
    margin: 1em 3em;
    border: 2px solid #999;
    padding: 0.3em 0;
    background-color: #f3fff3;
}
hr {
    height: 1px;
    border: none;
    border-top: 1px solid black;
}
table {
    padding: 0;
    margin: 1em 2em;
    border-spacing: 0;
    border-collapse: collapse;
}
table tr {
    border-top: 1px solid #cccccc;
    background-color: white;
    margin: 0;
    padding: 0;
}
table tr:nth-child(2n) {
    background-color: #f8f8f8;
}
table tr th {
    font-weight: bold;
    border: 1px solid #cccccc;
    text-align: left;
    margin: 0;
    padding: 6px 13px;
}
table tr td {
    border: 1px solid #cccccc;
    text-align: left;
    margin: 0;
    padding: 6px 13px;
}
table tr th :first-child, table tr td :first-child {
    margin-top: 0;
}
table tr th :last-child, table tr td :last-child {
    margin-bottom: 0;
}

-->
</style>
<script>
function copy(text) {
  prompt("Copy filepath below:", text);
}
</script>
</head>
<body>
"""
        link_str=""
        uri = ""
        fp =path.replace(DOCUMENT_ROOT,'').split('/')
        for i in fp:
            if i ==u'':
                continue
            uri +='/'+i
            if os.path.isfile(DOCUMENT_ROOT+uri) or os.path.isdir(DOCUMENT_ROOT+uri):                
                link_str += '/' + "<a href='%s'>%s</a>"%(uri,i)
        
        link_str +=  "<a class='filename' href=\"javascript:copy('%s');\">[copy]</a>"%(path)
        link_str = "<a href='/'>%s</a>"%(DOCUMENT_ROOT) + link_str
        
        search="""
<form action="/search" method="get",accept-charset="UTF-8">
<input name="path" type="hidden" value="" />
<input name="q" type="text" value="" size="24" />
<input type="submit" value="search" />
</form>
"""
        return html+"<div id=\"header\">%s %s</div>"%(link_str,search)


    def footer_html(self):
        html ="""
<footer>
<a href="https://github.com/saiias/pymamemose">pymamemose: ReStructuredText memo server</a>
</footer>
</body>
</html>
"""
        return html
    
    def req_search(self,path,query):        
        query=query.split("&q=")[1]
        print query.decode('utf-8')
        found = self.find(path,query)
        html_title = "Serch in "+path
        title = "</div><h1>Seach in %s </h1>"%(path)        
        body =""
        if query == "":
            body+="<h2>No Keyword </h2>"
        elif len(found)==0:
            body+="<h2>Not Found</h2>"
        elif len(found)>0:
            body +='<ul>'
            for k,v in found.items():
                v=v.replace(DOCUMENT_ROOT+'/','')                            
                body +='''
<li><a href="%s">%s</a>
<a class='filename' href="javascript:copy('%s');\">[ %s , KB]</a></li>
'''%(v,k,v,k)
                
        body +='<ul>'
        body = title+body
        header_html = self.header_html(html_title,path,query)
        footer_html = self.footer_html()
        return  header_html+body+footer_html

    def req_file(self,req,res):
        """
        アクセスされた先がファイルのとき呼び出される。
        そのファイルがRest記法であれば、rst2htmlで変換してhtmlを出力する。
        req:アクセスされたパス
        res:クエリ
        """
        if os.path.splitext(req)[1]==".rst":
            body =subprocess.check_output(['rst2html.py',req])            
            body=body.split('<body>')[1]
            body=body.split('</body>')[0]            
            header_html = self.header_html(req,req)
            footer_html = self.footer_html()
            return header_html.encode('ascii')+body+footer_html.encode('ascii')
        
    def req_index(self,req,res):
        """
        アクセスされた先がフォルダのとき呼び出される。
        フォルダ内を、ディレクトリ、ReSTファイル、その他のファイルと分類して、hmtlを出力する。
        req:アクセスされたパス
        res:クエリ
        """
        global RECENT_NUM
        dirs,rest,others=self.directory_files(req)
        body = "</div><h1>Index of %s </h1>"%(req)
        if RECENT_NUM > 0:
            body += "<h2>Recent:</h2>"
            recent = self.recent_files()
            if len(recent) < RECENT_NUM:
                RECENT_NUM = len(recent)               
            body +='<ul>'
            index = 0
            for k,v in sorted(recent.items(),key=lambda x:x[1][1]):
                if index  == RECENT_NUM:
                    break
                v[0] =v[0].replace(DOCUMENT_ROOT+'/','')
                body +='''
<li><a href=" %s "> %s </a>
<a class='filename' href="javascript:copy(' %s ');\">[ %s , file]</a></li>
'''%(v[0],k,v[0],k)
            body +='</ul>'
            index +=1
            
        body += "<h2>Directories:</h2>"
        if len(dirs)>0:
            body +='<ul>'
            for k,v in dirs.items():
                body +='''
<li><a href=" %s "> %s </a>
<a class='filename' href="javascript:copy(' %s ');\">[ %s , dir]</a></li>
'''%(k,k,v,k)
            body +='</ul>'
            
        body += "<h2>Rest documents:</h2>"
        if len(rest)>0:
            body +='<ul>'
            for k,v in rest.items():
                size = str(getFileSize(v)/1024)
                v=v.replace(DOCUMENT_ROOT+'/','')
                body +='''
<li><a href=" %s "> %s </a>
<a class='filename' href="javascript:copy(' %s ');\">[ %s , %s KB]</a></li>
'''%(v,k,v,k,size)
            body +='</ul>'
            
        body += "<h2>Other files:</h2>"
        if len(others)>0:
            body +='<ul>'
            for k,v in others.items():
                size = str(getFileSize(v)/1024)
                v=v.replace(DOCUMENT_ROOT,'')
                
                body +='''
<li><a href=" %s "> %s </a>
<a class='filename' href="javascript:copy(' %s ');\">[ %s , %s KB]</a></li>
'''%(k,k,v,k,size)
            body +='</ul>'
        header_html = self.header_html(req,req)
        footer_html = self.footer_html()
        return  header_html+body+footer_html

    def find(self,path,query):
        """
        クエリに指定された文字列をサイト内で検索する。
        もし見つかればそのファイル名をキー、そのファイルまでのパスをバリューとして辞書に入れる。
        検索が終わると辞書を返す。
        """
        found = dict()
        for root,dirs,files in os.walk(DOCUMENT_ROOT):
            for file in files:
                for line in codecs.open(root+'/'+file,'r',encoding='utf-8'):
                    if line.find(query.decode('utf-8')) != -1:
                        found[file]=root+'/'+file                
        return found
    
    def recent_files(self):
        recent ={}
        for root,dirs,files in os.walk(DOCUMENT_ROOT):
            for file in files:
                if not isMatchedFile(self.ignoreobj,file):
                    mtime = os.stat(root+'/'+file)
                    recent[file]=[root+'/'+file,mtime]        
        return recent
        
    
    def directory_files(self,path):
        dirs =dict()
        rest = dict()
        others = dict()
                
        df = os.listdir(path)
        for item in df:
            if os.path.isdir(path+"/"+item):
                dirs[item]=path+"/"+item
            if os.path.isfile(path+"/"+item):
                if isMatchedFile(self.restpatobj,item):
                    rest[item]=path+'/'+item
                else:
                    if not isMatchedFile(self.ignoreobj,item):
                        others[item]= path+'/'+item

        return dirs,rest,others
    

def abspath(path):
    return os.path.abspath(path)

def getFileSize(file):
    return os.path.getsize(file)

def isMatchedFile(patobj,filename):
    """
    拡張子が.rstだったらTrue
    そうでないならFalse
    >>> pat = re.compile(".(rst|rest|txt)$")
    >>> isMatchedFile(pat,"test.rst")
    True
    >>> isMatchedFile(pat,"test.doc")
    False
    >>> pattern = re.compile("TAGS")
    >>> isMatchedFile(pattern,"DS_STORE")
    False
    >>> isMatchedFile(pattern,"TAGS")
    True
    """
    match = patobj.search(filename)
    return False if (match == None) else True

def command():
    server = bts.HTTPServer(('localhost', PORT), GetHandler)
    print 'Starting server'
    server.serve_forever()

if __name__ == '__main__':
    command()

