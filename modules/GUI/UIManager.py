import pygame
from typing import *
from math import floor


class GUIManager:
    def __init__(self, display_window: pygame.Surface, UI_canvas_size: (int,int)):
        self._listening_for = {} # event_type : [element]
        self._elements = {}
        self._animating = []
        self.display_window = display_window
        self.UI_canvas_size = UI_canvas_size

    def update_at_event(self,event: pygame.event) -> None:
        for element,listens_for in self._listening_for.items():
            if event.type in listens_for:
                element.update_at_event(event)

    def update_animations(self, deltaTime: float) -> None:
        for element in self._animating:
            element.update_animations(deltaTime)

    def draw(self) -> None:
        for element in self._elements.values():
            element.draw()

    def get_state_of_element(self,name: str):
        if name in self._elements.keys():
            return self._elements[name].get_state()
        else:
            return None


    def get_type_of_element(self,name:str):
        if name in self._elements.keys():
            return type(self._elements[name])
        else:
            return None

    def add_element(self, element_type, name:str, *args) -> None:
        if name in self._elements.keys():
            raise NameError(f"gui manager already has element named {name} of type {self.get_type_of_element(name)}")

        args = list(args)
        args.insert(0,self)
        args.insert(1,name)
        self._elements[name] = element_type(*args)

    def scale(self,new_res) -> None:
        old_size = self.UI_canvas_size
        self.UI_canvas_size = new_res
        scale_multiplier = width if (width := new_res[0]/old_size[0]) < (height := new_res[1]/old_size[1]) else height
        for element in self._elements.values():
            element.scale(scale_multiplier)

"""     
IMPORTANT ALL CHILD ELEMENTS MUST HAVE THE ORDER OF (parent_Manager,name, all other arguments)
"""
class Element:
    def __init__(self,parent_Manager: GUIManager,name: str,pos: Tuple[int,int],interact_rect: pygame.Rect):
        self.parent_Manager = parent_Manager
        self.name = name
        self.pos = pos
        self.interact_rect = interact_rect

    def point_collides(self,point_pos: (int,int)) -> bool:
        return bool(self.interact_rect.collidepoint(point_pos[0],point_pos[1]))

    def update_at_event(self,event: pygame.event) -> None:
        pass

    def update_animations(self, deltaTime: float) -> None:
        pass

    def draw(self,display_window: pygame.Surface,) -> None:
        pass

    def get_state(self):
        pass

    def scale(self, scale_multiplier: float) -> None: #TODO: write Scaling Code
        pass

class Button(Element):
    def __init__(self,parent_Manager: GUIManager, name: str, pos: Tuple[int,int],interact_rect: pygame.Rect,on_click: Callable, unpressed_image: pygame.Surface, pressed_image: pygame.Surface):
        super().__init__(parent_Manager,name,pos,interact_rect)
        parent_Manager._listening_for[self] = (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP)
        self.on_click = on_click
        self.unpressed_image = unpressed_image
        self.pressed_image = pressed_image

        self.is_pressed_down = False

    def update_at_event(self, event: pygame.event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and not self.is_pressed_down and self.point_collides(event.pos):
            self.is_pressed_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.point_collides(event.pos) and self.is_pressed_down:
                self.on_click[0](*self.on_click[1])
            self.is_pressed_down = False

    def draw(self) -> None:
        if self.is_pressed_down:
            img = self.pressed_image
        else:
            img = self.unpressed_image
        self.parent_Manager.display_window.blit(img,self.pos)

    def get_state(self) -> bool:
        return self.is_pressed_down

    def scale(self,scale_multiplier : float) -> None: #TODO: This doesn't really work
        self.pos = (round(self.pos[0] * scale_multiplier) , round(self.pos[1] * scale_multiplier))
        self.unpressed_image = pygame.transform.scale(self.unpressed_image,[round(n * scale_multiplier) for n in self.unpressed_image.get_size()])
        self.pressed_image = pygame.transform.scale(self.pressed_image,[round(n * scale_multiplier) for n in self.pressed_image.get_size()])
        self.interact_rect = pygame.Rect(self.pos,self.unpressed_image.get_size())

    
class Slider(Element):
    def __init__(self, parent_Manager: GUIManager, name: str,pos: Tuple[int,int], bg_image: pygame.Surface,
                 slider_image: pygame.Surface, direction: int):
        super().__init__(parent_Manager, name, pos, bg_image.get_rect())
        parent_Manager._listening_for[self] = (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP)
        self.bg_image = bg_image
        self.slider_image = slider_image
        self.direction = direction
        self.is_pressed = False

        if self.direction == Directions.LEFTtoRIGHT:  #take only the x co-ord, min is left, max is right
            self.max_pos = pos[0] + self.bg_image.get_width() - self.slider_image.get_width()
            self.min_pos = pos[0]
            self.slider_rect = slider_image.get_rect().move(self.min_pos,pos[1])
            self.bg_bounds = (pos[1],pos[1] + slider_image.get_height())
        elif self.direction == Directions.RIGHTtoLEFT:
            self.max_pos = pos[0]
            self.min_pos = pos[0] + self.bg_image.get_width() - self.slider_image.get_width()
            self.slider_rect = slider_image.get_rect().move(self.min_pos, pos[1])
            self.bg_bounds = (pos[1], pos[1] + slider_image.get_height())
        elif self.direction == Directions.BOTTOMtoTOP:
            self.max_pos = pos[1]
            self.min_pos = pos[1] + self.bg_image.get_height() - self.slider_image.get_height()
            self.slider_rect = slider_image.get_rect().move(pos[0],self.min_pos)
            self.bg_bounds = (pos[0], pos[0] + slider_image.get_width())
        elif self.direction == Directions.TOPtoBOTTOM:
            self.max_pos = pos[1] + self.bg_image.get_height() - self.slider_image.get_height()
            self.min_pos = pos[1]
            self.slider_rect = slider_image.get_rect().move(pos[0], self.min_pos)
            self.bg_bounds = (pos[0], pos[0] + slider_image.get_width())
        else:
            raise ValueError("direction must be between 0 and 3")

        self.slider_len = self.max_pos - self.min_pos
        self.slider_pos = 0

    def draw(self) -> None:
        self.parent_Manager.display_window.blit(self.bg_image, self.pos)
        self.parent_Manager.display_window.blit(self.slider_image, (self.slider_rect[0], self.slider_rect[1]))

    def update_at_event(self,event: pygame.event) -> None:
        if event.type == pygame.MOUSEMOTION:
            if self.is_pressed:
                if self.direction == Directions.LEFTtoRIGHT:
                    if self.max_pos >= event.pos[0] >= self.min_pos:
                        self.slider_rect.x = event.pos[0]
                        self.slider_pos = self.slider_rect.x - self.min_pos
                elif self.direction == Directions.RIGHTtoLEFT:
                    if self.max_pos <= event.pos[0] <= self.min_pos:
                        self.slider_rect.x = event.pos[0]
                        self.slider_pos = self.slider_rect.x - self.min_pos
                elif self.direction == Directions.TOPtoBOTTOM:
                    if self.min_pos <= event.pos[1] <= self.max_pos:
                        self.slider_rect.y = event.pos[1]
                        self.slider_pos = self.slider_rect.y - self.min_pos
                elif self.direction == Directions.BOTTOMtoTOP:
                    if self.max_pos <= event.pos[1] <= self.min_pos:
                        self.slider_rect.y = event.pos[1]
                        self.slider_pos = self.slider_rect.y - self.min_pos


                            #If direction is horizontal check if the y is the bounds, if direction is horizontal check x is in bounds
        elif event.type == pygame.MOUSEBUTTONDOWN and ( (self.direction in (Directions.LEFTtoRIGHT, Directions.RIGHTtoLEFT) and (self.bg_bounds[0] <= event.pos[1] <= self.bg_bounds[1]) ) or
                                                        (self.direction in (Directions.TOPtoBOTTOM,Directions.BOTTOMtoTOP) and (self.bg_bounds[0] <= event.pos[0] <= self.bg_bounds[1]) ) ):

            self.is_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_pressed = False

    def get_state(self) -> float:
       return abs(round(self.slider_pos/self.slider_len, 2))


class DropDown(Element): #using the base Element class will cause issues here so code must be rewritten from scratch, Button class can be used here
    def __init__(self,parent_Manager: GUIManager, name: str, pos : Tuple[int,int], unselected_bg : pygame.Surface, selected_bg : pygame.Surface,surrounding_box : pygame.Surface,default_option : int = 0,*options):
        self._active = False #if the dropdown is showing
        self.pressed = None
        parent_Manager._listening_for[self] = (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP)
        self._selected_bg = selected_bg
        self._unselected_bg = unselected_bg
        self.surrounding_box = surrounding_box
        self._active_option = default_option
        self._options = list(options)
        self.selected_buttons = [self._selected_bg.copy() for i in range(len(options))]
        self.unselected_buttons = [self._unselected_bg.copy() for i in range(len(options))]

        self._inactive_interact_rect = pygame.Rect(pos, unselected_bg.get_size())
        self._active_interact_rect = pygame.Rect(pos, (unselected_bg.get_width(),unselected_bg.get_height() * (len(options)+1)))
        super().__init__(parent_Manager, name, pos, self._inactive_interact_rect)


        for index,option in enumerate(options):
            self.selected_buttons[index].blit(option[0],(0,0))
            self.unselected_buttons[index].blit(option[0],(0,0))
        self.surrounding_box = pygame.transform.scale(self.surrounding_box,[len(self._options) * i for i in self._unselected_bg.get_size()])

    def draw(self):
        #pygame.draw.rect(self.parent_Manager.display_window,[255,255,255],self.interact_rect)
        self.parent_Manager.display_window.blit(self.unselected_buttons[self._active_option],self.pos)
        y_step = self._unselected_bg.get_height()
        pos = list(self.pos)
        pos[1] += y_step
        if self._active:
            for index in range(len(self._options)):
                if index != self._active_option:
                    #print(index)
                    self.parent_Manager.display_window.blit(self.unselected_buttons[index], pos)
                else:
                    self.parent_Manager.display_window.blit(self.selected_buttons[index], pos)
                pos[1] += y_step

    def update_at_event(self,event: pygame.event.Event) -> None:
        if self.point_collides(event.pos):
            if self._active:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    rel_pos = (event.pos[0] - self.pos[0] , event.pos[1] - self.pos[1])
                    self.pressed = floor(rel_pos[1] / self._unselected_bg.get_height()) -1
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.pressed != None:
                        if self.pressed != -1:
                            self._active_option = self.pressed
                        self._active = False
                        self.pressed = None
                        self.interact_rect = self._inactive_interact_rect
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.pressed = -1
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.pressed == -1:
                        self._active = True
                        self.pressed = None
                        self.interact_rect = self._active_interact_rect

    def get_state(self):
        return self._options[self._active_option][1]

class ScollableDropdown(DropDown):
    pass #TODO: implement ScrollableDropdown class

class Directions:
    LEFTtoRIGHT = 0
    RIGHTtoLEFT = 1
    TOPtoBOTTOM = 2
    BOTTOMtoTOP = 3