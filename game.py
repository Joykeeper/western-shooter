import pygame
import random
import sys

from pygame.math import Vector2

from models import Cowboy
from models import SandSlime, Pehel
from models import Pistol
from models import Shotgun
from models import SMG
from models import GrenadeLauncher

from menu import Menu

from handlers import EnemyHandler
from handlers import CowboyHandler
from handlers import PowerUpHandler
from handlers import DifficultyHandler
from handlers import ScoreHandler
from handlers import ShopHandler


from utils import *

WIDTH = 1024
HEIGHT = 625
HEIGHT_SCREEN = 780

NUMBER_OF_ENEMIES = 2

FPS = 60

class WesternShooter:
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT_SCREEN))
        self.background = load_sprite("sand", 1, False)
        self.gui = load_sprite("gui", 1)
        self.clock = pygame.time.Clock()

        #GUI
        self.score_pos = Vector2((WIDTH//2)-32,0)

        self.health_name_pos = Vector2(245, 650)
        self.health_pos = Vector2(225, 715)

        self.ammo_name_pos = Vector2(750, 650)
        self.ammo_pos = (750, 710)

        self.player_skin_pos = Vector2(50, 655)
        self.weapon_sign_pos = Vector2(910, 650)
        self.reloading_sign_pos = Vector2(890, 700)

        #pause and menu settings
        self.menu = Menu(WIDTH, HEIGHT_SCREEN)
        self.game_started = False
        self.game_ended = False
        self.shop_entered = False
        self.paused = False


        #mouse_pointer_skin
        pygame.mouse.set_visible(False)

        #gameobjects
        self.gameobjects = []

        for wkey, wvalue in self.menu.shop_handler.weapons_cells.items():
            for skey, svalue in self.menu.shop_handler.skins_cells.items():
                if wvalue == 'equipped' and svalue == 'equipped':
                    self.cowboy = Cowboy(position=(400, 300), velocity=Vector2(0, 0), speed=6, health=20,
                                     gun=self.menu.shop_handler.weapon_cell_item[wkey]((400, 300)), skin=self.menu.shop_handler.skin_cell_item[skey])
                    break

        #inputcheck
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        #shooting
        self.shooting = False

        #handlers
        self.enemy_handler = EnemyHandler()
        self.cowboy_handler = CowboyHandler(self.cowboy)
        self.powerup_handler = PowerUpHandler()
        self.difficulty_handler = DifficultyHandler()
        self.score_handler = ScoreHandler()



    def main_loop(self):
        self.StartMenu()
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Western Shooter")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.bg = self.screen.copy()
                    self.Pause()
                if event.key == pygame.K_r:
                    self.cowboy.reloading = True
                if event.key == pygame.K_a:
                    self.left_pressed = True
                if event.key == pygame.K_d:
                    self.right_pressed = True
                if event.key == pygame.K_w:
                    self.up_pressed = True
                if event.key == pygame.K_s:
                    self.down_pressed = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.left_pressed = False
                if event.key == pygame.K_d:
                    self.right_pressed = False
                if event.key == pygame.K_w:
                    self.up_pressed = False
                if event.key == pygame.K_s:
                    self.down_pressed = False
            #shootinput
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.shooting = True
            if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.shooting = False
        if self.shooting:
            self.cowboy.Shoot()

    def _process_game_logic(self):
        #Handlers

        self.enemy_handler.update(WIDTH, HEIGHT, self.cowboy, self.difficulty_handler.level, self.score_handler)

        self.cowboy_handler.update(self.enemy_handler.enemies, WIDTH, HEIGHT, self.right_pressed, self.left_pressed,
                                   self.up_pressed, self.down_pressed)

        self.powerup_handler.update(WIDTH, HEIGHT, self.cowboy, self.difficulty_handler.level)

        self.difficulty_handler.update(self.score_handler.score)

        self.score_handler.update()

        self.GameObjectsUpdate()

        if self.cowboy_handler.cowboy.dead:
            self._draw()
            self.bg = self.screen.copy()
            self.ShowEndResult()

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.gui, (0, 625))
        for obj in self.gameobjects:
            obj.draw(self.screen)
        self.ShowGUI()
        pygame.display.flip()
        self.clock.tick(FPS)

    def GameObjectsUpdate(self):
        self.gameobjects = self.cowboy.gun.bullets + self.enemy_handler.enemies + self.powerup_handler.powerups + \
                           [self.cowboy] + [self.cowboy.gun] + self.enemy_handler.bullets


    def StartMenu(self):
        while self.game_started == False:
            mouse_pos = pygame.mouse.get_pos()
            self.menu.show_start_menu(self.screen)
            self.ShowMousePointer()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = False
                if event.type == pygame.MOUSEMOTION:
                    for button in self.menu.start_menu_buttons:
                        if button.isOver(mouse_pos):
                            button.is_over = True
                        elif button.isOver(mouse_pos) == False:
                            button.is_over = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.menu.start_menu_buttons[0].isOver(mouse_pos):
                        for button in self.menu.start_menu_buttons:
                            button.is_over = False
                        self.game_started = True
                    elif event.button == 1 and self.menu.start_menu_buttons[1].isOver(mouse_pos):
                        for button in self.menu.start_menu_buttons:
                            button.is_over = False
                        self.ShowControls()
                    elif event.button == 1 and self.menu.start_menu_buttons[2].isOver(mouse_pos):
                        for button in self.menu.start_menu_buttons:
                            button.is_over = False
                        self.ShowCredits()
            pygame.display.flip()
            self.clock.tick(FPS)

    def ShowControls(self):
        showing_controls = True
        while showing_controls:
            mouse_pos = pygame.mouse.get_pos()
            self.menu.show_controls(self.screen)
            self.ShowMousePointer()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = False
                if event.type == pygame.MOUSEMOTION:
                    for button in self.menu.controls_buttons:
                        if button.isOver(mouse_pos):
                            button.is_over = True
                        elif button.isOver(mouse_pos) == False:
                            button.is_over = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.menu.controls_buttons[0].isOver(mouse_pos):
                        for button in self.menu.controls_buttons:
                            button.is_over = False
                        showing_controls = False
            pygame.display.flip()
            self.clock.tick(FPS)

    def ShowCredits(self):
        showing_credits = True
        while showing_credits:
            mouse_pos = pygame.mouse.get_pos()
            self.menu.show_credits(self.screen)
            self.ShowMousePointer()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = False
                if event.type == pygame.MOUSEMOTION:
                    for button in self.menu.credits_buttons:
                        if button.isOver(mouse_pos):
                            button.is_over = True
                        elif button.isOver(mouse_pos) == False:
                            button.is_over = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.menu.controls_buttons[0].isOver(mouse_pos):
                        for button in self.menu.credits_buttons:
                            button.is_over = False
                        showing_credits = False
            pygame.display.flip()
            self.clock.tick(FPS)

    def ShowEndResult(self):
        self.game_ended = True
        while self.game_ended == True:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(self.bg, (0, 0))
            self.menu.show_end_result(self.screen, self.score_handler.enemies_killed, self.score_handler.score, WIDTH, HEIGHT)
            self.ShowMousePointer()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    quit()
                if event.type == pygame.MOUSEMOTION:
                    for button in self.menu.end_result_buttons:
                        if button.isOver(mouse_pos):
                            button.is_over = True
                        elif button.isOver(mouse_pos) == False:
                            button.is_over = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.menu.enter_the_shop_button.isOver(mouse_pos):
                        self.game_ended = False
                        self.cowboy_handler.cowboy.money += self.score_handler.score
                        self.menu.enter_the_shop_button.is_over = False
                        self.EnterTheShop()
            pygame.display.flip()
            self.clock.tick(FPS)

    def EnterTheShop(self):
        self.shop_entered = True
        slot = 'weapons'
        while self.shop_entered:
            mouse_pos = pygame.mouse.get_pos()
            self.menu.open_shop(self.screen, self.cowboy_handler.cowboy.money, slot)
            self.ShowMousePointer()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    quit()
                if event.type == pygame.MOUSEMOTION:
                    for button in self.menu.shop_scene_buttons:
                        if button.isOver(mouse_pos):
                            button.is_over = True
                        elif button.isOver(mouse_pos) == False:
                            button.is_over = False
                    if slot == 'weapons':
                        for button in self.menu.weapons_cells:
                            if button.isOver(mouse_pos):
                                button.is_over = True
                                for cell in self.menu.weapons_cells:
                                    if cell.button_active.isOver(mouse_pos):
                                        cell.button_active.is_over = True
                                    elif cell.button_active.isOver(mouse_pos) == False:
                                        cell.button_active.is_over = False
                            elif button.isOver(mouse_pos) == False:
                                button.is_over = False
                    elif slot == 'skins':
                        for button in self.menu.skins_cells:
                            if button.isOver(mouse_pos):
                                button.is_over = True
                                for cell in self.menu.skins_cells:
                                    if cell.button_active.isOver(mouse_pos):
                                        cell.button_active.is_over = True
                                    elif cell.button_active.isOver(mouse_pos) == False:
                                        cell.button_active.is_over = False
                            elif button.isOver(mouse_pos) == False:
                                button.is_over = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.menu.weapons_button.isOver(mouse_pos):
                            slot = 'weapons'
                        elif self.menu.skins_button.isOver(mouse_pos):
                            slot = 'skins'
                        elif self.menu.embark_button.isOver(mouse_pos):
                            if 'equipped' in self.menu.shop_handler.weapons_cells.values():
                                self.shop_entered = False
                                self.menu.embark_button.is_over = False
                                self.RestartGame()
                            else:
                                self.bg = self.screen.copy()
                                self.menu.embark_button.is_over = False
                                self.ShowMessage(load_sprite('message/choose_weapon', 1))

                        if slot == 'weapons':
                            for cell in self.menu.weapons_cells:
                                if cell.button_active.isOver(mouse_pos):
                                    if cell.state == 'equipped':
                                        self.menu.shop_handler.update(slot, self.menu.weapons_cells.index(cell)+1, 'unequipped')
                                    elif cell.state == 'not_purchased':
                                        if self.cowboy_handler.cowboy.money >= cell.price:
                                            self.cowboy_handler.cowboy.money -= cell.price
                                            self.menu.shop_handler.update(slot, self.menu.weapons_cells.index(cell) + 1,
                                                                          'unequipped')
                                    elif cell.state == 'unequipped':
                                        i = 0
                                        for value in self.menu.shop_handler.weapons_cells.values():
                                            i += 1
                                            if value == 'equipped':
                                                self.menu.shop_handler.weapons_cells[i] = 'unequipped'
                                        self.menu.shop_handler.update(slot, self.menu.weapons_cells.index(cell)+1, 'equipped')
                                        self.cowboy.gun = self.menu.shop_handler.weapon_cell_item[self.menu.weapons_cells.index(cell)+1](self.cowboy.position)
                        elif slot == 'skins':
                            for cell in self.menu.skins_cells:
                                if cell.button_active.isOver(mouse_pos):
                                    if cell.state == 'equipped':
                                        self.menu.shop_handler.update(slot, self.menu.skins_cells.index(cell)+1, 'unequipped')
                                    elif cell.state == 'not_purchased':
                                        if self.cowboy_handler.cowboy.money >= cell.price:
                                            self.cowboy_handler.cowboy.money -= cell.price
                                            self.menu.shop_handler.update(slot, self.menu.skins_cells.index(cell) + 1,
                                                                          'unequipped')
                                    elif cell.state == 'unequipped':
                                        i = 0
                                        for value in self.menu.shop_handler.skins_cells.values():
                                            i += 1
                                            if value == 'equipped':
                                                self.menu.shop_handler.skins_cells[i] = 'unequipped'
                                        self.menu.shop_handler.update(slot, self.menu.skins_cells.index(cell)+1, 'equipped')
                                        self.cowboy.skin = self.menu.shop_handler.skin_cell_item[self.menu.skins_cells.index(cell)+1]

            pygame.display.flip()
            self.clock.tick(FPS)

    def ShowMessage(self, message):
        self.showing_message = True
        while self.showing_message:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(self.bg, (0, 0))
            self.menu.show_message(self.screen, message)
            self.ShowMousePointer()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    quit()
                if event.type == pygame.MOUSEMOTION:
                    for button in self.menu.message_buttons:
                        if button.isOver(mouse_pos):
                            button.is_over = True
                        elif button.isOver(mouse_pos) == False:
                            button.is_over = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.menu.okay_button.isOver(mouse_pos):
                            self.showing_message = False
            pygame.display.flip()
            self.clock.tick(FPS)

    def RestartGame(self):
        self.enemy_handler.reset_enemies()
        self.cowboy_handler.reset_cowboy(Vector2(400, 300))
        self.score_handler.reset_score()
        self.powerup_handler.reset_powerups()
        self.ResetMoveInput()
        self.difficulty_handler.reset_difficulty()

    def Pause(self):
        self.paused = True
        self.ResetMoveInput()

        while self.paused:
            # draw
            mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(self.bg, (0, 0))
            self.menu.show_start_menu(self.screen)
            self.ShowMousePointer()
            #handle_input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = False
                if event.type == pygame.MOUSEMOTION:
                    for button in self.menu.start_menu_buttons:
                        if button.isOver(mouse_pos):
                            button.is_over = True
                        elif button.isOver(mouse_pos) == False:
                            button.is_over = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.menu.start_menu_buttons[0].isOver(mouse_pos):
                        for button in self.menu.start_menu_buttons:
                            button.is_over = False
                        self.paused = False
                    elif event.button == 1 and self.menu.start_menu_buttons[1].isOver(mouse_pos):
                        for button in self.menu.start_menu_buttons:
                            button.is_over = False
                        self.ShowControls()
                    elif event.button == 1 and self.menu.start_menu_buttons[2].isOver(mouse_pos):
                        for button in self.menu.start_menu_buttons:
                            button.is_over = False
                        self.ShowCredits()
            pygame.display.flip()
            self.clock.tick(FPS)

    def ResetMoveInput(self):
        self.right_pressed = False
        self.left_pressed = False
        self.up_pressed = False
        self.down_pressed = False

    def ShowGUI(self):
        font_other = use_font('pixelfont', 50)

        #score
        self.score_pic = use_font('pixelfont', 64).render(str(self.score_handler.score), True, (255, 255, 255))
        self.screen.blit(self.score_pic, self.score_pos)

        #health
        self.health_pic = font_other.render(str(self.cowboy.health)+'/'+str(self.cowboy.FULL_HEALTH), True, (255, 255, 255))
        self.screen.blit(self.health_pic, self.health_pos)
        self.health_name_pic = font_other.render('HP:', True, (255, 255, 255))
        self.screen.blit(self.health_name_pic, self.health_name_pos)

        #ammo
        self.ammo_pic = font_other.render(str(self.cowboy.gun.available_ammo) + '/' + str(self.cowboy.gun.ammo_capacity), True, (255, 255, 255))
        self.screen.blit(self.ammo_pic, self.ammo_pos)
        self.ammo_name_pic = font_other.render('Ammo:', True, (255, 255, 255))
        self.screen.blit(self.ammo_name_pic, self.ammo_name_pos)

        #playerskin
        self.screen.blit(pygame.transform.scale(self.cowboy.sprite, (int(self.cowboy.sprite.get_size()[0]*2.5), int(self.cowboy.sprite.get_size()[1]*2.5))), self.player_skin_pos)

        #weapon_skin
        if isinstance(self.cowboy.gun, Shotgun):
            self.screen.blit(pygame.transform.scale(self.cowboy.gun.sprite, (int(self.cowboy.gun.sprite.get_size()[0] * 2), int(self.cowboy.gun.sprite.get_size()[1] * 2.5))), Vector2(890, 695))
        elif isinstance(self.cowboy.gun, Pistol):
            self.screen.blit(pygame.transform.scale(self.cowboy.gun.sprite, (
            int(self.cowboy.gun.sprite.get_size()[0] * 2.5), int(self.cowboy.gun.sprite.get_size()[1] * 2.5))),
                             Vector2(890 + self.cowboy.gun.sprite.get_size()[0] * 2.5//2, 695))
        elif isinstance(self.cowboy.gun, SMG):
            self.screen.blit(pygame.transform.scale(self.cowboy.gun.sprite, (
            int(self.cowboy.gun.sprite.get_size()[0] * 3), int(self.cowboy.gun.sprite.get_size()[1] * 3))),
                             Vector2(890 + self.cowboy.gun.sprite.get_size()[0]//4, 695))
        elif isinstance(self.cowboy.gun, GrenadeLauncher):
            self.screen.blit(pygame.transform.scale(self.cowboy.gun.sprite, (
            int(self.cowboy.gun.sprite.get_size()[0] * 2), int(self.cowboy.gun.sprite.get_size()[1] * 2))),
                             Vector2(877 + self.cowboy.gun.sprite.get_size()[0]//4, 695))
        #weapon sign
        self.bullet_type_sign_pic = use_font('pixelfont', 23).render('Weapon:', True, (0, 0, 0))
        self.screen.blit(self.bullet_type_sign_pic, self.weapon_sign_pos)

        #pointerskin
        self.ShowMousePointer()

        #reloading sign
        if self.cowboy.gun.reloading:
            self.reload_sign_pic = use_font('pixelfont', 30).render('RELOADING', True, (255, 255, 255))
            self.screen.blit(self.reload_sign_pic, self.reloading_sign_pos)

    def ShowMousePointer(self):
        self.screen.blit(load_sprite('pointer_skin', 1), pygame.mouse.get_pos() - Vector2(10, 10))


