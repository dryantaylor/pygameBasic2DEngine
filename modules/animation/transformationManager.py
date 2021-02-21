import pygame
from typing import *


class Transformation:  # frame here like with an animation refers to the effects being applied at one point in time
    # TODO: Allow multiple effects to happen on a single transition frame
    def __init__(self, name: str, timings: Tuple[float, ...], transformations):
        self.name = name
        self.transformations = transformations
        self.timings = timings


class TransformationManager:
    def __init__(self):
        self.active_transformation = None
        self.frame_number = 0
        self.transformations = {}
        self.time = 0.0

    def add_transformation(self, name: str, timings: tuple[float, ...], *transformations: tuple[tuple[Callable, tuple, int], ...]) -> bool:
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

    # TODO: code in apply_transformation_to_frame to allow multiple effects to happen on a single transition frame
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
                    func, args, img_pos = self.active_transformation.transformations[self.frame_number]
                    args[img_pos] = image
                    return func(*args)
        return image

    def set_active_transformation(self,name: str):
        self.active_transformation = self.transformations[name]
        self.frame_number = 0
        self.time = 0.0


class CustomTransitions:
    """TODO: maybe see if way which uses less performance, presumably creating a new copy of the surface is causing
             impact """
    @staticmethod
    def tint_image(image: pygame.Surface,colour: tuple[int, int, int]) -> pygame.Surface:
        image_copy = image.copy().convert_alpha()
        image_copy.fill(colour, special_flags=pygame.BLEND_ADD)
        return image_copy
