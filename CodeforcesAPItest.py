'''
Created on Aug 17, 2016

@author: Peter
'''
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import sys
import ast
import json
HANDLE = "PeterASteele"
MAX = "100000"
    
if __name__ == '__main__':
    try:
        request = urllib2.Request('http://codeforces.com/api/user.status?handle=' + HANDLE + '&from=1&count=' + MAX)
        response = urllib2.urlopen(request)
        response_json = response.read();
        response_json = str(response_json.decode("utf-8"))
        parsed_response = json.loads(response_json)
        ok = 0;
        bad = 0;
        if parsed_response['result'] != []:
            for i in parsed_response['result']:
                if i['author']['participantType'] == "CONTESTANT":
                    if i['testset'] == "TESTS":
                        if i['verdict'] == 'OK':
                            ok = ok + 1
                        else:
                            bad = bad + 1
#                         print(str(i))              
        print("AC: " + str(ok) + " BAD: " + str(bad) + " TOTAL: " + str(ok + bad) + " Correct: " + str(100*ok/(ok+bad)) + "%")
    except:
        e = sys.exc_info()[0]
        print(str(e))
