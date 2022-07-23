import gym
import numpy as np
from DDQN import Agent
import matplotlib.pyplot as plt

EPISODE = 200


def main(agent):
    reward_list = []
    reward_mean = []
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
        reward_mean.append(np.mean(reward_list))

    return reward_mean

if __name__ == "__main__":
    env = gym.make('CartPole-v0')

    pri_agent = Agent(alpha=0.0005,
                  gamma=0.9,
                  n_actions=2,
                  epsilon=0.7,
                  batch_size=32,
                  epsilon_end=0.1,
                  epsilon_dec=0.9,
                  mem_size=8192,
                  iteration=20,
                  input_shape=4,
                  use_ddqn=True)

    ori_agent = Agent(alpha=0.0005,
                  gamma=0.9,
                  n_actions=2,
                  epsilon=0.7,
                  batch_size=32,
                  epsilon_end=0.1,
                  epsilon_dec=0.9,
                  mem_size=8192,
                  iteration=20,
                  input_shape=4,
                  use_ddqn=False)

    use_ddqn = main(pri_agent)
    not_use_ddqn = main(ori_agent)

    plt.plot(use_ddqn, label='use_ddqn')
    plt.plot(not_use_ddqn, label='not_use_ddqn')
    plt.legend()
    plt.grid()
    plt.show()

