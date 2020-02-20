import random, copy
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
        return self.string.count("1")

    def get_genome(self):
        return self.string

    def initialize(self, my_string):
        self.string = my_string

    def initialize_r(self):
        my_string = ""
        for i in range(self.length):
            my_string = my_string + random.choice(["0", "1"])
        self.string = my_string

    def mutate(self, rate = 0.5):
        num_flips = int(rate * self.length)
        child_genome = BitGenome(self.length)
        child = copy.copy(self.get_genome())
        child_list = list(child)
        indices = []
        for i in range(num_flips):
            x = random.randint(0, self.length)
            while x in indices:
                x = random.randint(0, self.length)
            indices.append(x)
        for i in indices:
            if child_list[i] == "0":
                child_list[i] ="1"
            else:
               child_list[i] = "0"

        child_genome.initialize("".join(child_list))
        return child_genome

    def crossover(self, other):
        child_genome = BitGenome(self.length)
        crossover_point = random.randint(1, self.length)
        child = self.get_genome()[0:crossover_point] + \
                other.get_genome()[crossover_point:self.length]
        child_genome.initialize(child)
        return child_genome

class Population():
    def generate_first_pop(self):
        abstract()
    def cull(self, size):
        abstract()
    def generate_future_pop(self, crossover_rate, mutation_rate):
        abstract()

class Pop_Bit_Genome(Population):
    def __init__(self, population_size, bit_length, population = []):
        self.pop_size = population_size
        self.bitlen = bit_length
        self.pop = population

    def generate_first_pop(self):
        popul = []
        for i in range(self.pop_size):
            gen = BitGenome(self.bitlen)
            gen.initialize_r()
            popul.append(gen)
        self.pop = popul

    def generate_future_pop(self, crossover_rate, mutation_rate):
        num_crossover_chi =
        x = self.cull
        for i in x:
            if i



        to_return = Pop_Bit_Genome(self.pop_size, self.bitlen)

    def cull(self, size):
        sum_fit = 0
        for i in self.pop:
            sum_fit += i.fitness()
        new_l = []
        for i in self.pop:
             new_l.append((i, i.fitness/sum_fit))
        new_l.sort(x[1])
        for i in range(len(new_l)):
            accum_sum = 0
            for j in range(i):
                accum_sum += new_l[j][1]
            new_l[i].append(accum_sum)
        culled_list = []
        for i in range(size):
            R = random.random(0, 1)
            not_found = True
            i = 0
            while not_found:
                if R >= new_l[i][2]:
                     culled_list.append(new_l[i][0])
        return culled_list















if __name__ == "__main__":
    gen1 = BitGenome(6)
    gen1.initialize_r()

    gen2 = BitGenome(6)
    gen2.initialize_r()

    print(gen1)
    print(gen1.mutate())

    print(gen2)
    print(gen1.crossover(gen2))











