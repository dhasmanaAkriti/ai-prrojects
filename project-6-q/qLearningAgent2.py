# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 14:24:26 2020

@author: Akriti
"""

import random
import numpy as np
import coffeegame
import gym
import matplotlib.pyplot as plt

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
    """
    This Q-Learning agent has 
    """
    INTERVAL = 1000
    def __init__(self, max_steps, max_num_eps, environment, learning_rate = 0.1, discount_rate = 0.6, exploration_rate = 1, render = False, decay_rate = 0.01):
        self.lr = learning_rate
        self.dr = discount_rate
        self.er = exploration_rate
        self.ms = max_steps
        self.num_eps = max_num_eps
        self.env = environment
        self.q_table = np.zeros((self.env.observation_space.n, self.env.action_space.n))
        self.render = render
        self.rewards = []
        self.decay_rate = decay_rate
    def learn(self):
        runs = 0
        while runs < self.num_eps:
            steps = 0
            reward_in_ep = 0
            state = self.env.reset()
            while steps < self.ms:
                r = random.random()
                if r < self.er:
#                    print("exploring" + str(steps))
                    action = self.env.action_space.sample()
                else:
#                    print("exploiting" + str(steps))
                    action = np.argmax(self.q_table[state, :])
                new_state, reward, done, info = self.env.step(action)
                # the q learning magic happens here.
                self.q_table[state, action] = self.q_table[state, action] * (1 - self.lr) + \
                                 self.lr * (reward + self.dr * np.max(self.q_table[new_state, :]))
                if self.render == True:
                    self.env.render()
#                    printQTable(self.q_table)
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
            self.er = (1-self.decay_rate)*self.er
            
    def behave(self):
        state = self.env.reset()
        done = False
        while not (done) :
            action = np.argmax(self.q_table[state, :])
            new_state, reward, done, info = self.env.step(action)
            state = new_state
            self.env.render()
        #printQTable(self.q_table)
    def plot(self):
        total = 0
        y = []
        x = list(range(0, self.num_eps+self.INTERVAL, self.INTERVAL))
        for i in x:
            if i == 0:
                y.append(0)
            else:
                total = sum(self.rewards[0:i])
                y.append(total/i)
        return (x, y)
        
if __name__ == "__main__":
    env = coffeegame.CoffeeEnv()
    env2 = gym.make("FrozenLake-v0", is_slippery=False)
    env3 = gym.make("Taxi-v3")
    LearningAgent = QLearningAgent(20, 20000, env, decay_rate = 0.01 )
    LearningAgent2 = QLearningAgent(30, 20000, env2, decay_rate = 0.001)
    LearningAgent3 = QLearningAgent(750, 20000, env3, decay_rate = 0.001)
    
    # LEARNING STUFF
    LearningAgent.learn()
    LearningAgent2.learn()
    LearningAgent3.learn()
    
    #BEHAVING
    LearningAgent.behave()
    LearningAgent2.behave()
    LearningAgent3.behave()
    
      #PLOTTING GRAPHS
    plt.xlabel("Number of Episodes")
    plt.ylabel("Average Reward per 1000 episodes")
    plt.plot(LearningAgent.plot()[0], LearningAgent.plot()[1])
    plt.show()
    
    plt.xlabel("Number of Episodes")
    plt.ylabel("Average Reward per 1000 episodes")
    plt.plot(LearningAgent2.plot()[0], LearningAgent2.plot()[1])
    plt.show()
    
    plt.xlabel("Number of Episodes")
    plt.ylabel("Average Reward per 1000 episodes")
    plt.plot(LearningAgent3.plot()[0], LearningAgent3.plot()[1])
    plt.show()
    
    
            






