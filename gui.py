#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import pygame
import sys
import time
from pygame.locals import *
import os
from queue import Queue, Empty


if(os.name != "nt"):
    import GPIOController as table
import threading

width = 800
height = 480
size = [width, height]
bg = [0, 0, 0]
btn_width = 180
btn_height = 100
buttons = [None] * 6

ON_POSIX = 'posix' in sys.builtin_module_names

clock = pygame.time.Clock()
fps = 60

screen = pygame.display.set_mode(size)
pygame.mouse.set_visible = False

currentScreen = "main"


def main():
    pygame.init()
    myfont = pygame.font.SysFont("freesansbold", 30)
    #Dette bruges til at køre Sopare
    process = subprocess.Popen(('./sopare.py -l'), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, close_fds=ON_POSIX, cwd="../sopare")
    q = Queue()
    t = threading.Thread(target=enqueue_output, args=(process.stdout, q))
    t.daemon = True
    t.start()

    while True:
        #using our enqueue_output thread to find out if sopare has sent anything
        try:  line = q.get_nowait() # or q.get(timeout=.1)
        except Empty:
            pass #do nothing
        else: # got a line from sopare
            nextline = line
            if process.poll() is not None:
                break
            #decoding from bytes to string
            currentline = nextline.decode()
            #This is where our if/elif statements will control the GPIO pins when a specific word is recognized
            if("ropox" in currentline):
                table.goUp(5) #Needs all logic and the command tree

        #optimized layoutcontrol
        if(currentScreen == "main"):
            sixButtonLayout(["PROFIL", "BORD", "SKAB", u"LÅS", "OVN", "INDSTILLINGER"], myfont)
        elif(currentScreen == "table"):
            sixButtonLayout(["OP", u"HØJDE", u"LÅS", "NED", "PROFIL", "TILBAGE"], myfont)
            # display headline
        pygame.display.set_caption('ROPOX')
        text("ROPOX", myfont, (width/2, height/10))
        pygame.display.flip()
        #managing clicks on buttons
        keepGoing = sixButtonEventHandler()
        if not keepGoing:
            break
        screen.fill(bg)
        clock.tick(fps)
        
    pygame.quit()
    if(os.name != "nt"):
        table.cleanUp()
    sys.exit
       

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

def sixButtonEventHandler():
    global currentScreen
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position

                # checks if mouse position is over the button

                if buttons[0].collidepoint(mouse_pos):
                    if(currentScreen == "main"):
                        print("Write functionality here")
                        
                    elif(currentScreen == "table"):
                        table.goUp(5)
                    
                elif buttons[1].collidepoint(mouse_pos):
                    if(currentScreen == "main"):
                        currentScreen = "table"
                    elif(currentScreen == "table"):
                        print("Write functionality here")

                    
                elif buttons[2].collidepoint(mouse_pos):
                    if(currentScreen == "main"):
                        print("Write functionality here")
                        
                    elif(currentScreen == "table"):
                        print("Write functionality here")
                    
                elif buttons[3].collidepoint(mouse_pos):
                    if(currentScreen == "main"):
                        print("Write functionality here")
                        
                    elif(currentScreen == "table"):
                        table.goDown(5)
                    
                elif buttons[4].collidepoint(mouse_pos):
                    if(currentScreen == "main"):
                        print("Write functionality here")
                    
                    elif(currentScreen == "table"):
                        print("Write functionality here")
                    
                elif buttons[5].collidepoint(mouse_pos):
                    if(currentScreen == "main"):
                        print("Write functionality here")
                        
                    elif(currentScreen == "table"):
                        currentScreen = "main"
                    
            if(event.type == pygame.KEYDOWN):
                if(event.key == K_ESCAPE):
                    return False
    return True


def button(x, y, width, height, color):

    button = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button)
    return button

def sixButtonLayout(names, myfont):
    # create and display buttons
        buttons[0] = button(width/4*1-btn_width/2, height/4,
                           btn_width, btn_height, [255, 0, 0])
        buttons[1] = button(width/4*2-btn_width/2, height/4,
                           btn_width, btn_height, [255, 0, 0])
        buttons[2] = button(width/4*3-btn_width/2, height/4,
                           btn_width, btn_height, [255, 0, 0])
        buttons[3] = button(width/4*1-btn_width/2, height/2,
                           btn_width, btn_height, [255, 0, 0])
        buttons[4] = button(width/4*2-btn_width/2, height/2,
                           btn_width, btn_height, [255, 0, 0])
        buttons[5] = button(width/4*3-btn_width/2, height/2,
                           btn_width, btn_height, [255, 0, 0])

        # display text for buttons
        text(names[0], myfont, buttons[0].center)
        text(names[1], myfont, buttons[1].center)
        text(names[2], myfont, buttons[2].center)
        text(names[3], myfont, buttons[3].center)
        text(names[4], myfont, buttons[4].center)
        text(names[5], myfont, buttons[5].center)


def text(txt, myfont, location):
    text_to_display = myfont.render(txt, 1, (255, 255, 255))
    placement = (location[0]-text_to_display.get_rect().width/2,
                 location[1]-text_to_display.get_rect().height/2)
    screen.blit(text_to_display, placement)




if __name__ == '__main__':
    main()
