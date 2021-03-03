import pygame
from typing import *
from copy import copy
from math import floor

from modules.animation.animations import Animation, AnimationManager

class Transformation:  # frame here like with an animation refers to the effects being applied at one point in time
    def __init__(self, name: str, timings: Tuple[float, ...], transformations):
        self.name = name
        self.transformations = transformations
        self.timings = timings

    def apply_transformation(self,frame: int, target_surface: pygame.Surface):
        #print("aaaa")
        funcs = self.transformations[frame]
        #print(target_surface)
        result = target_surface
        for func, args, img_pos in funcs:
            args[img_pos] = result
            result = func(*args)
        #print("nbbbbb")
        return result

class TransformationManager:
    def __init__(self):
        self.active_transformation = None
        self.frame_number = 0
        self.transformations = {}
        self.time = 0.0

    def add_transformation(self, name: str, timings: tuple[float, ...], *transformations: tuple[tuple[tuple[Callable, tuple, int], ...], ...]) -> bool:
        """
        :param name: name of the transformation to reference in set_active_transformation
        :param timings: amount of time in ms each transform in the series of transforms is applied for
        :param transformations: (function, variables,position of image argument when function is called)
        :return: True if successfully added, False if transformation called name already exists
        """
        if name not in self.transformations.keys():
            self.transformations[name] = Transformation(name, timings, transformations)
            return True
        return False

    def apply_transformation_to_frame(self, delta_time: int, image: pygame.Surface) -> pygame.Surface:
        if self.active_transformation is not None:
            self.time += delta_time
            while True:  # in case the remaining time is greater than how long that frame lasts, when changing frame, so loop until time is less than the current frames time
                if self.time > self.active_transformation.timings[self.frame_number]:
                    """ WORK OUT NEXT FRAME"""
                    #  if not at last from currently
                    if self.frame_number + 1 < len(self.active_transformation.transformations):  # len returns the number of items, so the max will be len - 1
                        self.time -= self.active_transformation.timings[self.frame_number]
                        self.frame_number += 1
                    else:  # if on last frame currently
                        self.time = 0.0
                        self.active_transformation = None
                        break
                else:
                    return self.active_transformation.apply_transformation(frame=self.frame_number, target_surface=image.copy())

        return image

    def set_active_transformation(self,name: str):
        self.active_transformation = self.transformations[name]
        self.frame_number = 0
        self.time = 0.0

    def transformation_to_animation(self, transformation_name: str, apply_to,does_loop: bool = True) -> Animation:
        """

        :param transformation_name: name of the transformation to apply
        :param apply_to: either pygame.Surface or animationManager.Animation
        :param does_loop: whether the animation loops or not
        :return: animation object of applied transformation
        """
        transformation = self.transformations[transformation_name]
        if type(apply_to) == pygame.Surface: #static image the transform is being applied to
            timings = transformation.timings
            images = [transformation.apply_transformation(frame, apply_to) for frame in range(0, len(timings)-1)]
            return Animation(transformation_name, images, timings, does_loop)
        elif type(apply_to) == Animation:
            """Convert timings to a form which is the total elapsed since first call"""
            elapsed_timings = [0.0]
            anim_elapsed_time = 0.0
            for frame_time in apply_to.timings:
                anim_elapsed_time += frame_time
                elapsed_timings.append(anim_elapsed_time)

            elapsed_time = 0.0
            for frame_time in transformation.timings:
                elapsed_time += frame_time
                elapsed_timings.append(elapsed_time)
            elapsed_timings.sort()

            frame_times = [0.0]
            """normally this would be i-1 but since n starts on elapsed_timing[1] and i starts on 0,
               so when n = elapsed_timings[x], i = x-1, and we want to subtract the (x-1)th value from the (x)th"""
            elapsed_timings = [x for x in elapsed_timings if x < anim_elapsed_time]
            # 100000 = 10^5 which you use to round down to 5 decimal places
            elapsed_timings[-1] = floor(elapsed_timings[-1] * 100000)/100000
            # this removes duplicate values, as dicts can't have repeated keys
            elapsed_timings = list(dict.fromkeys(elapsed_timings))
            frame_times.extend([round(n - elapsed_timings[i], 5) for i, n in enumerate(elapsed_timings[1:])])


            apply_to_copy = copy(apply_to)

            temp_transform_manager_vars = self.__dict__
            self.set_active_transformation(transformation_name)
            #self.time = 0.0
            #self.frame_number = 0

            temp_anim_mangager = AnimationManager()

            temp_anim_mangager.add_animation_from_Animation_object("t", apply_to_copy)
            temp_anim_mangager.set_active_animation("t")

            n = 0
            for x in frame_times:
                print(temp_anim_mangager.active_animation)
                print(elapsed_timings[n])
                n+=1
                self.apply_transformation_to_frame(x, temp_anim_mangager.get_frame(x))
            self.__dict__ = temp_transform_manager_vars
            #return Animation(transformation_name, frame_images, frame_times, does_loop)



class CustomTransitions:
    """TODO: maybe see if way which uses less performance, presumably creating a new copy of the surface is causing
             impact """
    @staticmethod
    def tint_image(image: pygame.Surface,colour: tuple[int, int, int]) -> pygame.Surface:
        image_copy = image.copy().convert_alpha()
        image_copy.fill(colour, special_flags=pygame.BLEND_ADD)
        return image_copy



