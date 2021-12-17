from difflib import SequenceMatcher
import random
import string

# starting parameters
STARTING_POPULATION = 25000
SELECTION_POOL_SIZE = 50
VARIATIONS_PER_GENERATION = 10
MUTATION_RATE = 0.1
GUESS_WORD = 'unicorn'
ALPHABET = list(string.ascii_lowercase)
ALPHABET.append('')
POPULATION_FILENAME = './english-words/words.txt'

# read entire population
with open(POPULATION_FILENAME, 'r') as pop_file:
    total_population = [line.rstrip() for line in pop_file.readlines()]

# mutate the DNA based on a given probability
def mutate(word):
    index = 0
    word_list = list(word)
    for char in word_list:
        if random.random() < MUTATION_RATE:
            word_list[index] = random.choice(ALPHABET)
        index += 1
    return "".join(word_list)

# evaluate the current pool elements
# and populate a list according to the fitness score
# elements with higher fitness score will appear
# in the valid_pool more often, making them
# more likely to be picked
def evaluate_pool(mating_pool):
    average_fitness = 0
    new_mating_pool = {}
    for k in mating_pool:
        fitness = calculate_fitness(k)
        new_mating_pool[k] = fitness
        average_fitness += fitness
    potential_mating_pool = dict(sorted(new_mating_pool.items(), key=lambda x:x[1], reverse=True))
    new_mating_pool = list(potential_mating_pool.items())[:SELECTION_POOL_SIZE]

    valid_pool = []
    for word in new_mating_pool:
        for i in range(int(word[1]*10)):
            valid_pool.append(word[0])
    print(f'Average fitness {(average_fitness*10/SELECTION_POOL_SIZE)}')
    return valid_pool

# REPRODUCTION function
def reproduction(mating_pool):
    new_pop = []
    no_items = len(mating_pool)-1

    for i in range(VARIATIONS_PER_GENERATION):
        # 1. Pick two parents with probability according to relative fitness
        i1, i2 = random.randint(0,no_items), random.randint(0,no_items)
        o1, o2 = mating_pool[i1], mating_pool[i2]
        # 2. Crossover - create a "child" by combining the DNA based on a given probability
        if i <= VARIATIONS_PER_GENERATION:
            item = o1[:len(mating_pool[i1])//2] + o2[len(mating_pool[i2])//2:]
        elif i > VARIATIONS_PER_GENERATION:
            item = o2[:len(mating_pool[i1])//2] + o1[len(mating_pool[i2])//2:]
        # 3. Mutation - mutate the child's DNA based on a given probability
        item = mutate(item)
        # 4. Add the new child to a new population
        new_pop.append(item)

    return new_pop

# calculate fitness for a word
def calculate_fitness(word):
    return SequenceMatcher(None, word, GUESS_WORD).ratio()



def main():

    total_generations = 0
    average_fitness = 0

    # INITIALIZE:
    # create a population of N elements,
    # each with randomly generated DNA
    init_population = random.sample(total_population, STARTING_POPULATION)

    # SELECTION:
    # evaluate the fitness of each element of the population
    # and build a mating pool
    mating_pool = evaluate_pool(init_population)
    #print(f'Initial pool: {mating_pool}')

    # REPRODUCTION:
    # repeat N times:
    while True:
        if GUESS_WORD in mating_pool:
            print('GUESSES !')
            break
        print(f'Generation {total_generations}')
        new_mating_pool = reproduction(mating_pool)
        print(f'Added to pool: {", ".join(new_mating_pool)}')
        for item in new_mating_pool:
            mating_pool.append(item)
        mating_pool = evaluate_pool(mating_pool)
        total_generations += 1

main()
