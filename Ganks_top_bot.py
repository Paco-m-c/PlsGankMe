import matplotlib.pyplot as plt
import pandas as pd
from numpy import block
from riotwatcher import ApiError, LolWatcher

from Stats import Stats as St

LANE_OFFSET = 6000

def get_ganks_per_lane(x_values,y_values):
    tops_x = []
    bots_x = []
    other_x = []
    tops_y = []
    bots_y = []
    other_y = []
    for i in range(len(x_values)):
        if y_values[i] - x_values[i] > LANE_OFFSET:
            tops_x.append(x_values[i])
            tops_y.append(y_values[i])
        elif x_values[i] - y_values[i] > LANE_OFFSET:
            bots_x.append(x_values[i])
            bots_y.append(y_values[i])
        else:
            other_x.append(x_values[i])
            other_y.append(y_values[i])
    return tops_x, bots_x, other_x, tops_y, bots_y, other_y

def get_num_ganks_per_lane_per_game(x_values,y_values):
    tops = []
    bots = []
    other = []
    for i in range(len(x_values)):
        tops.append(0)
        bots.append(0)
        other.append(0)
        for j in range(len(x_values[i])):
            if y_values[i][j] - x_values[i][j] > LANE_OFFSET:
                tops[i]+=1
            elif x_values[i][j] - y_values[i][j] > LANE_OFFSET:
                bots[i]+=1
            else:
                other[i]+=1
    return tops, bots, other



def get_kill_positions_by_name(name, region= 'euw1',count = 100,start  = 0,minute=15):
    summ = lol_watcher.summoner.by_name(region, name)
    matches = lol_watcher.match.matchlist_by_puuid(region, summ['puuid'], count = count,start = start)
    x_values_per_game = []
    y_values_per_game = []
    iteration = 0
    for m in matches:
        while True:
            try:
                m_data =  lol_watcher.match.by_id(region, m)
                m_timeline = lol_watcher.match.timeline_by_match(region, m)
                break
            except:
                print("Error, retrying")
        iteration += 1
        for p in m_data['info']['participants']:
            if p['summonerName'] == name and p['teamPosition'] == 'JUNGLE':
                pid = p['participantId']
                st = St(pid, m_timeline,m_data,minute=minute)    
                print("Iteration:",iteration)
                x_values_aux, y_values_aux = st.get_kill_positions_different_gank(add_assists=True)
                x_values_per_game.append(x_values_aux)
                y_values_per_game.append(y_values_aux)
            elif p['summonerName'] == name:
                print(p['teamPosition'],p['role'],p['lane'], "Iteration:", iteration)
    return x_values_per_game, y_values_per_game

def init(key):
    global lol_watcher
    lol_watcher = LolWatcher(key)


