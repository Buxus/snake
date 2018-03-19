#! /usr/bin/python3
"""
Snake Game
"""

import pygame
from pygame.locals import *
import pygcurse
import random
import string

res_x = 60
res_y = 40

win = pygcurse.PygcurseWindow(res_x, res_y)
win.font = pygame.font.Font(None, 28)
    
movements = {
    'n': lambda coord: (x_pos(coord), y_pos(coord) - 1),
    'e': lambda coord: (x_pos(coord) + 1, y_pos(coord)),
    'w': lambda coord: (x_pos(coord) - 1, y_pos(coord)),
    's': lambda coord: (x_pos(coord), y_pos(coord) + 1)
}
fruit_chars = list(string.printable)
colors = list(pygcurse.colornames.keys())

class Snake:
    """Documentation for Snake

    """

    def __init__(self):
        self.head = (30, 20)
        self.tail = [(29, 20), (28, 20), (27, 20), (26, 20)]
        self.head_color = 'red'
        self.tail_color = 'green'

    def move(self, direction='e', grow=False):
        head_pos = self.head
        self.head = movements[direction](head_pos)
        if grow == False:
            last_pos = self.tail[-1]
            self.tail = [head_pos] + self.tail[0:-1]
            win.write(' ', x=x_pos(last_pos), y=y_pos(last_pos))
        else:
            self.tail = [head_pos] + self.tail

        # draw changed segments
        win.write('@', x=x_pos(self.head), y=y_pos(self.head), fgcolor=self.head_color)
        win.write('O', x=x_pos(self.tail[0]), y=y_pos(self.tail[0]), fgcolor=self.tail_color)

    def died(self):
        head_pos_x = x_pos(self.head)
        head_pos_y = y_pos(self.head)
        if head_pos_x == 0 or head_pos_x == res_x:
            return True
        elif head_pos_y == 0 or head_pos_y == res_y:
            return True
        elif self.head in self.tail:
            return True
        else:
            return False

    def ate(self, fruit_list):
        i = 0
        for fruit in fruit_list:
            if self.head == (fruit.x, fruit.y):
                win.write(' ', x=fruit_list[i].x, y=fruit_list[i].y)
                del(fruit_list[i])
                return True
            i += 1
        else:
            return False


class Fruit:
    def __init__(self):
        self.x = int(random.random() * (res_x - 2)) + 1
        self.y = int(random.random() * (res_y - 2)) + 1
        self.char = random.choice(fruit_chars)


def x_pos(coord):
    return coord[0]


def y_pos(coord):
    return coord[1]


def draw_map():
    wall_char = '#'
    win.drawline((0, 0), (res_x - 1, 0), char=wall_char)
    win.drawline((0, 0), (0, res_y - 1), char=wall_char)
    win.drawline((res_x - 1, 0), (res_x - 1, res_y - 1), char=wall_char)
    win.drawline((0, res_y - 1), (res_x - 1, res_y - 1), char=wall_char)


def draw_snake(snake):
    # draw head
    win.write('@', x=x_pos(snake.head), y=y_pos(snake.head), fgcolor=snake.head_color)

    # draw tail
    for segment in snake.tail:
        win.write('O', x=x_pos(segment), y=y_pos(segment), fgcolor=snake.tail_color)


# def draw_fruit(win, fruit_list):
#     for fruit in fruit_list:
#         win.write(fruit.char, x=fruit.x, y=fruit.y)


def draw_score(snake):
    score = len(snake.tail) - 4
    win.write("Score: " + str(score), x=(res_x / 2) - 4, y=0)


def pause():
    while 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_p:
                return None


def main():
    pygame.init()
    
    clock = pygame.time.Clock()

    snake = Snake()
    fruit_list = [Fruit()]
    new_fruit = fruit_list[-1]
    win.write(new_fruit.char, x=new_fruit.x, y=new_fruit.y, fgcolor=random.choice(colors), bgcolor=random.choice(colors))
    
    direction = 'e'

    draw_map()
    draw_snake(snake)
    # draw_fruit(win, fruit_list) 
    draw_score(snake)
    message = '~~~Snake~~~'
    win.write(message, x=(res_x/2) - (len(message)/2), y=res_y - 1, fgcolor=random.choice(colors), bgcolor=random.choice(colors))
    
    pause()
    
    while 1:
        if snake.died():
            print(len(snake.tail) - 4)
            break
        
        if len(fruit_list) <= 3 and random.random() >= 0.99:
            fruit_list.append(Fruit())
            new_fruit = fruit_list[-1]
            win.write(new_fruit.char, x=new_fruit.x, y=new_fruit.y, fgcolor=random.choice(colors), bgcolor=random.choice(colors))
        
        draw_score(snake)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    direction = 'n'
                elif event.key == K_DOWN:
                    direction = 's'
                elif event.key == K_LEFT:
                    direction = 'w'
                elif event.key == K_RIGHT:
                    direction = 'e'
                elif event.key == K_p:
                    pause()
                    
        if snake.ate(fruit_list):
            snake.move(direction, grow=True)
        else:
            snake.move(direction)

        clock.tick(30)


if __name__ == '__main__':
    main()
