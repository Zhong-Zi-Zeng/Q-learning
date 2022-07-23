import pygame
import copy
import cv2
import numpy as np
from DQN import *
from parameter import Parameter
from ori_snake import OriSnake
from alert import Alert
from goal import Goal
from state import State


class SnakeGame(Parameter):
    def __init__(self):
        super().__init__()
        """初始化pygame"""
        pygame.init()
        """預設方向"""
        self.direction = 'down'
        """建立蛇"""
        self.snake = OriSnake()
        self.snake_list = self.snake.create_body()
        """目標"""
        self.goal = Goal().get_goal(self.snake_list)
        """State"""
        self.state = State()
        """agent"""
        self.agent = Agent(alpha=0.1,
                           gamma=0.5,
                           n_actions=3,
                           epsilon=1,
                           batch_size=32,
                           mem_size=20000,
                           epsilon_dec=0.99,
                           epsilon_end=0.01,
                           fixed_q=False)
        # self.agent.load_model()
        """建立視窗"""
        self.win_screen = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("Snake Game")

    def run(self):
        game_times = 1000
        scores = []
        length_list = []

        for i in range(game_times):
            done = 0
            score = 0
            self.restart_game()
            while not done:
                pygame.event.get()
                snake_old_location = copy.deepcopy(self.snake_list[0])

                """get action"""
                old_state = self.draw_frame()
                action = self.agent.choose_action(old_state)
                """parse action"""
                if(action == 0):
                    pass
                elif(action == 1):
                    if(self.direction == 'up'):
                        self.direction = 'right'
                    elif(self.direction == 'down'):
                        self.direction = 'left'
                    elif(self.direction == 'left'):
                        self.direction = 'up'
                    elif(self.direction == 'right'):
                        self.direction = 'down'
                elif(action == 2):
                    if (self.direction == 'up'):
                        self.direction = 'left'
                    elif(self.direction == 'down'):
                        self.direction = 'right'
                    elif (self.direction == 'left'):
                        self.direction = 'down'
                    elif (self.direction == 'right'):
                        self.direction = 'up'

                """改變座標"""
                if(self.direction == 'left'):
                    self.snake_list[0].x -= self.snake.step
                elif(self.direction == 'right'):
                    self.snake_list[0].x += self.snake.step
                elif(self.direction == 'up'):
                    self.snake_list[0].y -= self.snake.step
                elif(self.direction == 'down'):
                    self.snake_list[0].y += self.snake.step

                """判斷是否碰到自己"""
                if (self.snake_list[0] in self.snake_list[1:]):
                    done = 1

                """判斷是否撞到邊界"""
                if (self.snake_list[0].x < 0 or self.snake_list[0].x == self.win_width - 20 or self.snake_list[0].y < 0 or self.snake_list[0].y == self.win_height - 20):
                    done = 1

                """判斷有沒有吃到獎勵"""
                if(pygame.Rect.colliderect(self.snake_list[0],self.goal)):
                    self.snake_list = self.snake.add_body(snake_old_location, self.snake_list)
                    self.goal = Goal().get_goal(self.snake_list)
                    reward = 100
                else:
                    self.snake_list = self.snake.move_body(self.snake_list, snake_old_location)
                    reward = -1

                if(done):
                    reward = -100

                score += reward

                new_state = self.draw_frame()
                self.agent.remember(old_state,action,reward,new_state,done)
                self.agent.learn()

            scores.append(score)
            length_list.append(len(self.snake_list))

            print('='*50)
            print('Episode:',i)
            print('Snake length:',len(self.snake_list))
            print('Average Snake length: %.2f'%np.mean(length_list))
            print('Score: %.2f'%score)
            print('Average score: %.2f'%np.mean(scores))

            if(i % 10 == 0 and i > 0):
                self.agent.save_model()

    """繪製畫面"""
    def draw_frame(self):
        # fpsClock = pygame.time.Clock()

        self.win_screen.fill((0, 0, 0))
        for snake in self.snake_list:
            pygame.draw.rect(self.win_screen, self.snake.color, snake)
        pygame.draw.rect(self.win_screen, (255, 0, 0), self.goal)
        # pygame.display.update()
        """設定偵數"""
        # fpsClock.tick(200)

        frame = pygame.surfarray.pixels3d(self.win_screen)
        frame = frame.swapaxes(1,0)
        # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # frame = np.reshape(frame, 200 * 200)
        frame = frame / 255

        return frame

    """重新開始遊戲"""
    def restart_game(self):
        self.direction = 'down'
        self.snake_list = self.snake.create_body()
        self.goal = Goal().get_goal(self.snake_list)

    """產生狀態"""
    def generator_state(self) -> list:
        self.state.danger_state(snake_list=self.snake_list, direction=self.direction)
        self.state.direction_state(direction=self.direction)
        self.state.food_state(snake_list=self.snake_list, food_loc=self.goal)

        return self.state.get_state()

if __name__ == '__main__':
    main = SnakeGame()
    main.run()
