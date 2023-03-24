# CL.0 and TE.0 Finder
Two scripts that together automate the manual task of finding CL0 vulnerable endpoints ([Technique](https://portswigger.net/web-security/request-smuggling/browser/cl-0) discovered by James Kettle). As a result of a specific behaviour in one of the Web Security Academy client desync labs, I also add a script to find TE.0 vulnerabilities in the wild and see what happens (this technique is thought to theoretically break as the smuggled request has to be sent with the chunk length as a prefix. For the chunk ending, i do not send the 0. Lets see what happens in the wild!).

## Usage
The best and easy way to use this tool, is to navigate any target you want proxying the traffic through Burp Suite, and export all the intercepted links **Dashboard** -> **Target** -> **Right click on your target** -> **Copy links in this host**. Its better to include every static asset such as .js and .css files, as CL0 vulnerabilities sometimes arise from specific requests to these files.
After this, save every URL to a file and execute **FindCL0CandidateURLs.py** specifying that file (-u), saving the output (-o) to a new file like this:

```bash
python3 FindCL0CandidateURLs.py -u urlsToTest -o urls
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

* [200] Means that the first normal request to the url (issued by FindCL0CandidateURLs.py), generated a 200 OK response.
* 422 means that the response code to the smuggled request was 422 Unprocesable Entity
* 404 means that the follow up request generated a 404 Not Found response code

By seeing these three response codes, we see there is an odd behaviour as the follow up request that is sent after the smuggled request, generates a 404 response code, and by sending a normal request, we receive a 200 response code. This is a nice clue of an endpoint we should test to see if indeed is vulnerable to CL0.
