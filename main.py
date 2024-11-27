import pygame
import random
from icecream import ic


GRID_SIZE = 50
X_AMOUNT = 10
Y_AMOUNT = 10

WIDTH = GRID_SIZE * X_AMOUNT
HEIGHT = GRID_SIZE * Y_AMOUNT

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def sequence(state: int, amount: int) -> list[bool]:
    assert state in [0, 1]
    return [i % 2 == state for i in range(amount)]


def find_group(x: int, y: int, visited: set = set()):
    ic(x, y)
    if (x, y) in visited:
        return visited

    visited.add((x, y))

    if x > 0 and not x_sequences[x - 1][y]:
        visited |= find_group(x - 1, y, visited)
    if x < X_AMOUNT - 1 and not x_sequences[x][y]:
        visited |= find_group(x + 1, y, visited)
    if y > 0 and not y_sequences[x - 1][y]:
        visited |= find_group(x, y - 1, visited)
    if y < Y_AMOUNT - 1 and not y_sequences[x][y]:
        visited |= find_group(x, y + 1, visited)
    return visited


def reload_sequences():
    global x_sequences, y_sequences
    x_sequences = [
        sequence(random.choice([0, 1]), X_AMOUNT) for _ in range(Y_AMOUNT - 1)
    ]
    y_sequences = [
        sequence(random.choice([0, 1]), Y_AMOUNT) for _ in range(X_AMOUNT - 1)
    ]


global x_sequences, y_sequences
reload_sequences()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Check if 'R' is pressed
                reload_sequences()

    screen.fill("white")
    x, y = (0, 0)
    group = find_group(x, y)
    # for g in group:
    #     x, y = g
    #     pygame.draw.rect(
    #         screen, "blue", (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    #     )

    for x_index, seq in enumerate(y_sequences, 1):
        for y_index, state in enumerate(seq, 0):
            if state:
                pygame.draw.line(
                    screen,
                    "black",
                    (x_index * GRID_SIZE, y_index * GRID_SIZE),
                    (x_index * GRID_SIZE, y_index * GRID_SIZE + GRID_SIZE),
                    2,
                )

    for y_index, seq in enumerate(x_sequences, 1):
        for x_index, state in enumerate(seq, 0):
            if state:
                pygame.draw.line(
                    screen,
                    "black",
                    (x_index * GRID_SIZE, y_index * GRID_SIZE),
                    (x_index * GRID_SIZE + GRID_SIZE, y_index * GRID_SIZE),
                    2,
                )

    queue = [(x, y) for x in range(X_AMOUNT) for y in range(Y_AMOUNT)]

    pygame.display.flip()
    clock.tick(1)

pygame.quit()
