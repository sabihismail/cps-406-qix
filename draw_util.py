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
    vertices.append(lines[0][0])

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
