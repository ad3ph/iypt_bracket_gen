import numpy as np
import random

class RandomBracketGenerator:
    def __init__(self, teams, fights):
        self.number_of_teams = teams
        self.number_of_fights = fights
        self.bracket = []
        self.number_of_rooms = teams // 3

    def generate(self):
        for _ in range(self.number_of_fights):
            fight_list = []

            all_teams_list = [x for x in range(1, self.number_of_teams + 1)]
            random.shuffle(all_teams_list)

            number_of_four_teams_fights = self.number_of_teams % 3
            room = []

            for team in all_teams_list:
                this_room_len = 4 if len(fight_list) < number_of_four_teams_fights else 3
                if len(room) == this_room_len:
                    fight_list.append(room)
                    room = []
                room.append(team)
            fight_list.append(room)

            self.bracket.append(fight_list)

    def show(self):
        print(f'Random bracket for {self.number_of_teams} teams and {self.number_of_fights} fights')
        print('Room    |     ', *['     '+chr(i+65)+'      ' for i in range(self.number_of_rooms)],)
        for fight in self.bracket:
            print(f'Fight {self.bracket.index(fight)+1} | ', *fight, sep = '  ')

def generate_bracket_list(teams, fights):
    bracket_generator = RandomBracketGenerator(teams=teams, fights=fights)
    bracket_generator.generate()
    return bracket_generator.bracket