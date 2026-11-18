import pygame
import sys
import subprocess
import random

def start_levels():
    pygame.init()

    TILE_SIZE = 32
    WIDTH, HEIGHT = 1350, 700

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Clumsy Fish")
    clock = pygame.time.Clock()

    try:
        bg_img = pygame.image.load("../textures/level_bg.png").convert()
        bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

        block_img = pygame.image.load("../textures/cave_block.png").convert_alpha()
        block_img = pygame.transform.scale(block_img, (TILE_SIZE, TILE_SIZE))

        plat_img = pygame.image.load("../textures/platform.png").convert_alpha()
        plat_img = pygame.transform.scale(plat_img, (TILE_SIZE, TILE_SIZE))

        door_img = pygame.image.load("../textures/door.png").convert_alpha()
        door_img = pygame.transform.scale(door_img, (TILE_SIZE, TILE_SIZE))

        spike_img = pygame.image.load("../textures/spike.png").convert_alpha()
        spike_img = pygame.transform.scale(spike_img, (TILE_SIZE - 8, TILE_SIZE - 16))
        spike_img_flipped = pygame.transform.flip(spike_img, False, True)

        player_img = pygame.image.load("../textures/player.png").convert_alpha()
        player_img = pygame.transform.scale(player_img, (24, 28))

        player_img_left = player_img
        player_img_right = pygame.transform.flip(player_img, True, False)

        hint_box_img = pygame.image.load("../textures/dialog_box.png").convert_alpha()
        hint_box_img = pygame.transform.scale(hint_box_img, (400, 400))

    except pygame.error as e:
        print("Ошибка загрузки картинок:", e)
        sys.exit()

    #шрифт
    hint_font = pygame.font.SysFont("lucidaconsole", 20, bold=True)

    # карты уровней
    level_1_map = [
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "WWWW.........WWWWWWWW..............WWWWWWW",
        "WW............WWWWWW.....................W",
        "WWW............WWWW..........PPPPPPP..^.EW",
        "WWW.............WW...^.PPPP.........PPPPPW",
        "WWWW...............PPP......PPPP.........W",
        "WWW..........PPPP^................WWWWWWWW",
        "WW...PPPPP.......PPPPP...^..PPPP....WWWWWW",
        "W......................PPPP..........WWWWW",
        "W.............^..PPPP....................W",
        "W...........PPPP..............PPPPP......W",
        "W................PPPPP...^...............W",
        "W....^^^...............PPPPPP^...........W",
        "W.PPPPPPP................PPPPPPPPPPPPPP..W",
        "W............^^.........................WW",
        "W..........PPPPPP................^..WWWWWW",
        "W..............................PPPP...WWWW",
        "WWWS................^....PPPP....^......WW",
        "WWWWWW^...........PPPPP........PPPP....WWW",
        "WWWWWWWWW.....^PPP.....^...........^..WWWW",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
    ]

    # другое управление
    level_2_map = [
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "WWWWWWWW.....................WWWWWWWWWWWWW",
        "WWWWW...........^.................WWWWWWWW",
        "WWW.........PPPPPPPP....^................W",
        "WWWW...PPPP..........WWWWWWW.............W",
        "WWWWWW....PPPPPP..WWWWWWWWWWWW.PP^PPP....W",
        "WWWWWWWWW........WWWWWWWWW......PPP......W",
        "WWWWWWW.^^.....PPP..WWWWWWW^^^........^^^W",
        "WWWW...PPPPPPP...^^WWWWWWWWWWW......WWWWWW",
        "W..............WWWWWWWW...........WWWWWWWW",
        "W.........PPP...WWWWWW.....PPPPP...WWWWWWW",
        "WW..PPPP....^^.....WWWW.........PP..WWWWWW",
        "WWW.......PPPPP...WWWWWWW^^...........WWWW",
        "WWWWWWWW........WWWWWWWWWWW....PPPPPP^^WWW",
        "WWWWWWWWWWWW...^..WWWWWWWW^^........PPP.WW",
        "W............PPPP..^.WWWWWWW.PPPPP.......W",
        "WW......PPPPPP....WWWWWWWWWWW......PPP...W",
        "WWWWS..P......^^^WWWWWWWWWWWWWW.^^.....E.W",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
    ]

    #гравитация
    level_3_map = [
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "WWWWWWWW...WWWWWWWW............WWWWWWWWWWW",
        "WWWWW..............PPPPP.............WWWWW",
        "WWWS......PPPPPPPP.....................WWW",
        "WWW..PPPP.............PPPPPPPPP..........W",
        "W.PPPP...................................W",
        "W.......PPPPP.PPPPP......................W",
        "W...................PPPPPP...............W",
        "W...PPPPPPP..PPPPPP.....PPPPPP...........W",
        "W..............................PPPPP.....W",
        "W.......................PPPPPP...........W",
        "W...PPPPPPP.PP.PPPPPPPP..................W",
        "W.PPPP...................................W",
        "W......PPPPPP..PPPPPP....................W",
        "W..................PPPPPP....WWWWWWWWWWWWW",
        "W..........PPPPPPP.......WWWWWWWWWWWWWWWWW",
        "WWW....PP...........WWWWWWWWWWWWWWWWWWWWWW",
        "WWWWW......PPPPPPPP...WWWWWWWWWWWWWWWWWWWW",
        "WWWWWWW...................E...WWWWWWWWWWWW",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
    ]

    #течение
    level_4_map = [
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "WWWW.........WWWWWWWW..............WWWWWWW",
        "WW............WWWWWW.....................W",
        "WWW............WWWW..........PPPPPPP....EW",
        "WWW.............WW...^.PPPP.........PPPPPW",
        "WWWW...............PPP......PPPP.........W",
        "WWW..........PPPP^................WWWWWWWW",
        "WW...PPPPP.......PPPPP...^..PPPP....WWWWWW",
        "W......................PPPP..........WWWWW",
        "W.............^..PPPP....................W",
        "W...........PPPP..............PPPPP......W",
        "W................PPPPP...^...............W",
        "W....^^^...............PPPPPP^...........W",
        "W.PPPPPPP................PPPPPPPPPPPPPP..W",
        "W............^^.........................WW",
        "W..........PPPPPP................^..WWWWWW",
        "W..............................PPPP...WWWW",
        "WWW.................^....PPPP....^......WW",
        "WWWWWW^...........PPPPP........PPPP....WWW",
        "WWWWWWWWWS....^PPP.....^...........^..WWWW",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
    ]

    #высокий прыжок
    level_5_map = [
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "WWWW.........WWWWWWWW..............WWWWWWW",
        "WW............WWWWWW.....................W",
        "WWW............WWWW..........PPPPPPP....EW",
        "WWW.............WW...^.PPPP.........PPPPPW",
        "WWWW...............PPP......PPPP.........W",
        "WWW..........PPPP^................WWWWWWWW",
        "WW...PPPPP.......PPPPP...^..PPPP....WWWWWW",
        "W......................PPPP..........WWWWW",
        "W.............^..PPPP....................W",
        "W...........PPPP..............PPPPP......W",
        "W................PPPPP...^...............W",
        "W....^^^...............PPPPPP^...........W",
        "W.PPPPPPP................PPPPPPPPPPPPPP..W",
        "W............^^.........................WW",
        "W..........PPPPPP................^..WWWWWW",
        "W..............................PPPP...WWWW",
        "WWWS................^....PPPP....^......WW",
        "WWWWWW^...........PPPPP........PPPP....WWW",
        "WWWWWWWWW.....^PPP.....^...........^..WWWW",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
    ]

    LEVELS = [level_1_map, level_2_map, level_3_map, level_4_map, level_5_map]
    current_level_index = 0

    LEVEL_HINTS = [
        "Думаешь,\nбудет легко?",
        "Куда теперь\nбудешь нажимать?",
        "Ну давай попробуй\n, раз такой крутой",
        "Можешь выходить,\nты это не пройдешь",
        "Это самый легкий,\nтолько попробуй не\nпройти с первого раза"
    ]

    DEATH_TAUNTS = [
        "Опять тот шип?\nТы специально?",
        "Рыбка не должна\nбыть такой неуклюжей",
        "Шипы вообще-то\nне съедобные",
        "Говорят, у рыб память\n3 секунды. Заметно!",
        "Из тебя выйдет\nотличная консервная банка",
        "У тебя лапки\nили плавники?",
        "Даже камень плавает\nлучше тебя",
        "Немо бы уже давно\nнашел дорогу домой",
        "Кажется, кто-то пошел\nна корм крабам",
        "Этот шип стоял тут\nс самого начала!",
        "Кнопки перепутал\nили пальцы кривые?",
        "Может, лучше\nвыйдешь в меню?",
        "Нажми Alt+F4,\nтам секретный уровень",
        "Твоя клавиатура точно\nподключена к компу?",
        "Я бы поддалась,\nно мне тебя не жалко",
        "Сходи попей водички,\nты явно перегрелся",
        "Это был тактический\nпрыжок на шипы?",
        "Мне уже скучно\nсмотреть, как ты падаешь",
        "Попробуй открыть глаза\nво время игры",
        "Разработчики смеются\nнад этой попыткой",
        "Ты же в курсе, что\nшипы нужно обходить?",
        "Давай еще раз,\nя почти не смеюсь"
    ]

    death_count = 0
    active_dialog_text = ""

    #физика
    BASE_GRAVITY = 0.4
    BASE_MOVE_SPEED = 4
    BASE_JUMP_POWER = -10

    GRAVITY = BASE_GRAVITY
    MOVE_SPEED = BASE_MOVE_SPEED
    JUMP_POWER = BASE_JUMP_POWER

    player = pygame.Rect(0, 0, 24, 28)
    player_vel_y = 0
    on_ground = False
    facing_right = True
    exit_rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)

    spikes = []
    solid_tiles = []
    platform_tiles = []
    doors = []

    state = "hint"
    hint_timer = 4 * 60
    show_hint = True

    def load_level(lvl_idx, is_death=False):
        nonlocal player, player_vel_y, on_ground, exit_rect, spikes, solid_tiles, platform_tiles, doors, current_level_index, state, hint_timer, show_hint, GRAVITY, MOVE_SPEED, JUMP_POWER, active_dialog_text
        current_level_index = lvl_idx
        spikes.clear()
        solid_tiles.clear()
        platform_tiles.clear()
        doors.clear()

        #физика для каждого уровня
        if current_level_index == 0:
            GRAVITY = BASE_GRAVITY
            MOVE_SPEED = BASE_MOVE_SPEED
            JUMP_POWER = BASE_JUMP_POWER
        elif current_level_index == 1:
            # Уровень 2: меняется управление
            GRAVITY = BASE_GRAVITY
            MOVE_SPEED = BASE_MOVE_SPEED
            JUMP_POWER = BASE_JUMP_POWER
        elif current_level_index == 2:
            # Уровень 3: обратная гравитация
            GRAVITY = -BASE_GRAVITY
            MOVE_SPEED = BASE_MOVE_SPEED
            JUMP_POWER = 10  # Прыжок вниз (так как гравитация тянет вверх)
        elif current_level_index == 3:
            # Уровень 4: течение
            GRAVITY = BASE_GRAVITY
            MOVE_SPEED = BASE_MOVE_SPEED * 0.6  # Медленнее
            JUMP_POWER = -10
        elif current_level_index == 4:
            # Уровень 5: высокий прыжок
            GRAVITY = BASE_GRAVITY
            MOVE_SPEED = BASE_MOVE_SPEED
            JUMP_POWER = -16  # Выше обычного

        current_map = LEVELS[current_level_index]

        for row_idx, row in enumerate(current_map):
            for col_idx, char in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE

                if char == 'W':
                    solid_tiles.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                elif char == 'P':
                    platform_tiles.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                elif char == 'S':
                    player.x = x + 4
                    player.y = y + 4
                    player_vel_y = 0
                    on_ground = False
                    doors.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                elif char == 'E':
                    exit_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    doors.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                elif char == '^':
                    spikes.append(pygame.Rect(x + 4, y + 16, TILE_SIZE - 8, TILE_SIZE - 16))

        state = "hint"
        show_hint = True
        if is_death:
            hint_timer = 90
            if death_count % 5 == 0:
                active_dialog_text = f"Уже {death_count}-я смерть!\nТы бьешь все рекорды"
            else:
                active_dialog_text = random.choice(DEATH_TAUNTS)
        else:
            hint_timer = 4 * 60
            active_dialog_text = LEVEL_HINTS[current_level_index]

    load_level(0)


    def move_and_collide(dx, dy):
        nonlocal on_ground

        # движение по x
        player.x += dx
        for tile in solid_tiles:
            if player.colliderect(tile):
                if dx > 0:
                    player.right = tile.left
                elif dx < 0:
                    player.left = tile.right

        # движение по Y
        player.y += dy
        on_ground = False

        # проверка столкновений со стенами
        for tile in solid_tiles:
            if player.colliderect(tile):
                if dy > 0:
                    player.bottom = tile.top
                    if GRAVITY > 0:  # стоим на полу только если гравитация обычная
                        on_ground = True
                elif dy < 0:
                    player.top = tile.bottom
                    if GRAVITY < 0:  # стоим на потолке, если гравитация перевернута
                        on_ground = True

        # проверка платформ
        for tile in platform_tiles:
            if player.colliderect(tile):
                if GRAVITY > 0 and dy > 0:  # падаем вниз (обычная гравитация)
                    if player.bottom - dy <= tile.top + 5:
                        player.bottom = tile.top
                        on_ground = True
                elif GRAVITY < 0 and dy < 0:  # летим вверх (перевернутая гравитация)
                    if player.top - dy >= tile.bottom - 5:
                        player.top = tile.bottom
                        on_ground = True

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Выход в главное меню по клавише Esc
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

            if state == "game" and event.type == pygame.KEYDOWN:
                # прыжки на уровнях
                if on_ground:
                    if current_level_index == 0 and event.key == pygame.K_w:
                        player_vel_y = JUMP_POWER
                    elif current_level_index in [1, 2] and event.key == pygame.K_u:
                        player_vel_y = JUMP_POWER
                    elif current_level_index in [3, 4] and event.key == pygame.K_q:
                        player_vel_y = JUMP_POWER

                # рестарт
                if event.key == pygame.K_x:
                    load_level(current_level_index)


        if state == "hint":
            hint_timer -= 1
            if hint_timer <= 0:
                state = "game"
                show_hint = False

        elif state == "game":
            keys = pygame.key.get_pressed()
            dx = 0

            # движение по уровням
            if current_level_index == 0:
                if keys[pygame.K_a]: dx = -MOVE_SPEED
                if keys[pygame.K_d]: dx = MOVE_SPEED
            elif current_level_index in [1, 2]:
                if keys[pygame.K_l]: dx = -MOVE_SPEED
                if keys[pygame.K_r]: dx = MOVE_SPEED
            elif current_level_index in [3, 4]:
                if keys[pygame.K_e]: dx = -MOVE_SPEED
                if keys[pygame.K_s]: dx = MOVE_SPEED

            if dx > 0:
                facing_right = True
            elif dx < 0:
                facing_right = False

            player_vel_y += GRAVITY
            if abs(player_vel_y) > 7:
                player_vel_y = 7 if player_vel_y > 0 else -7

            # эффект течения
            if current_level_index == 3:
                wind_force = -1.5
                if player_vel_y < 0:
                    wind_force = -2.5

                dx += wind_force

            move_and_collide(dx, player_vel_y)

            # смерть от шипов
            for spike in spikes:
                if player.colliderect(spike):
                    death_count += 1
                    load_level(current_level_index, is_death=True)
                    break

            # переход на следующий уровень
            if player.colliderect(exit_rect):
                if current_level_index + 1 < len(LEVELS):
                    load_level(current_level_index + 1)
                else:
                    print("Чтоб больше тебя здесь не было")
                    return

        # отрисовка
        screen.blit(bg_img, (0, 0))

        for door in doors:
            screen.blit(door_img, door.topleft)

        for tile in solid_tiles:
            screen.blit(block_img, tile.topleft)

        for tile in platform_tiles:
            screen.blit(plat_img, tile.topleft)

        current_spike_img = spike_img_flipped if GRAVITY < 0 else spike_img
        for spike in spikes:
            screen.blit(current_spike_img, spike.topleft)

        current_player_img = player_img_right if facing_right else player_img_left
        if GRAVITY < 0:
            current_player_img = pygame.transform.flip(current_player_img, False, True)
        screen.blit(current_player_img, player.topleft)

        death_surf = hint_font.render(f"Смертей: {death_count}", True, (255, 255, 255))
        screen.blit(death_surf, (15, 10))

        # отрисовка диалогового окна
        if state == "hint" and show_hint:
            hint_x = 475
            hint_y = 150
            screen.blit(hint_box_img, (hint_x, hint_y))

            lines = active_dialog_text.split('\n')
            line_y_offset = 80

            for line in lines:
                text_surface = hint_font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(WIDTH // 2, hint_y + line_y_offset))
                screen.blit(text_surface, text_rect)
                line_y_offset += 30

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    start_levels()