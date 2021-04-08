import pygame

def draw_rect(surface, colour, bounds, line_width=1):
    draw_rect_specific(surface, colour, bounds.x, bounds.y, bounds.width, bounds.height, line_width=line_width)

def draw_rect_specific(surface, colour, x, y, width, height, line_width=1):
    lst = [
        ((x, y), (x, y + height)),
        ((x, y), (x + width, y)),
        ((x, y + height), (x + width, y + height)),
        ((x + width, y), (x + width, y + height))
    ]

    for elem in lst:
        pygame.draw.line(surface, colour, elem[0], elem[1], line_width)

    return lst

def get_lines_by_rect_specific(x, y, width, height):
    lst = [
        ((x, y), (x, y + height)),
        ((x, y + height), (x + width, y + height)),
        ((x + width, y + height), (x + width, y)),
        ((x + width, y), (x, y))
    ]

    return lst

def get_lines_by_rect(bounds):
    return get_lines_by_rect_specific(bounds.x, bounds.y, bounds.width, bounds.height)

def to_vertices_list(lines):
    vertices = [a[0] for a in lines]
    vertices.append(lines[len(lines) - 1][1])

    return vertices

def to_line_list(vertices):
    lines = []

    for i in range(len(vertices) - 1):
        lines.append((vertices[i], vertices[i+1]))

    return lines

def lines_to_dict(lines):
    d = {}

    for line in lines:
        d[line[0]] = line[1]
        d[line[1]] = line[0]

    return d

def vertices_to_dict(vertices):
    lines = to_line_list(vertices)

    d = {}

    for line in lines:
        a = d.get(line[0], [])
        a.append(line[1])

        b = d.get(line[1], [])
        b.append(line[0])

        d[line[0]] = a
        d[line[1]] = b

    return d

def unique_vertices_to_dict(vertices):
    d = vertices_to_dict(vertices)

    for key, value in d.items():
        lst = [x for x in value if x != key]
        lst = list(set(lst))

        d[key] = lst

    return d

# retrieved from https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
def rotate_surface(outer_surface, inner_surface, pos, originPos, angle):
    w, h       = inner_surface.get_size()
    box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot

    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

    rotated_surface = pygame.transform.rotate(inner_surface, angle)

    outer_surface.blit(rotated_surface, origin)
