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
HANDLES = ["pho", "ChrisWu", "PeterASteele", "godmar", "richard_xu", "espeon", "tourist"]
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
            ProblemLetter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U']
            goodArr = {}
            badArr = {}
            for i in ProblemLetter:
                goodArr[i] = 0
                badArr[i] = 0
            if parsed_response['result'] != []:
                for i in parsed_response['result']:
                    if i['author']['participantType'] == "CONTESTANT":
                        if i['testset'] == "TESTS" or i['testset'] == "PRETESTS" or i['testset'] == "CHALLENGES":
                            if i['verdict'] == 'OK':
                                ok = ok + 1
                                goodArr[i['problem']['index']] += 1
                            elif i['verdict'] == 'CHALLENGED' or i['verdict'] == 'RUNTIME_ERROR' or i['verdict'] == 'WRONG_ANSWER' or i['verdict'] == 'TIME_LIMIT_EXCEEDED' or i['verdict'] == 'MEMORY_LIMIT_EXCEEDED':
                                bad = bad + 1
                                badArr[i['problem']['index']] += 1
#                         try:
# #                             print(str(i)) 
#                         except:
#                             e = sys.exc_info()[0]
# #                             print(str(e))   
            if len(handle) < 10:
                handle = handle + "\t"
            print(handle + "\t AC: " + str(ok) + " BAD: " + str(bad) + " TOTAL: " + str(ok + bad) + " Correct: " + str(100*ok/(ok+bad)) + "%")
            for i in ProblemLetter:
                try:
                    print(handle + "\t Problem " + i + " AC: " + str(goodArr[i]) + " BAD: " + str(badArr[i]) + " TOTAL: " + str(goodArr[i] + badArr[i]) + " Correct: " + str(100*goodArr[i]/(goodArr[i]+badArr[i])) + "%")
                except:
                    pass
        except:
            e = sys.exc_info()[0]
            print(str(e))
