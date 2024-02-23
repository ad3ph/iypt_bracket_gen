def get_brackets(rows):
    indices = []

    i = 1
    while i < len(rows)-1:
        if rows[i-1].startswith("________") or rows[i].startswith("Recommended bracket"):
            indices.append([i + 1, ])
        elif rows[i].startswith("Fu = ") and rows[i-1].startswith("Room"):
            indices[-1].append(i-1)
        i += 1
    for pair in indices:
        try:
            start, stop = pair
            yield rows[start: stop + 1]
        except:
            pass

def convert_to_list(bracket):
    return [[list(map(int, x.split(' [')[1].rstrip(']').split(', '))) for x in j.split('\n') if x.startswith('Room')] for j in bracket.split('Fight ')[1:]]

ret = convert_to_list("""Fight 1:\nRoom 1: [8, 18, 5, 14]\nRoom 2: [3, 12, 9]\nRoom 3: [1, 10, 17]\nFight 2:\nRoom 1: [9, 15, 1, 6]\nRoom 2: [19, 4, 5]\nRoom 3: [11, 13, 14]\n""") 
assert ret  == [[[8, 18, 5, 14], [3, 12, 9], [1, 10, 17]], [[9, 15, 1, 6], [19, 4, 5], [11, 13, 14]]], f'{ret}'


def never_play_together(test_team, list_of_teams, bracket):
    for second_team in list_of_teams:
        for fight in bracket:
            for room in fight:
                if second_team in room and test_team in room:
                    return False
    return True 

assert never_play_together(1, [2, 3], [[[8, 18, 5, 14], [3, 12, 9], [1, 10, 17]], [[9, 15, 1, 6], [19, 4, 5], [11, 13, 14]]])

def check_bracket(bracket, num_fights, num_teams):
    teams = [x for x in range(1, num_teams+1)]

    clusters = []
    for team in teams:
        found = False
        for cluster in clusters:
            if never_play_together(team, cluster, bracket):
                cluster.append(team)
                found = True
                break
        if not found:
            clusters.append([team, ])
    return [x for x in clusters if len(x) > 1]
        

def main(filename):
    with open(filename) as f:
        rows = f.readlines()
    
    num_teams, num_fights = rows[0].lstrip('TOURNAMENT BRACKETS for ').split(' fights')[0].split(" teams and ")
    num_fights = int(num_fights)
    num_teams = int(num_teams)

    for idx, bracket in enumerate(get_brackets(rows)):
        bracket_list = convert_to_list("".join(bracket))
        assert len(bracket_list) == num_fights 
        
        clusters = check_bracket(bracket_list, num_fights, num_teams)
        report = [", ".join([str(a) for a in x]) + " (" + str(len(x)) + " teams)"  for x in clusters]
        print(f'Bracket {idx if idx else "recommended"}: found {len(clusters)} clusters: {"; ".join(report)}')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
                        prog='ProgramName',
                        description='What the program does',
                        epilog='Text at the bottom of help')
    parser.add_argument('filename')
    args = parser.parse_args()
    # test_filename = 'results_19t_4f.txt'
    main(args.filename)
    # print(check_bracket([[[8, 18, 5, 14], [3, 12, 9], [1, 10, 17]], [[9, 15, 1, 6], [19, 4, 5], [11, 13, 14]]], 2, 19))
