#!usr/bin/python3
# -*- coding: utf-8 -*-
import pygame as pg


(width, height) = (800, 800)
background_color = (110, 100, 110)
LBLUE = (100, 100, 255, 0)



pg.init()
screen = pg.display.set_mode((width, height))
pg.display.set_caption(('ClaustrOphobia'))
screen.fill(background_color)
animation_timer = pg.time.Clock()
pg.display.flip()

class ShadowBubble(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def make_shadow(self):
        shadow = pg.Surface(self.x, self.y)
        return shadow

class Bubble(object):

    def __init__(self, my_screen, R,G,B, pos_x, pos_y, radius, thickness, speed):
        self.my_screen = my_screen
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.R = R
        self.G = G
        self.B = B
        self.radius = radius
        self.thickness = thickness
        self.speed_y = speed
        self.speed_x = speed
        self.y_charge = 1
        self.x_charge = 1

    def alter_y(self, aninteger):
        if type(aninteger) != int:
            message = "alter_y(aninteger) for class Bubble: aninteger must be type int."
            raise TypeError(message)
        else:
            charge = self.y_charge
            self.pos_y += (aninteger * charge)

    def alter_x(self, aninteger):
        if type(aninteger) != int:
            message = "alter_x(aninteger) for class Bubble: aninteger must be type int."
            raise TypeError(message)
        else:
            charge = self.x_charge
            self.pos_x += (aninteger * charge)


    def move_bubble(self):
        dark = (self.R - 5, self.G - 5, self.B - 5)
        light = (self.R + 5, self.G + 5, self.B + 5)
        shine = (self.R + 5, self.G + 5, self.B + 10)
        color = (self.R, self.G, self.B)

        pg.draw.circle(screen, (dark), (self.pos_x + 10, self.pos_y + 10), self.radius, self.thickness)
        pg.draw.circle(screen, (color), (self.pos_x, self.pos_y), self.radius, self.thickness)
        pg.draw.circle(screen, (light), (self.pos_x, self.pos_y -2), self.radius - 5, self.thickness)
        pg.draw.circle(screen, (shine), (self.pos_x - 5, self.pos_y -1), self.radius//2, self.thickness)

        self.pos_x += self.speed_x
        self.pos_y += self.speed_y

    def bubble_collide(self):
        smallest = height
        if height < width:
            smallest = width
        max_rad = smallest // 40
        rad_change = smallest // 100
        diff_x = self.radius * self.x_charge
        diff_y = self.radius * self.y_charge
        if self.pos_x + diff_x >= width or self.pos_x + diff_x <= 0:
            #print("bubble collide on x")
            self.speed_x = self.speed_x * -1
            self.x_charge = self.x_charge * -1
            if self.radius < height//4 or self.radius < width//4:
                self.radius += rad_change
            else:
                self.radius = max_rad
            return True


        if self.pos_y + diff_y >= height or self.pos_y + diff_y <= 0:
            #print("bubble collide on y")
            self.speed_y = self.speed_y * -1
            self.y_charge = self.y_charge * -1
            if self.radius < height//3 or self.radius < width//3:
                self.radius += 10
            else:
                self.radius = 50
            return True

        return False



    def bubble_stick(self):
        pass




def new_bubble(x_pos, y_pos, radius):
    change_x = 1 * radius
    change_y = 1 * radius
    # leave wiggle room for shading effect when bubble is created
    # max of a (R, G, B) attribute is 255
    x = 90
    y = 90
    z = 90
    base_clr = 0
    place = radius * 2

    if x_pos - place <= 0:
        x += 50
    elif x_pos + place >= width:
        change_x = change_x * -1
    else:
        y += 20
    if y_pos + place >= height:
        change_y = change_y * -1
    elif y_pos - place <= 0:
        z += 50
    else:
        y += 20




    newx = x_pos + change_x
    newy = y_pos + change_y
    R = base_clr + x
    G = base_clr + y
    B = base_clr + z

    color = (base_clr + x, base_clr + y,  base_clr + z)
    new_bubble = Bubble(screen, R,G,B, newx, newy, 50, 0, 3)
    return new_bubble



running = True

#Light Blue tuple:
red = 100
green = 100
blue = 230
bubble = Bubble(screen, red, green, blue, 20, 20, 50, 0, 10)
alist = [bubble]

while running:
    animation_timer.tick(10)
    screen.fill(background_color)
    #shadow = pg.Surface(800, 800)
    #pg.Surface.blit(shadow, screen, BLEND_RGB)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    add_bubble = False
    for bubbles in alist:
        bubbles.move_bubble()
        if bubbles == bubble:
            if bubble.bubble_collide():
                print("creating new bubble --> collision")
                newbubble = new_bubble(bubbles.pos_x, bubbles.pos_y, bubbles.radius)
                newbubble.x_charge = bubble.x_charge
                newbubble.y_charge = bubble.y_charge
                newbubble.speed_x = bubble.x_charge * newbubble.speed_x
                newbubble.speed_y = bubble.y_charge * newbubble.speed_y
                if len(alist) % 2:
                    newbubble.alter_x(2)
                else:
                    newbubble.alter_y(2)
                add_bubble = True

        else:
            if bubbles.bubble_collide():
                print("newbubble collide")

    if add_bubble:
        alist.append(newbubble)
        print("alist size =============", len(alist))
    if len(alist) > 200:
        #https://stackoverflow.com/questions/850795/different-ways-of-clearing-lists
        # checking if del alist[:]
        # is a safer way to keep memory build up
        # python garbage collects, but I don't trust it
        # memory usage seems very slim... trying bigger list of bubbles
        del alist[:]
        #print("**********deleting alist[:]**********")
        alist = [bubble]



    pg.display.update()
