#! /usr/bin/python3
"""
Snake Game
"""

import pygame
from pygame.locals import *
import pygcurse
import random

res_x = 60
res_y = 40

movements = {
    'n': lambda coord: (x_pos(coord), y_pos(coord) - 1),
    'e': lambda coord: (x_pos(coord) + 1, y_pos(coord)),
    'w': lambda coord: (x_pos(coord) - 1, y_pos(coord)),
    's': lambda coord: (x_pos(coord), y_pos(coord) + 1)
}
fruit_chars = ['a', 'b', 'c', '!', '$', '%', '^', '&', '*', '(', ')']


class Snake:
    """Documentation for Snake

    """

    def __init__(self):
        self.head = (30, 20)
        self.tail = [(29, 20), (28, 20), (27, 20), (26, 20)]
        self.head_color = 'red'
        self.tail_color = 'green'

    def move(self, win, direction='e', grow=False):
        head_pos = self.head
        self.head = movements[direction](head_pos)
        if grow == False:
            last_pos = self.tail[-1]
            self.tail = [head_pos] + self.tail[0:-1]
            win.cursor = last_pos
            win.write(' ')
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
                del(fruit_list[i])
                return True
            i += 1
        else:
            return False


class Fruit:
    def __init__(self):
        self.x = int(random.random() * (res_x - 2)) + 1
        self.y = int(random.random() * (res_y - 2)) + 1
        self.char = fruit_chars[int(random.random() * len(fruit_chars))]


def x_pos(coord):
    return coord[0]


def y_pos(coord):
    return coord[1]


def draw_map(win):
    wall_char = '#'
    win.drawline((0, 0), (res_x - 1, 0), char=wall_char)
    win.drawline((0, 0), (0, res_y - 1), char=wall_char)
    win.drawline((res_x - 1, 0), (res_x - 1, res_y - 1), char=wall_char)
    win.drawline((0, res_y - 1), (res_x - 1, res_y - 1), char=wall_char)


def draw_snake(win, snake):
    # draw head
    win.write('@', x=x_pos(snake.head), y=y_pos(snake.head), fgcolor=snake.head_color)

    # draw tail
    for segment in snake.tail:
        win.write('O', x=x_pos(segment), y=y_pos(segment), fgcolor=snake.tail_color)


def draw_fruit(win, fruit_list):
    for fruit in fruit_list:
        win.write(fruit.char, x=fruit.x, y=fruit.y)


def draw_score(win, snake):
    score = len(snake.tail) - 4
    win.write("Score: " + str(score), x=res_x / 2, y=0)


def pause():
    while 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_p:
                return None


def main():
    pygame.init()
    win = pygcurse.PygcurseWindow(res_x, res_y)
    win.font = pygame.font.Font(None, 28)
    
    clock = pygame.time.Clock()

    snake = Snake()
    fruit_list = [Fruit()]

    direction = 'e'

    draw_map(win)
    draw_snake(win, snake)
    draw_fruit(win, fruit_list)
    draw_score(win, snake)
    pause()
    
    while 1:
        if snake.died():
            break
        
        if random.random() >= 0.98:
            fruit_list.append(Fruit())
        
        #draw_snake(win, snake)
        draw_fruit(win, fruit_list)
        draw_score(win, snake)

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
            snake.move(win, direction, grow=True)
        else:
            snake.move(win, direction)

        clock.tick(600)


if __name__ == '__main__':
    main()