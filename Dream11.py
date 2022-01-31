#!/usr/bin/env python3
"""
Created on Sat Apr 21 02:58:47 2019
@author: Karthik Nadarajan
"""
import itertools
import collections
import random
import time
import copy
class Dream11:
    def __init__(self,team1, team2, cat_range=[[1,3], [3,6], [1,4], [3,6]]):
        self.team1 = team1
        self.team2 = team2
        self.teams = {**team1, **team2}
        self.maxpts = 100
        self.minpts = 90
        self.cat_range = cat_range
        self.generatePlayers(team1, team2)

    def generatePlayers(self, t1, t2):
        self.t1_players = list(t1.keys())
        self.t2_players = list(t2.keys())
        self.t1t2_players = self.t1_players + self.t2_players
        self.player_types = {}
        x = {self.player_types.setdefault(self.teams[player]['type'],[]).append(player) for player in self.t1t2_players}
        #print(self.player_types)

    def generateAllComb(self, players, comb):
        return list(itertools.combinations(players, comb))

    def getValidTeams(self, teams, must,cat_ran=''):
        if not cat_ran:
            cat_ran = self.cat_range
        valid_teams = []
        for team in teams:
            if sum([self.teams[pl]['pts'] for pl in team]) not in range(self.minpts, self.maxpts+1):
                continue
            if sum([1 for pl in team if pl in self.t1_players]) not in range(4, 8):
                continue
            category = collections.Counter([self.teams[player]['type'] for player in team])
            if category['wk'] not in range(cat_ran[0][0],cat_ran[0][1]+1) or category['bat'] not in range(cat_ran[1][0],cat_ran[1][1]+1) \
                or category['all'] not in range(cat_ran[2][0],cat_ran[2][1]+1) or category['bowl'] not in range(cat_ran[3][0],cat_ran[3][1]+1):
                continue
            if not set(team).issuperset(set(must)):
                continue
            valid_teams.append(team)
        return valid_teams

    def selectTeams(self, count):
        st = time.time()
        allteams = self.generateAllComb(self.t1t2_players, 11)
        et = time.time()
        print(f"Time Taken for team comb : {et-st}")
        must_players = [pl for pl in self.t1t2_players if self.teams[pl]['max'] == count]
        valids = self.getValidTeams(allteams, must_players)
        print(f"Total Valid teams {len(valids)}")
        skip_players = set()
        [skip_players.add(x) for x in self.t1t2_players if self.teams[x]['max'] == 0]
        final_teams = {}
        self.players_count = collections.Counter()
        iter = 0
        pri = 0
        while len(final_teams) < count:
            iter += 1
            try:
                rand_num = random.choice(range(0,len(valids)))
            except IndexError:
                break
            team = valids[rand_num]
            valids.remove(team)
            if set(team) & skip_players:
                continue
            '''if skip_players:
                invalid = 0
                for pl in skip_players:
                    if pl in team:
                        invalid = 1
                        break
                if invalid:
                    continue
            if sum([1 for pl in team if pl in self.t1_players]) <= 5:
                pri += 1
                if pri >= 5:
                    continue'''
            self.players_count.update(team)
            [skip_players.add(x) for x in self.players_count if self.players_count[x] >= self.teams[x]['max']]
            final_teams[rand_num] = team
        print(f"No of Iterations : {iter}")
        return final_teams

    def print_players_count(self):
        for k,v in sorted(self.players_count.items(), key=lambda kv:(kv[1], kv[0])):
            print(f'{k} : {v}')


class Myteams:
    def __init__(self,team1, team2, cat_range=[[1,3], [3,6], [2,4], [3,6]]):
        self.team1 = team1
        self.team2 = team2
        self.teams = {**team1, **team2}
        self.maxpts = 100
        self.minpts = 85
        self.cat_range = cat_range
        self.generatePlayers(team1, team2)

    def generatePlayers(self, t1, t2):
        self.t1_players = list(t1.keys())
        self.t2_players = list(t2.keys())
        self.t1t2_players = self.t1_players + self.t2_players
        self.player_types = {}
        x = {self.player_types.setdefault(self.teams[player]['type'],[]).append(player) for player in self.t1t2_players}
        #print(self.player_types)

    def generateCatComb(self, cats=[], pl_ranges={}):
        if not cats:
            cats = [[1,len(pl_ranges['wk'])], [3,len(pl_ranges['bat'])], [1,len(pl_ranges['all'])], [3,len(pl_ranges['bowl'])]]
        pl_range = [[j for j in range(i[0],i[1]+1)] for i in cats]
        all_comb = list(itertools.product(*pl_range))
        cat_comb = [x for x in all_comb if sum(x) == 11]
        print(f"All Category combination : {cat_comb}")
        return cat_comb

    def generateAllComb(self, players, comb):
        return list(itertools.combinations(players, comb))

    def validateTeam(self, team):
        if sum([self.teams[pl]['pts'] for pl in team]) not in range(self.minpts, self.maxpts+1):
            return 0
        if sum([1 for pl in team if pl in self.t1_players]) not in range(4, 8) or len(team) != 11:
            return 0
        return 1

    def selectTeams(self, count):
        st = time.time()
        valid_comb = self.generateCatComb(cats=self.cat_range)
        final_teams = []
        self.players_count = collections.Counter()
        pl_cat_list = ['wk','bat','all','bowl']
        skip_player = set()
        [skip_player.add(x) for x in self.t1t2_players if self.teams[x]['max'] == 0]
        star_players = [pl for pl in self.t1t2_players if self.teams[pl]['max'] >= 7]
        star_players.sort(key= lambda x:self.teams[x]['max'], reverse=True)
        print(f'Star Players : {star_players}')
        min_comb = [1, 3, 1, 3]
        max_comb = [sum([self.teams[pl]['max'] for pl in self.player_types[pl_cat_list[i]]]) - (count*min_comb[i]) for i in range(4)]
        print(f"Max combination : {max_comb}")
        players_type = copy.deepcopy(self.player_types)
        iter = 0
        pri = 0
        max_limit = {}
        while len(final_teams) < count and iter < 550000:
            iter += 1
            break_flag, cont_flag = 0, 0
            form_team = []
            try:
                rand_comb = random.choice(valid_comb)
            except:
                break
            for n in range(len(rand_comb)):
                try:
                    plrs = random.sample(players_type[pl_cat_list[n]], rand_comb[n])
                    form_team += plrs
                except:
                    if len(players_type[pl_cat_list[n]]) < min_comb[n]:
                        break_flag = 1
                    cont_flag = 1
                    print("exception occurred")
                    valid_comb = self.generateCatComb(pl_ranges=players_type)
                    break
            if break_flag:
                break
            if cont_flag:
                continue
            [star_players.remove(pl) for pl in set(star_players).intersection(skip_player)]
            if set(form_team).intersection(skip_player):
                continue
            if len(final_teams) >= 5 and star_players:
                if len(set(form_team).intersection(set(star_players))) < len(star_players)/2:
                    if len(star_players) >= 3:
                        replace = round(len(star_players)/2)
                    else:
                        replace = 1
                    for i in range(replace):
                        st_pl = star_players[i]
                        for sp in enumerate(form_team):
                            if self.teams[st_pl]['type'] == self.teams[sp[1]]['type'] and sp[1] not in star_players:
                                form_team[sp[0]] = st_pl
                                break

            if not self.validateTeam(form_team):
                continue
            '''if sum([1 for pl in form_team if pl in self.t1_players]) <= 5:
                pri += 1
                if pri >= 5:
                    continue'''
            {max_limit.setdefault(pl_cat_list[t],0)+1 for t in range(4) if rand_comb[t] > min_comb[t]}
            for k,v in max_limit.items():
                index = pl_cat_list.index(k)
                if v == max_comb[index]:
                    self.cat_range[index][1] = min_comb[index]
                    print(self.cat_range)
                    valid_comb = self.generateCatComb(cats=self.cat_range)
            if max_limit:
                max_limit = {}
            self.players_count.update(form_team)
            try:
                [skip_player.add(x) for x in form_team if self.players_count[x] == self.teams[x]['max']]
            except:
                [print(x, players_type[self.teams[x]['type']]) for x in self.players_count if self.players_count[x] == self.teams[x]['max']]
            #[print(x) for x in self.players_count if self.players_count[x] == self.teams[x]['max']]
            final_teams.append([rand_comb, form_team])
        print(f"No of Iterations : {iter}")
        et = time.time()
        print(f"Time Taken for team comb : {et-st}")
        print(f"Players Type : {players_type}")
        print(f'Star Players left : {star_players}')
        return final_teams

    def print_players_count(self):
        for k,v in sorted(self.players_count.items(), key=lambda kv:(kv[1], kv[0])):
            print(f'{k} : {v}')


"""       
def Dream11s(team1, team2, team_count, t1_nos = 6, t2_nos=5, bat=[], bowl=[], wk=[], ar=[], cat_range=[[1,1], [3,5], [1,2], [3,5]]):
    players_point = {}
    t1_list = list(team1.keys())
    t2_list = list(team2.keys())
    players_point.update(team1)
    players_point.update(team2)
    players = t1_list + t2_list
    teams = list(itertools.combinations(players,11))
    valid_teams = []
    for team in teams:
        pts = 0
        for pl in team:
            pts += players_point[pl]
        if pts not in range(95, 101):
            continue
        a = set(team).intersection(set(t1_list))
        b = set(team).intersection(set(t2_list))
        c = set(team).intersection(set(wk))
        d = set(team).intersection(set(bat))
        e = set(team).intersection(set(ar))
        f = set(team).intersection(set(bowl))
        if len(c) in range(cat_range[0][0], cat_range[0][1]+1) and len(d) in range(cat_range[1][0], cat_range[1][1]+1) \
                and len(e) in range(cat_range[2][0], cat_range[2][1] + 1) and len(f) in range(cat_range[3][0], cat_range[3][1]+1):
            if len(a) == t1_nos:
                valid_teams.append(team)
    print("Total Valid Teams : %s"%len(valid_teams))
    count = 0
    while count < team_count:
        rand_num = random.choice(range(len(valid_teams)))
        count += 1
        yield (rand_num, valid_teams[rand_num])
    pass

#Teams
CSK = ['Faf', 'Gaikwad', 'Ali', 'Raina', 'Rayudu', 'Dhoni', 'Jadeja', 'Sam', 'Lungi', 'D Chahar', 'Thakur']
DC = ['Shaw', 'Dhawan', 'Smith', 'Pant', 'Stoinis', 'Hetmeyer', 'Axer', 'Rabada', 'Ishanth', 'Mishra', 'Avesh']
KKR = ['Rana', 'Gill', 'Tripathi', 'Morgan', 'Karthik', 'Russel', 'Naren', 'Cummins', 'Shivam', 'Krishna', 'Varun']
MI = ['Q de', 'Sharma', 'Surya', 'Hardik', 'Pollard', 'Kurunal', 'Neesham', 'Kulkarni', 'R Chahar', 'Boult', 'Bumrah']
PK = ['Rahul', 'Agarwal', 'Gayle', 'Hooda', 'Pooran', 'Khan', 'Hendri', 'Jordan', 'Shami', 'Bishnoi', 'Arshdeep']
RCB = ['Padikkal', 'Kohli', 'Rajat', 'Maxwell', 'ABD', 'Dan', 'Sundar', 'Jamieson', 'H Patel', 'Siraj', 'Chahal']
RR = ['Buttler', 'Jiaswal', 'Samson', 'Dube', 'Miller', 'Parag', 'Tewatia', 'Morris', 'Unatkat', 'Sakariya', 'Rahman']
SRH = ['Pandey', 'Bairstow', 'Williamson', 'Holder', 'Kedar', 'Vijay', 'Samad', 'Rashid', 'Bhuvi', 'Khaleel', 'Sandeep']
NETHERLAND = {'Myburgh':9, 'Dowd':9.5, 'Cooper':8.5, 'Seelaar':9.5, 'Edwards':8.5, 'Leede':8.5, 'Zulfiqar':8, 'Beek':8.5, 'Gugten':9, 'Klaassen':8.5, 'Glover':8}
IRELAND = {'Stirling':10.5, 'Balbirnie':9.5, 'Porterfield':9, 'Tector':8.5, 'Tucker':8.5, 'Simi':9, 'Dockrell':8.5, 'McBrine':9, 'McCarthy':8, 'Young':8.5, 'Little':8.5}
INDIA = {'RSharma':9, 'Gill':8.5, 'Pujara':9.5, 'Kohli':10, 'Rahane':8.5, 'Jadeja':9, 'Pant':9, 'Ashwin':9, 'Shami':8.5, 'Ishant':8.5, 'Bumrah':9}
NEWZEALAND = {'Conway':8.5, 'Latham':9, 'Williamson':10, 'Taylor':9, 'Nicholls':9, 'Watling':8.5, 'Patel':8, 'Jamieson':8.5, 'Southee':9, 'Wagner':8.5, 'Boult':9}
Islamabad = {'Khawaja':10, 'Munro':9.5, 'Akhlaq':8, 'Iftikhar':9.5, 'Shadab':9, 'Talat':8.5, 'Asif':8.5, 'Faheem':9, 'Hasan':9, 'Wasim':8.5, 'Javed':8.5}
Multan = {'Masood':8.5, 'Rizwan':11, 'Sohaib':9.5, 'Charles':8.5, 'Rossouw':9, 'Khushdil':8.5, 'Sohail':8.5, 'Muzarabani':8, 'Imran':8.5, 'Tahir':9, 'Dhani':9}
Peshawar = {'Zazai':9, 'Akmal':9.5, 'Imam':8.5, 'Malik':9.5, 'Khalid':9, 'Rovman':8.5, 'Rutherford':9, 'Riaz':9, 'Umaid':9, 'Irfan':8.5, 'Imran':8.5}
ENGLAND = {'Buttler':10, 'Roy':9, 'Malan':9.5, 'Bairstow':10, 'Morgan':9, 'Ali':8.5, 'Curran':9, 'Woakes':8.5, 'Jordan':8.5, 'Wood':8.5, 'Rashid':9}
SRILANKA = {'Gunathilaka':9, 'Kusal':9, 'Oshada':8.5, 'Nissanka':8, 'Mendis':8.5, 'Dhananjaya':9, 'Shanaka':8.5, 'Hasaranga':9, 'Dananjaya':8.5, 'Chameera':8.5, 'Sandakan':8.5}

#Catagory Players
keepers = ['Buttler', 'Bairstow', 'Kusal']
batsmans = ['Roy', 'Malan', 'Morgan', 'Gunathilaka', 'Oshada', 'Nissanka', 'Mendis']
allrounders = ['Ali', 'Curran', 'Dhananjaya', 'Shanaka', 'Hasaranga']
bowlers = ['Woakes', 'Jordan', 'Wood', 'Rashid', 'Dananjaya', 'Chameera', 'Sandakan']

WTC = Dream11(ENGLAND, SRILANKA, 3, t1_nos=4, bat=batsmans, bowl=bowlers, wk=keepers, ar=allrounders, cat_range=[[1,3], [3,4], [2,4], [3,5]])
for i,j in WTC:
    print(f' Team {i} : {j}')
"""

