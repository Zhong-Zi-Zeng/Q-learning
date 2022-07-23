import pygame
import copy
import cv2
from Q_learning import RL
from parameter import Parameter
from ori_snake import OriSnake
from alert import Alert
from goal import Goal
from state import State


class Main(Parameter):
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
        """RL"""
        self.rl = RL()
        """建立視窗"""
        self.win_screen = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("Snake Game")

    def run(self):
        """設定偵數"""
        fpsClock = pygame.time.Clock()
        """Train"""
        max = 1

        for epoch in range(10000):
            self.restart_game()
            while True:
                pygame.event.get()
                snake_old_location = copy.deepcopy(self.snake_list[0])

                """train action"""
                old_state = self.generator_state()
                self.rl.add_state(old_state)
                action = self.rl.train_action(old_state)

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
                    reward = -20
                    self.update_q_table(old_state=old_state,reward=reward)
                    break

                """判斷是否撞到邊界"""
                if (self.snake_list[0].x < 0 or self.snake_list[0].x == self.win_width or self.snake_list[0].y < 0 or self.snake_list[0].y == self.win_height):
                    reward = -20
                    self.update_q_table(old_state=old_state, reward=reward)
                    break

                """判斷有沒有吃到獎勵"""
                if(pygame.Rect.colliderect(self.snake_list[0],self.goal)):
                    self.snake_list = self.snake.add_body(snake_old_location, self.snake_list)
                    self.goal = Goal().get_goal(self.snake_list)
                    reward = 100
                    self.update_q_table(old_state=old_state, reward=reward)
                else:
                    self.snake_list = self.snake.move_body(self.snake_list, snake_old_location)
                    reward = -1
                    self.update_q_table(old_state=old_state, reward=reward)


                """繪製"""
                if(epoch > 100):
                    self.win_screen.fill((0, 0, 0))
                    for snake in self.snake_list:
                        pygame.draw.rect(self.win_screen,self.snake.color,snake)
                    pygame.draw.rect(self.win_screen, (255, 0, 0), self.goal)


                    pygame.display.update()
                    fpsClock.tick(40)


                if(len(self.snake_list) > max):
                    max = len(self.snake_list)

            self.rl.adjust_hyperparameter(epoch)

            print('Train times:',epoch)
            print('Best score:',max)
        # self.rl.save_q_table()

    def update_q_table(self,old_state,reward):
        new_state = self.generator_state()
        self.rl.add_state(new_state)
        self.rl.update_q_tabel(old_state, new_state, reward)

    def generator_state(self) -> list:
        self.state.danger_state(snake_list=self.snake_list, direction=self.direction)
        self.state.direction_state(direction=self.direction)
        self.state.food_state(snake_list=self.snake_list, food_loc=self.goal)

        return self.state.get_state()

    def restart_game(self):
        self.direction = 'down'
        self.snake_list = self.snake.create_body()
        self.goal = Goal().get_goal(self.snake_list)


if __name__ == '__main__':
    main = Main()
    main.run()
