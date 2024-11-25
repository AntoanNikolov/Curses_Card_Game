import StarHareFunc
import curses
stdscr = curses.initscr()
curses.noecho()
key = ''
file = ('/Users/1049811/Desktop/python/StarHare.txt')
while key != ord('Q'):
    key = stdscr.getch()
    if key == ord('p'):
        StarHareFunc.gDifuse(0,0,40,20,0,0,file)