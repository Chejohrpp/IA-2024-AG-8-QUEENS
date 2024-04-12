import random
from entities.Bloke import Blocke
from entities.Piece import Piece

#Por ruleta

# Constants
POPULATION_NUMBER = 10
MINIMUM_ROW = 1
MAXIMUM_ROW = 8
LENGTH_BLOKE = 8
TOTAL_SONS = 5
MUTATION_PROBABILITY = 15

def create_population():
    return generate_random_population()

def generate_random_population():
    return [generate_random_bloke() for _ in range(POPULATION_NUMBER)]

def generate_random_bloke():
    return [random.randint(MINIMUM_ROW, MAXIMUM_ROW) for _ in range(LENGTH_BLOKE)]

def evaluate_aptitude(population):
    # Initialize blokes list
    blokes = []
    for bloke in population:
        blokes.append((generate_number_aptitude(bloke)))
    return blokes

def generate_total_blokes(blokes):
    total = 0
    for bloke in blokes:
        print(bloke)
        total += bloke.aptitude_value
    print('sum_total ', total)
    return total

def search_better_aptitude_value(blokes):
    better = 0
    for bloke in blokes:
        if ( better < bloke.aptitude_value):
            better = bloke.aptitude_value
    print('Better apitude ', better)
    return better

def generate_number_aptitude(bloke):
    # Chessboard 8 x 8
    # chessboard_8x8 = [[0] * 8 for _ in range(8)]  # Initialize an empty chessboard
    aptitude_value = 0
    for i in range(len(bloke)):
        # fill_chessboard(chessboard_8x8, i+1, bloke[i])
        for j in range(i + 1, len(bloke)):
            aptitude_value += verify_chessboard(Piece(i+1, bloke[i]), j+1, bloke[j])

    # for row in chessboard_8x8:
    #     print(row)
    return Blocke(bloke,aptitude_value)

def fill_chessboard(chessboard, column, row):
    chessboard[row - 1][column - 1] = 1  # Update the position of the queen

def verify_chessboard(queen, column, row):
    # not the same column
    if (queen.column == column): return 0
    # not the same row
    if (queen.row == row): return 0
    # Diagonal (top-left to bottom-right) straight line equations = 1 
    if abs(queen.column - column) == abs(queen.row - row):
        # print (queen.column,queen.row,column,row)
        return 0
    return 1

def generation_S_fun_select(total):
    return random.randint(0, total)

def fun_select(sum_total_pick,blokes):
    # print ('picking number of total', sum_total_pick)
    total = 0
    for bloke in blokes:
        total += bloke.aptitude_value
        if total >= sum_total_pick:
            # print ('total', total)
            # print(bloke)
            return bloke

def newSons(total,blokes,blokes_new_gen):
    # Pick the bloke population
    blokesi = []
    for i in range (2):
        sum_total_pick = generation_S_fun_select(total)
        blokesi.append(fun_select(sum_total_pick,blokes))

    blokes_sons = []
    # crossover
    blokes_sons = one_point_crossover(blokesi[0], blokesi[1])

    #Mutations
    for bloke in blokes_sons:
        probability = generation_S_fun_select(100)
        if probability <= MUTATION_PROBABILITY:
            mutation(bloke)

    #sustitutions, elitis or generational, return 1 or 2
    for bloke in blokes_sons:
        blokes_new_gen.append(bloke)

def one_point_crossover(bloke1,bloke2):
    point = generation_S_fun_select(MAXIMUM_ROW-1)
    # print('point is', point+1)
    bloke_son1 = []
    bloke_son2 = []
    for i in range(8):
        if (point > i):
            bloke_son1.append(bloke1.bloke[i])
            bloke_son2.append(bloke2.bloke[i])
        else:
            bloke_son1.append(bloke2.bloke[i])
            bloke_son2.append(bloke1.bloke[i])

    # print('son1', generate_number_aptitude(bloke_son1))
    # print('son2', generate_number_aptitude(bloke_son2))

    son1 = generate_number_aptitude(bloke_son1)
    son2 = generate_number_aptitude(bloke_son2)

    if (son1.aptitude_value >= son2.aptitude_value):
        return [bloke_son1]
    else:
        return [bloke_son2]
    
    return [bloke_son1,bloke_son2]

def mutation(bloke):
    # print ("ready for mutations")
    #Random Resting 
    point = generation_S_fun_select(MAXIMUM_ROW-1)
    gen_mutate = random.randint(1, 8)
    bloke[point] = gen_mutate
    
def sustitution(bloke):
    None

if __name__ == '__main__':
    # Create a dictionary to store generations and their corresponding aptitudes
    gen_aptitude = {}
    population = create_population()
    for i in range(40):
        #New population ->
        print("Gen", i)
        blokes = evaluate_aptitude(population)
        total = generate_total_blokes(blokes)
        better_gen = search_better_aptitude_value(blokes)
        gen_aptitude[i] = [better_gen]
        # if better_gen > 26 : break
        blokes_new_gen = []
        for i in range(TOTAL_SONS*2):
            (newSons(total, blokes,blokes_new_gen))
        population = blokes_new_gen

    print(gen_aptitude) # print like this -> { No.Generation : [better_value_that_generation] , ...}


    