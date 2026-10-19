
import pygame
import sys
import os
import random


RED    = (255, 0, 0)
ORANGE = (255, 127, 0)
YELLOW = (255, 255, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
INDIGO = (75, 0, 130)
VIOLET = (148, 0, 211)
WHITE = (255, 255, 255)
BLACK = (0,0,0)

MID_X = 250
MID_Y = 300

if not os.environ.get("DISPLAY"):
    os.environ["DISPLAY"] = ":99"

if not os.environ.get("XDG_RUNTIME_DIR"):
    os.environ["XDG_RUNTIME_DIR"] = "/tmp/runtime-vscode"
    os.makedirs("/tmp/runtime-vscode", exist_ok=True)

os.environ["SDL_AUDIODRIVER"] = "dummy"

#---------------------------------------------------------
pygame.init()
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()
FPS = 60
screen = pygame.display.set_mode((500, 600))

player = pygame.Rect(0, 0, 20, 60)
left_wing = pygame.Rect(0, 0, 30, 10)
right_wing = pygame.Rect(0, 0, 30, 10)

player.center = (MID_X, 485)

stats = {
    "speed": 3,
    "gold": 0
}
plane = {
    "original_health": 50,
    "health": 50,
    "flashing": False,
    "flash_start_time": -1
}

gun = {
    "type": 1,
    "stutter": 0,
    "ammo": 60,
    "reload": 5,
    "speed": 5,

    "original ammo": 60,
    "original stutter": 0.125,
    "original reload": 5
}

state = "menu"
screen.fill((0,0,0))


#---------------------------- SHOOTING ----------------------------
reloading = False
bullets = []
def shoot():
    global reloading
    if gun["type"] == 1:
        if gun["ammo"] > 0 and not reloading:
            bullet = pygame.Rect(player.centerx - 3, player.top - 10, 6, 10)
            bullets.append(bullet)
            gun["ammo"] -= 1


def reload():
    global reloading
    if not reloading and gun["ammo"] < gun["original ammo"]:
        reloading = True
    if gun["ammo"] == 0:
        if gun["reload"] <= 0:
            gun["ammo"] = gun["original ammo"]
            gun["reload"] = gun["original reload"]
        else:
            gun["reload"] -= 1/FPS


#---------------------------- ENEMIES ----------------------------

enemies = []
enemy_spawn = 3
counter = 0
boss_spawn = 10
def spawn_enemy():

    enemy_type = random.randint(1, 2)
    if enemy_type == 1:

        enemy = pygame.Rect(0, -60, 20, 60)

        enemy.centerx = random.randint(15, 485)
        enemies.append({
            "rect": enemy,
            "health": 8,
            "type": "bomber",
            "speed": 1.25,

            "maxspd": 1.25, 
            "minspd": 1,

            "leftwing": pygame.Rect(0, 0, 30, 10),
            "rightwing": pygame.Rect(0, 0, 30, 10),
            "time till bomb": random.random()*2 + 0.25,
            "can bomb": True
        })

    elif enemy_type == 2:
        enemy = pygame.Rect(0, -60, 15, 60)
        enemy.centerx = random.randint(15, 485)

        enemy_type = random.randint(1, 3)

        if enemy_type == 1:  
            enemies.append({
                "speed": 1.6,
                "rect": enemy,
                "health": 7,
                "type": "fighter",
                "first shot": 0.25,
                "ammo": random.randint(15, 17),
                "stutter": 0.10,

                "maxspd": 1.6,
                "minspd": 1.3,

                "leftwing": pygame.Rect(0, 0, 30, 10),
                "rightwing": pygame.Rect(0, 0, 30, 10),
            })

        elif enemy_type == 2: 
            enemies.append({
                "speed": 1.5,
                "rect": enemy,
                "health": 10,
                "type": "fighter",
                "first shot": 0.25,
                "ammo": random.randint(13, 17),
                "stutter": 0.15,

                "maxspd": 1.5,
                "minspd": 1.2,

                "leftwing": pygame.Rect(0, 0, 30, 10),
                "rightwing": pygame.Rect(0, 0, 30, 10),
            })

        else:
            enemies.append({
                "speed": 1.4,
                "rect": enemy,
                "health": 12,
                "type": "fighter",
                "first shot": 0.225,
                "ammo": 999999,
                "stutter": 0.40,

                "maxspd": 1.4,
                "minspd": 1.1,

                "leftwing": pygame.Rect(0, 0, 30, 10),
                "rightwing": pygame.Rect(0, 0, 30, 10),
            })


def spawn_bomb(bomber):

    bomb = pygame.Rect(0, bomber["rect"].bottom, 10, 40)
    bomb.centerx = bomber["rect"].centerx
    enemies.append({
        "speed": 2.5,
        "rect": bomb,
        "health": 1,
        "type": "bomb",
        "maxspd": 2.5,
        "minspd": 2.5
    })

enemy_bullets = []
def enemy_shoot(fighter):
    global enemy_bullets
    bullet = pygame.Rect(
        fighter["rect"].centerx - 3,
        fighter["rect"].bottom,
        6,
        10
    )

    enemy_bullets.append(bullet)

#misc---------------------

def damage(dmg):
    global state
    plane["health"] -= dmg
    if plane["health"] <= 0:
        state = "death"
    else:
        plane["flashing"] = True
        plane["flash_start_time"] = pygame.time.get_ticks()

state = "menu"
#---------------------------- MAIN LOOP ----------------------------
boss = False
draw_plane = True
while True:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and state == "death":
            if event.key == pygame.K_r:
                state = "gameplay" 
                enemies = []
                enemy_bullets = []
                plane["health"] = plane["original_health"]
            elif event.key == pygame.K_m:
                state = "menu" 
        if state == "gameplay" and event.type == pygame.KEYDOWN:

            if (event.key == pygame.K_r and gun["ammo"] < gun["original ammo"]) and not reloading:
                reload()
        if state == "menu" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                if stats["gold"] > 9:
                    stats["gold"] -= 10
                    stats["speed"] = 5
            elif event.key == pygame.K_2:
                if stats["gold"] > 14:
                    plane["original_health"] = 75
                    stats["gold"] -= 15
            elif event.key == pygame.K_3:
                if stats["gold"] > 24:
                    gun["original reload"] = 4
                    stats["gold"] -= 25
            elif event.key == pygame.K_4:
                if stats["gold"] > 24:
                    gun["original stutter"] = 0.1
                    stats["gold"] -= 25
            elif event.key == pygame.K_5:
                if stats["gold"] > 29:
                    gun["original ammo"] = 90
                    stats["gold"] -= 30

            elif event.key == pygame.K_SPACE:
                state = "gameplay"
                enemies = []
                
                plane["health"] = plane["original_health"]
                enemy_bullets = []
                    
            
    if state == "gameplay":
        screen.fill(BLACK)            

        xtext = font.render(f"x: {player.x}", True, WHITE)
        ytext = font.render(f"y: {player.y}", True, WHITE)
        healthtext = font.render(f"health: {plane['health']}", True, WHITE)


        screen.blit(xtext, (50, 50))
        screen.blit(ytext, (50, 100))
        screen.blit(healthtext, (50, 560))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.x -= stats["speed"]
        if keys[pygame.K_d]:
            player.x += stats["speed"]

        if keys[pygame.K_SPACE]:
            if gun["stutter"] <= 0:
                shoot()
                gun["stutter"] = gun["original stutter"]

        
        for bullet in bullets[:]:
            bullet.y -= gun["speed"]

            if bullet.bottom < 0 and bullet in bullets:
                bullets.remove(bullet)
                break
            else:
                pygame.draw.rect(screen, WHITE, bullet)

            for enemy_bullet in enemy_bullets[:]:
                hitbox = enemy_bullet.inflate(8, 8)
                if bullet.colliderect(hitbox):
                    bullets.remove(bullet)
                    enemy_bullets.remove(enemy_bullet)
                    break

            if bullet not in bullets:
                continue

            for enemy in enemies[:]:
                if enemy["type"] == "bomber":

                    if (
                        bullet.colliderect(enemy["rect"])
                        or bullet.colliderect(enemy["leftwing"])
                        or bullet.colliderect(enemy["rightwing"])
                    ):
                        enemy["health"] -= 1
                        if enemy["type"] != "bomb":
                            enemy["speed"] -= (enemy["maxspd"] - enemy["minspd"]) / (enemy["health"] + 1)
                        bullets.remove(bullet)

                        if enemy["health"] <= 0:
                            enemies.remove(enemy)
                            stats["gold"] += 2
                        break

                elif enemy["type"] == "bomb":

                    if bullet.colliderect(enemy["rect"]):
                        enemy["health"] -= 1
                        bullets.remove(bullet)

                        if enemy["health"] <= 0:
                            enemies.remove(enemy)

                elif enemy["type"] == "fighter":
                    if bullet.colliderect(enemy["rect"]) or bullet.colliderect(enemy["leftwing"]) or bullet.colliderect(enemy["rightwing"]):
                        enemy["health"] -= 1
                        if enemy["type"] != "bomb":
                            enemy["speed"] -= enemy["speed"] / 100
                        bullets.remove(bullet)
                    
                        if enemy["health"] <= 0:
                            enemies.remove(enemy)
                            stats["gold"] += 3
                        break

                    
                    
        #-------------ENEMIES-----------------
        enemy_spawn -= 1/FPS
        
        if boss_spawn <= 0:
            boss_spawn = 10
            boss = True
            enemy_spawn = 1.5

        if enemy_spawn <= 0:
            spawn_enemy()
            if boss == True:
                enemy_spawn = 1.5
                counter += 1
                if counter == 9:
                    boss = False
                    counter = 0
                    boss_spawn = 10
            else:
                enemy_spawn = 4
                boss_spawn -= 1

        for enemy in enemies[:]:
            enemy["rect"].y += enemy["speed"]

            if enemy["rect"].top > 600:
                enemies.remove(enemy)
                continue

            if enemy["type"] == "bomber":
                enemy["leftwing"].x = enemy["rect"].x - enemy["leftwing"].width
                enemy["leftwing"].y = enemy["rect"].y + 20

                enemy["rightwing"].x = enemy["rect"].right
                enemy["rightwing"].y = enemy["rect"].y + 20

                pygame.draw.rect(screen, RED, enemy["rect"])
                pygame.draw.rect(screen, RED, enemy["leftwing"])
                pygame.draw.rect(screen, RED, enemy["rightwing"])

                if enemy["time till bomb"] > 0:
                    enemy["time till bomb"] -= 1 / FPS
                else:
                    if enemy["can bomb"] == True:
                        spawn_bomb(enemy)
                        enemy["can bomb"] = False
                if enemy["rect"].colliderect(player) or enemy["rect"].colliderect(left_wing) or enemy["rect"].colliderect(right_wing):
                    damage(enemy["health"] // 2)
                    enemies.remove(enemy)

            elif enemy["type"] == "bomb":
                pygame.draw.rect(screen, RED, enemy["rect"])

                if enemy["rect"].colliderect(player) or enemy["rect"].colliderect(left_wing) or enemy["rect"].colliderect(right_wing):
                    damage(3)
                    enemies.remove(enemy)

            elif enemy["type"] == "fighter":
                enemy["leftwing"].x = enemy["rect"].x - enemy["leftwing"].width
                enemy["leftwing"].y = enemy["rect"].y + 20
                
                enemy["rightwing"].x = enemy["rect"].right
                enemy["rightwing"].y = enemy["rect"].y + 20

                pygame.draw.rect(screen, BLUE, enemy["rect"])
                pygame.draw.rect(screen, BLUE, enemy["leftwing"])
                pygame.draw.rect(screen, BLUE, enemy["rightwing"])

                enemy["first shot"] -= 1 / FPS

                if enemy["first shot"] <= 0 and enemy["ammo"] > 0:
                    enemy_shoot(enemy)
                    enemy["ammo"] -= 1
                    enemy["first shot"] = enemy["stutter"]

                if enemy["rect"].colliderect(player) or enemy["rect"].colliderect(left_wing) or enemy["rect"].colliderect(right_wing):
                    damage(enemy["health"] // 2)
                    enemies.remove(enemy)

                

        for bullet in enemy_bullets[:]:
                bullet.y += 5
        
                if bullet.top > 600:
                    enemy_bullets.remove(bullet)
                    continue
        
                if bullet.colliderect(player) or bullet.colliderect(left_wing) or bullet.colliderect(right_wing):
                    enemy_bullets.remove(bullet)
                    damage(1)
                    continue
        
                pygame.draw.rect(screen, ORANGE, bullet)

        # ------------------------- PLAYER --------------------

        if player.x <= 15:
            player.x = 15
        else:
            left_wing.x = player.x - left_wing.width
            left_wing.y = player.y + 20
            right_wing.x = player.right
            right_wing.y = player.y + 20
            
        if player.x >= 455:
            player.x = 455
            right_wing.x = player.right
            left_wing.x = player.x - left_wing.width
        else:
            left_wing.x = player.x - left_wing.width
            left_wing.y = player.y + 20
            right_wing.x = player.right
            right_wing.y = player.y + 20

        
        
        if plane["flashing"]:
            time_passed = pygame.time.get_ticks() - plane["flash_start_time"]
            
            if time_passed >= 180:
                plane["flashing"] = False
                draw_plane = True
            else:
                draw_plane = (time_passed // 25) % 2 == 0

        if draw_plane:
            pygame.draw.rect(screen, GREEN, player)
            pygame.draw.rect(screen, GREEN, left_wing)
            pygame.draw.rect(screen, GREEN, right_wing)

        # gun stuff
        if reloading:
            ammo_text = font.render(f"RELOADING... ({int(gun['reload'])+1}s) / {gun['original ammo']}", True, WHITE)
            screen.blit(ammo_text, (220, 560))
            
            gun["reload"] -= 1/FPS
            
            if gun["reload"] <= 0:
                gun["ammo"] = gun["original ammo"]
                gun["reload"] = gun["original reload"]
                reloading = False
        else:
            ammo_text = font.render(f"{gun['ammo']} / {gun['original ammo']}", True, WHITE)
            screen.blit(ammo_text, (410, 560))
            
            if gun["ammo"] <= 0:
                reload()

        gun["stutter"] -= 1/FPS


        pygame.display.flip()
        clock.tick(FPS)

    elif state == "death":
        screen.fill(RED)

        lines = [
            "You died.",
            "Press R to respawn.",
            "Press M to go to the menu."
        ]

        line_height = 40
        for i, line in enumerate(lines):
            death_text = font.render(line, True, WHITE)
            
            text_x = MID_X - (death_text.get_width() // 2)
            text_y = MID_Y + (i * line_height)
            
            screen.blit(death_text, (text_x, text_y))

        pygame.display.flip()
        clock.tick(FPS)

    elif state == "menu":
        screen.fill(BLACK)
        speed_text = pygame.font.Font(None, 25).render("Press 1 to upgrade speed from 3 -> 5, cost 10.", True, WHITE)
        health_text = pygame.font.Font(None, 25).render("Press 2 to upgrade health from 50hp -> 75hp, cost 15.", True, WHITE)
        reload_text = pygame.font.Font(None, 25).render("Press 3 to upgrade reload from 5s -> 4s, cost 25.", True, WHITE)
        stutter_text = pygame.font.Font(None, 25).render("Press 4 to upgrade stutter from 0.125s -> 0.1s, cost 25.", True, WHITE)
        capacity_text = pygame.font.Font(None, 25).render("Press 5 to upgrade ammo capacity from 60 -> 90, cost 30.", True, WHITE)

        start_text = font.render("Press space to start!", True, RED)
        gold_text = pygame.font.Font(None, 25).render(f"Gold: {stats['gold']}", True, YELLOW)
        screen.blit(speed_text, (15, 50))
        screen.blit(health_text, (15, 100))
        screen.blit(reload_text, (15, 150))
        screen.blit(stutter_text, (15, 200))
        screen.blit(capacity_text, (15, 250))
        screen.blit(start_text, (15, 400))
        screen.blit(gold_text, (15, 570))


        pygame.display.flip()
        clock.tick(FPS)

