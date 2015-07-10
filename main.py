import sys, pygame, math
from pygame.locals import *
import time
import pygame.time
import pygame.font
import pygame.image
import collision
import draw
from random import randint

pygame.init()

clock = 0

size = width, height = 640, 480

draw.init(width,height)

# shape = {'id': id, 'pos':[x,y], 'poly':[[x1,y1],[x2,y2],...]}

# shape = {'pos':[x,y], 'type': type, 'data': xxxxx}

# object = {'id': id, 'type':type, 'shape': shape}

#shapes = {}

object_dict = {'creep':{}, 'tower':{}, 'projectile':{}, 'particle':{}}
large_dict =  {'creep':-1, 'tower':-1, 'projectile':-1, 'particle':-1}

kill_list = set()

scale = 15
tile_size = 11
tile_border_size = (scale-tile_size)/2

def make_map(level):
    world_map = {}
    
    #for i in range(len(level)):
    #    for j in range(len(level[i])):
    #        if level[i][j]:
    #            world_map[(i,j)] = {'cord':(i,j), 'next':None, 'dist':9999999}

    width = 0
    i = -1
    j = 0
    for c in level:
        i += 1
        if c == '1':
            world_map[(i,j)] = {'cord':(i,j), 'next':None, 'dist':9999999}
            width = max(i, width)
        elif c == ':':
            j += 1
            i = -1

    return world_map, width+1, j+1

def pathing(world, dest):
    nodes = [dest]
    world[dest]['dist'] = 0
    while nodes:
        #print nodes
        #print '------------'
        n = nodes[0]
        nodes.remove(n)
        nx = world[n]['cord'][0]
        ny = world[n]['cord'][1]
        #for i,j in [(-1,0),(1,0),(0,-1),(0,1)]:
        for i,j in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            if world.get((nx+i, ny+j),None) and world[n]['next'] != (nx+i, ny+j) and world[(nx+i,ny+j)]['dist'] >= world[n]['dist'] + pow(pow(i,2) + pow(j,2),0.5):
                nodes.append(world[(nx+i,ny+j)]['cord'])
                world[(nx+i,ny+j)]['next'] = n
                #print world[(nx+i,ny+j)]['dist'], ', ', world[n]['dist'] + pow(pow(i,2) + pow(j,2),0.5)
                world[(nx+i,ny+j)]['dist'] = world[n]['dist'] + pow(pow(i,2) + pow(j,2),0.5)
    return world



level = ['00000110000:',
         '00000110000:',
         '00011110000:',
         '00011000000:',
         '00011000000:',
         '00010000000:',
         '00011000000:',
         '00001111111:',
         '00000000000:',
]

level = ''.join(level)

world_map, world_map_width, world_map_height = make_map(level)
world_map = pathing(world_map,(10,7))


#type: 1 = point, 2 = circle, 4 = poly
def shape_build(type, rad=None, poly=None):
    shape = {}
    shape['type'] = type
    if rad:
        shape['rad'] = rad
    if poly:
        shape['poly'] = poly
    return shape    

class Object:
    def register(self):
        global object_dict, large_dict
        id = 0
        while id in object_dict[self.type]:
            id += 1
        large_dict[self.type] = max(large_dict[self.type], id)
        self.id = id
        object_dict[self.type][id] = self

class Test_Creep(Object):
    def __init__(self, start, speed=1.0, debug=False): 
        self.type = 'creep'
        self.x = start[0]*scale + scale/2
        self.y = start[1]*scale + scale/2
        self.speed = speed
        self.node = world_map[start]['next']
        self.shape = shape_build(2, rad=5)
        self.debug = debug
        self.dx = self.node[0]*scale + scale/2 #+ randint(-scale/3,scale/3)
        self.dy = self.node[1]*scale + scale/2 #+ randint(-scale/3,scale/3)
        self.max_hp = 10.0
        self.hp = 10.0

        self.register()

    def update(self):
        if self.node == None:
            #self.node = 1
            #self.x,self.y = self.route[0]
            object_kill(self.id, 'creep')
        else:
            #print self.node
            #dx,dy = self.node
            diff_x = self.dx-self.x
            diff_y = self.dy-self.y
            dist = pow(pow(diff_x,2) + pow(diff_y,2),0.5)
            dir = math.atan2(diff_y, diff_x)

            if dist < scale/5:
                self.node = world_map[self.node]['next']
                if self.node:
                    self.dx = self.node[0]*scale + scale/2 #+ randint(-scale/3,scale/3)
                    self.dy = self.node[1]*scale + scale/2 #+ randint(-scale/3,scale/3)
            else:
                #mx = self.speed * diff_x/(abs(diff_x)+abs(diff_y))
                #my = self.speed * diff_y/(abs(diff_x)+abs(diff_y))
                mx = min(self.speed, dist) * math.cos(dir)
                my = min(self.speed, dist) * math.sin(dir)
                #print x,',', y
                self.x,self.y = self.x+mx, self.y+my

        if self.debug:
            draw.draw_text('node: '+str(self.node), (0,15), 255, 255, 255)
            draw.draw_text('pos: '+str((self.x,self.y)), (0,45), 255, 255, 255)
            draw.draw_text('dest: '+str((self.dx,self.dy)), (0,60), 255, 255, 255)
 

    def draw(self):
        draw.draw_circle((int(self.x),int(self.y)), self.shape['rad'], 50, 150, 255)
        draw.draw_circle((int(self.x),int(self.y)), int(self.shape['rad']*self.hp/self.max_hp), 255, 100, 200)

    def damage(self, d):
        self.hp = max(self.hp - d, 0)
        if self.hp <= 0:
            object_kill(self.id, 'creep')
        

class Tower_beam(Object):
    def __init__(self, x, y, range, speed, debug=False):
        self.type = 'tower'
        self.x = x
        self.y = y
        self.range = range
        self.speed = speed
        self.cooldown = 0
        
        self.shape = shape_build(2, rad=8)
        self.debug = debug
        
        self.register()
        
    def update(self):
        if self.cooldown > 0:
            self.cooldown = max(self.cooldown - self.speed, 0)
            
        else:
            target_id = -1
            close = 0
            for c in object_dict['creep'].values():
               dist = pow(pow(c.x-self.x,2) + pow(c.y-self.y,2),0.5)
               if dist <= self.range and (dist < close or target_id == -1):
                   close = dist
                   target_id = c.id

            if target_id >= 0:
                #print 'fire at target: ', target_id
                Beam(self.x, self.y, object_dict['creep'][target_id].x, object_dict['creep'][target_id].y)
                self.cooldown = 1000
                #object_kill(target_id)
                object_dict['creep'][target_id].damage(2)
                
        if self.debug:
            draw.draw_text('cooldown: '+str(self.cooldown), (0,15), 255, 255, 255)
        
    def draw(self):
        draw.draw_circle((int(self.x),int(self.y)), self.shape['rad'], 250, 100, 100)
        draw.draw_circle((int(self.x),int(self.y)), self.shape['rad'] * (1000-self.cooldown)/1000, 100, 250, 100)
        #if self.cooldown > self.speed:
        #    draw.draw_arc((int(self.x),int(self.y)), self.shape['rad'], 0, 2*math.pi*self.cooldown/1000, 100, 250, 100, 4)


class Tower_missile(Object):
    def __init__(self, x, y, range, speed, debug=False):
        self.type = 'tower'
        self.x = x
        self.y = y
        self.range = range
        self.speed = speed
        self.cooldown = 0
        
        self.shape = shape_build(2, rad=8)
        self.debug = debug
        self.target_id = -1
        
        self.register()
        
    def update(self):
        if self.cooldown > 0:
            self.cooldown = max(self.cooldown - self.speed, 0)
            
        else:
            target_id = -1
            close = 0
            for c in object_dict['creep'].values():
               dist = pow(pow(c.x-self.x,2) + pow(c.y-self.y,2),0.5)
               if dist <= self.range and (dist < close or target_id == -1):
                   close = dist
                   target_id = c.id

            self.target_id = target_id
            if target_id >= 0:
                #print 'fire at target: ', target_id
                Missile(self.x, self.y, target_id)
                self.cooldown = 1000
                
        if self.debug:
            draw.draw_text('cooldown: '+str(self.cooldown), (0,15), 255, 255, 255)
            draw.draw_text('target: '+str(self.target_id), (0,30), 255, 255, 255)
        
    def draw(self):
        draw.draw_circle((int(self.x),int(self.y)), self.shape['rad'], 250, 100, 100)
        draw.draw_circle((int(self.x),int(self.y)), self.shape['rad'] * (1000-self.cooldown)/1000, 100, 250, 100)
        #if self.cooldown > self.speed:
        #    draw.draw_arc((int(self.x),int(self.y)), self.shape['rad'], 0, 2*math.pi*self.cooldown/1000, 100, 250, 100, 4)


class Beam(Object):
    def __init__(self, x1, y1, x2, y2):
        self.type = 'particle'
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.lifetime = 50
        self.age = 0

        self.register()

    def update(self):
        if self.age >= self.lifetime:
            object_kill(self.id, self.type)
            
        self.age += 1

    def draw(self):
        draw.draw_line((self.x1, self.y1), (self.x2, self.y2), 255*(self.lifetime-self.age)/self.lifetime, 0, 0, 2)

class Missile(Object):
    def __init__(self, x, y, target_id):
        self.type = 'projectile'
        
        self.x = x
        self.y = y
        self.target_id = target_id
        self.lifetime = 100
        self.speed = 2.5
        self.age = 0
        self.dir = 0

        self.register()

    def update(self):
        if self.age >= self.lifetime or object_dict['creep'].get(self.target_id, None) == None:
            object_kill(self.id, self.type)

        else:
            self.age += 1

            tx = object_dict['creep'][self.target_id].x
            ty = object_dict['creep'][self.target_id].y

            diff_x = tx-self.x
            diff_y = ty-self.y
            dist = pow(pow(diff_x,2) + pow(diff_y,2),0.5)
            self.dir = math.atan2(diff_y, diff_x)

            if dist < 4:
                object_kill(self.id, self.type)
                object_dict['creep'][self.target_id].damage(5)
            else:
                mx = min(self.speed, dist) * math.cos(self.dir)
                my = min(self.speed, dist) * math.sin(self.dir)
                #print x,',', y
                self.x,self.y = self.x+mx, self.y+my
        
    def draw(self):
        poly = []
        for x,y in [(0,0),(8,2),(0,4)]:
            newx = (x*math.cos(self.dir) - y*math.sin(self.dir))
            newy = (x*math.sin(self.dir) + y*math.cos(self.dir))
            poly.append((self.x+newx, self.y+newy))
        draw.draw_poly(poly, 255, 255, 255)

def object_kill(id, type):
    global kill_list
    kill_list.add((id, type))

def get_shape(obj):
    shape = obj['shape']
    type = shape['type']
    pos = obj['pos']
    
    if type == 1:
        return (type, pos)
    if type == 2:
        return (type, pos, shape['rad'])
    if type == 4:         
        poly = []
        for p in shape['poly']:
            poly.append(t_add(p,pos))
        return (type, poly)


def t_add(t1,t2):
    return map(lambda a,b: a+b,t1,t2)
        


#pathing test
#object_build('creep', (200, 100), shape_build(2, rad = 4))

route = [(200,100), (200,250), (300,250), (350, 200), (400, 300), (100, 300)]
#Creep(route, speed=0.5)
#Creep(route, speed=1.0)
#Creep(route, speed=1.5)
#Creep(route, speed=2.0)
#Creep(route, speed=2.5)
#Creep(route, speed=3.0)
#Creep(route, speed=3.5)
#Tower(300, 270, 30, 50)
#Tower(350, 230, 30, 50)

tile_id = draw.load_image('tile_15x15_center.tif')
tile_corner_id = draw.load_image('tile_15x15_corner.tif')
tile_side_id = draw.load_image('tile_15x15_side.tif')

count = 0
#main loop
done = False
while not done:
    clock = pygame.time.get_ticks()
    m_pos = mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                Tower_missile(mx, my, 150, 20)
            if event.button == 3:
                Tower_beam(mx, my, 40, 50)


    count += 1
    if count > 20:
        count = 0
        Test_Creep(start=(6,0), speed=1.0)

    for x in range(world_map_width):
        for y in range(world_map_height):
            tile = world_map.get((x,y), None)
            if tile:
                pos_x = x*scale+tile_border_size
                pos_y = y*scale+tile_border_size
                draw.draw_image(tile_id, pos_x, pos_y)

    for x in range(world_map_width+1):
        for y in range(world_map_height+1):
            t_left  = bool(world_map.get((x-1,y-1)))
            t_right = bool(world_map.get((x,y-1)))
            b_left  = bool(world_map.get((x-1,y)))
            b_right = bool(world_map.get((x,y)))
            if t_left or t_right or b_left or b_right:
                pos_x = x*scale-tile_border_size
                pos_y = y*scale-tile_border_size
                draw.draw_image(tile_corner_id, pos_x, pos_y)
            if b_left or b_right:
                pos_x = x*scale-tile_border_size
                pos_y = y*scale+tile_border_size
                draw.draw_image(tile_side_id, pos_x, pos_y)
            if t_right or b_right:
                pos_x = x*scale+tile_border_size
                pos_y = y*scale-tile_border_size
                draw.draw_image(tile_side_id, pos_x, pos_y, angle=-90)
                
    
    #for n in world_map.values():
        #pos = map(lambda a:a*scale, n['cord'])
        #draw.draw_image(tile_id, pos[0], pos[1])
        #draw.draw_poly([], 255,150,150)
        #draw.fill(pos[0]+scale/2+1,pos[1]+scale/2+1,scale-2,scale-2,100,100,200) 
        #screen.fill((100,100,200), (pos[0]+1,pos[1]+1,scale-2,scale-2))

    #objects[0]['pos'] = m_pos

    #update loop
    for type in object_dict:
        for obj in object_dict[type].values():
            obj.update()

    for id, type in kill_list:
        object_dict[type].pop(id)

    kill_list = set()

    #draw loop
    for type in object_dict:
        for obj in object_dict[type].values():
            obj.draw()

    
    draw.draw_text(str(clock/1000.0), (0,0), 255, 255, 255)
    
    draw.flip()

    time.sleep(0.02)

pygame.quit()
