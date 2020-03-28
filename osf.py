# Operator Selection Function for MAPF
# Used in EPEA*
from collections import deque
from collections import defaultdict
import itertools
import time
import math

class OSF:
    def __init__(self, my_map, goals):
        """OSF is a singleton that calculates the next operator for any given step."""
        self.map = my_map

        # usage: h[agent][x][y]
        self.h = self.get_heuristics(self.map, goals)
        self.visited = set()
        self.indiv_ops = [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]
        num_agents = len(goals)
        self.agent_osf = self.populate_agent_osfs(my_map, num_agents, self.indiv_ops, self.h)
        self.osf_tables = dict()

    def get_heuristics(self, my_map, goals):
        num_agents = len(goals)
        all_h = []
        for i in range(num_agents):
            this_goal = goals[i]
            new_h = []
            for x, row in enumerate(my_map):
                this_row_h = []
                for y, cell in enumerate(row):
                    if cell:
                        this_row_h.append(math.inf)
                    else:
                        this_row_h.append(self.manhattan_distance((x,y), this_goal))
                new_h.append(this_row_h)
            all_h.append(new_h)
        return all_h

    def populate_agent_osfs(self, my_map, num_agents, indiv_ops, h_table):
        agent_osf = []
        for agent in range(num_agents):
            new_agent_osf = self.get_agent_osf(my_map, h_table[agent], indiv_ops)
            agent_osf.append(new_agent_osf)
        return agent_osf

    def get_agent_osf(self, my_map, h_table, indiv_ops):
        agent_osf = {}
        for x, row in enumerate(my_map):
            for y, cell in enumerate(row):
                good_ops = []
                if cell:
                    agent_osf[(x,y)] = []
                else:
                    for op in indiv_ops:
                        new_x = x + op[0]
                        new_y = y + op[1]
                        if not my_map[new_x][new_y]:
                            good_ops.append((op, h_table[x][y] - h_table[new_x][new_y]))
                agent_osf[(x,y)] = good_ops
        return agent_osf

    def manhattan_distance(self, loc1, loc2):
        return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])

    def get_children_and_next_F(self, node, get_min = False):
        operators, next_big_F = self.select_operators(node, get_min)
        if not operators:
            return [], next_big_F
        new_child_nodes = self.get_new_children(node['agent_locs'], operators)
        return new_child_nodes, next_big_F
        
    def select_operators(self, node, get_min = False):
        agent_locs, big_F, h, g = node['agent_locs'], node['big_F'], node['h'], node['g']
        small_f = h + g
        requested_row = big_F - small_f
        if agent_locs in self.osf_tables:
            op_table = self.osf_tables[agent_locs]
        else:
            ops_to_cross_prod = self.get_on_map_ops(agent_locs, self.indiv_ops)
            all_possible_ops = list(itertools.product(*ops_to_cross_prod))
            op_table, min_delta_small_f = self.get_op_table_and_min_row(all_possible_ops, agent_locs, small_f, h, g)
            self.osf_tables[agent_locs] = op_table
            if not op_table:
                return None, math.inf
            if get_min:
                requested_row = min_delta_small_f
        delta_big_F_next = self.get_delta_big_F_next(list(op_table.keys()), requested_row)
        next_big_F = small_f + delta_big_F_next
        if requested_row not in op_table:
            return None, next_big_F
        return op_table[requested_row]['operators'], next_big_F

    def get_on_map_ops(self, agent_locs, ops):
        all_ops = []
        for loc in agent_locs:
            this_agent_ops = []
            for op in ops:
                new_x = loc[0] + op[0]
                new_y = loc[1] + op[1]
                if not self.map[new_x][new_y]:
                    this_agent_ops.append(op)
            all_ops.append(this_agent_ops)
        return all_ops

    def get_op_table_and_min_row(self, all_possible_ops, agent_locs, small_f, h, g):
        op_table = dict()
        num_agents = len(agent_locs)
        min_delta_small_f = math.inf
        for op in all_possible_ops:
            new_op_table_row = dict()
            new_locs = self.get_new_locations(op, agent_locs)
            if self.move_invalid(agent_locs, new_locs):
                continue
            this_h = self.list_of_locations_to_heuristic(new_locs)
            this_g = g + num_agents # We make a decision for everyone simultaneously
            this_small_f = this_h + this_g
            delta_small_f = this_small_f - small_f
            min_delta_small_f = min(min_delta_small_f, delta_small_f)
            if delta_small_f not in op_table:
                new_op_table_row['delta_h'] = this_h - h
                new_op_table_row['operators'] = [op]
                op_table[delta_small_f] = new_op_table_row
            else:
                op_table[delta_small_f]['operators'].append(op)
        return op_table, min_delta_small_f

    def list_of_locations_to_heuristic(self, locs):
        h = 0
        for i,loc in enumerate(locs):
            h += self.h[i][loc[0]][loc[1]]
        return h

    def get_new_children(self, locs, group_ops):
        children = []
        for op in group_ops:
            new_child = tuple(self.get_new_locations(op, locs))
            children.append(new_child)
        return children

    def get_new_locations(self, ops, locs):
        new_locs = []
        for i, op in enumerate(ops):
            new_x = locs[i][0] + op[0]
            new_y = locs[i][1] + op[1]
            new_locs.append((new_x, new_y))
        return new_locs

    def get_delta_big_F_next(self, all_keys, requested_row):
        all_keys.sort()
        if requested_row not in all_keys:
            return min(all_keys)
        req_index = all_keys.index(requested_row)
        delta_big_F_next = all_keys[req_index + 1] if req_index + 1 < len(all_keys) else math.inf
        return delta_big_F_next

    def move_invalid(self, this_locs, next_locs):
        vertex_collision = len(set(next_locs)) != len(next_locs)
        edge_collision = self.has_edge_collisions(this_locs, next_locs)
        return vertex_collision or edge_collision

    def has_edge_collisions(self, this_locs, next_locs):
        forward = [pair for pair in zip(this_locs, next_locs) if pair[0] != pair[1]]
        backward = [pair for pair in zip(next_locs, this_locs) if pair[0] != pair[1]]
        edge_collisions = set(forward).intersection(set(backward))
        return len(edge_collisions) > 0

    def print_heuristics(self):
        for i, agent_table in enumerate(self.h):
            print("Agent", i, "heuristics:")
            for row in agent_table:
                for cell in row:
                    if cell != math.inf:
                        print(cell, end=" ")
                    else:
                        print(". ", end="")
                print("\n")