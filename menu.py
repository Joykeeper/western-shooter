import pygame

from utils import *

from handlers import ShopHandler

from models import Pistol
from models import Shotgun
from models import SMG
from models import GrenadeLauncher


class Menu:
    def __init__(self, sc_width, sc_height):
        self.start_menu_image = load_sprite('menu_bg', 1)
        self.controls_scene_image = load_sprite('controls_scene', 1)
        self.credits_scene_image = load_sprite('credits_scene', 1)
        self.end_result_image = load_sprite('end_result_bg', 1)
        self.shop_scene_image = load_sprite('ShopScene/shop_bg_screen', 1)
        self.message_bg = load_sprite('message/attention_bg', 1)
        self.end_menu_image = []

        self.weapons_cells = []
        self.skins_cells = []
        #start_menu_buttons
        self.play_button = button(sc_width//2 - 100, sc_height//2 - 130, 200, 60,
                                  [load_sprite('Buttons/play_button/play_button1', 1), load_sprite('Buttons/play_button/play_button2', 1)])
        self.controls_button = button(sc_width // 2 - 100, sc_height // 2 - 50, 200, 60,
                                      [load_sprite('Buttons/controls_button/controls_button1', 1), load_sprite('Buttons/controls_button/controls_button2', 1)])
        self.credits_button = button(sc_width // 2 - 100, sc_height // 2 + 30, 200, 60,
                                     [load_sprite('Buttons/credits_button/credits_button1', 1), load_sprite('Buttons/credits_button/credits_button2', 1)])

        #end_screen_buttons
        self.enter_the_shop_button = button(sc_width // 2 + 300, sc_height // 2 - 45, 163, 109,
                                     [load_sprite('Buttons/enter_the_shop_button/enter_the_shop1', 1), load_sprite('Buttons/enter_the_shop_button/enter_the_shop2', 1)])
        #shop_scene_buttons
        self.weapons_button = button(125, 167, 257, 59,
                                     [load_sprite('ShopScene/weapons_button/weapons_button1', 1), load_sprite('ShopScene/weapons_button/weapons_button2', 1)])
        self.skins_button = button(385, 167, 257, 59,
                                     [load_sprite('ShopScene/skins_button/skins_button1', 1),
                                      load_sprite('ShopScene/skins_button/skins_button2', 1)])
        self.embark_button = button(388, 660, 248, 45,
                                   [load_sprite('ShopScene/embark_button/embark1', 1),
                                    load_sprite('ShopScene/embark_button/embark2', 1)])
        #weapon_cells
        self.pistol_cell = shop_cell(140, 258, 233, 178,
                                     [load_sprite('ShopScene/weapon_cells/pistol', 1),
                                      load_sprite('ShopScene/weapon_cells/weapon_stats_cell', 1)], 'equipped', 0, Pistol)
        self.shotgun_cell = shop_cell(386, 258, 233, 178,
                                     [load_sprite('ShopScene/weapon_cells/shotgun', 1),
                                      load_sprite('ShopScene/weapon_cells/weapon_stats_cell', 1)], 'not_purchased', 50, Shotgun)
        self.smg_cell = shop_cell(630, 258, 233, 178,
                                      [load_sprite('ShopScene/weapon_cells/smg', 1),
                                       load_sprite('ShopScene/weapon_cells/weapon_stats_cell', 1)], 'not_purchased', 300, SMG)
        self.grenade_launcher_cell = shop_cell(140, 447, 233, 178,
                                  [load_sprite('ShopScene/weapon_cells/grenade_launcher', 1),
                                   load_sprite('ShopScene/weapon_cells/weapon_stats_cell', 1)], 'not_purchased', 500, GrenadeLauncher)

        self.weapons_cells = [self.pistol_cell, self.shotgun_cell, self.smg_cell, self.grenade_launcher_cell]

        #skin_cells
        self.standard_skin_cell = shop_cell(140, 258, 233, 178,
                                     [load_sprite('ShopScene/skin_cells/standard_skin', 1),
                                      load_sprite('ShopScene/shop_cell', 1)], 'equipped', 0)
        self.yellow_skin_cell = shop_cell(386, 258, 233, 178,
                                            [load_sprite('ShopScene/skin_cells/yellow_skin', 1),
                                             load_sprite('ShopScene/shop_cell', 1)], 'not_purchased', 100)
        self.summer_skin_cell = shop_cell(630, 258, 233, 178,
                                          [load_sprite('ShopScene/skin_cells/summer_skin', 1),
                                           load_sprite('ShopScene/shop_cell', 1)], 'not_purchased', 300)
        self.skins_cells = [self.standard_skin_cell, self.yellow_skin_cell, self.summer_skin_cell]

        self.shop_handler = ShopHandler()

        self.sc_width = sc_width
        self.sc_height = sc_height

        self.start_menu_buttons = [self.play_button, self.controls_button, self.credits_button]

        self.end_result_buttons = [self.enter_the_shop_button]

        self.shop_scene_buttons = [self.weapons_button, self.skins_button, self.embark_button]

        self.okay_button = button(452, 485, 120, 42,
                                  [load_sprite('message/okay_button/okay_button1', 1),
                                   load_sprite('message/okay_button/okay_button2', 1)])
        self.message_buttons = [self.okay_button]

        self.back_button = button(42, 695, 183, 64,
                                  [load_sprite('back_button/back_button1', 1),
                                   load_sprite('back_button/back_button2', 1)])
        self.controls_buttons = [self.back_button]
        self.credits_buttons = [self.back_button]

    def show_start_menu(self, surface):
        surface.blit(self.start_menu_image, (0, 0))
        for button in self.start_menu_buttons:
            button.update(surface)

    def show_end_result(self, surface, result, score, width, height):
        surface.blit(self.end_result_image, (0, 0))
        self.enter_the_shop_button.update(surface)
        r = 0
        for key, value in result.items():
            pic = load_sprite(f"Enemies/{key}/idle", 1.5)
            pic_pos = (width//2 - 148.5, height//2 - 81 + 41 * r)
            killed = use_font('pixelfont', 40).render(str(value), True, (0, 0, 0))
            killed_pos = (width//2 - 90, height//2 - 89 + 41 * r)
            total = use_font('pixelfont', 65).render(str(score), True, (255, 255, 255))
            total_pos = (width // 2 - len(str(score))*10, height // 2 + 200)
            surface.blit(pic, pic_pos)
            surface.blit(killed, killed_pos)
            surface.blit(total, total_pos)
            r += 1

    def open_shop(self, surface, cowboys_money, slot='weapons'):
        surface.blit(self.shop_scene_image, (0, 0))
        self.weapons_button.update(surface)
        self.skins_button.update(surface)
        self.embark_button.update(surface)
        money_pic = use_font('pixelfont', 60).render(str(cowboys_money), True, (255, 255, 255))
        surface.blit(money_pic, pygame.math.Vector2(843, 168)-pygame.math.Vector2(len(str(cowboys_money))*30, 0))
        if slot == 'weapons':
            i = 1
            for weapon_cell in self.weapons_cells:
                weapon_cell.update(surface, self.shop_handler.weapons_cells[i])
                i += 1
        elif slot == 'skins':
            i = 1
            for skin_cell in self.skins_cells:
                skin_cell.update(surface, self.shop_handler.skins_cells[i])
                i += 1

    def show_controls(self, surface):
        surface.blit(self.controls_scene_image, (0, 0))
        for button in self.controls_buttons:
            button.update(surface)

    def show_credits(self, surface):
        surface.blit(self.credits_scene_image, (0, 0))
        for button in self.credits_buttons:
            button.update(surface)

    def show_message(self, surface, message):
        surface.blit(self.message_bg, (0, 0))
        surface.blit(message, (0, 0))
        self.okay_button.update(surface)




class button():
    def __init__(self, x, y, width, height, sprite_pack):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprite_pack = sprite_pack

        self.sprite = sprite_pack[0]
        self.is_over = False

    def update(self, win):
        self.draw(win)
        if self.is_over:
            self.sprite = self.sprite_pack[1]
        elif self.is_over == False:
            self.sprite = self.sprite_pack[0]

    def draw(self, win):
        win.blit(self.sprite, (self.x, self.y))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

class shop_cell():
    def __init__(self, x, y, width, height, sprite_pack, state, price, item='skin'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprite_pack = sprite_pack
        self.state = state
        self.price = price
        self.item = item

        self.sprite = sprite_pack[0]
        self.is_over = False

        self.purchase_button = button(self.x + 51, self.y + 152, 122, 23,
                                     [load_sprite('ShopScene/shop_cell_buttons/purchase_button/purchase_button1', 1),
                                      load_sprite('ShopScene/shop_cell_buttons/purchase_button/purchase_button2', 1)])
        self.equip_button = button(self.x + 51, self.y + 152, 122, 23,
                                     [load_sprite('ShopScene/shop_cell_buttons/equip_button/equip_button1', 1),
                                      load_sprite('ShopScene/shop_cell_buttons/equip_button/equip_button2', 1)])
        self.unequip_button = button(self.x + 51, self.y + 152, 122, 23,
                                     [load_sprite('ShopScene/shop_cell_buttons/unequip_button/unequip_button1', 1),
                                      load_sprite('ShopScene/shop_cell_buttons/unequip_button/unequip_button2', 1)])

        self.button_active = self.unequip_button if state == 'equipped' else self.purchase_button

    def update(self, win, state):
        self.state = state
        self.draw(win)
        if self.is_over:
            if self.item != 'skin':
                dmg = use_font('pixelfont', 35).render(str(self.item.bullet_type.damage), True, (0, 0, 0))
                dmg_pos = pygame.math.Vector2(self.x, self.y) + pygame.math.Vector2(103, 8)
                win.blit(dmg, dmg_pos)
                sspd = use_font('pixelfont', 35).render(str(self.item.sspd), True, (0, 0, 0))
                sspd_pos = pygame.math.Vector2(self.x, self.y) + pygame.math.Vector2(112, 44)
                win.blit(sspd, sspd_pos)
                rld = use_font('pixelfont', 35).render(str(self.item.rld), True, (0, 0, 0))
                rld_pos = pygame.math.Vector2(self.x, self.y) + pygame.math.Vector2(95, 78)
                win.blit(rld, rld_pos)
                ammo = use_font('pixelfont', 35).render(str(self.item.ammo), True, (0, 0, 0))
                ammo_pos = pygame.math.Vector2(self.x, self.y) + pygame.math.Vector2(125, 111)
                win.blit(ammo, ammo_pos)
            self.sprite = self.sprite_pack[1]
            if state == 'not_purchased':
                self.purchase_button.update(win)
                self.button_active = self.purchase_button
            elif state == 'unequipped':
                self.equip_button.update(win)
                self.button_active = self.equip_button
            elif state == 'equipped':
                self.unequip_button.update(win)
                self.button_active = self.unequip_button
        elif self.is_over == False:
            self.sprite = self.sprite_pack[0]


    def draw(self, win):
        win.blit(self.sprite, (self.x, self.y))


    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False
