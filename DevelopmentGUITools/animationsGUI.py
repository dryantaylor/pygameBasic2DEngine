import modules.animations.animationManager as animationManager
import pygame
from pygame.locals import *
from PIL import Image, ImageTk
import tkinter as Tkinter   

import os
os.chdir("\\".join(os.getcwd().split("\\")[:-1]))

pygame.display.init()
window = pygame.Surface((1000, 800))
animation_manager = animationManager.AnimationManager()
timing = 1/8

""" ADD ANIMATIONS"""
images = [pygame.image.load("./assets/character/idle/00.png"),
          pygame.image.load("./assets/character/idle/01.png"),
          pygame.image.load("./assets/character/idle/02.png"),
          pygame.image.load("./assets/character/idle/03.png")]
for i, image in enumerate(images):
    images[i] = pygame.transform.scale(image, (500, 370))
animation_manager.add_animation("idle", images, (timing, timing, timing, timing), does_loop= True)

"""NECESSARY --- SET IDLE AND ACTIVE ANIMATION"""
animation_manager.set_idle_animation("idle")  #IDLE - should be looping
animation_manager.set_active_animation("idle")

mode = "RGBA"

# export as string / import to PIL
image_str = pygame.image.tostring(window, mode)         # use 'RGB' to export
size      = window.get_size()
image     = Image.frombuffer(mode, size, image_str, 'raw', mode, 0, 1) # use 'RGB' to import

# create Tk window/widgets
root      = Tkinter.Tk()
tkimage   = ImageTk.PhotoImage(image) # use ImageTk.PhotoImage class instead
label     = Tkinter.Label(root, image=tkimage)
label.pack()

clock = pygame.time.Clock()
#display = pygame.display.set_mode((1280,720))
while True:
    deltaTime = clock.tick()  # deltaTime is in MilliSeconds
    if deltaTime > 0:
        deltaTime /= 1000  # ms to seconds
    else:
        deltaTime = 0.0005  # half an ms
    window.fill((128,128,128))
    window.blit(animation_manager.get_frame(deltaTime), (100, 100))

    #display.blit(window,(0,0))
    #pygame.display.flip()
    image_str = pygame.image.tostring(window, mode)  # use 'RGB' to export
    image = Image.frombuffer(mode, size, image_str, 'raw', mode, 0, 1)  # use 'RGB' to import
    tkimage = ImageTk.PhotoImage(image)  # use ImageTk.PhotoImage class instead
    label.configure(image=tkimage)
    label.image = tkimage
    label.update()
    root.update()

