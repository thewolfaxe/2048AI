"""
Python 2048 Game : Basic Console Based User Interface For Game Play

Written by Matthew Starkey, University of Strathclyde
"""

from py2048_classes import Board, Tile
import time
import math
import random


def main():
    #    allmoves = ['UP','LEFT','DOWN','RIGHT']
    board = Board()
    board.add_random_tiles(2)
    print("main code")

    move_counter = 0
    move = None
    move_result = False

    overalltime = time.time()
    while True:
        gridstate = board.export_state()
        print("Number of successful moves:{}, Last move attempted:{}:, Move status:{}".format(move_counter, move,
                                                                                              move_result))
        print(board)
        if not possible_moves(gridstate):
            if board.get_max_tile()[0] < 2048:
                print("You lost!")
            else:
                print("Congratulations - you won!")
            break
        begin = time.time()
        ######################################
        ######################################
        scores = {}
        moves = {}
        posses = possible_moves(gridstate)

        for possible in posses:
            scores[possible] = 0
            moves[possible] = 0

        while time.time() - begin < 2.95:
            for possible in posses:
                scores[possible] += random_rollout(board, possible)
                moves[possible] += 1

        for possible in posses:
            scores[possible] /= moves[possible]

        best = 0
        move = None
        for key, value in scores.items():
            if value > best:
                best = value
                move = key

        board.make_move(move)
        ######################################
        ######################################
        print("Move time: ", time.time() - begin)
        board.add_random_tiles(1)
        move_counter = move_counter + 1
    average_move = (time.time() - overalltime) / move_counter
    print("Average time per move:", (time.time() - overalltime) / move_counter)
    return board.score, average_move


# optimised possible moves
def possible_moves(gridstate):
    all_moves = ('UP', 'DOWN', 'LEFT', 'RIGHT')
    possible = []
    places = (0, 1, 2, 3)
    for y in places:
        for x in places:
            current = gridstate[y][x]
            if current is not None:

                if all_moves[0] not in possible:
                    up = y-1
                    if up >= 0:
                        test = gridstate[up][x]
                        if test is None or test == current:
                            possible.append(all_moves[0])

                if all_moves[1] not in possible:
                    down = y+1
                    if down <= 3:
                        test = gridstate[down][x]
                        if test is None or test == current:
                            possible.append(all_moves[1])

                if all_moves[2] not in possible:
                    left = x-1
                    if left >= 0:
                        test = gridstate[y][left]
                        if test is None or test == current:
                            possible.append(all_moves[2])

                if all_moves[3] not in possible:
                    right = x+1
                    if right <= 3:
                        test = gridstate[y][right]
                        if test is None or test == current:
                            possible.append(all_moves[3])

        if len(possible) == 4:
            break
    return possible


def random_rollout(board, move):
    gridstate = board.export_state()
    scores = [board.score, board.merge_count]

    board.make_move(move)
    board.add_random_tiles(1)

    grid = gridstate.copy()
    possible = possible_moves(grid)
    while not (board.is_board_full() and possible == []):
        n = random.randint(0, len(possible) - 1)

        board.make_move(possible[n])
        board.add_random_tiles(1)

        grid = board.export_state()
        possible = possible_moves(grid)
    retscore = board.score
    board.__init__(gridstate, scores[0], scores[1])
    return retscore


if __name__ == "__main__":
    score = 0
    runs = 10
    total = 0
    maxi = float('-inf')
    mini = float('inf')
    average_time = 0
    for run in range(runs):
        score, average_moves = main()
        total += score
        average_time += average_moves
        if score < mini:
            mini = score
        if score > maxi:
            maxi = score
        results = open('resultsV3', 'a')
        results.write('run ' + str(run + 1) + ' completed with score: ' + str(score) + '\n')
        results.close()

    average_time /= runs
    average = total/runs
    results = open('resultsV3', 'a')
    results.write("finished " + str(runs) + ' with average score of: ' + str(average) + '       Average time of' + str(average_time) + '\n')
    results.close()
    print('average score: ', total/runs)
    print(mini)
    print(maxi)

