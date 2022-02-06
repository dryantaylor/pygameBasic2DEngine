import pygame
from typing import *
from zipfile import ZipFile
from os import listdir, unlink


class Animation:
    def __init__(self, name: str, images: Tuple[pygame.Surface, ...], timings: Tuple[float, ...], does_loop: bool) -> None:
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

    def get_Animation_object_by_name(self,name: str) -> str:
        if name in self.animations.keys():
            return self.animations[name]
        return None

    def add_animation(self, name: str, images: Tuple[pygame.Surface], timings: Tuple[float, ...], does_loop: bool = True) -> bool:
        if name not in self.animations.keys():
            self.animations[name] = Animation(name, images, timings, does_loop)
            return True
        return False

    def add_animation_from_file(self, animation_name: str, file: str, display: pygame.Surface,  res_scale: float = 1.0) -> bool:
        try:
            with ZipFile(file, "r") as zip:  # open the zip file
                zip.extractall("./temp")  # move the contents to ./temp dir
            with open("./temp/info.cfg", "r") as f:
                data = f.read()  # reading the config information, see documentation for the format of .anim files
            data = data.replace("\n", "").split(";")
            data_dict = {}
            for i in data:
                name, value = i.split("=")
                if name == 'resolution':
                    data_dict[name] = [int(i) for i in value.split(",")]
                elif name == 'timings':
                    data_dict[name] = [float(i) for i in value.split(",")]
                elif name == 'image_locs':
                    data_dict[name] = [i for i in value.split(",")]
                else:
                    data_dict[name] = bool(value)

            og_x, og_y = [i for i in data_dict['resolution']] # the resoloution values are still strings so must be made ints
            res = (int(og_x * res_scale), int(og_y * res_scale))
            img_objects = [pygame.image.load(f"./temp/{loc}").convert_alpha(display) for loc in data_dict['image_locs']]  #images are stored in /temp

            img_objects = tuple([pygame.transform.scale(img_obj,res) for img_obj in img_objects])  # scale images, convert to tuple
            return_value = self.add_animation(animation_name, img_objects, data_dict['timings'], data_dict['does_loop'])

            for file in listdir("./temp"):  # cleanup, files extracted should be deleted
                unlink("./temp/"+file)

            return return_value
        except Exception as e:
            for file in listdir("./temp"):  # this needs to be done even when exiting due to an error
                unlink("./temp/"+file)      # to prevent a leak of the files from the animation not being
            raise e                         # not being deleted (unlink is the func to delete files)

    def add_animation_from_Animation_object(self, name:str, Animation_object: Animation):
        Animation_object.name = name
        if name not in self.animations.keys():
            self.animations[name] = Animation_object
            return True
        return False

    def set_idle_animation(self, name: str) -> bool:
        temp_animation = self.animations.get(name)
        if temp_animation is None:
            return False  # return true if animation name doesn't exist
        self.idle_animation = temp_animation
        if self.active_animation == None:
            self.active_animation = self.idle_animation
        return True

    def set_active_animation(self, anim_name: str,reset_to_start:bool = True) -> bool:
        anim = self.animations.get(anim_name)
        if anim is not None:
            self.active_animation = anim
            if reset_to_start:
                self.time = 0.0
                self.frame_number = 0
            return True
        return False  # returns false if animation can't be found
    
    def get_frame(self, delta_time: float) -> pygame.Surface:
        self.time += delta_time
        while True:  # in case the remaining time is greater than how long that frame lasts, when changing frame, so loop until time is less than the current frames time
            if self.time > self.active_animation.timings[self.frame_number]:
                """ WORK OUT NEXT FRAME"""
                #  if not at last from currently
                if self.frame_number + 1 < len(self.active_animation.images): # len returns the number of items, so the max will be len - 1
                    self.time -= self.active_animation.timings[self.frame_number]
                    self.frame_number += 1
                else:  # if on last frame currently
                    if self.active_animation.does_loop:  # if it loops go back to frame[0]
                        self.time -= self.active_animation.timings[self.frame_number]
                        self.frame_number = 0
                    else:  # if not go to idle animation
                        self.time -= self.active_animation.timings[self.frame_number]
                        self.frame_number = 0
                        self.active_animation = self.idle_animation
            else:
                return self.active_animation.images[self.frame_number]

    def update_time(self, delta_time: float) -> None:
        self.time += delta_time
