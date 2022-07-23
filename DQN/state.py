from parameter import Parameter
import copy

class State(Parameter):
    def __init__(self):
        super().__init__()
        self.state_list = [0]*11
        """
            [0]danger straight
            [1]danger right
            [2]danger left
            [3]direction up
            [4]direction down
            [5]direction left
            [6]direction right
            [7]food up
            [8]food down
            [9]food left
            [10]food right
        """
    def danger_state(self,snake_list,direction):
        head_copy = []
        for i in range(4):
            head_copy.append(copy.deepcopy(snake_list[0]))

        head_copy[0].y -= 20
        head_copy[1].y += 20
        head_copy[2].x -= 20
        head_copy[3].x += 20

        if(direction == 'up'):
            if(snake_list[0].y == 0):
                self.state_list[0] = 1
            if(head_copy[0] in snake_list):
                self.state_list[0] = 1
            if(snake_list[0].x == self.win_width - 20):
                self.state_list[1] = 1
            if(head_copy[3] in snake_list):
                self.state_list[1] = 1
            if(snake_list[0].x == 0):
                self.state_list[2] = 1
            if(head_copy[2] in snake_list):
                self.state_list[2] = 1

        elif(direction == 'down'):
            if(snake_list[0].y == self.win_height - 20):
                self.state_list[0] = 1
            if(head_copy[1] in snake_list):
                self.state_list[0] = 1
            if(snake_list[0].x == 0):
                self.state_list[1] = 1
            if(head_copy[2] in snake_list):
                self.state_list[1] = 1
            if(snake_list[0].x == self.win_width - 20):
                self.state_list[2] = 1
            if(head_copy[3] in snake_list):
                self.state_list[2] = 1

        elif(direction == 'left'):
            if(snake_list[0].x == 0):
                self.state_list[0] = 1
            if(head_copy[2] in snake_list):
                self.state_list[0] = 1
            if(snake_list[0].y == 0):
                self.state_list[1] = 1
            if(head_copy[0] in snake_list):
                self.state_list[1] = 1
            if(snake_list[0].y == self.win_height - 20):
                self.state_list[2] = 1
            if(head_copy[1] in snake_list):
                self.state_list[2] = 1

        elif(direction == 'right'):
            if(snake_list[0].x == self.win_width - 20):
                self.state_list[0] = 1
            if(head_copy[3] in snake_list):
                self.state_list[0] = 1
            if(snake_list[0].y == self.win_height - 20):
                self.state_list[1] = 1
            if(head_copy[1] in snake_list):
                self.state_list[1] = 1
            if(snake_list[0].y == 0):
                self.state_list[2] = 1
            if(head_copy[0] in snake_list):
                self.state_list[2] = 1

    def direction_state(self,direction):
        if(direction == 'up'):
            self.state_list[3] = 1
        elif(direction == 'down'):
            self.state_list[4] = 1
        elif(direction == 'left'):
            self.state_list[5] = 1
        elif(direction == 'right'):
            self.state_list[6] = 1

    # def danger_closed(self):


    def food_state(self,snake_list,food_loc):
        """food up"""
        if(snake_list[0].y > food_loc.y):
            self.state_list[7] = 1
        """food down"""
        if(snake_list[0].y < food_loc.y):
            self.state_list[8] = 1
        """food left"""
        if(snake_list[0].x > food_loc.x):
            self.state_list[9] = 1
        """food right"""
        if(snake_list[0].x < food_loc.x):
            self.state_list[10] = 1

    def get_state(self):
        state = self.state_list
        self.state_list = [0] * 11
        return state
