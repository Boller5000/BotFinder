import urllib.request, json,random
region = 'euw1'
apiKey = ''
bots = []
apiCalls = 0


def getSummoner(name):

    url = 'https://'+region+'.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + name+ '?api_key='+apiKey
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    global apiCalls
    apiCalls+=1
    return data

def getMatches(accountId):

    url = 'https://'+region+'.api.riotgames.com/lol/match/v4/matchlists/by-account/' + accountId + '?api_key='+apiKey
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    matchId = data['matches']
    global apiCalls
    apiCalls+=1
    return matchId
def getMatch(matchId):
    url = 'https://'+region+'.api.riotgames.com/lol/match/v4/matches/' + str(matchId) + '?api_key='+apiKey
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    global apiCalls
    apiCalls+=1
    return data
def isBotMatch(matchId):
    data = getMatch(matchId)
    accountId = data['participantIdentities'][6]['player']['accountId']
    return (accountId == str(0))
def getMastery(summonerId):
    url = 'https://'+region+'.api.riotgames.com/lol/champion-mastery/v4/scores/by-summoner/' + summonerId + '?api_key='+apiKey
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    matchId = data
    global apiCalls
    apiCalls+=1
    return (matchId == 0)

def checkPlayer(name):
    summonerData = getSummoner(name)
    print(" ")
    summonerName = summonerData['name']
    summonerLevel = summonerData['summonerLevel']
    accountId = summonerData['accountId']
    summonerId = summonerData['id']
    masteryLevel = getMastery(summonerId)


    print('Summoner Name: '+ summonerName)
    print('Summoner Level: ' + str(summonerLevel))
    print('Account ID(Encrypted): ' + str(accountId))
    print('Summoner ID(Encrypted): ' + str(summonerId))
    print('Mastery indicator: ' + str(masteryLevel))
    if(summonerLevel >= 18 and masteryLevel):
        matchHistory = getMatches(accountId)
        botIndicatorMatch = matchHistory[int(random.uniform(0,20))]['gameId']
        bot = isBotMatch(botIndicatorMatch)
        print('Bot indicator: ' + str(bot))
        if(bot):
            bots.append(summonerName)
            for player in getMatch(botIndicatorMatch)['participantIdentities']:
                selectedPlayer = player['player']
                if(selectedPlayer['summonerName'] != summonerName):
                    if(selectedPlayer['accountId'] != str(0)):
                        if(selectedPlayer['summonerName'] not in bots):
                            print('more bots have been found')
                            checkPlayer(selectedPlayer['summonerName'])



print('--------------------------------------Bot finder V.1.0.0-----------------------------------------\n\n\n')
f = open('bots.txt','r')
for x in f:
    bots.append(x.rstrip('\n'))
print('bots.txt read as already know names-summoners will be ignored\n')
print('loaded names: ' + str(len(bots)))
f.close()
apiCalls = 0
name = input('Enter summoner Name: ')
try:
    checkPlayer(name)
except:
    print('max calls reached or invalid name or just an error(ApiCalls: ' + str(apiCalls)+')')
f = open('bots.txt','w')
#f.write('#' + str(len(bots)) + 'Bots have been found(' + str(apiCalls) + 'api calls)')
for player in bots:
    f.write(player + '\n')
f.close()
exit()
