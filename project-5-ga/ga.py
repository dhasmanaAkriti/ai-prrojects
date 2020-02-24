import random, copy, utilities, math
class Genome:
    """
    An interface class for a genome.
    """
    def __str__(self):
        """
        Returns a string representing the genome.
        """
        abstract()

    def fitness(self):
        """
        Returns the fitness of the genome.
        """
        abstract()
    def mutate(self, rate):
        """
        Returns the child after mutating.
        """
        abstract()
    def crossover(self, other):
        """
        Returns the child after doing a crossover with the other genome.
        """
        abstract()

class BitGenome(Genome):
    def __init__(self, length, r):
        self.length = length
        self.string = ""
        self.rand = r

    def __str__(self):
        return self.string

    def fitness(self):
        return float(self.string.count("1"))
    def mutate(self, rate = 0.5):
        child_genome = BitGenome(self.length, self.rand)
        child = copy.copy(self.get_genome())
        child_list = list(child)
        num, den = utilities.convert_rate_to_fraction(rate)
        for i in range(len(child_list)):
            loc = self.rand.randint(1, den+1)
            if loc <= num:
                child_list[i] = utilities.flip(child_list[i])
        child_genome.initialize("".join(child_list))
        return child_genome

    def crossover(self, other):
        child_genome1 = BitGenome(self.length, self.rand)
        child_genome2 = BitGenome(self.length, self.rand)
        crossover_point = self.rand.randint(1, self.length)
        child1 = self.get_genome()[0:crossover_point] + \
                other.get_genome()[crossover_point:self.length]
        child2 = other.get_genome()[0:crossover_point] + \
                 self.get_genome()[crossover_point:self.length]
        child_genome1.initialize(child1)
        child_genome2.initialize(child2)
        return (child_genome1, child_genome2)

    def get_genome(self):
        return self.string

    def initialize(self, my_string):
        self.string = my_string

    def initialize_r(self):
        my_string = ""
        for i in range(self.length):
            my_string = my_string + self.rand.choice(["0", "1"])
        self.string = my_string

class BitGenome_GA_RR():
    def __init__(self, length, r):
        self.length = length
        self.string = ""
        self.rand = r
    def fitness(self):
        initial_sum = 1
        runs = int(math.log(self.length, 2))
        for i in range(3, runs+1):
            initial_sum = self.fitness_helper(initial_sum, i)
        return float(initial_sum)

    def fitness_helper(self, initial_sum, num):
        byte = 2**num
        num_bit_strings = self.length // byte
        first = 0
        for i in range(num_bit_strings):
            last = first + byte
            string = "1" * byte
            if self.string[first:last] == string:
                initial_sum += byte
            first = last
        return initial_sum

    def mutate(self, rate = 0.5):
        child_genome = BitGenome_GA_RR(self.length, self.rand)
        child = copy.copy(self.get_genome())
        child_list = list(child)
        num, den = utilities.convert_rate_to_fraction(rate)
        for i in range(len(child_list)):
            loc = self.rand.randint(1, den+1)
            if loc <= num:
                child_list[i] = utilities.flip(child_list[i])
        child_genome.initialize("".join(child_list))
        return child_genome

    def crossover(self, other):
        child_genome1 = BitGenome_GA_RR(self.length, self.rand)
        child_genome2 = BitGenome_GA_RR(self.length, self.rand)
        crossover_point = self.rand.randint(1, self.length)
        child1 = self.get_genome()[0:crossover_point] + \
                other.get_genome()[crossover_point:self.length]
        child2 = other.get_genome()[0:crossover_point] + \
                 self.get_genome()[crossover_point:self.length]
        child_genome1.initialize(child1)
        child_genome2.initialize(child2)
        return (child_genome1, child_genome2)

    def get_genome(self):
        return self.string

    def __str__(self):
        return self.string

    def initialize(self, my_string):
        self.string = my_string

    def initialize_r(self):
        my_string = ""
        for i in range(self.length):
            my_string = my_string + self.rand.choice(["0", "1"])
        self.string = my_string


class Population():
    def generate_first_pop(self):
        abstract()
    def __str__(self):
        abstract()
    def cull(self, size):
        abstract()
    def find_best(self):
        abstract()
    def generate_next_gen(self, crossover_rate, mutation_rate):
        abstract()

class Pop_Bit_Genome_GA(Population):
    def __init__(self, population_size, bit_length, r,  population = [], gen = 0):
        self.pop_size = population_size
        self.bitlen = bit_length
        self.pop = population
        self.gen = gen
        self.rand = r

    def __str__(self):
        to_return = "POPULATION: \n"
        for i in self.pop:
            to_return += str(i) + "\n"
        to_return += "\nSIZE : "
        to_return += str(self.pop_size)
        to_return += "\n_______________________________________________________________________________________________\n"
        return to_return

    def generate_first_pop(self):
        popul = []
        for i in range(self.pop_size):
            gen = BitGenome(self.bitlen, self.rand)
            gen.initialize_r()
            popul.append(gen)
        self.pop = popul

    def generate_next_gen(self, crossover_rate, mutation_rate):
        x = self.cull(self.pop_size//2)
        next_gen = []
        num, dem = utilities.convert_rate_to_fraction(crossover_rate)
        while len(next_gen) != self.pop_size:
            loc = self.rand.randint(1, dem)
            if loc <= num:
                p1 = self.rand.choice(x)
                p2 = self.rand.choice(x)
                child = p1.crossover(p2)
                next_gen.append(child[1].mutate(mutation_rate))
                next_gen.append(child[0].mutate(mutation_rate))
            else:
                p1 = self.rand.choice(x)
                p2 = self.rand.choice(x)
                next_gen.append(p1.mutate(mutation_rate))
                next_gen.append(p2.mutate(mutation_rate))
        population = Pop_Bit_Genome_GA(self.pop_size, self.bitlen, self.rand, next_gen, self.gen + 1)
        return population

    def cull(self, size):
        sum_fit = 0
        for i in self.pop:
            sum_fit += i.fitness()
        new_l = []
        for i in self.pop:
            f = i.fitness()
            new_l.append([i, f/sum_fit])
        new_l.sort(key = lambda x: x[1])

        for i in range(len(new_l)):
            accum_sum = new_l[i][1]
            for j in range(i):
                accum_sum += new_l[j][1]
            new_l[i].append(accum_sum)
        culled_list = []
        for i in range(size):
            R = self.rand.random()
            not_found = True
            j = 0
            while not_found:
                if new_l[j][2] >= R:
                    not_found = False
                    culled_list.append(new_l[j][0])
                j += 1
        return culled_list

    def find_best(self):
        best = self.pop[0]
        for i in range(len(self.pop)):
            if self.pop[i].fitness() > best.fitness():
                best = self.pop[i]
        return best

class Pop_Bit_Genome_GA_RR(Population):
    def __init__(self, population_size, bit_length, r,  population = [], gen = 0):
        self.pop_size = population_size
        self.bitlen = bit_length
        self.pop = population
        self.gen = gen
        self.rand = r

    def __str__(self):
        to_return = "POPULATION: \n"
        for i in self.pop:
            to_return += str(i) + "\n"
        to_return += "\nSIZE : "
        to_return += str(self.pop_size)
        to_return += "\n_______________________________________________________________________________________________\n"
        return to_return

    def generate_first_pop(self):
        popul = []
        for i in range(self.pop_size):
            gen = BitGenome_GA_RR(self.bitlen, self.rand)
            gen.initialize_r()
            popul.append(gen)
        self.pop = popul

    def generate_next_gen(self, crossover_rate, mutation_rate):
        x = self.cull(self.pop_size//2)
        next_gen = []
        num, dem = utilities.convert_rate_to_fraction(crossover_rate)
        while len(next_gen) != self.pop_size:
            loc = self.rand.randint(1, dem)
            if loc <= num:
                p1 = self.rand.choice(x)
                p2 = self.rand.choice(x)
                child = p1.crossover(p2)
                next_gen.append(child[1].mutate(mutation_rate))
                next_gen.append(child[0].mutate(mutation_rate))
            else:
                p1 = self.rand.choice(x)
                p2 = self.rand.choice(x)
                next_gen.append(p1.mutate(mutation_rate))
                next_gen.append(p2.mutate(mutation_rate))
        population = Pop_Bit_Genome_GA_RR(self.pop_size, self.bitlen, self.rand, next_gen, self.gen + 1)
        return population

    def cull(self, size):
        sum_fit = 0
        for i in self.pop:
            sum_fit += i.fitness()
        new_l = []
        for i in self.pop:
            f = i.fitness()
            new_l.append([i, f/sum_fit])
        new_l.sort(key = lambda x: x[1])

        for i in range(len(new_l)):
            accum_sum = new_l[i][1]
            for j in range(i):
                accum_sum += new_l[j][1]
            new_l[i].append(accum_sum)
        culled_list = []
        for i in range(size):
            R = self.rand.random()
            not_found = True
            j = 0
            while not_found:
                if new_l[j][2] >= R:
                    not_found = False
                    culled_list.append(new_l[j][0])
                j += 1
        return culled_list

    def find_best(self):
        best = self.pop[0]
        for i in range(len(self.pop)):
            if self.pop[i].fitness() > best.fitness():
                best = self.pop[i]
        return best

class Pop_Bit_Genome_HC(Population):
    def __init__(self, population_size, bit_length, r, population=[], gen=0):
        self.pop_size = population_size
        self.bitlen = bit_length
        self.pop = population
        self.gen = gen
        self.rand = r

    def __str__(self):
        to_return = "POPULATION: \n"
        for i in self.pop:
            to_return += str(i) + "\n"
        to_return += "\nSIZE : "
        to_return += str(self.pop_size)
        to_return += "\nGEN : "
        to_return += str(self.gen)
        to_return += "\n_______________________________________________________________________________________________\n"
        return to_return

    def generate_next_gen(self, mutation_rate):
        x = self.cull(self.pop_size//2)
        next_gen = []
        for i in x:
            next_gen.append(i.mutate(mutation_rate))
        population = Pop_Bit_Genome_HC(self.pop_size, self.bitlen, self.rand, next_gen, self.gen + 1)
        return population

    def generate_first_pop(self):
        popul = []
        for i in range(self.pop_size):
            gen = BitGenome(self.bitlen, self.rand)
            gen.initialize_r()
            popul.append(gen)
        self.pop = popul

    def cull(self, size):
        sum_fit = 0
        for i in self.pop:
            sum_fit += i.fitness()
        new_l = []
        for i in self.pop:
            f = i.fitness()
            new_l.append([i, f/sum_fit])
        new_l.sort(key = lambda x: x[1])

        for i in range(len(new_l)):
            accum_sum = new_l[i][1]
            for j in range(i):
                accum_sum += new_l[j][1]
            new_l[i].append(accum_sum)
        culled_list = []
        for i in range(size):
            R = self.rand.random()
            not_found = True
            j = 0
            while not_found:
                if new_l[j][2] >= R:
                    not_found = False
                    culled_list.append(new_l[j][0])
                j += 1
        return culled_list

    def find_best(self):
        best = self.pop[0]
        for i in range(len(self.pop)):
            if self.pop[i].fitness() > best.fitness():
                best = self.pop[i]
        return best

def hill_climber(pop_size, bit_len, mutation_rate, seed, run):
    r = random.Random(seed)
    start_pop = Pop_Bit_Genome_HC(pop_size, bit_len, r)
    file = open("HillClimber" + str(run), "w+")
    file.write("RandomSeed," + str(seed) + "," + "Population size:" + str(pop_size) + "," +"Bit Length:" + str(bit_len) + "," + "Crossover Rate:"+ "0" + ","
                     +"Mutation Rate:" + str(mutation_rate) + "\n")
    file.write("gen,BestFitness,FitnessEval" + "\n")
    start_pop.generate_first_pop()
    best = start_pop.find_best()
    opt_string = "1"* bit_len
    while str(best) != opt_string and  start_pop.gen < 2000:
        next = start_pop.generate_next_gen(mutation_rate)
        start_pop = next
        best = start_pop.find_best()
        file.write(str(start_pop.gen) + "," + str(int(best.fitness())) + "," + str(int(best.fitness()) * pop_size) + "\n")
    file.close()

def GA_RR(pop_size, bit_len, crossover_rate, mutation_rate, seed, run):
    r = random.Random(seed)
    start_pop = Pop_Bit_Genome_GA_RR(pop_size, bit_len, r)
    start_pop.generate_first_pop()
    file = open("GARRIntermediate" + str(run), "w+")
    file.write("RandomSeed," + str(seed) + "," + "Population size:" + str(pop_size) + "," + "Bit Length:" + str(
        bit_len) + "," + "Crossover Rate:" + str(crossover_rate) + ","
               + "Mutation Rate:" + str(mutation_rate) + "\n")
    file.write("gen,BestFitness,FitnessEval" + "\n")
    best = start_pop.find_best()
    opt_string = "1" * bit_len
    while str(best) != opt_string and start_pop.gen < 2000:
        next = start_pop.generate_next_gen(crossover_rate, mutation_rate)
        start_pop = next
        best = start_pop.find_best()
        file.write(str(start_pop.gen) + "," + str(best.fitness()) + "," + str(
            int(best.fitness() * pop_size)) + "\n")
    file.close()


def GA(pop_size, bit_len, crossover_rate, mutation_rate, seed, run):
    r = random.Random(seed)
    start_pop = Pop_Bit_Genome_GA(pop_size, bit_len, r)
    start_pop.generate_first_pop()
    best = start_pop.find_best()
    file = open("GARR" + str(run), "w+")
    file.write("RandomSeed," + str(seed) + "," + "Population size:" + str(pop_size) + "," + "Bit Length:" + str(
        bit_len) + "," + "Crossover Rate:" + str(crossover_rate) + ","
               + "Mutation Rate:" + str(mutation_rate) + "\n")
    file.write("gen,BestFitness,FitnessEval" + "\n")
    opt_string = "1" * bit_len
    while start_pop.gen < 2000 and str(best) != opt_string:
        next = start_pop.generate_next_gen(crossover_rate, mutation_rate)
        start_pop = next
        best = start_pop.find_best()
        file.write(str(start_pop.gen) + "," + str(int(best.fitness())) + "," + str(
           int(best.fitness() * pop_size)) + "\n")
    file.close()

if __name__ == "__main__":
    for i in range(1, 31):
        seed = random.randint(0, 100000)
        hill_climber(128, 64, 0.005, seed, i)
    for i in range(1, 31):
        seed = random.randint(0, 100000)
        GA_RR(128, 64, 0.7, 0.005, seed, i)
    # for i in range(1, 31):
    #     seed = random.randint(0, 100000)
    #     GA(128, 64, 0.7, 0.005, seed, i)


















