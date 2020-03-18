import pygame as pg
from vector import Vector
from Laser import *


class Ship:
    def __init__(self, game, vector=Vector()):
        self.game = game
        self.screen = game.screen
        self.velocity = vector
        self.screen_rect = game.screen.get_rect()
        self.image = pg.image.load('ship.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.laser = pg.sprite.Group()

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom

    def fire(self):
        self.laser.add(Laser(game=self.game))

    def remove_lasers(self):
        self.laser.remove()

    def move(self):
        if self.velocity == Vector():
            return
        self.rect.left += self.velocity.x
        self.rect.top += self.velocity.y
        self.game.limit_on_screen(self.rect)

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        fleet = self.game.fleet
        self.move()
        self.draw()
        # draw laser and check if the laser is reach the screen limit
        for laser in self.laser.sprites():
            laser.update()
        for laser in self.laser.copy():
            if laser.rect.bottom <= 0:
                self.laser.remove(laser)
        aliens_hit = pg.sprite.groupcollide(fleet.aliens, self.laser, False, True)
        # check if aliens is hit and destroy aliens also display the message of aliens key
        if len(aliens_hit.key()) > 0:
            print('{} aliens hit'.format(len(aliens_hit.key())))
        for alien in aliens_hit:
            aliens_hit()
            if alien.health <= 0:
                fleet.aliens.remove(alien)
        if not fleet.aliens:
            self.game.restart()
