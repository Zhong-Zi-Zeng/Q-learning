import gym
import numpy as np
import cv2
from Mix import MixAgent
from DQN import DqnAgent
import matplotlib.pyplot as plt

EPISODE = 200

def main(agent):
    reward_list = []

    for i in range(EPISODE):
        done = False
        total_reward = 0
        state = env.reset()
        print('now episode is: {}'.format(i))

        while not done:
            # env.render()
            action = agent.choose_action(state)
            next_state, reward, done, _ = env.step(action)
            total_reward += reward

            agent.remember(state,action,reward,next_state,done)
            agent.learn()

            state = next_state

        reward_list.append(total_reward)

    return reward_list

if __name__ == "__main__":
    env = gym.make('CartPole-v0')

    mix_agent = MixAgent(alpha=0.0005,
                  gamma=0.99,
                  n_actions=2,
                  epsilon=0.7,
                  batch_size=32,
                  epsilon_end=0.1,
                  epsilon_dec=0.9,
                  mem_size=8192,
                  iteration=20,
                  input_shape=4)

    dqn_agent = DqnAgent(alpha=0.0005,
                  gamma=0.99,
                  n_actions=2,
                  epsilon=0.7,
                  batch_size=32,
                  epsilon_end=0.1,
                  epsilon_dec=0.95,
                  mem_size=8192,
                  iteration=20,
                  input_shape=4)

    mix_agent_score = main(mix_agent)
    dqn_agent_score = main(dqn_agent)

    plt.plot(mix_agent_score, label='mix_agent')
    plt.plot(dqn_agent_score, label='dqn_agent')
    plt.ylabel('Score')
    plt.legend()
    plt.grid()
    plt.show()

