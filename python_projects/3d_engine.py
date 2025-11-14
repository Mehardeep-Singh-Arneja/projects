import numpy as np
import pygame

vertices = np.array([
    [1, 1, 1],
    [1, 1, -1],
    [1, -1, 1],
    [1, -1, -1],
    [-1, 1, 1],
    [-1, 1, -1],
    [-1, -1, 1],
    [-1, -1, -1],
],dtype=np.double)

projection = np.array([
    [1,0,0],
    [0,1,0],
    [0,0,0]
]
,dtype=np.double)

def rot_x(theta):
    return np.array([
        [1, 0, 0],
        [0, np.cos(theta), -np.sin(theta)],
        [0, np.sin(theta),  np.cos(theta)]
    ])

def rot_z(theta):
    return np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta),  np.cos(theta), 0],
        [0, 0, 1]
    ])


def rot_y(theta):
    return np.array([
        [ np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)]
    ])

def project_point(v, d):
    x, y, z = v
    factor = d / (z + d)
    return np.array([x * factor, y * factor])


def draw_lines(mat):
    edges = [
        (0, 1), (1, 3), (3, 2), (2, 0),
        (4, 5), (5, 7), (7, 6), (6, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]

    for a, b in edges:
        x1 = mat[a][0]
        y1 = mat[a][1]
        x2 = mat[b][0]
        y2 = mat[b][1]
        pygame.draw.line(display, (255,255,0), (x1,y1), (x2,y2), 2)


display = pygame.display.set_mode((1920,1080),pygame.FULLSCREEN|pygame.SCALED)
clock = pygame.time.Clock()

dx,dy,dz = 0.01,0.02,0.01
depth = 3

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                break

    display.fill((0,0,0))

    vertices = np.matmul(vertices,rot_x(dx))
    vertices = np.matmul(vertices, rot_y(dy))
    vertices = np.matmul(vertices, rot_z(dz))
    projected = []

    for v in vertices:
        px, py = project_point(v, depth)
        px = px * 100 + 900
        py = py * 100 + 600
        projected.append([px, py])
        pygame.draw.circle(display, (255, 255, 255), (px, py), 6)

    draw_lines(np.array(projected))
    clock.tick(60)
    pygame.display.flip()
