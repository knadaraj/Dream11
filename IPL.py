import itertools
import random
CSK = ['Faf', 'Gaikwad', 'Ali', 'Raina', 'Rayudu', 'Dhoni', 'Jadeja', 'Sam', 'Lungi', 'D Chahar', 'Thakur']
DC = ['Shaw', 'Dhawan', 'Smith', 'Pant', 'Stoinis', 'Hetmeyer', 'Axer', 'Rabada', 'Ishanth', 'Mishra', 'Avesh']
KKR = ['Rana', 'Gill', 'Tripathi', 'Morgan', 'Karthik', 'Russel', 'Naren', 'Cummins', 'Shivam', 'Krishna', 'Varun']
MI = ['Q de', 'Sharma', 'Surya', 'Hardik', 'Pollard', 'Kurunal', 'Neesham', 'Kulkarni', 'R Chahar', 'Boult', 'Bumrah']
PK = ['Rahul', 'Agarwal', 'Gayle', 'Hooda', 'Pooran', 'Khan', 'Hendri', 'Jordan', 'Shami', 'Bishnoi', 'Arshdeep']
RCB = ['Padikkal', 'Kohli', 'Rajat', 'Maxwell', 'ABD', 'Dan', 'Sundar', 'Jamieson', 'H Patel', 'Siraj', 'Chahal']
RR = ['Buttler', 'Jiaswal', 'Samson', 'Dube', 'Miller', 'Parag', 'Tewatia', 'Morris', 'Unatkat', 'Sakariya', 'Rahman']
SRH = ['Pandey', 'Bairstow', 'Williamson', 'Holder', 'Kedar', 'Vijay', 'Samad', 'Rashid', 'Bhuvi', 'Khaleel', 'Sandeep']
NETHERLAND = ['Myburgh', 'Dowd', 'Cooper', 'Seelaar', 'Edwards', 'Leede', 'Zulfiqar', 'Beek', 'Gugten', 'Klaassen', 'Glover']
IRELAND = ['Stirling', 'Balbirnie', 'Porterfield', 'Tector', 'Tucker', 'Simi', 'Dockrell', 'McBrine', 'McCarthy', 'Young', 'Little']
#dream11 = ['Faf', 'S Khan', 'Ali', 'Shami', 'A Singh', 'Rahul', 'Jadeja', 'Sam', 'Bravo', 'Chahar', 'Hooda']
keeper = ['Tucker', 'Edwards']
batsman = ['Myburgh', 'Stirling', 'Dowd', 'Balbirnie', 'Cooper', 'Porterfield', 'Tector']
allrounder = ['Seelaar', 'Simi', 'Leede', 'McBrine', 'Zulfiqar', 'Dockrell']
bowler = ['Beek', 'Klaassen', 'Glover', 'Gugten', 'McCarthy', 'Young', 'Little']
main_players = ['Bairstow', 'Pandey', 'Tewatia', 'Sakariya']
players = NETHERLAND + IRELAND
#print(players)
teams = list(itertools.combinations(players,11))
#print(len(teams))
valid_teams = []
for team in teams:
    #print(team)
    a = set(team).intersection(set(NETHERLAND))
    b = set(team).intersection(set(IRELAND))
    c = set(team).intersection(set(keeper))
    d = set(team).intersection(set(batsman))
    e = set(team).intersection(set(allrounder))
    f = set(team).intersection(set(bowler))
    g = set(team).intersection(set(main_players))
    #print(g)
    if len(a) == 7 and len(b) == 4 and len(c) >= 1 and len(d) in range(3,5) and len(e) >= 3 and len(f) in range(3,6):
        valid_teams.append(team)
        #if set(team) == set(dream11):
        #    print('Winner {}'.format(team))
print(len(valid_teams))
random_1 = random.sample(range(len(valid_teams)),2)
#dream_teams = random.sample(valid_teams,11)
i = 1
for x in random_1:
    print('Team %s : %s'%(i,valid_teams[x]))
    print('Team number : %s\n'%x)
    #print('Team Cap and VC : %s\n'%random.sample(dream,2))
    i += 1