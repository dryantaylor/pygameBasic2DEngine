import pygame
from typing import *


class GUIManager:
    def __init__(self, display_window: pygame.Surface, UI_canvas_size: (int,int)):
        self.listening_for = {} # event_type : [element]
        self.elements = []
        self.animating = []
        self.display_window = display_window
        self.UI_canvas_size = UI_canvas_size

    def update_at_event(self,event: pygame.event) -> None:
        for element,listens_for in self.listening_for.items():
            if event.type in listens_for:
                element.update_at_event(event)

    def update_aimations(self,deltaTime: float) -> None:
        for element in self.animating:
            element.update_animations(deltaTime)

    def draw(self):
        for element in self.elements:
            element.draw()


class Element:
    def __init__(self,parent_Manager: GUIManager,name: str,pos: Tuple[int,int],interact_rect: pygame.Rect):
        self.parent_Manager = parent_Manager
        self.name = name
        self.pos = pos
        self.interact_rect = interact_rect
        parent_Manager.listening_for[self] = (pygame.MOUSEBUTTONDOWN,pygame.MOUSEBUTTONUP)

    def point_collides(self,point_pos: (int,int)) -> bool:
        return self.interact_rect.collidepoint(point_pos[0],point_pos[1])

    def update_at_event(self,event: pygame.event) -> None:
        pass

    def update_animations(self, deltaTime: float) -> None:
        pass

    def draw(self,display_window: pygame.Surface,) -> None:
        pass


class Button(Element):
    def __init__(self,parent_Manager: GUIManager,name: str, pos: Tuple[int,int],interact_rect: pygame.Rect,on_click: Callable, unpressed_image: pygame.Surface, pressed_image: pygame.Surface):
        super().__init__(parent_Manager,name,pos,interact_rect)
        self.on_click = on_click
        self.unpressed_image = unpressed_image
        self.pressed_image = pressed_image

        self.is_pressed_down = False

    def update_at_event(self, event: pygame.event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.is_pressed_down and self.point_collides(event.pos):
            self.is_pressed_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.point_collides(event.pos):
                self.on_click[0](*self.on_click[1])
            self.is_pressed_down = False

    def draw(self):
        if self.is_pressed_down:
            img = self.pressed_image
        else:
            img = self.unpressed_image
        self.parent_Manager.display_window.blit(img,self.pos)


class Slider(Element):
    def __init__(self,parent_Manager: GUIManager,name: str,pos: Tuple[int,int],interact_rect: pygame.Rect, bg_image: pygame.Surface,
                 slider_image: pygame.Surface, direction: int, slider_rect: pygame.Rect):

        super().__init__(parent_Manager,name,pos,interact_rect)
        self.bg_image = bg_image
        self.slider_image = slider_image
        self.direction = direction
        self.slider_rect = slider_rect


        if self.direction == Directions.LEFTtoRIGHT:  #take only the x co-ord, min is left, max is right
            self.max_pos = self.pos[0] + self.bg_image.get_width() - self.slider_image.get_width()
            self.min_pos = self.pos[0]
        elif self.direction == Directions.RIGHTtoLEFT:
            self.max_pos = self.pos[0]
            self.min_pos = self.pos[0] + self.bg_image.get_width() - self.slider_image.get_width()
        elif self.direction == Directions.BOTTOMtoTOP:
            self.max_pos = self.pos[1]
            self.min_pos = self.pos[1] + self.bg_image.get_height() - self.slider_image.get_height()
        elif self.direction == Directions.TOPtoBOTTOM:
            self.max_pos = self.pos[1] + self.bg_image.get_height() - self.slider_image.get_height()
            self.min_pos = self.pos[1]

        else: raise ValueError("direction must be between 0 and 3")

    def draw(self,display_window: pygame.Surface,) -> None:
        display_window.blit(self.bg_image,self.pos)
        display_window.blit(self.slider_image, (self.slider_rect[0],self.slider_rect[1]))

class Directions:
    LEFTtoRIGHT = 0
    RIGHTtoLEFT = 1
    TOPtoBOTTOM = 2
    BOTTOMtoTOP = 3