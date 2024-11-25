import curses
stdscr = curses.initscr()
curses.noecho()
artx = 0
arty = 0
sprite = []
def gDifuse(x, y, length, hight, xpos, ypos, file):
    global artx, arty, stdscr, sprite
    art = open(file, 'r')
    lines = art.readlines()
    for i in range(y,y+hight):
        sprite.append([])
        for n in range(x,x+length):
            char = lines[i][n]
            stdscr.addstr(arty+ypos, artx+xpos, char)
            artx += 1
        arty +=1
        artx = 0
    else:
        artx, arty = 0, 0
    art.close