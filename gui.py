import pygame
import os
        
class GUI:
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def render(self, surface):
        for element in self.elements:
            render = getattr(element, 'render', None)
            if callable(render):
                element.render(surface)

    def update(self):
        for element in self.elements:
            update = getattr(element, 'update', None)
            if callable(update):
                element.update()

    def get_event(self, event):
        for element in self.elements:
            get_event = getattr(element, 'get_event', None)
            if callable(get_event):
                element.get_event(event)        
