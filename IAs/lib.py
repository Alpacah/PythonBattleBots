import sys
import os
import json

# GLOBALS
CELL_EMPTY = -1
CELL_OBSTACLE = -2

# GRABBING INFOS
PATH = os.getcwd().replace('\\', '/') + '/' + sys.argv[1]
#PATH = 'C:/Users/arthc/Desktop/PythonBattleBots/Fights/45/'
with open(PATH + 'game.dat', 'r') as file:
    GAME_DAT = json.loads(file.read())
with open(PATH + 'players.dat', 'r') as file:
    PLAYERS_DAT = json.loads(file.read())
with open(PATH + 'map.dat', 'r') as file:
    MAP_DAT = json.loads(file.read())

# INFO FUNCTIONS
def myId():
    global GAME_DAT
    return GAME_DAT['whoPlays']

def getEnemyId():
    global PLAYERS_DAT
    for player in PLAYERS_DAT:
        if player['id'] != myId():
            return player['id']

def getCell(entity):
    global PLAYERS_DAT
    return [PLAYERS_DAT[entity]['x'], PLAYERS_DAT[entity]['y']]

def getCellContent(x, y):
    global MAP_DAT
    if y >= 0 and x >= 0 and y < len(MAP_DAT) and x < len(MAP_DAT[y]):
        if MAP_DAT[y][x] > 0: return 0
        else: return MAP_DAT[y][x]
    else:
        return CELL_OBSTACLE

def getObstacles():
    global MAP_DAT
    OBSTACLES = []
    HEIGHT = len(MAP_DAT)
    WIDTH = len(MAP_DAT[0])
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if getCellContent(x,y) == CELL_OBSTACLE:
                OBSTACLES.append([x,y])
    return OBSTACLES

def getLineOfSight(pos, pos2):
    
    OBSTACLES = getObstacles()      
    if pos2[0] != pos[0]:
        for obstacle in OBSTACLES:
            u = 0
            d = 0
            if (obstacle[0] > pos[0]) == (pos2[0] > pos[0]) and (obstacle[1] > pos[1]) == (pos2[1] > pos[1]) and abs(obstacle[0]-pos[0])+abs(obstacle[1]-pos[1]) < abs(pos[0]-pos2[0])+abs(pos[1]-pos2[1]) and obstacle != pos:
                for a, b in [[0,0], [0,1], [1,0], [1,1]]: # Check that the 4 corners of the obstacle are below or above the line between pos and [x,y]
                    if obstacle[1]+b > ((pos[1]-pos2[1])/(pos[0]-pos2[0]))*(obstacle[0]+a-pos2[0]-0.5)+pos2[1]+0.5:
                        u += 1
                    elif obstacle[1]+b < ((pos[1]-pos2[1])/(pos[0]-pos2[0]))*(obstacle[0]+a-pos2[0]-0.5)+pos2[1]+0.5:
                        d += 1
                    else:
                        u += 1
                        d += 1
                if d != 4 and u != 4:
                    print(pos2[0],pos2[1],obstacle)
                    return 0
    else:
        for obstacle in OBSTACLES:
            if obstacle[0] == pos2[0] and (min(pos[1], pos2[1]) < obstacle[1] < max(pos[1], pos2[1])):
                return 0    
    return 1
    


# ACTION FUNCTIONS
def moveOn(x, y):
    print('[MOVE] {0} {1}'.format(x, y))
    return 1

def mark(x, y, color):
    print('[MARK] {0} {1} {2}'.format(x, y, color))
    return 1
