import sys, pygame, math
from pygame.locals import *
import time
import pygame.time
import pygame.font
import collision
import draw
pygame.init()

clock = 0

size = width, height = 640, 480

draw.init(width,height)

        


# shape = {'id': id, 'pos':[x,y], 'poly':[[x1,y1],[x2,y2],...]}

# shape = {'pos':[x,y], 'type': type, 'data': xxxxx}

# object = {'id': id, 'type':type, 'shape': shape}

#shapes = {}

objects = {}
large = 0

scale = 40

def make_map(level):
    world_map = {}
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j]:
                world_map[(i,j)] = {'cord':(i,j), 'next':None, 'dist':9999999}

    return world_map

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
        for i,j in [(-1,0),(1,0),(0,-1),(0,1)]:  
            if world.get((nx+i, ny+j),None) and world[n]['next'] != (nx+i, ny+j) and world[(nx+i,ny+j)]['dist'] > world[n]['dist'] + pow(pow(i,2) + pow(j,2),0.5):
                nodes.append(world[(nx+i,ny+j)]['cord'])
                world[(nx+i,ny+j)]['next'] = n
                #print world[(nx+i,ny+j)]['dist'], ', ', world[n]['dist'] + pow(pow(i,2) + pow(j,2),0.5)
                world[(nx+i,ny+j)]['dist'] = world[n]['dist'] + pow(pow(i,2) + pow(j,2),0.5)
    return world

level = [[0,0,1,1,1,1,0,0],
         [0,0,1,1,0,0,0,0],
         [0,1,1,1,0,0,0,0],
         [0,1,1,0,0,0,0,0],
         [0,1,1,1,0,0,1,1],
         [0,0,1,1,1,1,1,0],
         [0,0,0,0,1,1,0,0]]

world_map = make_map(level)
world_map = pathing(world_map,(4,7))


#type: 1 = point, 2 = circle, 4 = poly
def shape_build(type, rad=None, poly=None):
    shape = {}
    shape['type'] = type
    if rad:
        shape['rad'] = rad
    if poly:
        shape['poly'] = poly
    return shape    

class Creep:
    def __init__(self, start, speed=1.0, debug=False):
        global objects, large
        id = 0
        while id in objects:
            id += 1
        large = max(large, id)
        self.id = id
        self.type = 'creep'
        self.x = start[0]*scale+scale
        self.y = start[1]*scale+scale
        self.speed = speed
        self.node = world_map[start]['next']
        self.shape = shape_build(2, rad=5)
        self.debug = debug
        objects[id] = self
        

    def update(self):
        if self.node == None:
            #self.node = 1
            #self.x,self.y = self.route[0]
            object_kill(self.id)
        else:
            #print self.node
            dx,dy = self.node
            diff_x = dx*scale+scale-self.x
            diff_y = dy*scale+scale-self.y
            dist = pow(pow(diff_x,2) + pow(diff_y,2),0.5)
            dir = math.atan2(diff_y, diff_x)

            if dist < 0.5:
                self.node = world_map[self.node]['next']
            else:
                #mx = self.speed * diff_x/(abs(diff_x)+abs(diff_y))
                #my = self.speed * diff_y/(abs(diff_x)+abs(diff_y))
                mx = min(self.speed, dist) * math.cos(dir)
                my = min(self.speed, dist) * math.sin(dir)
                #print x,',', y
                self.x,self.y = self.x+mx, self.y+my

        if self.debug:
            draw.draw_text('node: '+str(self.node), (0,15), 255, 255, 255)
            draw.draw_text('diff: '+str(diff_x)+','+str(diff_y), (0,30), 255, 255, 255)
            draw.draw_text('pos: '+str((self.x,self.y)), (0,45), 255, 255, 255)
            draw.draw_text('dest: '+str((dx,dy)), (0,60), 255, 255, 255)
            draw.draw_text('len: '+str(len(self.route)), (0,75), 255, 255, 255)
            

    def draw(self):
        draw.draw_circle((int(self.x),int(self.y)), self.shape['rad'], 200, 255, 200)

class Tower:
    def __init__(self, x, y, range, speed, debug=False):
        global objects, large
        id = 0
        while id in objects:
            id += 1
        large = max(large, id)

        self.id = id
        self.type = 'tower'
        self.x = x
        self.y = y
        self.range = range
        self.speed = speed
        self.cooldown = 0
        
        self.shape = shape_build(2, rad=8)
        self.debug = debug
        
        objects[id] = self
        
    def update(self):
        if self.cooldown > 0:
            self.cooldown = max(self.cooldown - self.speed, 0)
            
        else:
            target_id = -1
            close = 0
            for o in [o for o in objects.values() if o.id != self.id and o.type == 'creep']:
               dist = pow(pow(o.x-self.x,2) + pow(o.y-self.y,2),0.5)
               if dist <= self.range and (dist < close or target_id == -1):
                   close = dist
                   target_id = o.id

            if target_id >= 0:
                #print 'fire at target: ', target_id
                Beam(self.x, self.y, objects[target_id].x, objects[target_id].y)
                self.cooldown = 1000
                object_kill(target_id)
                
        if self.debug:
            draw.draw_text('cooldown: '+str(self.cooldown), (0,15), 255, 255, 255)
        
    def draw(self):
        draw.draw_circle((int(self.x),int(self.y)), self.shape['rad'], 250, 100, 100)
        if self.cooldown > self.speed:
            draw.draw_arc((int(self.x),int(self.y)), self.shape['rad'], 0, 2*math.pi*self.cooldown/1000, 100, 250, 100, 4)
            draw.draw_arc((int(self.x),int(self.y)), self.shape['rad'], 0.1, 2*math.pi*self.cooldown/1000, 100, 250, 100, 4)
            draw.draw_arc((int(self.x),int(self.y)), self.shape['rad'], 0.2, 2*math.pi*self.cooldown/1000, 100, 250, 100, 4)

class Beam:
    def __init__(self, x1, y1, x2, y2):
        global objects, large
        id = 0
        while id in objects:
            id += 1
        large = max(large, id)
        self.id = id
        self.type = 'beam'
        
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.lifetime = 50
        self.age = 0

        objects[id] = self

    def update(self):
        if self.age >= self.lifetime:
            object_kill(self.id)
            
        self.age += 1

    def draw(self):
        draw.draw_line((self.x1, self.y1), (self.x2, self.y2), 255*(self.lifetime-self.age)/self.lifetime, 0, 0, 2)

def object_kill(id):
    global objects
    objects.pop(id)

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
            Tower(mx, my, 40, 50)

    """
    d_key = []
    for k in spawner:
        if k <= clock:
            for x in spawner.get(k,[]):
                polygon=[(-20,-20),(20,-20),(20,20),(-20,20)]
                object_build(4,(x,100), shape_build(4, poly=polygon))
            d_key.append(k)
    for k in d_key:
        del spawner[k]
    """

    count += 1
    if count > 10:
        count = 0
        Creep(start=(0,5), speed=2.0)
        
    for n in world_map.values():
        pos = map(lambda a:a*scale, n['cord'])
        draw.fill(pos[0]+scale/2+1,pos[1]+scale/2+1,scale-2,scale-2,100,100,200) 
        #screen.fill((100,100,200), (pos[0]+1,pos[1]+1,scale-2,scale-2))

    #objects[0]['pos'] = m_pos

    #update loop
    for o in objects.values():
        o.update()


    #draw loop
    for o in objects.values():
        o.draw()

    #for p in route:
    #    draw.draw_circle(p,2, 0,100,150)
    #for i in range(len(route)-1):
    #    draw.draw_line(route[i],route[i+1], 0,100,150)

    
    draw.draw_text(str(clock/1000.0), (0,0), 255, 255, 255)
    
    draw.flip()

    time.sleep(0.02)

pygame.quit()
