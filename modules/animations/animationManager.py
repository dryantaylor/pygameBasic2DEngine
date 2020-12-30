import pygame
from typing import *

class Animation:
    def __init__(self, name: str, images: Tuple[pygame.Surface,...], timings: Tuple[float,...], does_loop: bool) -> None:
        self.name = name
        self.images = images
        self.timings = timings
        self.does_loop = does_loop


class AnimationManager:
    def __init__(self):
        self.active_animation = None
        self.frame_number = 0
        self.animations = {}
        self.time = 0.0
        self.idle_animation = None

    def add_animation(self, name: str, images: Tuple[pygame.Surface], timings: Tuple[float,...], does_loop: bool = True) -> None:
        self.animations[name] = Animation(name, images, timings, does_loop)

    def add_animation_from_file(self,name: str, fileLoc: str):
        with open(fileLoc,"r") as file:
            data = file.read().split("\n")
            does_loop = bool(data[0])
            mode = int(data[1])
            num_images = int(data[2])
            images = data[3:3+num_images]
            if mode == 0:
                images = [pygame.image.load(image) for image in images]
                timings = [float(timing) for timing in data[3 + num_images: 3 + 2 * num_images]]

            elif mode == 1:
                sizes = data[3+num_images : 3 + 2 * num_images]
                images = images #work stuff out here
                timings = data[3 + 2* num_images : 3 + 3 * num_images]
            self.add_animation(name,images,timings,does_loop)

    def set_idle_animation(self, name: str) -> bool:
        self.idle_animation = self.animations.get(name)
        if self.idle_animation is None:
            return False  # return true if animation name doesn't exist
        return True

    def set_active_animation(self, anim_name: str) -> bool:

        anim = self.animations.get(anim_name)
        if anim is not None:
            self.active_animation = anim
            self.time = 0.0
            self.frame_number = 0
            return True
        return False  # returns false if animation can't be found
    
    def get_frame(self, delta_time: float) -> pygame.Surface:
        self.time += delta_time
        while True:  #  in case the remaining time is greater than how long that frame lasts, when changing frame, so loop until time is less than the current frames time
            if self.time > self.active_animation.timings[self.frame_number]:
                """ WORK OUT NEXT FRAME"""
                #  if not at last from currently
                if self.frame_number + 1 < len(self.active_animation.images): #  len returns the number of items, so the max will be len - 1
                    self.time -= self.active_animation.timings[self.frame_number]
                    self.frame_number += 1
                else:  #  if on last frame currently
                    if self.active_animation.does_loop:  #  if it loops go back to frame[0]
                        self.time -= self.active_animation.timings[self.frame_number]
                        self.frame_number = 0
                    else:  #  if not go to idle animation
                        self.time -= self.active_animation.timings[self.frame_number]
                        self.frame_number = 0
                        self.active_animation = self.idle_animation
            else:
                return self.active_animation.images[self.frame_number]
