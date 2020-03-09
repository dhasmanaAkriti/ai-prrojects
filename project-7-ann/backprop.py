"""
Complete this implementation of backpropagation learning for
feedforward networks.
"""

#------------------------------------------------------------------------------

import random, string, math

def pretty(values):
    string = ""
    return string.join(['%.3f' % v for v in values])

#------------------------------------------------------------------------------

class Unit:
    """
    A Unit object represents a node in a network.  It keeps track of
    the node's current activation value (between 0.0 and 1.0), as well
    as all of the connections from other units into this unit, and all
    of the connections from this unit to other units in the network.
    """

    def __init__(self, activation=0.0):
        assert 0.0 <= activation <= 1.0, 'activation out of range'
        self.activation = activation
        self.incomingConnections = []
        self.outgoingConnections = []
        self.delta = 0

    def sigmoidFunction(self, x):
        return 1 / (1 + math.exp(-x))


#------------------------------------------------------------------------------

class Connection:
    """
    A Connection object represents a connection between two units of a
    network.  The connection strength is initialized to a small random
    value.
    """

    def __init__(self, fromUnit, toUnit):
        self.fromUnit = fromUnit
        self.toUnit = toUnit
        self.randomize()
        self.increment = 0

    def randomize(self):
        self.weight = random.uniform(-0.1, +0.1)

#------------------------------------------------------------------------------

class Network:
    """
    A Network object represents a three-layer feedforward network with
    a given number of input, hidden, and output units.
    """
    def __init__(self, numInputs, numHiddens, numOutputs):
        # create the units
        self.outputLayer = [Unit() for i in range(numOutputs)]
        self.hiddenLayer = [Unit() for j in range(numHiddens)]
        self.inputLayer = [Unit() for k in range(numInputs)]
        # wire up the network
        self.allConnections = []
        self.connectLayers(self.inputLayer, self.hiddenLayer)
        self.connectLayers(self.hiddenLayer, self.outputLayer)
        # connect the bias units
        outputBias = Unit(1.0)
        self.connectToLayer(outputBias, self.outputLayer)
        hiddenBias = Unit(1.0)
        self.connectToLayer(hiddenBias, self.hiddenLayer)
        # set the learning parameters
        self.learningRate = 0.3
        self.tolerance = 0.1

    def connect(self, fromUnit, toUnit):
        c = Connection(fromUnit, toUnit)
        fromUnit.outgoingConnections.append(c)
        toUnit.incomingConnections.append(c)
        self.allConnections.append(c)

    def connectToLayer(self, unit, layer):
        for otherUnit in layer:
            self.connect(unit, otherUnit)

    def connectLayers(self, fromLayer, toLayer):
        for unit in fromLayer:
            self.connectToLayer(unit, toLayer)

    def initialize(self):
        for c in self.allConnections:
            c.randomize()
        print('weights randomized')

    def test(self):
        print('weights =', pretty([c.weight for c in self.allConnections]))
        for pattern in self.inputs:
            output = pretty(self.propagate(pattern))
            hiddenRep = pretty([h.activation for h in self.hiddenLayer])
            print('%s -> [%s] -> output %s' % (pattern, hiddenRep, output))
        print()

    def propagate(self, pattern):
        """
        This method takes an input pattern, represented as a list of
        floating-point values, propagates the pattern through the
        network, and returns the resulting output pattern as a list of
        floating-point values.  This method should update the
        activation values of all input, hidden, and output units in
        the network as a side effect.

        It ensures that given pattern is the appropriate length and
        that the values are in the range 0-1. 
        """
        if len(pattern) == len(self.inputLayer):
            for unit_ind in range(len(pattern)):
                (self.inputLayer[unit_ind]).activation = pattern[unit_ind]
        for unit in self.hiddenLayer:
            sum_act = 0
            for connection in unit.incomingConnections:
                sum_act += connection.weight * connection.fromUnit.activation
            unit.activation = unit.sigmoidFunction(sum_act)
        for unit in self.outputLayer:
            sum_act = 0
            for connection in unit.incomingConnections:
                sum_act += connection.weight * connection.fromUnit.activation
            unit.activation = unit.sigmoidFunction(sum_act)
        toReturn = []
        for i in self.outputLayer:
            toReturn.append(i.activation)
        return toReturn

    def computeError(self):
        """
        This method evaluates the network's performance on the
        patterns stored in self.inputs with answers stored in
        self.targets, returning a tuple of the form

        (correct, total, score, error)

        where total is the total number of individual values in the
        target patterns, correct is the number of these that the
        network got right (to within self.tolerance), score is the
        percentage (0-100) of correct values, and error is the total
        sum squared error across all values.  
        """
        num_correct = 0
        total = len(self.targets) * len(self.targets[0])
        err = 0
        for index in range(len(self.inputs)):
            desired_output = self.targets[index]
            actual_output = self.propagate(self.inputs[index])
            for i in range(len(desired_output)):
                off_by = abs(actual_output[i] - desired_output[i])
                if off_by <= self.tolerance:
                    num_correct += 1
                err += (desired_output[i] - actual_output[i])**2
        score = (num_correct*100)/total
        # print(num_correct, total, score, err)
        return (num_correct, total, score, err)


    def teachPattern(self, pattern, target):
        """
        Modifies the weights according to the back-propagation
        learning rule using the given input pattern and associated
        target pattern.

        This method should begin by forward propagating activations.
        Next it should backward propagate error as follows:
        1. Update the deltas associated with every unit in the output layer.
        2. Update the deltas associated with every unit in the hidden layer.
        3. Update the increments associated with every connection in the
           network and then use these to update all weights in the network.
        """

        actual_output = self.propagate(pattern)
        desired_output = target
        for i in range(0, len(self.outputLayer)):
            err = desired_output[i] - actual_output[i]
            self.outputLayer[i].delta = err*self.sigmoidprime(self.outputLayer[i].activation)

        for i in range(0, len(self.hiddenLayer)):
            term = 0
            for j in self.hiddenLayer[i].outgoingConnections:
                term += j.weight * j.toUnit.delta
            self.hiddenLayer[i].delta = term*self.sigmoidprime(self.hiddenLayer[i].activation)
        for connection in self.allConnections:
            connection.increment = self.learningRate * connection.fromUnit.activation * connection.toUnit.delta
            connection.weight += connection.increment
        # for connection in self.allConnections:
        #     print(connection.increment)

    def sigmoidprime(self, term):
        return term *(1-term)
    def teachDataset(self):
        """
        Performs one learning sweep through the training set.  Patterns
        are randomly reordered on each sweep.
        """
        assert len(self.inputs) > 0, 'no training data'
        dataset = list(zip(self.inputs, self.targets))
        random.shuffle(dataset)
        for (pattern, target) in dataset:
            #print '   teaching %s -> %s' % (pattern, target)
            self.teachPattern(pattern, target)

    def train(self, cycles=10000):
        """
        Trains the network for the given number of training cycles
        (with a default of 10000).  This method repeatedly calls
        teachDataset, displaying the current cycle number and
        performance of the network after each call.
        """
        assert len(self.inputs) > 0, 'no training data'
        (correct, total, score, error) = self.computeError()
        print('Epoch #    0: TSS error %7.4f, %d/%d correct (%.1f%%)' % \
              (error, correct, total, score))
        for t in range(1, cycles+1):
            self.teachDataset()
            (correct, total, score, error) = self.computeError()
            print('Epoch #%5d: TSS error %7.4f, %d/%d correct (%.1f%%)' % \
                  (t, error, correct, total, score))
            if correct == total:
                print('All patterns learned')
                break

#------------------------------------------------------------------------------
# XOR function

x = Network(2, 3, 1)

x.inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
x.targets = [[0], [1], [1], [0]]

x.test()
x.train()
x.test()

#------------------------------------------------------------------------------
# auto-association

a = Network(8, 3, 8)

a.inputs = [[1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1]]

a.targets = a.inputs

a.test()
a.train()
a.test()
