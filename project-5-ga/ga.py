import random, copy, utilities
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
    def __init__(self, length):
        self.length = length
        self.string = ""

    def __str__(self):
        return self.string

    def fitness(self):
        return float(self.string.count("1"))
    def mutate(self, rate = 0.5):
        child_genome = BitGenome(self.length)
        child = copy.copy(self.get_genome())
        child_list = list(child)
        num, den = utilities.convert_rate_to_fraction(rate)
        for i in range(len(child_list)):
            loc = random.randint(1, den+1)
            if loc <= num:
                child_list[i] = utilities.flip(child_list[i])
        child_genome.initialize("".join(child_list))
        return child_genome

    def crossover(self, other):
        child_genome1 = BitGenome(self.length)
        child_genome2 = BitGenome(self.length)
        crossover_point = random.randint(1, self.length)
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
            my_string = my_string + random.choice(["0", "1"])
        self.string = my_string

class BitGenome_GA_RR(BitGenome):
    def initialize(self, length):
        super().__init__(length)
    def fitness(self):
        initial_sum = 0
        copy_of_the_first = copy.copy(self.string)
        num_bit_strings = self.length / 8
        for i  in range(num_bit_strings):
            first = 0
            last = first + 8
            if copy_of_the_first[first:last] == "11111111":
                initial_sum += 8
            first = last
            copy_of_the_first = copy_of_the_first[first:]
        return initial_sum

    def mutate(self, rate = 0.5):
        child_genome = BitGenome_HC(self.length)
        child = copy.copy(self.get_genome())
        child_list = list(child)
        num, den = utilities.convert_rate_to_fraction(rate)
        for i in range(len(child_list)):
            loc = random.randint(1, den+1)
            if loc <= num:
                child_list[i] = utilities.flip(child_list[i])
        child_genome.initialize("".join(child_list))
        return child_genome

    def crossover(self, other):
        child_genome1 = BitGenome_HC(self.length)
        child_genome2 = BitGenome_HC(self.length)
        crossover_point = random.randint(1, self.length)
        child1 = self.get_genome()[0:crossover_point] + \
                other.get_genome()[crossover_point:self.length]
        child2 = other.get_genome()[0:crossover_point] + \
                 self.get_genome()[crossover_point:self.length]
        child_genome1.initialize(child1)
        child_genome2.initialize(child2)
        return (child_genome1, child_genome2)


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
    def __init__(self, population_size, bit_length, population = [], gen = 0):
        self.pop_size = population_size
        self.bitlen = bit_length
        self.pop = population
        self.gen = gen

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
            gen = BitGenome(self.bitlen)
            gen.initialize_r()
            popul.append(gen)
        self.pop = popul

    def generate_next_gen(self, crossover_rate, mutation_rate):
        x = self.cull(self.pop_size//2)
        next_gen = []
        num, dem = utilities.convert_rate_to_fraction(crossover_rate)
        while len(next_gen) != self.pop_size:
            loc = random.randint(1, dem)
            if loc <= num:
                p1 = random.choice(x)
                p2 = random.choice(x)
                child = p1.crossover(p2)
                next_gen.append(child[1].mutate(mutation_rate))
                next_gen.append(child[0].mutate(mutation_rate))
            else:
                p1 = random.choice(x)
                p2 = random.choice(x)
                next_gen.append(p1.mutate(mutation_rate))
                next_gen.append(p2.mutate(mutation_rate))
        population = Pop_Bit_Genome_GA(self.pop_size, self.bitlen, next_gen, self.gen + 1)
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
            R = random.random()
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
    def __init__(self, population_size, bit_length, population = [], gen = 0):
        self.pop_size = population_size
        self.bitlen = bit_length
        self.pop = population
        self.gen = gen

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
            gen = Pop_Bit_Genome_GA_RR(self.bitlen)
            gen.initialize_r()
            popul.append(gen)
        self.pop = popul

    def generate_next_gen(self, crossover_rate, mutation_rate):
        x = self.cull(self.pop_size//2)
        next_gen = []
        num, dem = utilities.convert_rate_to_fraction(crossover_rate)
        while len(next_gen) != self.pop_size:
            loc = random.randint(1, dem)
            if loc <= num:
                p1 = random.choice(x)
                p2 = random.choice(x)
                child = p1.crossover(p2)
                next_gen.append(child[1].mutate(mutation_rate))
                next_gen.append(child[0].mutate(mutation_rate))
            else:
                p1 = random.choice(x)
                p2 = random.choice(x)
                next_gen.append(p1.mutate(mutation_rate))
                next_gen.append(p2.mutate(mutation_rate))
        population = Pop_Bit_Genome_GA_RR(self.pop_size, self.bitlen, next_gen, self.gen + 1)
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
            R = random.random()
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
    def __init__(self, population_size, bit_length, population=[], gen=0):
        self.pop_size = population_size
        self.bitlen = bit_length
        self.pop = population
        self.gen = gen

    def __str__(self):
        to_return = "POPULATION: \n"
        for i in self.pop:
            to_return += str(i) + "\n"
        to_return += "\nSIZE : "
        to_return += str(self.pop_size)
        to_return += "\n_______________________________________________________________________________________________\n"
        return to_return
    def generate_next_gen(self, mutation_rate):
        x = self.find_best()
        next_gen = []
        for i in range(self.pop_size):
            next_gen.append(x.mutate(mutation_rate))
        population = Pop_Bit_Genome_HC(self.pop_size, self.bitlen, next_gen, self.gen + 1)
        return population
    def generate_first_pop(self):
        popul = []
        for i in range(self.pop_size):
            gen = BitGenome(self.bitlen)
            gen.initialize_r()
            popul.append(gen)
        self.pop = popul

    def find_best(self):
        best = self.pop[0]
        for i in range(len(self.pop)):
            if self.pop[i].fitness() > best.fitness():
                best = self.pop[i]
        return best

def hill_climber(pop_size, bit_len, mutation_rate, seed):
    # r = random.Random(seed)
    start_pop = Pop_Bit_Genome_HC(pop_size, bit_len)
    print(start_pop)
    start_pop.generate_first_pop()
    print(start_pop)
    next = start_pop.generate_next_gen(mutation_rate)
    print(next)

if __name__ == "__main__":
    # gen1 = BitGenome(6)
    # gen1.initialize_r()
    #
    # gen2 = BitGenome(6)
    # gen2.initialize_r()
    #
    # print(gen1)
    # print(gen1.mutate(0.5))
    #
    # print(utilities.convert_rate_to_fraction(0.75))
    #
    # print(gen2)
    # print(gen1.crossover(gen2))
    hill_climber(4, 10, 0.5)










