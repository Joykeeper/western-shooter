import math
import random
from pygame.math import Vector2
from utils import load_sprite
from pygame import mouse
from pygame import transform

class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self):
        self.position = self.position + self.velocity

    def animate(self):
        pass

    def collides_with(self, other_self):
        distance = Vector2(self.position).distance_to(other_self.position)
        return distance < self.radius + other_self.radius


class Cowboy(GameObject):

    def __init__(self, position, velocity, speed, health, gun, skin):
        super().__init__(position, load_sprite("cowboy_skins/Standard/idle1", 2), velocity)
        self.velocity = velocity
        self.speed = speed
        self.health = health
        self.FULL_HEALTH = health
        self.gun = gun
        self.skin = skin

        self.dead = False

        self.money = 1000

        self.PutOnClothes()
        self.frame_count2 = 0
        self.frame_count3 = 0

    def move(self):
        if self.velocity != Vector2(0):
            self.position += self.velocity.normalize() * self.speed
        else:
            self.position += self.velocity * self.speed

        if self.health > self.FULL_HEALTH:
            self.health = self.FULL_HEALTH
        self.gun.update(self.position)
            
    def animate(self):
        if self.frame_count3 + 1 >= 15:
            self.frame_count3 = 0
        if self.frame_count2 + 1 >= 16:
            self.frame_count2 = 0

        if (self.velocity.x > 0):
            self.sprite = self.runR[self.frame_count3 // 5]
        elif (self.velocity.x < 0):
            self.sprite = self.runL[self.frame_count3 // 5]
        elif (self.velocity.y != 0)and(self.velocity.x == 0):
            self.sprite = self.runY[self.frame_count3 // 5]
        elif (self.velocity.x == 0)and(self.velocity.y == 0):
            self.sprite = self.idle[self.frame_count2 // 8]
        self.frame_count2 += 1
        self.frame_count3 += 1

    def Die(self):
        self.health = 0
        self.sprite = load_sprite(f"cowboy_skins/{self.skin}/dead",2)
        self.velocity = Vector2(0, 0)
        self.dead = True

    def Shoot(self):
        self.gun.Shoot()

    def PutOnClothes(self):
        self.runR = [load_sprite(f"cowboy_skins/{self.skin}/runr1", 2),
                     load_sprite(f"cowboy_skins/{self.skin}/runr2", 2),
                     load_sprite(f"cowboy_skins/{self.skin}/runr3", 2)]
        self.runL = [load_sprite(f"cowboy_skins/{self.skin}/runl1", 2),
                     load_sprite(f"cowboy_skins/{self.skin}/runl2", 2),
                     load_sprite(f"cowboy_skins/{self.skin}/runl3", 2)]
        self.runY = [load_sprite(f"cowboy_skins/{self.skin}/runy1", 2),
                     load_sprite(f"cowboy_skins/{self.skin}/runy2", 2),
                     load_sprite(f"cowboy_skins/{self.skin}/runy3", 2)]
        self.idle = [load_sprite(f"cowboy_skins/{self.skin}/idle1", 2),
                     load_sprite(f"cowboy_skins/{self.skin}/idle2", 2)]

class Enemy(GameObject):

    def __init__(self, position, speed, health, damage, runAnims):
        super().__init__(position, load_sprite("Enemies/SandSlime/run1",2), Vector2(0))

        self.velocity = Vector2(0)
        self.speed = speed
        self.health = health
        self.frame_count = 0
        self.runAnims = runAnims
        self.damage = damage
        self.bullets = []

    def move(self, player_pos):
        self.velocity = player_pos - self.position
        self.position += self.velocity.normalize() * self.speed
        self.update()

    def update(self):
        pass

    def animate(self):
        if self.frame_count + 1 >= 27:
            self.frame_count = 0
        self.sprite = self.runAnims[self.frame_count // 9]
        self.frame_count += 1



class Gun():
    def __init__(self, position, sprite, bullet_type, shoot_delay, reload_time, ammo_capacity, bullet_reloader, bullet_reload_time = 0):
        self.position = Vector2(position)
        self.sprite = sprite
        self.flipped_sprite = transform.flip(sprite, True, False)
        self.bullet_type = bullet_type
        self.shoot_delay = shoot_delay
        self.reload_time = reload_time
        self.ammo_capacity = ammo_capacity
        self.bullet_reloader = bullet_reloader
        self.bullet_reload_time = bullet_reload_time
        self.size = Vector2(self.sprite.get_size())

        self.bullets = []

        self.shoot_time_count = 0
        self.able_to_shoot = True
        self.reloading = False
        self.available_ammo = self.ammo_capacity

        self.flipped = False

        self.radius = sprite.get_width() / 2
        self.damage = self.bullet_type.damage

    def update(self, player_pos):
        self.rotate()
        if self.flipped:
            self.move(player_pos + Vector2(self.radius, 0))
        else:
            self.move(player_pos - Vector2(self.radius, 0))
        self.superpower()
        self.AmmoCheck()

    def Shoot(self):
        mouse_pos = mouse.get_pos()
        if self.able_to_shoot and not self.reloading:
            if self.flipped:
                self.bullets.append(self.bullet_type(self.position - Vector2(self.sprite.get_width()*1.5, self.sprite.get_height()*1.5), mouse_pos))
            else:
                self.bullets.append(self.bullet_type(self.position + Vector2(self.sprite.get_width()//2, -self.sprite.get_height()*1.5), mouse_pos))
            self.available_ammo -= 1
            self.able_to_shoot = False
            if self.available_ammo <= 0:
                self.reloading = True

    def AmmoCheck(self):
        for bullet in self.bullets:
            if bullet.dead:
                self.bullets.pop(self.bullets.index(bullet))

        if not(self.able_to_shoot) and not(self.reloading):
            self.shoot_time_count += 1
            if self.shoot_time_count >= self.shoot_delay:
                self.able_to_shoot = True
                self.shoot_time_count = 0
        if self.reloading:
            self.shoot_time_count += 1
            self.available_ammo = self.shoot_time_count//(self.reload_time//self.ammo_capacity)
            if self.shoot_time_count >= self.reload_time:
                self.reloading = False
                self.able_to_shoot = True
                self.available_ammo = self.ammo_capacity
                self.shoot_time_count = 0

    def move(self, player_pos):
        self.position = player_pos + Vector2(self.radius)

    def draw(self, surface):
        if self.flipped:
            blit_position = self.position - Vector2(self.radius) - Vector2(self.sprite.get_width(), 0)
        else:
            blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def rotate(self):
        mouse_pos = Vector2(mouse.get_pos())
        if (mouse_pos.x - self.position.x) < 0:
            self.sprite = self.flipped_sprite
            self.flipped = True
        else:
            self.sprite = transform.flip(self.flipped_sprite, True, False)
            self.flipped = False

    def superpower(self):
        pass

class Bullet(GameObject):
    def __init__(self, position, mouse_pos, sprite, lifetime, damage):
        super().__init__(position, sprite, Vector2(0))
        self.mouse_pos = Vector2(mouse_pos)
        self.sprite = sprite
        self.lifetime = lifetime
        self.damage = damage
        self.speed = 10
        self.angle = math.atan2(self.mouse_pos.y - self.position.y, self.mouse_pos.x - self.position.x)
        self.velocity = Vector2(math.cos(self.angle) * self.speed, math.sin(self.angle) * self.speed)
        self.dead = False

    def update(self):
        self.move()
        self.CheckSelf()

    def move(self):
        self.position += self.velocity

    def CheckSelf(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.dead = True

class Medkit(GameObject):
    def __init__(self, position):
        super().__init__(position, load_sprite('PowerUps/medkit',1), Vector2(0,0))
        self.position = position
        self.heal = random.randint(4,6)

    def HealCowboy(self, obj):
        if isinstance(obj, Cowboy):
            obj.health += self.heal


#Enemies
class SandSlime(Enemy):
    def __init__(self, position):
        super().__init__(position, speed = 4, health = 30, damage = 5,
                         runAnims = [load_sprite("Enemies/SandSlime/run1", 2), load_sprite("Enemies/SandSlime/run2", 2), load_sprite("Enemies/SandSlime/run3", 2)])

class Pehel(Enemy):
    def __init__(self, position):
        super().__init__(position, speed=6, health=10, damage=5,
                         runAnims=[load_sprite("Enemies/Pehel/run1", 2), load_sprite("Enemies/Pehel/run2", 2), load_sprite("Enemies/Pehel/run3", 2)])

class Redrum(Enemy):
    def __init__(self, position):
        super().__init__(position, speed=5, health=10, damage=5,
                         runAnims=[load_sprite("Enemies/Redrum/run1", 2), load_sprite("Enemies/Redrum/run2", 2), load_sprite("Enemies/Redrum/run3", 2)])
        self.gun = RedrumGun(position)
    def update(self):
        self.gun.update(self.position)
        if self.health <= 0:
            self.gun.Shoot()
            self.bullets = self.gun.bullets


#Bullets
class PistolBullet(Bullet):
    damage = 10
    def __init__(self, position, mouse_pos):
        super().__init__(position, mouse_pos, sprite=load_sprite('Bullets/pistol_bullet', 2), lifetime=80, damage=10)

class ShotgunBullet(Bullet):
    damage = 30
    def __init__(self, position, mouse_pos):
        super().__init__(position, mouse_pos, sprite=load_sprite('Bullets/shotgun_bullet', 2), lifetime=30, damage=30)

class SMGBullet(Bullet):
    damage = 4
    def __init__(self, position, mouse_pos):
        super().__init__(position, mouse_pos, sprite=load_sprite('Bullets/smg_bullet', 1), lifetime=70, damage=4)

class RedrumBullet(Bullet):
    damage = 4
    def __init__(self, position, mouse_pos):
        super().__init__(position, mouse_pos, sprite=load_sprite('Bullets/smg_bullet', 2), lifetime=70, damage=4)

class Explosive(Bullet):
    damage = 15
    def __init__(self, position, mouse_pos):
        super().__init__(position, mouse_pos, sprite=load_sprite('Bullets/grenade', 1), lifetime=80, damage=15)
        self.explosion_animation = [load_sprite('Explosion/explosion_effect1', 5), load_sprite('Explosion/explosion_effect2', 5), load_sprite('Explosion/explosion_effect3', 5),
                                    load_sprite('Explosion/explosion_effect4', 5)]
        self.exploded = False
        self.frame_count = 0
        self.sprt = load_sprite('Bullets/grenade', 1)
        self.rot_ang = 0

    def update(self):
        if self.rot_ang >= 360:
            self.rot_ang = 0
        self.rot_ang += 2

        self.velocity /= 1.04
        self.damage = 0
        self.CheckSelf()
        if self.lifetime <= 0 and self.exploded == False:
            self.Explode()
        else:
            if self.dead == False:
                self.move()
                self.sprite = transform.rotate(self.sprt, self.rot_ang)
    def Explode(self):
        self.frame_count += 1
        if self.frame_count + 1 >= 16:
            self.exploded = True
        self.sprite = self.explosion_animation[self.frame_count // 4]
        if self.frame_count == 1:
            self.damage = Explosive.damage
        else:
            self.damage = 0

    def CheckSelf(self):
        self.lifetime -= 1
        if self.exploded:
            self.dead = True
        elif self.lifetime <= 0:
            self.radius = load_sprite('Explosion/explosion_effect1', 5).get_width()//2

#Guns
class Pistol(Gun):
    bullet_type = PistolBullet
    sspd = format(60/30, '.1f')
    rld = format(100/60, '.1f')
    ammo = 15
    def __init__(self, position):
        super().__init__(position, load_sprite('Guns/pistol', 0.3), bullet_type=PistolBullet, shoot_delay=30, reload_time=100, ammo_capacity=15, bullet_reloader=False)

class Shotgun(Gun):
    bullet_type = ShotgunBullet
    sspd = format(60 / 50, '.1f')
    rld = format(70 / 60, '.1f')
    ammo = 5
    def __init__(self, position):
        super().__init__(position, load_sprite('Guns/shotgun', 0.4), bullet_type=ShotgunBullet, shoot_delay=50, reload_time=70, ammo_capacity=5, bullet_reloader=False)

    def superpower(self):
        for bullet in self.bullets:
            if bullet.lifetime <= 0 and isinstance(bullet, ShotgunBullet):
                dir = Vector2(0, -1)
                for i in range(4):
                    #angle = 72 * i
                    #dir = Vector2(dir.x * math.cos(angle) - dir.y * math.sin(angle), dir.x * math.sin(angle) + dir.y * math.cos(angle))
                    #self.bullets.append(PistolBullet(bullet.position, bullet.position+dir))
                    if i == 0:
                        self.bullets.append(PistolBullet(bullet.position, bullet.position + (0, -1)))
                    elif i == 1:
                        self.bullets.append(PistolBullet(bullet.position, bullet.position + (-1, 0)))
                    elif i == 2:
                        self.bullets.append(PistolBullet(bullet.position, bullet.position + (0, 1)))
                    elif i == 3:
                        self.bullets.append(PistolBullet(bullet.position, bullet.position + (1, 0)))

class SMG(Gun):
    bullet_type = SMGBullet
    sspd = format(60 / 5, '.1f')
    rld = format(70 / 60, '.1f')
    ammo = 30
    def __init__(self, position):
        super().__init__(position, transform.flip(load_sprite('Guns/smg', 0.2), True, False), bullet_type=SMGBullet, shoot_delay=5, reload_time=70, ammo_capacity=30, bullet_reloader=False)
    def Shoot(self):
        mouse_pos = mouse.get_pos()
        if self.able_to_shoot and not self.reloading:
            if self.flipped:
                self.bullets.append(self.bullet_type(self.position - Vector2(self.sprite.get_width()*1.5, self.sprite.get_height()), mouse_pos))
            else:
                self.bullets.append(self.bullet_type(self.position + Vector2(self.sprite.get_width()//2, -self.sprite.get_height()), mouse_pos))
            self.available_ammo -= 1
            self.able_to_shoot = False
            if self.available_ammo <= 0:
                self.reloading = True

class GrenadeLauncher(Gun):
    bullet_type = Explosive
    sspd = format(60 / 70, '.1f')
    rld = format(150 / 60, '.1f')
    ammo = 8
    def __init__(self, position):
        super().__init__(position, load_sprite('Guns/grenade_launcher', 0.8), bullet_type=Explosive,
                         shoot_delay=70, reload_time=150, ammo_capacity=8, bullet_reloader=False)

    def Shoot(self):
        mouse_pos = mouse.get_pos()
        if self.able_to_shoot and not self.reloading:
            if self.flipped:
                self.bullets.append(self.bullet_type(
                    self.position - Vector2(self.sprite.get_width() * 1.5, self.sprite.get_height() * 1.5), mouse_pos))
            else:
                self.bullets.append(self.bullet_type(
                    self.position + Vector2(self.sprite.get_width() // 2, -self.sprite.get_height() * 1.5), mouse_pos))
            self.available_ammo -= 1
            self.able_to_shoot = False
            if self.available_ammo <= 0:
                self.reloading = True

class RedrumGun(Gun):
    def __init__(self, position):
        super().__init__(position, load_sprite('Guns/pistol', 0.2), bullet_type=Explosive,
                         shoot_delay=10, reload_time=70, ammo_capacity=30, bullet_reloader=False)
    def Shoot(self):
        for i in range(4):
            if i == 0:
                self.bullets.append(RedrumBullet(self.position, self.position + (0, -1)))
            elif i == 1:
                self.bullets.append(RedrumBullet(self.position, self.position + (-1, 0)))
            elif i == 2:
                self.bullets.append(RedrumBullet(self.position, self.position + (0, 1)))
            elif i == 3:
                self.bullets.append(RedrumBullet(self.position, self.position + (1, 0)))