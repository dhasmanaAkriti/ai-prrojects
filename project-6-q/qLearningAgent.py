import random
import numpy as np
import coffeegame
#import matplotlib as m

def printQTable(qt):
    rows,cols  = qt.shape
    print("State ||    LEFT  |   DOWN  |   RIGHT  | UP     |")
    print("-------------------------------------------------")
    for row in range(rows):
        outstr = "   "+str(row)+"  "
        col = qt[row]
        for val in col:
            outstr+='    {:6.2f}'.format(val)
        print(outstr)


class QLearningAgent():
    def __init__(self, max_steps, max_num_eps, environment, learning_rate = 0.1, discount_rate = 0.6, exploration_rate = 0.5):
        self.lr = learning_rate
        self.dr = discount_rate
        self.er = exploration_rate
        self.ms = max_steps
        self.num_eps = max_num_eps
        self.env = environment
        self.q_table = np.zeros((self.env.observation_space.n, self.env.action_space.n))
        self.rewards = []
    def learn(self):
        runs = 0
        while runs < self.num_eps:
            steps = 0
            reward_in_ep = 0
            print(runs)
            state = self.env.reset()
            while steps < self.ms:
                r = random.random()
                self.env.render()
                if r < self.er:
                    print("exploring" + str(steps))
                    action = self.env.action_space.sample()
                else:
                    print("exploiting" + str(steps))
                    action = np.argmax(self.q_table[state, :])
                new_state, reward, done, info = env.step(action)
                #printQTable(self.q_table)
                # the q learning magic happens here.
                self.q_table[state, action] = self.q_table[state, action] * (1 - self.lr) + \
                                 self.lr * (reward + self.dr * np.max(self.q_table[new_state, :]))
                reward_in_ep += reward
                if (done):
                    # reset if game is over
                    break
                else:
                    # otherwise update state
                    state = new_state
                steps += 1
            self.rewards.append(reward_in_ep)
            runs += 1
        print("training time finished")
    def behave(self):
        state = self.env.reset()
        done = False
        while not (done) :
            self.env.render()
            action = np.argmax(self.q_table[state, :])
            new_state, reward, done, info = self.env.step(action)
            state = new_state
            

if __name__ == "__main__":
    env = coffeegame.CoffeeEnv()
    LearningAgent = QLearningAgent(10, 1000, env)
    LearningAgent.learn()
    LearningAgent.behave()





