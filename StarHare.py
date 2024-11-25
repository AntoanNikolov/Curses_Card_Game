import curses
stdscr = curses.initscr()
curses.noecho()
def gDifuse(x, y, length, hight, xpos, ypos, file):
    global artx, arty, stdscr, sprite
    art = open(file, 'r')
    lines = art.readlines()
    for i in range(y,y+hight):
        sprite.append([])
        for n in range(x,x+length):
            char = lines[i][n]
            #print(char)
            stdscr.addstr(arty+ypos, artx+xpos, char)
            artx += 1
        arty +=1
        artx = 0
    else:
        artx, arty = 0, 0
    art.close
key = ''
artx = 0
arty = 0
sprite = []
file = "/Users/1049811/Desktop/python/StarHare.txt"
while key != ord('Q'):
    key = stdscr.getch()
    cursesKey = stdscr.getch
#File test
    if key == ord('p'):
        #Coords in the text file, length and hight of the rectangl you want, coords of plancemnt on the terminal, file
        gDifuse(0,10,20,10,0,0,file)
    if key == ord('c'):
        stdscr.clear()
    stdscr.refresh()
curses.endwin()