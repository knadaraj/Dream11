import sys

from Dream11 import *
import json
import os
import sys

input_file = os.path.join(sys.path[0], 'teams_input.json')
with open(input_file) as f:
    all_teams = json.load(f)

team1 = all_teams['BBL']['STA']
team2 = all_teams['BBL']['REN']
teams = {**team1, **team2}
#teams = team1
total_players = 0
for pl in teams:
    total_players += teams[pl]['max']
print(f" Total size : {total_players}")
print("-------------------------")
method1 = 1
if method1:
    match = Dream11(team1, team2, cat_range=[[1,3], [3,5], [1,3], [3,6]])
    teams = match.selectTeams(4)
    i = 1
    for k,v in teams.items():
        print("***************")
        print(f'Team {i} : {k}')
        print(v)
        i += 1
    print("\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n")
    match.print_players_count()
else:
    match = Myteams(team2, team1, cat_range=[[1,3], [3,6], [1,4], [3,5]])
    teams = match.selectTeams(10)
    for i in range(0,len(teams)):
        print("***************")
        print(f'Team {i+1} : ',end='')
        print(*teams[i][0],sep='-')
        print(teams[i][1])
    print("\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n")
    match.print_players_count()
