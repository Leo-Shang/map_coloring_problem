import time
import operator

global_G = [[1, 2, 3, 4, 6, 7, 10], [2, 1, 3, 4, 5, 6], [3, 1, 2], [4, 1, 2], [5, 2, 6], [6, 1, 2, 5, 7, 8],
            [7, 1, 6, 8, 9, 10], [8, 6, 7, 9], [9, 7, 8, 10], [10, 1, 7, 9]]
n = 10
k = 3
solution = []


def select_by_degree(G_copy):
    max_length = 0
    index = 0
    for item in G_copy:
        if len(item) > max_length:
            max_length = len(item)
            index = G_copy.index(item)
    var = G_copy.pop(index)[0]
    # print(var)
    return var


def select_by_least_constraining_value(G_copy):
    min_length = float("inf")
    index = 0
    for items in G_copy:
        if len(items) < min_length:
            min_length = len(items)
            index = G_copy.index(items)
    var = G_copy.pop(index)[0]
    # print("var is " + str(var))
    # print(solution)
    return var


def select_by_minimum_remaining_value(G_copy):
    min_count = float("inf")
    min_count_index = 0
    for items in G_copy:
        index = 1
        count = 0
        while index < len(items):
            search_value = items[index]
            is_exist = False
            for tuples in solution:
                if tuples[0] == search_value:
                    is_exist = True
            if is_exist == True:
                count += 1  # count represents the number of adjacent values have been colored
            index += 1      # so, the higher the 'count' is, the less the remaining values are
        remaining_colors = k - count
        if remaining_colors < min_count:
            min_count = count
            min_count_index = G_copy.index(items)
    var = G_copy.pop(min_count_index)[0]
    return var


def check_consistent(var, value, solution):
    # print(global_G)
    for tuples in global_G:
        if var == tuples[0]:
            for items in tuples:
                if items != var and (items, value) in solution:
                    return False
    return True


def solve(n, k, G):
    global conflict
    G_copy = G.copy()
    if len(solution) == n:
        return solution
    var = select_by_degree(G_copy)
    # var = select_by_minimum_remaining_value(G_copy)
    # var = G_copy.pop()[0]
    # print(var)
    for value in range(1, k + 1):
        if check_consistent(var, value, solution):
            solution.append((var, value))
            result = solve(n, k, G_copy)
            if result != -1:
                return result
            else:
                conflict += 1
            solution.remove((var, value))
        conflict += 1
    return -1


def find_least_constraining_value(var, solution, color):
    target = []
    for tuples in global_G:
        if tuples[0] == var:
            target = tuples.copy()
    for item in target:
        for tuples in solution:
            if item == tuples[0]:
                target.remove(item)
    constraint_count = 0
    for item in target:  # target has already remove the illegal values
        colors = list(range(1, k + 1))
        neighbour = []
        if len(global_G) != n:
            print("ERROR")
        for temp in global_G:
            if temp[0] == item:
                neighbour = temp[0:]
        for a in neighbour:     # neighbour is the adjacent vertex of 'item'
            for b in solution:
                if a == b[0]:
                    if b[1] in colors:
                        colors.remove(b[1])
        if color in colors:
            constraint_count += 1
    return constraint_count


def solve_least_constraining_value(n, k, G):
    global conflict
    G_copy = G.copy()
    if len(solution) == n:
        return solution
    # var = select_by_degree(G_copy)
    # var = select_by_minimum_remaining_value(G_copy)
    var = G_copy.pop()[0]
    color = list(range(1, k+1))
    result = []
    for items in color:
        result.append((find_least_constraining_value(var, solution, items), items))
    result.sort(key=operator.itemgetter(0))
    # print(result)
    for tuples in result:
        value = tuples[1]
        if check_consistent(var, value, solution):
            solution.append((var, value))
            # print(solution)
            result = solve_least_constraining_value(n, k, G_copy)
            if result != -1:
                return result
            else:
                conflict += 1
            solution.remove((var, value))
        conflict += 1
    return -1


global conflict
conflict = 0
start = time.clock()
solution = solve(n, k, global_G)
# solution = solve_least_constraining_value(n, k, global_G)
time_taken = time.clock() - start
if solution == -1:
    print("FAIL")
    print("time used is " + str(time_taken * pow(10, 3)) + " ms")
    print("There are " + str(conflict) + " conflicts occurred and solved")
else:
    print(solution)
    print("time used is " + str(time_taken * pow(10, 3)) + " ms")
    print("There are " + str(conflict) + " conflicts occurred and solved")