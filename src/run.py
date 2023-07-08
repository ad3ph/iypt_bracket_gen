from copy import deepcopy
import numpy as np
from src.generator import generate_bracket_list
from src.genetic_generator import random_swap
from .dumper import Dumper
import pickle as pkl

#We are giving weights in order for the 'basic' disturbances in bracket make the partial coefficients equal to nearly 1
CALIBRATION_COEFFICIENTS = dict(
    meets=0.5,
    four_teams_total=2,
    first_roles=1,
    room_visits=1,
    consequent_fours=1
)

#These weights are real weights of importance for every criteria. In parts of 1
WEIGHTS = dict(
    meets=2,
    four_teams_total=3,
    first_roles=0.2,
    room_visits=0.1,
    consequent_fours=0.2
)

MAX_ITER = 1500
DO_SLEEP_REARRANGEMENT = False
REARRANGEMENT_ENTROPY_INCREASE = 1 #... this many random swaps

GENERATE_DATASET_MODE = False

class Bracket:
    def __init__(self, _teams, _fights):
        self.number_of_teams = _teams
        self.number_of_fights = _fights
        self.fights_list = [[] for _ in range(self.number_of_fights)]
        self.number_of_rooms = self.number_of_teams // 3
        self.rooms_list = [i for i in range(self.number_of_rooms)]

        self.teams_list = []
        self.team_names_list = []
        self.fu = 0
        self.as_list = []

    def find_fu(self):
        self.fu = FuMetric(self).fu

    def show_fu_results(self):
        fu = FuMetric(self)
        fu.show_results()

    def print(self):
        print(f'Bracket for {self.number_of_teams} teams and {self.number_of_fights} fights')
        print(f'You will need {self.number_of_rooms} rooms and {self.number_of_teams % 3} four-team fights will happen')
        print(f'Teams participating: {self.team_names_list}')
        for j in range(self.number_of_rooms):
            print(f'\tRoom {j + 1}\t', end='|')
        print()
        for i in range(self.number_of_fights):
            print(f'FIGHT {i+1}:')
            for j in range(self.number_of_rooms):
                print('\t', *self.fights_list[i][j], '\t', end='|')
            print()
        print('Fu = ', self.fu)


    def from_list(self, li):
        self.as_list = li
        *self.fights_list, = li
        self.teams_list = [i for i in range(1, self.number_of_teams+1)]
        self.team_names_list = [chr(i+64) for i in self.teams_list]

class FuMetric:
    def __init__(self, bracket):
        self.fu = None
        self.bracket = bracket
        self.number_of_teams = self.bracket.number_of_teams
        self.meets_number_matrix = None
        self._find_fu()

    def _meets_number(self):
        self.meets_number_matrix = np.zeros((self.number_of_teams, self.number_of_teams))
        for i in range(self.number_of_teams):
            for j in range(self.number_of_teams):
                if i == j:
                    continue
                i_j_meets_number = 0
                for fight in self.bracket.fights_list:
                    for room in fight:
                        if i+1 in room and j+1 in room:
                            i_j_meets_number += 1

                self.meets_number_matrix[i, j] = i_j_meets_number

        self.meets_coef = np.sum(self.meets_number_matrix[self.meets_number_matrix > 1] - 1)

    def _four_team_fights(self):
        four_team_fights_numbers = []
        for team in range(self.number_of_teams):
            four_team_fights_number = 0
            for fight in self.bracket.fights_list:
                for room in fight:
                    if len(room) == 4 and team+1 in room:
                        four_team_fights_number += 1
            four_team_fights_numbers.append(four_team_fights_number)

        self.four_team_fights_numbers = four_team_fights_numbers
        self.four_team_fights_coef = round(np.std(four_team_fights_numbers)/np.average(four_team_fights_numbers), 3) if np.average(four_team_fights_numbers) != 0 else 0

    def _first_roles(self):
        first_roles_per_team = [[], [], [], []]

        for team in range(self.number_of_teams):

            for role in first_roles_per_team:
                role.append(0)

            for fight in self.bracket.fights_list:
                for room in fight:
                    if team+1 in room:
                        first_roles_per_team[room.index(team+1)][team] += 1

        self.first_roles_per_team = first_roles_per_team

        sum_delta = 0
        for team in range(self.number_of_teams):
            team_list = [first_role[team] for first_role in self.first_roles_per_team]
            team_delta = max(team_list) - min(team_list)
            sum_delta += team_delta
        self.first_roles_coef = sum_delta

    def _room_visits(self):
        room_visits_per_team = [[] for _ in range(self.bracket.number_of_rooms)]

        for team in range(self.number_of_teams):

            for room in room_visits_per_team:
                room.append(0)

            for fight in self.bracket.fights_list:
                for room_index, room in enumerate(fight):
                    if team+1 in room:
                        room_visits_per_team[room_index][team] += 1

        self.room_visits_per_team = room_visits_per_team

        sum_delta = 0
        for team in range(self.number_of_teams):
            team_list = [room_visits[team] for room_visits in self.room_visits_per_team]
            team_delta = max(team_list) - min(team_list)
            sum_delta += team_delta
        self.room_visits_coef = sum_delta

    def _consequent_four_team_fights(self):
        self.consequent_fours_coef = 0

        if self.bracket.number_of_fights >= 2:
            self.consequent_fours_per_team = []
            flags_teams = []
            for team in range(self.number_of_teams):
                flags = []
                for fight_index, fight in enumerate(self.bracket.fights_list):
                    flags.append(0)

                    for room in fight:
                        if team + 1 in room and len(room) == 4:
                            flags[fight_index] = 1
                flags_teams.append(flags)

            for flags_team in flags_teams:
                consequent_fours_team = 0
                for i in range(len(flags_team)-1):
                    if flags_team[i] == flags_team[i+1] == 1:
                        consequent_fours_team += 1
                self.consequent_fours_per_team.append(consequent_fours_team)

            self.consequent_fours_coef = sum(self.consequent_fours_per_team)

    def _find_fu(self):
        self._meets_number()
        self._four_team_fights()
        self._first_roles()
        self._room_visits()
        self._consequent_four_team_fights()
      
        self.fu = round(self.meets_coef * CALIBRATION_COEFFICIENTS['meets'] * WEIGHTS['meets'] \
                  + self.four_team_fights_coef * CALIBRATION_COEFFICIENTS['four_teams_total'] * WEIGHTS['four_teams_total'] \
                  + self.first_roles_coef * CALIBRATION_COEFFICIENTS['first_roles'] * WEIGHTS['first_roles'] \
                  + self.room_visits_coef * CALIBRATION_COEFFICIENTS['room_visits'] * WEIGHTS['room_visits'] \
                  + self.consequent_fours_coef * CALIBRATION_COEFFICIENTS['consequent_fours'] * WEIGHTS['consequent_fours'], 3)
  
    def show_results(self):
        print('FU METRIC RESULTS')
        print('Meets matrix')
        print(self.meets_number_matrix.astype(int))
        print()
        print('Team           | ', *self.bracket.team_names_list)
        print('4-Team Fights  | ', *self.four_team_fights_numbers)
        print('First reporter | ', *self.first_roles_per_team[0])
        print('First opponent | ', *self.first_roles_per_team[1])
        print('First reviewer | ', *self.first_roles_per_team[2])
        print('First observer | ', *self.first_roles_per_team[3])
        for i in range(len(self.room_visits_per_team)):
            print(f'Room {i+1}         | ', *self.room_visits_per_team[i])
        print('Consequent 4TF | ', *self.consequent_fours_per_team)
        print()
        print('Uncalibrated coefficients:')
        print('Meets = ', self.meets_coef)
        print('Four-Team fights = ', self.four_team_fights_coef)
        print('First roles = ', self.first_roles_coef)
        print('Room visits = ', self.room_visits_coef)
        print('Consequent Four-Team fights = ', self.consequent_fours_coef)
        print()
        print('Calibrated coefficients:')
        print('Meets = ', self.meets_coef * CALIBRATION_COEFFICIENTS['meets'])
        print('Four-Team fights = ', self.four_team_fights_coef * CALIBRATION_COEFFICIENTS['four_teams_total'])
        print('First roles = ', self.first_roles_coef * CALIBRATION_COEFFICIENTS['first_roles'])
        print('Room visits = ', self.room_visits_coef * CALIBRATION_COEFFICIENTS['room_visits'])
        print('Consequent Four-Team fights = ', self.consequent_fours_coef * CALIBRATION_COEFFICIENTS['consequent_fours'])
        print()
        print('Weights are ', WEIGHTS)
        print()        
        print('Fu =', self.fu)
        print()
        print('(coefficients are calibrated such way that a perfect bracket has Fu = 0 and a bracket with one basic disturbance with WEIGHT = 1 has Fu = 1)')

def get_optimized_bracket(t, f):
    teams_number = t #int(input('Teams:\n'))
    fights_number = f #int(input('Fights:\n'))

    initial_bracket = Bracket(teams_number, fights_number)
    initial_bracket.from_list(generate_bracket_list(teams_number, fights_number))
    initial_bracket.find_fu()

    old_bracket = deepcopy(initial_bracket)
    iter_counter = 0
    dumper = Dumper()

    while True:
        iter_counter += 1
        new_bracket = Bracket(teams_number, fights_number)

        #TODO: add swap code to random_swap, go neural after MAX_ITER is exceeded

        new_bracket.from_list(random_swap(old_bracket.as_list))

        new_bracket.find_fu()

        with open('log.txt', 'a') as loh:
            loh.write(str(new_bracket.fu)+'\n')

        if new_bracket.fu < old_bracket.fu:
            dumper.write_x(old_bracket.as_list)
            dumper.write_y(new_bracket.as_list)
            old_bracket = deepcopy(new_bracket)
            
            if DO_SLEEP_REARRANGEMENT:
                for _ in range(REARRANGEMENT_ENTROPY_INCREASE):
                    old_bracket = deepcopy(new_bracket)
                    new_bracket.from_list(random_swap(old_bracket.as_list))  
            iter_counter = 0

        if iter_counter > MAX_ITER:
            break

    #print('\nFinal bracket:')
    final_bracket = deepcopy(old_bracket)
    dumper.dump_pkl()
    return final_bracket