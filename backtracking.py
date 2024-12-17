# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import sys
 
import pygame
from pygame.locals import *
from random import randrange


class Cell:
    
    def __init__(self, x, y, size, walls):
        self.x = x
        self.y = y
        self.size = size
        self.walls = walls
        
        self.visited = False
        
        self.normal_bg = (34, 34, 34, 255)
        self.visited_bg = (255, 255, 255, 255)
        self.current_bg = self.normal_bg
        
    def draw(self):
        self.current_bg = self.visited_bg if self.visited else self.normal_bg
        
        pygame.draw.rect(screen, self.current_bg, pygame.Rect(self.x, self.y, self.size, self.size))
        self.draw_walls()
        
    def draw_walls(self):
        # 0 - top
        if self.walls[0]:
            self.draw_line((self.x, self.y), (self.x + self.size, self.y))
        # 1 - right
        if self.walls[1]:
            self.draw_line((self.x + self.size, self.y), (self.x + self.size, self.y + self.size))
        # 2 - bottom
        if self.walls[2]:
            self.draw_line((self.x, self.y + self.size), (self.x + self.size, self.y + self.size))
        # 3 - left
        if self.walls[3]:
            self.draw_line((self.x, self.y), (self.x, self.y + self.size))

    def draw_line(self, start_pos, end_pos):
        pygame.draw.line(screen, (97, 97, 97, 255), start_pos, end_pos)
        
    def remove_wall(self, idx):
        self.walls[idx] = False
 
pygame.init()
 
fps = 1
fpsClock = pygame.time.Clock()
 
width, height = 1200, 640
screen = pygame.display.set_mode((width, height))
 
grid = []
size = 5

cols = width // size
rows = height // size
margin = 2

grid = [[(0,0) for _ in range(rows)] for _ in range(cols)]

for i in range(cols):
    for j in range(rows):
        grid[i][j] = Cell(i*size, j*size, size, [True, True, True, True])
        
s_visited = []
current_cell = grid[randrange(cols)][randrange(rows)]
current_cell.visited = True

s_visited.append(current_cell)
        
# Game loop.
while True:
  screen.fill((0, 0, 0))
  
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  
  # Update.
  while len(s_visited) > 0:
      current_cell = s_visited.pop()
      
      i = current_cell.x // size
      j = current_cell.y // size
      
      if j != 0: top = grid[i][j - 1]
      if i != cols - 1: right = grid[i + 1][j]   
      if j != rows - 1: bottom = grid[i][j + 1]
      if j != 0: left = grid[i - 1][j]
      
      s_unvisited_neigh = []
      if not top.visited: s_unvisited_neigh.append(top)
      if not right.visited: s_unvisited_neigh.append(right)
      if not bottom.visited: s_unvisited_neigh.append(bottom)
      if not left.visited: s_unvisited_neigh.append(left)
      
      if len(s_unvisited_neigh)> 0:
        s_visited.append(current_cell)
        new_cell = s_unvisited_neigh[randrange(0, len(s_unvisited_neigh))]
        
        if new_cell == top:
            current_cell.remove_wall(0)
            new_cell.remove_wall(2)
        elif new_cell == right:
            current_cell.remove_wall(1)
            new_cell.remove_wall(3)
        elif new_cell == bottom:
            current_cell.remove_wall(2)
            new_cell.remove_wall(0)
        elif new_cell == left:
            current_cell.remove_wall(3)
            new_cell.remove_wall(1)
          
        current_cell = new_cell
        current_cell.visited = True
        s_visited.append(current_cell)

  # Draw.
  for i in range(cols):
      for j in range(rows):
          grid[i][j].draw()        
          
  pygame.display.flip()
  fpsClock.tick(fps)
