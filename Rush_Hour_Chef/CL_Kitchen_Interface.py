import pygame
from CL_Base import Base

class Truck_Floor(Base):
    def __init__(self, window, loc, scale):
        self.surface = pygame.image.load('Rush_Hour_Chef/Assets/Truck_kitchen/Truck.png')
        super().__init__(window, loc, scale)
        self.rect.topleft = self.loc

    def handleEvent(self, event):
        return super().handleEvent(event)
    
    def draw(self):
        return super().draw()

class DashBoard(Base):
    def __init__(self, window, loc, scale):
        self.surface = pygame.image.load('Rush_Hour_Chef/Assets/Truck_kitchen/Dashboard.png')
        super().__init__(window, loc, scale)
        self.rect.topright = self.loc


    def handleEvent(self, event):
        return super().handleEvent(event)\
        
    def draw(self):
        return super().draw()

class Kitchen(Base):
    def __init__(self, window, loc, scale):
        self.surface = pygame.image.load('Rush_Hour_Chef/Assets/Truck_kitchen/kitchen.png')
        super().__init__(window, loc, scale)

    def handleEvent(self, event):
        return super().handleEvent(event)
    
    def draw(self):
        return super().draw()
    
class Grill(Base):
    def __init__(self, window, loc, scale):
        self.surface = pygame.image.load('Rush_Hour_Chef/Assets/Truck_kitchen/GrillRect.png')
        super().__init__(window, loc, scale)

    def handleEvent(self, event):
        return super().handleEvent(event)
    
    def draw(self):
        return super().draw()
    
class Timer(Base):
    def __init__(self, window, loc, scale):
        self.surface = pygame.image.load('Rush_Hour_Chef/Assets/Truck_kitchen/Timer.png')
        super().__init__(window, loc, scale)
        self.rect.topright = self.loc

    def handleEvent(self, event):
        return super().handleEvent(event)
    
    def draw(self):
        return super().draw()
    
class Customer_Sit(Base):
    def __init__(self, window, loc, scale):
        self.surface = pygame.image.load('Rush_Hour_Chef/Assets/Truck_kitchen/Sit.png')
        super().__init__(window, loc, scale)

    def handleEvent(self, event):
        return super().handleEvent(event)
    
    def draw(self):
        return super().draw()