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
HANDLES = ["pho", "ChrisWu", "PeterASteele", "godmar", "espeon", "tourist"]
MAX = "100000"
    
if __name__ == '__main__':
    for handle in HANDLES:
        try:
            request = urllib2.Request('http://codeforces.com/api/user.status?handle=' + handle + '&from=1&count=' + MAX)
            response = urllib2.urlopen(request)
            response_json = response.read();
            response_json = str(response_json.decode("utf-8"))
            parsed_response = json.loads(response_json)
            ok = 0
            bad = 0
            if parsed_response['result'] != []:
                for i in parsed_response['result']:
                    if i['author']['participantType'] == "CONTESTANT":
                        if i['testset'] == "TESTS" or i['testset'] == "PRETESTS":
                            if i['verdict'] == 'OK':
                                ok = ok + 1
                            else:
                                bad = bad + 1
#                         print(str(i))    
            if len(handle) < 10:
                handle = handle + "\t"
            print(handle + "\t AC: " + str(ok) + " BAD: " + str(bad) + " TOTAL: " + str(ok + bad) + " Correct: " + str(100*ok/(ok+bad)) + "%")
        except:
            e = sys.exc_info()[0]
            print(str(e))
