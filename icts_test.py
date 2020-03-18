import map_utils

from ict import IncreasingCostTree, TreeNode
from icts import ICTSSolver

def test_find_most_optimal_paths():
    file_name = "instances/exp2_1.txt"
    my_map, starts, goals = map_utils.import_mapf_instance(file_name)
    icts = ICTSSolver(my_map, starts, goals)
    optimal_paths = icts.find_most_optimal_paths()
    assert optimal_paths == [[(1,1), (1,2), (1,3), (1,4), (1,5)], [(1,2), (1,3), (1,4)]], "Cannot find most optimal paths of a map instance"

def test_find_most_optimal_cost_of_paths():
    file_name = "instances/exp2_1.txt"
    my_map, starts, goals = map_utils.import_mapf_instance(file_name)
    icts = ICTSSolver(my_map, starts, goals)
    cost_of_optimal_paths = icts.find_cost_of_initial_estimate_for_root()
    assert cost_of_optimal_paths == [4, 2], "Cannot find cost of most optimal paths of a map instance"

def test_create_initial_cost_for_ict():
    file_name = "instances/exp2_1.txt"
    my_map, starts, goals = map_utils.import_mapf_instance(file_name)
    icts = ICTSSolver(my_map, starts, goals)
    root = icts.ict.get_next_node_to_expand()
    root_costs = root.get_cost()
    assert root_costs == [4, 2], "Cost of the root node of the ict is incorrect"

def test_bfs_on_ict_with_valid_solution():
    file_name = "instances/exp2_1.txt"
    my_map, starts, goals = map_utils.import_mapf_instance(file_name)
    icts = ICTSSolver(my_map, starts, goals)
    solution = icts.find_solution()
    assert solution == [[(1,1), (1,2), (1,3), (1,4), (1,5)],
                        [(1,2), (1,3), (2,3), (1,3), (1,4)]], "BFS in ICTS could not find solution even though valid solution exists"

def test_number_of_open_spaces():
    file_name = "instances/no_solution.txt"
    my_map, starts, goals = map_utils.import_mapf_instance(file_name)
    number_of_open_spaces = map_utils.find_number_of_open_spaces(my_map)
    assert number_of_open_spaces == 5, "ICTS cannot find the correct number of open spaces in a map"

def test_calculate_upperbound_cost_of_all_agents():
    file_name = "instances/no_solution.txt"
    my_map, starts, goals = map_utils.import_mapf_instance(file_name)
    icts = ICTSSolver(my_map, starts, goals)
    upper_bound = icts.calculate_upper_bound_cost()
    assert upper_bound == 15, "ICTS cannot find the correct upper bound for a map"

def test_node_has_exceeded_upper_bound():
    node = TreeNode([10, 11])
    upper_bound = 20

    file_name = "instances/no_solution.txt"
    my_map, starts, goals = map_utils.import_mapf_instance(file_name)
    icts = ICTSSolver(my_map, starts, goals)
    node_exceeds_bound = icts.node_has_exceeded_upper_bound(node, upper_bound)

    assert node_exceeds_bound is True, "ICTS believes nodes has not exceeded the upper bound even though the node exceeds the upper bound"

def test_node_has_not_exceeded_upper_bound():
    node = TreeNode([10, 9])
    upper_bound = 20

    file_name = "instances/no_solution.txt"
    my_map, starts, goals = map_utils.import_mapf_instance(file_name)
    icts = ICTSSolver(my_map, starts, goals)
    node_exceeds_bound = icts.node_has_exceeded_upper_bound(node, upper_bound)

    assert node_exceeds_bound is False, "ICTS believes nodes has exceeded the upper bound even though the node has not exceeded the upper bound"

def test_bfs_terminates_if_no_solution_exists():
    file_name = "instances/no_solution.txt"
    my_map, starts, goals = map_utils.import_mapf_instance(file_name)
    icts = ICTSSolver(my_map, starts, goals)
    solution_paths = icts.find_solution()

    assert solution_paths == [], "ICTS returns a solution when no solution exists"

if __name__ == "__main__":
    test_find_most_optimal_paths()
    test_find_most_optimal_cost_of_paths()
    test_create_initial_cost_for_ict()
    test_bfs_on_ict_with_valid_solution()
    test_number_of_open_spaces()
    test_calculate_upperbound_cost_of_all_agents()
    test_node_has_exceeded_upper_bound()
    test_node_has_not_exceeded_upper_bound()
    test_bfs_terminates_if_no_solution_exists()
    print("ALL TEST PASSED")