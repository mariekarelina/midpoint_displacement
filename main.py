import random
import pygame
import collections
import math
from pygame import gfxdraw

# Опредеяем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


# Выбираем высоты для точек
def height_determination(heights, start_point, end_point, roughness):
    segment_center = (start_point + end_point + 1) // 2
    length = end_point - start_point + 1
    while heights[segment_center] <= 0 or heights[segment_center] >= 700:
        heights[segment_center] = (heights[start_point] + heights[end_point]) // 2
        heights[segment_center] += roughness * length * random.randint(-1, 1)


# Строим разбиения прямой
def make_segments(width, heights, roughness):
    # Создаём дек
    seg_queue = collections.deque()
    # Добавляем отрезок
    seg_queue.append((width - 701, width - 1, roughness))
    # И добавляем отрезки далее
    while len(seg_queue) != 0:
        start, end, randomness = seg_queue.popleft()
        center = (start + end + 1) // 2

        height_determination(heights, start, end, roughness)

        # Проверяем ширину отрезка (можем ли еще раз разделить)
        if end - start > 2:
            # Уменьшаем случайность
            seg_queue.append((start, center, math.floor(randomness // 2)))
            seg_queue.append((center, end, math.floor(randomness // 2)))

def render_heights(screen, heights):
    for i, height in enumerate(heights):
        gfxdraw.pixel(screen, i, int(height), WHITE)


# --------------------------------- #
def main():
    # Задаём размеры окна
    Width: int = 700
    Height: int = 700
    # Создаём массив всех высот
    heights = [0] * Width
    # Инициализируем начальную и конечную высоты
    heights[0] = random.randint(0, 700)
    heights[Width - 1] = random.randint(0, 700)
    # Ставим шероховатость
    #print('Введите шероховатость:')
    #roughness = float(input())
    roughness = random.uniform(0, 1)

    # Создаём окно
    pygame.init()
    screen = pygame.display.set_mode((Width, Height))
    screen.fill(BLACK)

    make_segments(Width, heights, roughness)
    render_heights(screen, heights[Width - 700:Width - 1])

    #Отрисовка
    # Создаём переменные для прокрутки
    index: int = 0
    is_right: bool = False
    is_left: bool = False
    flag: bool = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    is_right = True
                if event.key == pygame.K_LEFT:
                    is_left = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    is_right = False
                if event.key == pygame.K_LEFT:
                    is_left = False
        if is_right:
            index += 1
            flag = False
        if is_left:
            if index > 0:
                index -= 1
        # Если прошли весь "путь"
        if index % 700 == 0 and not flag:
            Width += 700
            heights.extend([0] * 700)
            heights[Width - 1] = heights[0] + (roughness * 700 * random.randint(-1, 1)) % 700
            make_segments(Width, heights, roughness)
            flag = True

        screen.fill((0, 0, 0))
        render_heights(screen, heights[0 + index:Width - 1 + index])
        pygame.display.update()


main()