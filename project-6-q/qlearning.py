#interactive q learning on coffee game


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

LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3

import coffeegame
import numpy as np
import getch

learning_rate = 0.1
discount_rate = 0.6
env = coffeegame.CoffeeEnv()

action_space_size = env.action_space.n
state_space_size = env.observation_space.n

#create the qtable
q_table = np.zeros((state_space_size, action_space_size))

#reset environment
state = env.reset()


while(True):
    #print some stuff
    env.render()
    printQTable(q_table)
    print('0: LEFT, 1: DOWN, 2: RIGHT, 3:UP')
    # get next action from user
    #you'll need to install getch in order to get this part to work
    # or comment out and replace with the line below it.
    # pip3 install --user getch
    #action = int(getch.getch())%4
    action = int(input('0: LEFT, 1: DOWN, 2: RIGHT, 3:UP'))
    new_state,reward,done, info = env.step(action)
    #the q learning magic happens here.
    q_table[state,action] = q_table[state, action] * (1 - learning_rate) + \
                            learning_rate * (reward + discount_rate * np.max(q_table[new_state, :]))
    if (done):
            #reset if game is over
        state = env.reset()
    else:
            #otherwise update state
        state = new_state
