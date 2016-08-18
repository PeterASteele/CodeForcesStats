'''
Created on Aug 17, 2016

@author: Peter and Chris
'''
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import sys
import ast
import json
import re

pattern = re.compile('div\.?\s*(\d)', re.IGNORECASE)
def get_division(contest_name):
    match = pattern.search(contest_name)
    if match:
        return int(match.group(1))
    else:
        return 2

# Can delete this, just testing the regex
# print('Codeforces Round #360 (Div. 1)' + ' ' + get_division('Codeforces Round #360 (Div. 1)'))
# print('Codeforces Round #360 (Div. 2)' + ' ' + get_division('Codeforces Round #360 (Div. 2)'))
# print('VK Cup 2016 - Round 1 (Div.1 Edition)' + ' ' + get_division('VK Cup 2016 - Round 1 (Div.1 Edition)'))
# print('Codeforces Beta Round #12 (Div 2 Only)' + ' ' + get_division('Codeforces Beta Round #12 (Div 2 Only)'))
# print('Codeforces Round #355 (div. 1)' + ' ' + get_division('Codeforces Round #355 (div. 1)'))
# print('Codeforces Round #356 (div. 2)' + ' ' + get_division('Codeforces Round #356 (div. 2)'))

contest_id_to_div = {}
contest_list = json.loads(str(urllib2.urlopen(urllib2.Request('http://codeforces.com/api/contest.list?gym=true')).read().decode("utf-8")))['result']
for contest in contest_list:
    division = get_division(contest['name'])
    contest_id_to_div[contest['id']] = division
contest_list = json.loads(str(urllib2.urlopen(urllib2.Request('http://codeforces.com/api/contest.list?gym=false')).read().decode("utf-8")))['result']
for contest in contest_list:
    division = get_division(contest['name'])
    contest_id_to_div[contest['id']] = division
# print(contest_id_to_div)

HANDLES = ["pho", "ChrisWu", "PeterASteele", "godmar", "richard_xu", "intrepidcoder", "espeon", "tourist"]
MAX = "100000"

if __name__ == '__main__':
    for handle in HANDLES:
        try:
            request = urllib2.Request('http://codeforces.com/api/user.status?handle=' + handle + '&from=1&count=' + MAX)
            response = urllib2.urlopen(request)
            response_json = response.read()
            response_json = str(response_json.decode("utf-8"))
            parsed_response = json.loads(response_json)
            ok = 0
            bad = 0
            ProblemLetter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            goodArr = {}
            badArr = {}
            goodTags = {}
            badTags = {}
            for i in ProblemLetter:
                goodArr[i] = 0
                badArr[i] = 0
            if parsed_response['result'] != []:
                for i in parsed_response['result']:
                    if i['author']['participantType'] != "PRACTICE":
                        if i['testset'] == "TESTS" or i['testset'] == "PRETESTS" or i['testset'] == "CHALLENGES":
                            if i['verdict'] == 'OK':
                                ok = ok + 1
                                
                                for j in i['problem']['tags']:
                                    if j in goodTags.keys():
                                        goodTags[j] += 1
                                    else:
                                        goodTags[j] = 1
                                        badTags[j] = 0
                                goodArr[chr(ord(i['problem']['index'])+2-contest_id_to_div[i['contestId']]+2-contest_id_to_div[i['contestId']])] += 1
                            elif i['verdict'] == 'CHALLENGED' or i['verdict'] == 'RUNTIME_ERROR' or i['verdict'] == 'WRONG_ANSWER' or i['verdict'] == 'TIME_LIMIT_EXCEEDED' or i['verdict'] == 'MEMORY_LIMIT_EXCEEDED':
                                bad = bad + 1
                                for j in i['problem']['tags']:
                                    if j in badTags.keys():
                                        badTags[j] += 1
                                    else:
                                        badTags[j] = 1
                                        goodTags[j] = 0
                                badArr[chr(ord(i['problem']['index'])+2-contest_id_to_div[i['contestId']]+2-contest_id_to_div[i['contestId']])] += 1
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
                    print(handle + "\t\t Problem " + i + " -> AC: " + str(goodArr[i]) + " BAD: " + str(badArr[i]) + " TOTAL: " + str(goodArr[i] + badArr[i]) + " Correct: " + str(100*goodArr[i]/(goodArr[i]+badArr[i])) + "%")
                except:
                    pass
            for i in badTags.keys():
                print(handle + "\t\t Tag " + i + " -> AC: " + str(goodTags[i]) + " BAD: " + str(badTags[i]) + " TOTAL: " + str(goodTags[i] + badTags[i]) + " Correct: " + str(100*goodTags[i]/(goodTags[i]+badTags[i])) + "%")
        except:
            e = sys.exc_info()[0]
            print(str(e))
