#!/usr/bin/env python3

import icts
import map_utils
from map_utils import MapDetails

if __name__ == "__main__":
    result_file_name = "results/demo.txt"
    map_file_name = "tbd"
    my_map = [
        # somehow we need a border of obstacles
        [True, True, True, True, True, True, True, True, True],
        [True, False, False, False, False, False, False, False, True],
        [True, False, False, False, False, False, False, False, True],
        [True, False, False, False, False, False, False, False, True],
        [True, True, True, True, False, True, True, True, True],
        [True, False, False, False, False, False, False, False, True],
        [True, False, False, False, False, False, False, False, True],
        [True, False, False, False, False, False, False, False, True],
        [True, True, True, True, True, True, True, True, True]
    ]
    starts = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6)]  # , (1, 7)]
    goals = [(7, 7), (7, 6), (7, 5), (7, 4), (7, 3), (7, 2)]  # , (7, 1)]

    # result_file_name = "results/icts_test.txt"
    # map_file_name = "instances/exp2_1.txt"
    # my_map, starts, goals = map_utils.import_mapf_instance(map_file_name)

    map_utils.print_mapf_instance(my_map, starts, goals)

    md = MapDetails(result_file_name,
                    map_file_name, my_map, starts, goals)
    s = icts.ICTSSolver(md)
    r = s.find_solution()

    print(r)
