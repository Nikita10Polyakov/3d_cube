import pygame
import sys
import math
import numpy as np

# Ініціалізація Pygame
pygame.init()

# Розмір вікна
width, height = 800, 600

# Створення вікна
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('3D Cube Visualization')

# Колір фону
background_color = (255, 255, 255)

# Функція для зчитування даних куба з файлу і збереження їх в змінні
def read_cube_data(filename):
    cube_data = {}
    with open(filename, 'r') as file:
        exec(file.read(), cube_data)
    return cube_data.get('cube_vertices', []), cube_data.get('cube_edges', [])

# Зчитування даних куба з файлу та збереження їх у змінні
cube_vertices, cube_edges = read_cube_data('cube_data.txt')

# Точка перспективи
camera_x = 100
camera_y = 10
camera_z = 10

# Кути повороту та масштаби для кожної вісі
rotation_angles = [0, 0, 0]  # кути повороту навколо вісей OX, OY, OZ
scale_factors = [1, 1, 1]  # масштаби за віссю OX, OY, OZ

# Основний цикл програми
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Поворот окремо за кожною віссю
    if keys[pygame.K_LEFT]:
        rotation_angles[1] += 0.002
    if keys[pygame.K_RIGHT]:
        rotation_angles[1] -= 0.002
    if keys[pygame.K_UP]:
        rotation_angles[0] += 0.002
    if keys[pygame.K_DOWN]:
        rotation_angles[0] -= 0.002
    if keys[pygame.K_a]:
        rotation_angles[2] += 0.002
    if keys[pygame.K_d]:
        rotation_angles[2] -= 0.002

    # Масштабування окремо за кожною віссю
    if keys[pygame.K_w]:
        scale_factors[1] += 0.002
    if keys[pygame.K_s]:
        scale_factors[1] -= 0.002
    if keys[pygame.K_q]:
        scale_factors[0] += 0.002
    if keys[pygame.K_e]:
        scale_factors[0] -= 0.002
    if keys[pygame.K_r]:
        scale_factors[2] += 0.002
    if keys[pygame.K_f]:
        scale_factors[2] -= 0.002

    # Поворот та масштабування одночасно за усіма вісями
    if keys[pygame.K_z]:
        rotation_angles = [angle + 0.002 for angle in rotation_angles]
    if keys[pygame.K_x]:
        rotation_angles = [angle - 0.002 for angle in rotation_angles]
    if keys[pygame.K_c]:
        scale_factors = [factor + 0.0002 for factor in scale_factors]
    if keys[pygame.K_v]:
        scale_factors = [factor - 0.0002 for factor in scale_factors]

    # Рух фігури вгору, вниз, ліворуч або праворуч
    if keys[pygame.K_i]:
        camera_y += 0.2
        if camera_y > height / 2:
            print("Reached the top boundary of OY axis")
            camera_y = camera_y - 200  # Зупиняємо фігуру на межі
    if keys[pygame.K_k]:
        camera_y -= 0.2
        if camera_y < -height / 2:
            print("Reached the bottom boundary of OY axis")
            camera_y = camera_y + 200  # Зупиняємо фігуру на межі
    if keys[pygame.K_j]:
        camera_x += 0.2
        if camera_x > width / 2:
            print("Reached the right boundary of OX axis")
            camera_x = camera_x - 200  # Зупиняємо фігуру на межі
    if keys[pygame.K_l]:
        camera_x -= 0.2
        if camera_x < -width / 2:
            print("Reached the left boundary of OX axis")
            camera_x = camera_x + 200  # Зупиняємо фігуру на межі

    # Очищення екрану
    screen.fill(background_color)

    # Рендерінг куба
    rotation_matrix_x = np.array([[1, 0, 0],
                                  [0, math.cos(rotation_angles[0]), -math.sin(rotation_angles[0])],
                                  [0, math.sin(rotation_angles[0]), math.cos(rotation_angles[0])]])

    rotation_matrix_y = np.array([[math.cos(rotation_angles[1]), 0, -math.sin(rotation_angles[1])],
                                  [0, 1, 0],
                                  [math.sin(rotation_angles[1]), 0, math.cos(rotation_angles[1])]])

    rotation_matrix_z = np.array([[math.cos(rotation_angles[2]), math.sin(rotation_angles[2]), 0],
                                  [-math.sin(rotation_angles[2]), math.cos(rotation_angles[2]), 0],
                                  [0, 0, 1]])

    rotation_matrix = np.dot(rotation_matrix_x, np.dot(rotation_matrix_y, rotation_matrix_z))

    scaled_vertices = np.dot(cube_vertices, np.diag(scale_factors))
    rotated_and_scaled_vertices = np.dot(scaled_vertices, rotation_matrix)

    projected_vertices = []
    for vertex in rotated_and_scaled_vertices:
        x = vertex[0] - camera_x
        y = vertex[1] - camera_y
        z = vertex[2] - camera_z

        # Проекція вершин на екран
        depth = 200
        scale = depth / (depth + z)
        screen_x = int(x * scale + width / 2)
        screen_y = int(y * scale + height / 2)
        projected_vertices.append((screen_x, screen_y))

    for edge in cube_edges:
        start_x, start_y = projected_vertices[edge[0]]
        end_x, end_y = projected_vertices[edge[1]]
        pygame.draw.line(screen, (255, 20, 147), (start_x, start_y), (end_x, end_y), 4)

    # Введення координат з консолі
    if keys[pygame.K_t]:
        print("Enter coordinates (x, y, z): ")
        x_input = float(input("x: "))
        y_input = float(input("y: "))
        camera_x = x_input
        camera_y = y_input

    # Оновлення вікна
    pygame.display.flip()

# Завершення роботи Pygame
pygame.quit()
sys.exit()
