import matplotlib.pyplot as plt


def init_champs(m_data):
    champs = {}
    for p in m_data['info']['participants']:
        champs[p['participantId']] = p['championName']
    return champs


class Stats:
    def __init__(self,participantid,timeline ,data,minute=15):
        self.participantId = participantid
        self.minute = min(minute,len(timeline['info']['frames'])-1)
        self.kills = 0
        self.assists = 0
        self.deaths = 0
        self.kills_info = []
        self.assists_info = []
        self.deaths_info = []
        self.killed = []
        self.dead_by = []
        self.assisted_to = []
        self.assisted_by = []
        self.summoner_name = data['info']['participants'][participantid-1]['summonerName']
        for f in timeline['info']['frames'][:minute+1]:
            for e in f['events']:
                if e['type'] == 'CHAMPION_KILL':
                    if e['victimId'] == self.participantId:
                        self.deaths+=1
                        self.dead_by.append(e['killerId'])
                        self.deaths_info.append(e)
                    if e['killerId'] == self.participantId:
                        self.kills+=1
                        self.killed.append(e['victimId'])
                        self.kills_info.append(e)
                        if 'assistingParticipantIds' in e:
                            self.assisted_by.append(e['assistingParticipantIds'])
                        else:
                            self.assisted_by.append([])
                    if 'assistingParticipantIds' in e and int(self.participantId) in e['assistingParticipantIds']:
                        self.assists+=1
                        self.assisted_to.append(e['victimId'])
                        self.assists_info.append(e)
        try:
            self.gold = timeline['info']['frames'][self.minute]['participantFrames'][str(self.participantId)]['totalGold']
            self.cs = timeline['info']['frames'][self.minute]['participantFrames'][str(self.participantId)]['minionsKilled']
        except:
            print(self.minute,len(timeline['info']['frames']))
            self.gold = 0
            self.cs = 0
        self.champs = init_champs(data)
        
    def get_kill_positions(self,add_assists=False):
        x_values = []
        y_values = []
        kills = []
        if add_assists:
            kills = self.kills_info + self.assists_info
        else:
            kills = self.kills_info
        for e in kills:
            x_values.append(e['position']['x'])
            y_values.append(e['position']['y'])
        return x_values,y_values

    def get_kill_positions_different_gank(self,add_assists=False,):
        x_values = []
        y_values = []
        last = None
        kills = []
        skipped = 0
        if add_assists:
            kills = self.kills_info + self.assists_info
            kills.sort(key=lambda x: x['timestamp'])
        else:
            kills = self.kills_info
        for e in kills:
            if last != None and e['timestamp'] - last['timestamp'] > 15000:
                x_values.append(e['position']['x'])
                y_values.append(e['position']['y'])
            else:
                skipped+=1
            last = e
        if (self.kills+self.assists-skipped) != len(x_values):
            print("ERROR")
        return x_values,y_values


    def champ_name(self):
        return self.champs[self.participantId]
    
    def __repr__(self):
        return '{}: {} {}/{}/{} Gold = {} Cs = {}\n Killed {}\n Dead_by {}\n Assisted to {}\n Assisted by {}'.format(self.summoner_name,self.champ_name(),self.kills,self.deaths,self.assists,self.gold,self.cs,list(map(lambda x : self.champs[x] ,self.killed)) , list(map(lambda x: self.champs[x],self.dead_by)) ,list(map(lambda x: self.champs[x],self.assisted_to)), list(map(lambda x : list(map(lambda y : self.champs[y],x)),self.assisted_by)))


