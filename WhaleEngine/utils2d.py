import math

def distance2D(Entity1,Entity2):
    dx = Entity2.get_position()[0] - Entity1.get_position()[0]
    dy = Entity2.get_position()[1] - Entity1.get_position()[1]
    return math.sqrt(dx**2 + dy**2)

def distance2D_points(pos1,pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    return math.sqrt(dx**2 + dy**2)

def angle_to2D(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    return math.degrees(math.atan2(dy, dx))

def forwardPos2D(pos,angle,distance):
    rad = math.radians(angle)
    return (pos[0] + math.cos(rad) * distance, pos[1] + math.sin(rad) * distance)

def forwardMove2D(angle, distance):
    rad = math.radians(angle)
    return (math.cos(rad) * distance, math.sin(rad) * distance)