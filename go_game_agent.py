import os
import copy
import random
import math

n = 5

def fetch_previous_game_moves():
    '''
        This function reads the input.txt file and understands the
        previous moves of both the opponent and the player itself.
    '''
    file_pointer = open('input.txt', mode="r")
    file_pointer.seek(0)
    file_data = file_pointer.readlines()
    file_pointer.close()

    player_num = int(file_data[0])
    prev_move = []
    opp_move = []
    for i in range(1, 6):
        prev_move.append([int(state) for state in file_data[i] if state != '\n'])
        opp_move.append([int(state) for state in file_data[i + 5] if state != '\n'])
    return (player_num,opp_move,prev_move)

def output_game_result(response):
    '''
        This function writes the game result into the output file
    '''
    result = ''
    if response != 'PASS':
        output = list(map(lambda res: str(res), response[0:2]))
        result = result + ','.join(output)
    else:
        result = response
    file_pointer = open('output.txt', mode="w")
    file_pointer.write(result)
    file_pointer.close()

def game_logic(curr_go,player_id):
    pawn = 0
    other_pawn = 0
    ideal_pawn = 0
    ideal_other = 0
    for i in range(0,n):
        for j in range(0,n):
            if curr_go[i][j] == 3 - player_num:
                other_pawn = other_pawn + 1
                temp = other_pawn + perform_liberty(curr_go, i, j)
                ideal_other = ideal_other + temp
            elif curr_go[i][j] == player_num:
                pawn = pawn + 1
                temp = pawn + perform_liberty(curr_go, i, j)
                ideal_pawn = ideal_pawn + temp
    if player_id == player_num:
        return ideal_pawn - ideal_other
    return ideal_other - ideal_pawn

def fetch_capturable_pawns(curr_go, player_num):
    captives = []
    for i in range(0,n):
        for j in range(0,n):
            if curr_go[i][j] == player_num:
                if not perform_liberty(curr_go, i, j):
                    if not ((i,j) in captives):
                        captives.append((i, j))
    return captives

def delete_pawns(curr_go, positions):
    for pawn in positions:
        curr_go[pawn[0]][pawn[1]] = 0
    return curr_go

def delete_capturable_pawns(curr_go, player_num):
    captives = fetch_capturable_pawns(curr_go, player_num)
    if len(captives) == 0:
        return curr_go
    result_board = delete_pawns(curr_go, captives)
    return result_board

def fetch_next_neighbors(curr_go,i,j):
    curr_go = delete_capturable_pawns(curr_go,(i,j))
    allies = []
    allies.append((i-1,j))
    allies.append((i+1,j))
    allies.append((i,j-1))
    allies.append((i,j+1))
    res = []
    for ally in allies:
        if 0<=ally[0]<n:
            if 0<=ally[1]<n:
                res.append(ally)
    return res

def fetch_group_pawns(curr_go,i,j):
    group = []
    adjacents = fetch_next_neighbors(curr_go,i,j)
    for loc in adjacents:
        if curr_go[loc[0]][loc[1]] == curr_go[i][j]:
            group.append(loc)
    return group

def fetch_same_crowd(curr_go,i,j):
    sequence = [(i,j)]
    group = []
    while sequence:
        element = sequence.pop(0)
        group.append(element)
        allies = fetch_group_pawns(curr_go, element[0], element[1])
        for ally in allies:
            if not (ally in sequence or ally in group):
                sequence.append(ally)
    return group

def perform_liberty(curr_go,i,j):
    total = 0
    group = fetch_same_crowd(curr_go,i,j)
    for ally in group:
        adjacents = fetch_next_neighbors(curr_go,ally[0],ally[1])
        for move in adjacents:
            if curr_go[move[0]][move[1]] == 0:
                total = total + 1
    return total

def perform_ko(init_go,curr_go):
    flag = True
    for i in range(0,n):
        for j in range(0,n):
            if curr_go[i][j] != init_go[i][j]:
                flag = False
                break
    return flag

def make_a_play(curr_go,init_go, player,i,j):
    if not curr_go[i][j] == 0:
        return False
    dupe_go = copy.deepcopy(curr_go)
    dupe_go[i][j] = player
    captives = fetch_capturable_pawns(dupe_go, 3 - player)
    dupe_go = delete_capturable_pawns(dupe_go, 3 - player)
    lib = perform_liberty(dupe_go,i,j)
    ko = perform_ko(init_go,dupe_go)
    if lib >= 1:
        if not captives or not ko:
            return True

def fetch_favorable_gameplays(curr_go,init_go,player):
    right_play = []
    for i in range(0,n):
        for j in range(0,n):
            stat = make_a_play(curr_go,init_go,player,i,j)
            if stat:
                right_play.append((i,j))
    return right_play

def apply_min_max_algorithm(curr_go,init_go,dep,alpha,beta,player_num):
    game_play = []
    good = 0
    dupe_go = copy.deepcopy(curr_go)
    fav_plays = fetch_favorable_gameplays(curr_go,init_go,player_num)
    for play in fav_plays:
        temp_go = copy.deepcopy(curr_go)
        temp_go[play[0]][play[1]] = player_num
        temp_go = delete_capturable_pawns(temp_go,3-player_num)
        ideal_move = game_logic(temp_go,3-player_num)
        criteria = alpha_beta_pruning(temp_go,dupe_go,dep,alpha,beta,ideal_move,3-player_num)
        points = -1 * criteria
        if points > good or not game_play:
            good = points
            alpha = good
            game_play = [play]
        elif points == good:
            game_play.append(play)
    return game_play

def alpha_beta_pruning(curr_go,init_go,dep,alpha,beta,ideal_move,opponent):
    if dep == 0:
        return ideal_move
    reference = ideal_move
    dupe_go = copy.deepcopy(curr_go)
    fav_games = fetch_favorable_gameplays(curr_go,init_go,opponent)
    for play in fav_games:
        temp_go = copy.deepcopy(curr_go)
        temp_go[play[0]][play[1]] = opponent
        temp_go = delete_capturable_pawns(temp_go,3-opponent)
        ideal_move = game_logic(temp_go,3-opponent)
        criteria = alpha_beta_pruning(temp_go,dupe_go,dep - 1,alpha,beta,ideal_move,3-opponent)
        points = -1 * criteria
        if points > reference:
            reference = points
        npoints = -1 * reference
        if opponent == 3-player_num:
            pawn = npoints
            if pawn < alpha:
                return reference
            if reference > beta:
                beta = reference
        elif opponent == player_num:
            opponent = npoints
            if opponent < beta:
                return reference
            if reference > alpha:
                alpha = reference
    return reference

def game_begin():
    counter=0
    flag = False
    for i in range(0,5):
        for j in range(0,5):
            if current_go[i][j] != 0:
                if i == 2 and j == 2:
                    flag = True
                counter = counter + 1
    if counter==0 and player_num==1:
        move = [(2,2)]
    elif counter==1 and player_num==2 and flag is False:
        move = [(2,2)]
    else:
        move = apply_min_max_algorithm(current_go,initial_go, 2,-math.inf,-math.inf,player_num)
    if move == []:
        response = ['PASS']
    else:
        response = random.choice(move)
    output_game_result(response)

player_num,current_go,initial_go = fetch_previous_game_moves()
game_begin()