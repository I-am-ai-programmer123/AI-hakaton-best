'''
Autor: Bartłomiej Baran
'''
import gym
import matplotlib.pyplot as plt
import numpy as np
from gym.envs.registration import register

register(
        id='Frozenlake8x8-v0',
        entry_point='gym.envs.toy_text:FrozenLakeEnv',
        kwargs={'map_name': '8x8', 'is_slippery': False},
        max_episode_steps=1000,
        reward_threshold=0.78,  # optimum = .8196
)


def modify_reward(r, done, action, state, next_state):
    # hole
    if done and r == 0:
        return -50
    # goal
    elif done and r == 1:
        return 60
    # border
    elif state == next_state:
        return -30
    # closer to goal
    # down or right
    elif action == 1 or action == 2:
        return -3
    # left or up
    elif action == 0 or action == 3:
        return -2
    else:
        return 0


def epsilon_greedy_strategy(state_actions, epsilon):
    max_values = []
    for k in range(len(state_actions)):
        if state_actions[k] == max(state_actions):
            max_values.append(k)
    possible_moves_chances = np.ones(4)
    possible_moves_chances *= epsilon
    possible_moves_chances /= 4
    possible_moves_chances[np.random.choice(max_values)] += 1 - epsilon
    return possible_moves_chances


def main():
    episodes = 10000
    max_steps = 1000
    epsilon = 0.1
    beta = 0.6
    gamma = 1
    env = gym.make("Frozenlake8x8-v0")
    episodes_num = np.zeros(10000)
    episodes_r = np.zeros(10000)

    Q = np.zeros((env.observation_space.n, env.action_space.n))
    print('**Learning**')
    for episode in range(episodes):
        print('Episode:', episode)
        state = env.reset()
        for t in range(max_steps):
            action = np.random.choice(np.arange(4), p=epsilon_greedy_strategy(Q[state, :], epsilon))
            next_state, r, done, _ = env.step(action)
            # comment line below to leave default rewarding system
            r = modify_reward(r, done, action, state, next_state)
            Q[state, action] = Q[state, action] + beta * (r + gamma * np.max(Q[next_state, :]) - Q[state, action])
            episodes_num[episode] = t
            episodes_r[episode] += r
            state = next_state
            if done:
                break

    # print(Q)
    episodes1 = np.arange(10000)
    fig, axs = plt.subplots(2)
    axs[0].plot(episodes1, episodes_num, 'g', linewidth=0.1)
    axs[0].set(ylabel='Number of steps', xlabel='Episode number')
    episodes2 = np.arange(10000)
    axs[1].plot(episodes2, episodes_r, 'b', linewidth=0.1)
    axs[1].set(ylabel='Reward', xlabel='Episode number')
    fig.tight_layout()
    plt.show()

    print("**Testing**")
    success = 0
    for episode in range(episodes):
        print('Episode:', episode)
        state = env.reset()
        for t in range(max_steps):
            action = np.random.choice(np.arange(4), p=epsilon_greedy_strategy(Q[state, :], epsilon))
            next_state, r, done, _ = env.step(action)
            state = next_state
            if r == 1:
                success += 1
            if done:
                break
    return success/episodes


if __name__ == '__main__':
    print(main())
