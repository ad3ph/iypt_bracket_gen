from random import randint
from copy import deepcopy


def decode_bracket(bracket_list):
    decoded_list = []
    separations_list = []
    for i in bracket_list:
        mdl_dec_lst = []
        mdl_sep_lst = []
        for j in i:
            mdl_sep_lst.append(len(j))
            for g in j:
                mdl_dec_lst.append(g)
        decoded_list.append(mdl_dec_lst)
        separations_list.append(mdl_sep_lst)
    return decoded_list, separations_list
    # [[[1, 2, 3], [1, 2, 3, 4]], []]

def make_swap(decoded_list, fight_idx=None, swap_idxs=None):
    dec_lst = deepcopy(decoded_list)
    if fight_idx is None:
        fight_idx = randint(0, len(dec_lst) - 1)
    if swap_idxs is None:
        swap_idxs = [randint(0, len(dec_lst[fight_idx]) // 2),
                     randint(len(dec_lst[fight_idx]) // 2 + 1, len(dec_lst[fight_idx]) - 1)]
    dec_lst[fight_idx][swap_idxs[0]], dec_lst[fight_idx][swap_idxs[1]] = \
        dec_lst[fight_idx][swap_idxs[1]], dec_lst[fight_idx][swap_idxs[0]]
    return dec_lst


def encode_list(decoded_list, separtions):
    encoded_list = []
    for i in range(len(decoded_list)):
        fight = []
        stop_idx = 0
        for j in separtions[i]:
            fight.append([decoded_list[i][g] for g in range(stop_idx, stop_idx+j)])
            stop_idx += j
        encoded_list.append(fight)
    return encoded_list


if __name__ == '__main__':
    init_array = [[[1, 2, 3], [11, 12, 13, 14]], [[15, 4, 5, 6], [7, 8, 9, 10]]]
    dec_array, seps = decode_bracket(init_array)

    print(dec_array, seps)
    print(make_swap(dec_array))
    print(encode_list(make_swap(dec_array), seps))

def random_swap(bracket_list):
    dec_array, seps = decode_bracket(bracket_list)
    swapped_bracket_list = encode_list(make_swap(dec_array), seps)
    return swapped_bracket_list