import random

from pygame.math import Vector2

from models import Enemy
from models import SandSlime
from models import Pehel
from models import Redrum

from models import Cowboy

from models import Medkit

from models import Pistol
from models import Shotgun
from models import SMG
from models import GrenadeLauncher


class Handler:
    def __init__(self):
        pass

    def update(self):
        pass

class EnemyHandler(Handler):

    def __init__(self):
        self.enemies = []
        self.bullets = []
        self.NUMBER_OF_ENEMIES = len([cls.__name__ for cls in Enemy.__subclasses__()])

    def update(self, width, height, cowboy, difficulty, score):
        self.EnemySpawn(width, height, difficulty)
        self.BulletCheck(cowboy)
        self.EnemyCheck(cowboy, score)

    def EnemySpawn(self, WIDTH, HEIGHT, difficulty):
        if len(self.enemies) <= difficulty:
            rp = random.randint(1, 4)
            enemy_num = random.randint(1, self.NUMBER_OF_ENEMIES)
            if rp == 1:
                pos = (0, random.randint(0, HEIGHT))
            elif rp == 2:
                pos = (random.randint(0, WIDTH), 0)
            elif rp == 3:
                pos = (WIDTH, random.randint(0, HEIGHT))
            elif rp == 4:
                pos = (random.randint(0, WIDTH), HEIGHT)

            if enemy_num == 1:
                enemy = SandSlime(pos)
            elif enemy_num == 2:
                enemy = Pehel(pos)
            elif enemy_num == 3:
                enemy = Redrum(pos)

            self.enemies.append(enemy)

    def EnemyCheck(self, cowboy, score):
        for enemy in self.enemies:
            if enemy.collides_with(cowboy):
                cowboy.health -= enemy.damage
                enemy.health = 0
        for enemy in self.enemies:
            if enemy.health <= 0 and enemy.collides_with(cowboy) == False:
                enemy.update()
                self.BulletCheck(cowboy)
                self.enemies.pop(self.enemies.index(enemy))
                score.AddScoreFor(enemy)
                continue
            elif enemy.health <= 0 and enemy.collides_with(cowboy):
                self.enemies.pop(self.enemies.index(enemy))
                continue
            enemy.animate()
            enemy.move(cowboy.position)

    def BulletCheck(self, cowboy):
        for enemy in self.enemies:
            self.bullets += enemy.bullets
        for bullet in self.bullets:
            if bullet.collides_with(cowboy):
                cowboy.health -= bullet.damage
                bullet.lifetime = 0
            bullet.update()
            if bullet.dead:
                self.bullets.pop(self.bullets.index(bullet))


    def reset_enemies(self):
        self.enemies = []
        self.bullets = []


class CowboyHandler(Handler):
    def __init__(self, cowboy):
        self.cowboy = cowboy

    def update(self, enemies, width, height, r_p, l_p, u_p, d_p):
        self.MoveHandle(width, height, r_p, l_p, u_p, d_p)
        self.BulletCheck(enemies)
        self.CowboyCheck()

    def BulletCheck(self, enemies):
        for bullet in self.cowboy.gun.bullets:
            for enemy in enemies:
                if bullet.collides_with(enemy):
                    enemy.health -= bullet.damage
                    bullet.lifetime = 0
            bullet.update()

    def MoveHandle(self, WIDTH, HEIGHT, r_p, l_p, u_p, d_p):
        self.cowboy.velocity.x = 0
        self.cowboy.velocity.y = 0
        if (l_p and not r_p) and self.cowboy.position.x > 0 + \
                self.cowboy.sprite.get_size()[0] // 2:
            self.cowboy.velocity.x = -1
        if (r_p and not l_p) and self.cowboy.position.x < WIDTH - \
                self.cowboy.sprite.get_size()[0] // 2:
            self.cowboy.velocity.x = 1
        if (u_p and not d_p) and self.cowboy.position.y > 0 + self.cowboy.sprite.get_size()[1] // 2:
            self.cowboy.velocity.y = -1
        if (d_p and not u_p) and self.cowboy.position.y < HEIGHT - \
                self.cowboy.sprite.get_size()[1] // 2:
            self.cowboy.velocity.y = 1
        self.cowboy.move()
        if self.cowboy.dead == False:
            self.cowboy.animate()

    def CowboyCheck(self):
        if self.cowboy.health <= 0:
            self.cowboy.health = 0
            self.cowboy.Die()

    def reset_cowboy(self, position):
        self.cowboy.health = self.cowboy.FULL_HEALTH
        self.cowboy.position = position
        self.cowboy.dead = False
        self.cowboy.gun.bullets = []
        self.cowboy.gun.available_ammo = self.cowboy.gun.ammo_capacity
        self.cowboy.PutOnClothes()


class PowerUpHandler(Handler):
    def __init__(self):
        self.NUMBER_OF_POWERUPS = 1
        self.POWERUP_SPAWN_TIME = 300
        self.may_spawn = False
        self.spawn_time = self.POWERUP_SPAWN_TIME
        self.time_count = 0
        self.powerups = []

    def update(self, width, height, cowboy, difficulty):
        self.PowerUpSpawn(width,height, difficulty)
        self.PowerUpCheck(cowboy)

    def PowerUpSpawn(self, WIDTH, HEIGHT, difficulty):
        rp = random.choice(['medkit'])
        if self.may_spawn == False:
            self.time_count += 1
            if self.time_count >= self.spawn_time:
                self.may_spawn = True
                self.time_count = 0
        elif self.may_spawn and len(self.powerups)<=3:
            power_up = 0
            if rp == 'medkit':
                power_up = Medkit(Vector2(random.randint(20, WIDTH-20), random.randint(20, HEIGHT-20)))
            self.powerups.append(power_up)
            self.may_spawn = False
        self.spawn_time = difficulty * self.POWERUP_SPAWN_TIME

    def PowerUpCheck(self, cowboy):
        for powerup in self.powerups:
            if powerup.collides_with(cowboy):
                if isinstance(powerup, Medkit) and cowboy.health < cowboy.FULL_HEALTH:
                    self.powerups.pop(self.powerups.index(powerup))
                    powerup.HealCowboy(cowboy)

    def reset_powerups(self):
        self.powerups = []
        self.may_spawn = False
        self.time_count = 0


class DifficultyHandler(Handler):
    def __init__(self):
        self.level = 1

    def update(self, score):
        self.CheckDifficulty(score)

    def CheckDifficulty(self, score):
        if 40 > score >= 20:
            self.level = 2
        elif 60 > score >= 40:
            self.level = 3
        elif 80 > score >= 60:
            self.level = 4
        elif score >= 80:
            self.level = 5

    def reset_difficulty(self):
        self.level = 1

class ScoreHandler(Handler):
    def __init__(self):
        self.point_dict = {'sandslime': 1,  'pehel': 2, 'redrum': 2}
        self.enemies_killed = {'SandSlime': 0, 'Pehel': 0, 'Redrum': 0}
        self.score = 0

    def update(self):
        pass

    def AddScoreFor(self, obj):
        if isinstance(obj, SandSlime):
            self.score += self.point_dict['sandslime']
            self.enemies_killed['SandSlime'] += 1
        elif isinstance(obj, Pehel):
            self.score += self.point_dict['pehel']
            self.enemies_killed['Pehel'] += 1
        elif isinstance(obj, Redrum):
            self.score += self.point_dict['redrum']
            self.enemies_killed['Redrum'] += 1

    def reset_score(self):
        self.score = 0
        for key in self.enemies_killed.keys():
            self.enemies_killed[key] = 0

class ShopHandler(Handler):
    def __init__(self):
        self.weapons_cells = {1: 'equipped', 2: 'not_purchased',
                              3: 'not_purchased', 4: 'not_purchased',
                              5: 'not_purchased', 6: 'not_purchased'}
        self.skins_cells = {1: 'equipped', 2: 'not_purchased',
                              3: 'not_purchased', 4: 'not_purchased',
                              5: 'not_purchased', 6: 'not_purchased'}
        self.weapon_cell_item = {1: Pistol, 2: Shotgun,
                              3: SMG, 4: GrenadeLauncher,
                              5: None, 6: None}
        self.skin_cell_item = {1: 'Standard', 2: 'Yellow',
                                 3: 'Summer', 4: None,
                                 5: None, 6: None}


    def update(self, slot, ind, val):
        if slot == 'weapons':
            self.weapons_cells.update({ind:val})
        elif slot == 'skins':
            self.skins_cells.update({ind:val})