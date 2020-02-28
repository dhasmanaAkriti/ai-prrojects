import random
import numpy as np
import coffeegame

def convert_rate_to_fraction(rate):
    rate_string = str(rate)
    denominator = "1"
    list_a = rate_string.split(".")
    numerator = list_a[0] + list_a[1]
    for i in range(len(list_a[1])):
        denominator += "0"
    return (int(numerator), int(denominator))

class QLearningAgent():
    def __init__(self, max_steps, max_num_eps, environment, learning_rate = 0.1, discount_rate = 0.6, exploration_rate = 0.5):
        self.lr = learning_rate
        self.dr = discount_rate
        self.er = exploration_rate
        self.ms = max_steps
        self.num_eps = max_num_eps
        self.env = environment
        self.q_table = np.zeros((self.env.state_space_size, self.env.action_space_size))
    def learn(self):
        num, den = convert_rate_to_fraction(self.er)
        runs = 0
        while runs < self.num_eps:
            r = random.randint(1, den)
            if r in range(1, num+1):
                steps = 0
                while steps < self.ms:
                    action = env.action_space.sample()
                    new_state, reward, done, info = env.step(action)
                    # the q learning magic happens here.
                    self.q_table[state, action] = self.q_table[state, action] * (1 - self.lr) + \
                                 self.lr * (reward + self.dr * np.max(self.q_table[new_state, :]))
                    if (done):
                        # reset if game is over
                        state = env.reset()
                        steps += 1
                    else:
                        # otherwise update state
                        state = new_state
            else:
                steps = 0
                while steps < self.ms:
                    action = np.arg_max(self.q_table[new_state, :])
                    new_state, reward, done, info = env.step(action)
                    # the q learning magic happens here.
                    self.q_table[state, action] = self.q_table[state, action] * (1 - self.lr) + \
                                             self.lr * (reward + self.dr * np.max(self.q_table[new_state, :]))
                    if (done):
                        # reset if game is over
                        state = env.reset()
                        steps += 1
                    else:
                        # otherwise update state
                        state = new_state
    # def behave(self):
    #     self.learn()
    #     state = env.reset()




if __name__ == "__main__":
    env = CoffeeEnv()
    LearningAgent = QLearningAgent(20, 10, env)
    LearningAgent.learn()





