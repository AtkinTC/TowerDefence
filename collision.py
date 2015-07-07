def t_add(t1,t2):
    return map(lambda a,b: a+b,t1,t2)

def collide(s1, s2):
    #s = type, pos, data
    if s1[0] > s2[0]:
        st = s1
        s1 = s2
        s2 = st

    #def position_poly(s):
    #    shape = []
    #    for p in s[2]:
    #        shape.append(t_add(p,s[1]))
    #    return shape

    type = s1[0] + s2[0]
    #point on point
    if type == 2:
        return collide_pnt2pnt(s1[1],s2[1])
    #point on circle
    elif type == 3:
        return collide_pnt2circle(s1[1],s2[1],s2[2])
    #circle on circle
    elif type == 4:
        return collide_circle2circle(s1[1],s1[2],s2[1],s2[2])
    #point on poly
    elif type == 5:
        return collide_pnt2pol(s1[1], s2[1])
    #circle on poly
    elif type == 6:
        return collide_circle2pol(s1[1],s1[2],s2[1])
    #poly on poly
    elif type == 8:
        return collide_pol2pol(s1[1],s2[1])
    
"""
def collide(pos1, poly1, pos2, poly2):
    poly1_t = []
    for p in poly1:
        poly1_t.append(t_add(pos1, p))
    poly1 = poly1_t
    poly2_t = []
    for p in poly2:
        poly2_t.append(t_add(pos2, p))
    poly2 = poly2_t
    
    if len(poly1) < 1 or len(poly2) < 1:
        return False
    if len(poly1) > len(poly2):
        polyt = poly1
        poly1 = poly2
        poly2 = polyt
    if len(poly1) > 1:
        return collide_pol2pol(poly1,poly2)
    elif len(poly2) > 1:
        return collide_pnt2pol(poly1,poly2)
    else:
        return collide_pnt2pnt(poly1,poly2)
"""

def collide_pnt2pnt(p1,p2):
    if p1 == p2:
        return p1
    return False

def collide_pnt2circle(p1, p2, r2):
    return False

def collide_circle2circle(p1,r1,p2,r2):
    return Faqlse

def collide_pnt2pol(p1, poly2):
    t_s = poly2 + [poly2[0]]

    c = p1
    d = (c[0]+1, c[1])

    count = 0

    for i in range(len(poly2)):
        a = t_s[i]
        b = t_s[i+1]
        p = intersect_bound(a,b,c,d, rb=False)
        if p:
            count += 1

    if (count%2)==1:
        return c
    else:
        return False

def collide_circle2pol(p1, r1, poly2):
    return False

def collide_pol2pol(poly1, poly2):
    t_s1 = poly1 + [poly1[0]]
    t_s2 = poly2 + [poly2[0]]
    #print t_s1, t_s2
    col = False
    for i in range(len(poly1)):
        for j in range(len(poly2)):
            a = t_s1[i]
            b = t_s1[i+1]
            c = t_s2[j]
            d = t_s2[j+1]
            #print a, b, c, d
            p = intersect_bound(a,b,c,d)
            #print p
            if p:
                return p
                #col = True
                #break
        #if col:
            #break
    return col

def intersect_bound(a,b,c,d, lb=True, rb=True, ub=True, bb=True):
    min1x = min(a[0],b[0])
    min1y = min(a[1],b[1])
    max1x = max(a[0],b[0])
    max1y = max(a[1],b[1])

    min2x = min(c[0],d[0])
    min2y = min(c[1],d[1])
    max2x = max(c[0],d[0])
    max2y = max(c[1],d[1])

    #print min1x, max2x
    #if min1x > max2x or min2x > max1x or min1y > max2y or min2y > max2y:
    #    return None

    x1 = max(min1x, min2x)
    x2 = min(max1x, max2x)
    y1 = max(min1y, min2y)
    y2 = min(max1y, max2y)

    p = intersect(a,b,c,d)
    if p:
        px, py = p
    else:
        return None
    
    if not lb:
        x1 = px
    if not rb:
        x2 = px
    if not ub:
        y1 = py
    if not bb:
        y2 = py

    if x1 <= px <= x2 and y1 <= py <= y2:
        #print px, py
        return (px, py)
    return None

def intersect(a,b,c,d):
    de = (a[0]-b[0])*(c[1]-d[1]) - (a[1]-b[1])*(c[0]-d[0])
    if de == 0:
        return None

    nx = (a[0]*b[1]-a[1]*b[0])*(c[0]-d[0]) - (a[0]-b[0])*(c[0]*d[1]-c[1]*d[0])
    ny = (a[0]*b[1]-a[1]*b[0])*(c[1]-d[1]) - (a[1]-b[1])*(c[0]*d[1]-c[1]*d[0])

    px = float(nx)/float(de)
    py = float(ny)/float(de)

    return (px, py)
