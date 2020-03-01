import gym
import numpy as np


from gym.envs.classic_control import rendering

MAX_ITERATIONS = 100

env = gym.make("FrozenLake-v0")
env.reset()                    

print("Action space: ", env.action_space)
print("Observation space: ", env.observation_space)

for i in range(MAX_ITERATIONS):
    random_action = env.action_space.sample()
    new_state, reward, done, info = env.step(
       random_action)
    env.render()
    if done:
        break
env.close()
