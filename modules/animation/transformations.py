import pygame
from typing import *
from copy import deepcopy
from math import floor
from decimal import Decimal

from modules.animation.animations import Animation, AnimationManager


class CONVERT_MODE:
    END_AT_SHORTEST = 0
    class END_AFTER_LONGEST:
        LOOP_SHORTEST = 1
        DONT_LOOP_SHORTEST = 2

class Transformation:  # frame here like with an animation refers to the effects being applied at one point in time
    def __init__(self, name: str, timings: Tuple[float, ...], transformations):
        self.name = name
        self.transformations = transformations
        self.timings = timings

    def apply_transformation(self, frame: int, target_surface: pygame.Surface):
        funcs = self.transformations[frame]
        result = target_surface
        for func, args, img_pos in funcs:
            args[img_pos] = result
            result = func(*args)
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

    def add_transformation_from_transform_object(self,name: str, obj: Transformation):
        if name not in self.transformations.keys():
            self.transformations[name] = obj
            return True
        return False

    def apply_transformation_to_frame(self, delta_time: float, image: pygame.Surface) -> pygame.Surface:
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

    def transformation_to_animation(self, transformation_name: str, apply_to,does_loop: bool = True,
                                    convert_mode = CONVERT_MODE.END_AT_SHORTEST) -> Animation:
        """

        :param transformation_name: name of the transformation to apply
        :param apply_to: either pygame.Surface or animationManager.Animation
        :param does_loop: whether the animation loops or not
        :param convert_mode: if converting with an animation file how to handle either the anim or transform ending
        earlier than the other
        :return: animation object of applied transformation
        """
        transformation = self.transformations[transformation_name]
        if type(apply_to) == pygame.Surface: #static image the transform is being applied to
            timings = transformation.timings
            images = [transformation.apply_transformation(frame, apply_to) for frame in range(0, len(timings)-1)]
            return Animation(transformation_name, images, timings, does_loop)
        elif type(apply_to) == Animation:
            """
                    CONVERT FLOATS OF THE TWO LISTS TO THE Decimal TYPE
                    THIS IS DONE TO PREVENT WEIRDNESS WHEN DOING ADDITION AND SUBTRACTION
                    ON FLOATS AS Decimal STORES THE VALUES EXACTLY
            """

            dec_tr_timings = [Decimal(str(n)) for n in transformation.timings]
            dec_anim_timings = [Decimal(str(n)) for n in apply_to.timings]

            # ------------------BEGIN MAIN PART OF THE FUNC------------------#
            elapsed_timings = [Decimal("0.0")]
            """CREATE A LIST CONTAINING ALL THE ELAPSED TIMES AT EACH FRAME CHANGE
                IN EITHER THE TRANSFORMATION OR ANIMATION"""
            elapsed_time = Decimal("0.0")
            for an_timing in dec_anim_timings:
                elapsed_time += an_timing
                elapsed_timings.append(elapsed_time)
            # time of the animation in ms
            anim_length = elapsed_time
            elapsed_time = Decimal("0.0")
            for tr_timing in dec_tr_timings:
                elapsed_time += tr_timing
                elapsed_timings.append(elapsed_time)
            trans_length = elapsed_time
            # remove duplicates by converting to a dictionary and back again
            elapsed_timings = list(dict.fromkeys(elapsed_timings))
            elapsed_timings.sort()  # order into ascending times


            # TODO: different ways of handling either the animation or transoform being longer than the other
            if convert_mode == CONVERT_MODE.END_AT_SHORTEST:
                max_time = min(anim_length,trans_length)
                elapsed_timings = [x for x in elapsed_timings if x <= max_time]

            """
                Get the frame_time from the elapsed_timings
               This can be calculated by:
               frame_time[n] = elapsed_timings[n+1] - elapsed_timings[n]
               for n is contained in N_0, n < length of elapsed_timings
               e.g:
               elapsed_timings = [0.0,0.2,0.3]
               frame_timings = []
               when n = 0:
               frame_timings[0] = 0.2 - 0.0 = 0.2
               when n = 1:
               frame_timings[1] = 0.3 - 0.2 = 0.1
            """
            dec_frame_timings = []
            for n in range(0, len(elapsed_timings) - 1):
                dec_frame_timings.append(elapsed_timings[n + 1] - elapsed_timings[n])

            float_frame_timings = [float(x) for x in dec_frame_timings]
            temp_anim_manager = AnimationManager()

            temp_apply_to = deepcopy(apply_to)

            temp_anim_manager.add_animation_from_Animation_object("i",temp_apply_to)
            temp_anim_manager.set_idle_animation("i")
            temp_trans_manager = TransformationManager()

            temp_transform = deepcopy(self.active_transformation)

            temp_trans_manager.add_transformation_from_transform_object("i",temp_transform)
            temp_trans_manager.set_active_transformation("i")
            images = tuple([temp_trans_manager.apply_transformation_to_frame(n,temp_anim_manager.get_frame(n)) for n in float_frame_timings])

            return Animation(transformation_name,images,tuple(float_frame_timings),does_loop)


class CustomTransitions:
    @staticmethod
    def tint_image(image: pygame.Surface,colour: tuple[int, int, int]) -> pygame.Surface:
        image_copy = image.copy().convert_alpha()
        image_copy.fill(colour, special_flags=pygame.BLEND_ADD)
        return image_copy


