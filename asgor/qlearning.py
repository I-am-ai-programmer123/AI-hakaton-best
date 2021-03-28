import numpy as np
import gym
import random
import time
from matplotlib import pyplot as plt

def new_reward(reward, done):
    if not done:
        return -0.1
    elif done and reward == 0:
        return -100
    else:
        return 100


env = gym.make("FrozenLake8x8-v0")

action_space_size = env.action_space.n
state_space_size = env.observation_space.n

q_table = np.zeros((state_space_size, action_space_size))

print(q_table)

max_steps_per_episode = 150

learning_rate = 0.1
discount_rate = 0.9

exploration_rate = 1
max_exploration_rate = 1
min_exploration_rate = 0.0001
exploration_decay_rate = 0.0001
success = []
rewards_all_episodes = []
env.render()


state = env.reset()
steps = []
done = False
rewards_current_episode = 0
exploration_rate - max_exploration_rate
rewards = {}

new_punishments = []


for i in range(20000):
    exploration_rate = exploration_rate - exploration_decay_rate
    state = env.reset()
    new_punishments.append(0)

    for step in range(max_steps_per_episode):

        exploration_rate_threshold = random.uniform(0, 1)
        if exploration_rate_threshold > exploration_rate:
            action = np.argmax(q_table[state,:])
        else:
            action = env.action_space.sample()
        
        new_state, reward, done, info = env.step(action)
        reward = new_reward(reward, done)

        if reward < 0:
            new_punishments[-1] += reward



        q_table[state, action] = q_table[state, action] * (1 - learning_rate) + learning_rate * (reward + discount_rate * np.max(q_table[new_state, :]))
        state = new_state





        rewards_current_episode += reward


        if done == True:
            break

    if reward > 0:
        success.append(1)
    else:
        success.append(0)
    env.render()
    rewards_all_episodes.append(reward)
    steps.append(step)

print(rewards.keys())

print(q_table)
x = []
y = []
for i in range(200):
    plt.xlabel("iterations")
    plt.ylabel("punishents  during last 100 iterations")
    x.append((i+1) * 100)
    y.append(sum(success[i*100:(i+1)*100]))
    print((i+1) * 100, sum(new_punishments[i*100:(i+1)*100]))


plt.plot(x, y)
plt.show()