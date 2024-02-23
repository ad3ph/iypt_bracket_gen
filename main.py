from src.run import get_optimized_bracket
from progress.bar import IncrementalBar as Bar
from io import StringIO
import sys

import argparse as ar
par = ar.ArgumentParser()
par.add_argument('n_teams', type=int)
par.add_argument('n_fights', type=int)
args = par.parse_args()

ATTEMPTS = 100
NBEST = 5
TEAMS = args.n_teams
FIGHTS = args.n_fights

print(f"performing {ATTEMPTS} attempts to optimize brackets for {TEAMS} teams and {FIGHTS} fights")

progress_bar = Bar(max = ATTEMPTS)

good_brackets_list = []

for _ in range(ATTEMPTS):
    good_brackets_list.append(get_optimized_bracket(t=TEAMS, f=FIGHTS))

    fu_list = [x.fu for x in good_brackets_list]
    best_fu_list = sorted([x.fu for x in good_brackets_list])[0:NBEST]

    best_brackets_list = [good_brackets_list[fu_list.index(x)] for x in best_fu_list]

    with open(f'results_{TEAMS}t_{FIGHTS}f.txt', 'w') as results:
        results.write(f'TOURNAMENT BRACKETS for {TEAMS} teams and {FIGHTS} fights\n')
        results.write(f'Performed {ATTEMPTS} genetic optimization attempts\n')
        results.write(f'Fu for every found bracket: {fu_list}\n')
        results.write(f'Best {NBEST} Fu are: {best_fu_list}\n')
        results.write(f'Following are best brackets with their short stats\n\n')

        for bracket_index, bracket in enumerate(best_brackets_list):
            if bracket_index == 0:
                results.write('Recommended bracket:\n')

            bracket_list = bracket.as_list
            for i, fight in enumerate(bracket_list):
                results.write(f'Fight {i+1}:\n')
                for j, room in enumerate(fight):
                    results.write(f'Room {j+1}: {room}\n')

            results.write(f'Fu = {bracket.fu}\n')

            buffer = StringIO()
            sys.stdout = buffer

            bracket.show_fu_results()

            print_output = buffer.getvalue()
            sys.stdout = sys.__stdout__

            results.write(print_output)

            results.write('________________\n\n')
    progress_bar.next()

progress_bar.finish()
with open(f'results_{TEAMS}t_{FIGHTS}f.txt', 'a') as results:
    results.write('\nFINISHED\n')
