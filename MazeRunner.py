# -*- coding: utf-8 -*-

import os, sys
import msvcrt
import random
from collections import defaultdict


OBJMAP = {0: ' ', 1: '@', 9: 'p', 2: '$'}
DIRECT_4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
DIRECT_8 = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))
CONTROL = {'\xe0H': (-1, 0), '\xe0P': (1, 0), 
           '\xe0K': (0, -1), '\xe0M': (0, 1)}


def get_neighbor(p, xlim, ylim, directions):
    constraint = lambda p: 0 < p[0] < xlim-1 and 0 < p[1] < ylim-1
    plist = [(p[0]+i, p[1]+j) for i,j in directions]
    return set(filter(constraint, plist))

def generate_maze(w, h):
    maze = [[1] * w for _ in range(h)]
    to_search = [(random.randint(1, h-1), random.randint(1, w-1))]
    while to_search:
        cur_p = to_search[-1]
        maze[cur_p[0]][cur_p[1]] = 0
        neighbors = [(i,j) for i,j in get_neighbor(cur_p, h, w, DIRECT_4) if maze[i][j]]
        
        available = []
        for p in neighbors:
            new_neighs = get_neighbor(p, h, w, DIRECT_8).difference(get_neighbor(cur_p, h, w, DIRECT_4))
            if sum([maze[i][j] == 0 for i,j in new_neighs]) <= 1:
                available.append(p)
        
        if available:
            to_search.append(random.choice(available))
        else:
            to_search.pop()
    return maze

def generate_object(maze, n = 5):
    xlim, ylim = len(maze), len(maze[0])
    p = (random.randrange(1, xlim), random.randrange(1, ylim))
    while maze[p[0]][p[1]]:
        p = (random.randrange(1, xlim), random.randrange(1, ylim))
    maze[p[0]][p[1]] = 9
    return maze

def parse_maze(maze):
    objs = defaultdict(set)
    for i,r in enumerate(maze):
        for j,n in enumerate(r):
            if n > 1:
                objs[n].add((i, j))
                objs[(i, j)] = n
    return objs

def move(maze, command):
    xlim, ylim = len(maze), len(maze[0])
    objs = parse_maze(maze)

    if command not in CONTROL:
        return maze
    
    pi, pj = objs[9].pop()
    qi = pi + CONTROL[command][0]
    qj = pj + CONTROL[command][1]
    if 1 <= qi < xlim - 1 and 1 <= qj < ylim - 1 and maze[qi][qj] == 0:
        maze[pi][pj] = 0
        maze[qi][qj] = 9
    return maze

def show_maze(maze):
    show = [map(OBJMAP.get, r) for r in maze]
    for line in show:
        print ' '.join(line)

def main():
    mz = generate_object(generate_maze(30, 20))

    command = ''
    while True:
        os.system("cls")
        mz = move(mz, command)
        show_maze(mz)
        
        ch = msvcrt.getch()
        print [ch]
        if ch in 'q|Q|\x1b':
            print "\nBye."
            break
        else:
            command = command[-1] + ch if len(command) else ch

        if command not in CONTROL:
            continue
        else:
            print CONTROL[command]

if __name__=='__main__':
    main()