import pygame
from pygame.locals import *
import random

pygame.init()
clock = pygame.time.Clock()
frame_rate = 60

# Screen default
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), RESIZABLE)

# Title
pygame.display.set_caption('Random Boolean')

# Colors
black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
cyan = [0, 255, 255]
orange = [255, 165, 0]
yellow = [255, 255, 0]
purple = [128, 0, 128]
pink = [255, 192, 203]

# Cells
number_of_cells = 15
color_on = purple
color_off = black


class MainClass:
    def __init__(self):
        self.cells = []
        self.cell_links = {}
        self.history = []
        self.cell_size = screen_height / number_of_cells
        self.step = 0

        for i in range(number_of_cells):
            num_of_con = random.randint(2, number_of_cells - 1)
            con_list = []
            link = random.randint(0, number_of_cells - 1)

            for c in range(num_of_con):
                while link == i or link in con_list:
                    link = random.randint(0, number_of_cells - 1)
                con_list.append(link)

            con_list.sort()
            self.cell_links[i] = con_list
            self.cells.append(random.randint(0, 1))

    def draw_cells(self, x, cells):
        for i in range(len(cells)):
            if cells[i] == 1:
                pygame.draw.rect(screen, color_on, (x + 1, i * self.cell_size + 1, self.cell_size - 2,
                                                    self.cell_size - 2))
            elif color_off != black:
                pygame.draw.rect(screen, color_off, (x + 1, i * self.cell_size + 1, self.cell_size - 2,
                                                     self.cell_size - 2))

    def draw(self):
        if self.step * self.cell_size + self.cell_size <= screen_width:
            self.draw_cells(self.step * self.cell_size, self.cells)
            for i in range(len(self.history)):
                self.draw_cells(self.step * self.cell_size - (i + 1) * self.cell_size,
                                self.history[len(self.history) - i - 1])
        else:
            cols = int(screen_width / self.cell_size)
            self.draw_cells(self.cell_size * (cols - 1), self.cells)
            for i in range(cols - 1):
                hist_index = len(self.history) - i - 1
                if hist_index >= 0:
                    self.draw_cells(self.cell_size * (cols - 2 - i), self.history[hist_index])

    def advance(self):
        if len(self.history) < 100000:
            self.history.append(self.cells)
        else:
            self.history.pop(0)
            self.history.append(self.cells)
        change = []
        # for i in range(len(self.cells)):
        #     change_var = 0
        #     for c in range(len(self.cell_links[i])):
        #         change_var += self.cells[self.cell_links[i][c]]
        #
        #     change_var = int(change_var / len(self.cell_links[i]) * 100)
        #
        #     if change_var % 3 == 0:
        #         change.append(1)
        #     else:
        #         change.append(0)
        for i in range(len(self.cells)):
            change_var = 0
            for c in range(len(self.cell_links[i])):
                change_var += self.cells[self.cell_links[i][c]]

            if change_var % 2 != 0:
                change.append(1)
            else:
                change.append(0)

        self.cells = change
        self.step += 1

    def step_back(self):
        if self.step != 0:
            self.cells = self.history[len(self.history) - 1]
            self.history.pop(len(self.history) - 1)
            self.step -= 1

    def random_disturb(self):
        ran = random.randint(0, len(self.cells) - 1)
        if self.cells[ran] == 1:
            self.cells[ran] = 0
        else:
            self.cells[ran] = 1


main_class = MainClass()

held_keys = []
hold_delay = frame_rate / 2
hold_counter = 0
paused = False
running = True
while running:
    screen.fill(black)

    # Event loop
    for event in pygame.event.get():
        # Press close button
        if event.type == pygame.QUIT:
            running = False
            break

        # Key down events
        if event.type == pygame.KEYDOWN:
            keys_list = pygame.key.get_pressed()
            # Close window shortcut
            if (keys_list[K_LCTRL] or keys_list[K_RCTRL]) and keys_list[K_w]:
                running = False
                break

            # Disturb
            if keys_list[K_d]:
                main_class.random_disturb()

            # Reset
            if (keys_list[K_LCTRL] or keys_list[K_RCTRL]) and keys_list[K_r]:
                main_class.__init__()

            # Pause
            if keys_list[K_SPACE] and not paused:
                paused = True
            elif keys_list[K_SPACE] and paused:
                paused = False

            # Frame advance
            if paused:
                if keys_list[K_RIGHT]:
                    main_class.advance()
                    if 'K_RIGHT' not in held_keys:
                        held_keys.append('K_RIGHT')
                        hold_counter = hold_delay
                if keys_list[K_LEFT]:
                    main_class.step_back()
                    if 'K_LEFT' not in held_keys:
                        held_keys.append('K_LEFT')
                        hold_counter = hold_delay

        # Key up events
        if event.type == pygame.KEYUP:
            keys_list = pygame.key.get_pressed()
            if keys_list[K_RIGHT] == 0 and 'K_RIGHT' in held_keys:
                held_keys.pop(held_keys.index('K_RIGHT'))
            if keys_list[K_LEFT] == 0 and 'K_LEFT' in held_keys:
                held_keys.pop(held_keys.index('K_LEFT'))

        # Window resize event
        if event.type == pygame.VIDEORESIZE:
            screen_width = event.w
            screen_height = event.h
            screen = pygame.display.set_mode((screen_width, screen_height), RESIZABLE)
            if screen_height / number_of_cells > 4:
                main_class.cell_size = screen_height / number_of_cells

    # Held keys
    if hold_counter > 0:
        hold_counter -= 1
    else:
        if 'K_RIGHT' in held_keys:
            main_class.advance()
        elif 'K_LEFT' in held_keys:
            main_class.step_back()

    main_class.draw()
    if not paused:
        main_class.advance()

    clock.tick(frame_rate)
    pygame.display.flip()

pygame.display.quit()
pygame.quit()
