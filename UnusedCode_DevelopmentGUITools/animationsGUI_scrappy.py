import modules.animations.animationManager as animationManager
import pygame
from pygame.locals import *
from PIL import Image, ImageTk
import tkinter as Tkinter   

import os
os.chdir("\\".join(os.getcwd().split("\\")[:-1]))

class MenuBar:
    def __init__(self):
        self.frame = Tkinter.Frame(root,bg = "black",width = 1920, height = 25)
        self.frame.pack(side = Tkinter.TOP)


class AnimationDisplay:
    def __init__(self):
        self.frame = Tkinter.Frame(TopWorkSpace,width = 1000,height = 800)
        self.frame.pack()

class FileBrowser:
    def __init__(self):
        self.frame = Tkinter.Frame(TopWorkSpace,bg = "yellow",width = 460, height = 800)
        self.frame.pack(side = Tkinter.RIGHT)

class ImagePreviewer:
    def __init__(self):
        self.frame = Tkinter.Frame(TopWorkSpace,bg = "green",width = 460,height = 800)
        self.frame.pack(side = Tkinter.LEFT)

class AnimationMaker:
    def __init__(self):
        self.frame = Tkinter.Frame(root,bg = "red",width = 1920,height = 188)
        self.frame.pack()

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
root.wm_state('zoomed')

menuBar = MenuBar()
TopWorkSpace = Tkinter.Frame(root,bg = "purple",width = 1920, height = 800)
TopWorkSpace.pack(side = Tkinter.TOP)
imagePreview = ImagePreviewer()
fileBrowser = FileBrowser()
animationDisplay = AnimationDisplay()
animationMaker = AnimationMaker()





tkimage   = ImageTk.PhotoImage(image) # use ImageTk.PhotoImage class instead
label     = Tkinter.Label(animationDisplay.frame, image=tkimage)
label.pack()

clock = pygame.time.Clock()

while True:
    deltaTime = clock.tick()  # deltaTime is in MilliSeconds
    if deltaTime > 0:
        deltaTime /= 1000  # ms to seconds
    else:
        deltaTime = 0.0005  # half an ms
    window.fill((128,128,128))
    window.blit(animation_manager.get_frame(deltaTime), (100, 100))

    image_str = pygame.image.tostring(window, mode)  # use 'RGB' to export
    image = Image.frombuffer(mode, size, image_str, 'raw', mode, 0, 1)  # use 'RGB' to import
    tkimage = ImageTk.PhotoImage(image)  # use ImageTk.PhotoImage class instead
    label.configure(image=tkimage)
    label.image = tkimage
    label.update()
    root.update()

