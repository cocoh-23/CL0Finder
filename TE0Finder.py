from requests import Request, Session
import argparse
from urllib.parse import urlparse as parse

#try:
#    from http.client import HTTPConnection
#except ImportError:
#    from httplib import HTTPConnection
#HTTPConnection.debuglevel = 2

parser = argparse.ArgumentParser()
parser.add_argument('-u','--urlFile', help='file with urls to test from specific host', required=True)
args = parser.parse_args()
proxies = {'http': '127.0.0.1:8080','https': '127.0.0.1:8080'}

URLFilePath = args.urlFile.strip()
session = Session()

URLs = open(URLFilePath, "r")
for url in URLs:
    CandidateMethod = url.split("---")[1]
    FullUrl = parse(url.split("---")[0])
    NormalRespCode = url.split("---")[2]
    TE0Scheme = FullUrl.scheme
    TE0Host = FullUrl.netloc
    TE0TestPath = FullUrl.path
    TE0ResultPath = FullUrl.path
    TE0TestBody = '2c\r\nGET /thisPageDoesNotExist HTTP/1.1\r\nFoo: Bar\r\n0\r\n\r\n'
    if(CandidateMethod == 'GET'):#We send the second get always, as the same request can appear several times with different methods
        TE0TestPrepReq = Request('GET', TE0Scheme + "://" + TE0Host + TE0TestPath, data=TE0TestBody)
        TE0ResultPrepReq = Request('GET', TE0Scheme + "://" + TE0Host + TE0TestPath)
        TE0TestPrep = TE0TestPrepReq.prepare()
        TE0ResultPrep = TE0ResultPrepReq.prepare()
        TE0TestPrep.headers['content-length'] = 0 #Needed to full server that request is chunked
        TE0TestPrep.headers['Transfer-Encoding'] = 'chunked'
        TE0TestPrep.headers['Connection'] = 'keep-alive'
        TE0Test = session.send(TE0TestPrep,stream=True)
        TE0Result = session.send(TE0TestPrep,stream=True)
    elif(CandidateMethod == 'POST'):
        TE0TestPrepReq = Request('POST', TE0Scheme + "://" + TE0Host + TE0TestPath, data=TE0TestBody)
        TE0ResultPrepReq = Request('POST', TE0Scheme + "://" + TE0Host + TE0TestPath)
        TE0TestPrep = TE0TestPrepReq.prepare()
        TE0ResultPrep = TE0ResultPrepReq.prepare()
        TE0TestPrep.headers['content-length'] = 0 #Needed to full server that request is chunked
        TE0TestPrep.headers['Transfer-Encoding'] = 'chunked'
        TE0TestPrep.headers['Connection'] = 'keep-alive'
        TE0Test = session.send(TE0TestPrep,stream=True)
        TE0Result = session.send(TE0TestPrep,stream=True)
    else: #PUT
        TE0TestPrepReq = Request('PUT', TE0Scheme + "://" + TE0Host + TE0TestPath, data=TE0TestBody)
        TE0ResultPrepReq = Request('PUT', TE0Scheme + "://" + TE0Host + TE0TestPath)
        TE0TestPrep = TE0TestPrepReq.prepare()
        TE0ResultPrep = TE0ResultPrepReq.prepare()
        TE0TestPrep.headers['content-length'] = 0 #Needed to full server that request is chunked
        TE0TestPrep.headers['Transfer-Encoding'] = 'chunked'
        TE0TestPrep.headers['Connection'] = 'keep-alive'
        TE0Test = session.send(TE0TestPrep,stream=True)
        TE0Result = session.send(TE0TestPrep,stream=True)
    print("[%s] - The response code for %s is %s and after CL0 is %s for method %s" % (NormalRespCode,TE0TestPath,str(TE0Test.status_code),str(TE0Result.status_code),CandidateMethod))
