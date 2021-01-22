import wasabi2d as w
import random # needed for die

# (3) define some _pretty_ distinguishable colors
colors = ["#fed402","#0477bb","#02a039",
          "#ef7c02","#925ea4", "#ffffff"]

# (6) always add tuples
def add(s,t):
    return tuple(map(sum, zip(s,t)))

# (0) basic scene
scene = w.Scene(width=400,height=400,background='#111111')
scene.title = "Minimal Viable Product"

# (1) field objects are white rects attached to a layer, grouped
class Fields(w.Group):
    def __init__(self, layer, ypos=25, bgcolor=None):
        super().__init__(self)
        self.layer = layer
        [self.square(i, ypos, color=bgcolor) for i in range(11)]
# (7) labels for green fields in top margin
    def square(self, i, ypos, color='white'):
        size = 40
        pos = (25+35*i,ypos)
        height = 60 if color == colors[2] else size
        self.layer.add_rect(
            color=color,width=size,height=height,pos=pos)
        size = height = 30
        self.layer.add_rect(
            color='white',width=size,height=height,pos=pos)
        if color == colors[2]:
            self.layer.add_label(str(int(0.5*(i+1)*(i+2))),
                    color='black',fontsize=11,align='center',
                    pos=(pos[0]+2,pos[1]-18))
# (8) labels for oranges fields in squares
        if color == colors[3]:
            if i in [3, 6, 8, 10]:
                self.layer.add_label("x2",
                        color=colors[3],fontsize=13,align='center',
                        pos=(pos[0]+2,pos[1]+4))
# (9) less than sign polygons for purple fields
        if color == colors[4]:
            if i > 0:
                self.lt(pos)
    def lt(self, pos):
        _lt_bg = self.layer.add_polygon(color=colors[4], fill=True, vertices=\
                        [(-5,0),
                         (+8,-9),
                         (+8,+9),
                        ], pos=(pos[0]-20,pos[1]))
        _lt_fg = self.layer.add_polygon(color='white', fill=True, vertices=\
                        [(-1,0),
                         (+6,-5),
                         (+6,+5),
                        ], pos=(pos[0]-20,pos[1]))
        return (_lt_bg, _lt_fg)


greens  = Fields(scene.layers[10], ypos=scene.height-105, bgcolor=colors[2])
oranges = Fields(scene.layers[10], ypos=scene.height-65, bgcolor=colors[3])
purples = Fields(scene.layers[10], ypos=scene.height-25, bgcolor=colors[4])

# (2) die needs to be thrown, drawn and grouped (no dots)
class Dice(w.Group):
    def __init__(self, layer):
        super().__init__(self)
        self.layer = layer
        self.dice = [self.die(i) for i in range(6)]
    def die(self, i):
        rect = self.layer.add_rect(
            color=colors[i],width=30,height=30,pos=(25+35*i,25))
        value = random.randint(1,6)
        dots = w.Group(self.dots(rect.pos, value))
        return (value, rect, dots)
    def throw(self, i=None):
        values, rects, dots = zip(*self.dice)
        [dot.clear() for dot in dots]
        new_values = [random.randint(1,6) for i in range(6)]
        new_dots   = [w.Group(self.dots(rect.pos, value)) 
                for rect, value in zip(rects, new_values)]
        self.dice = list(zip(new_values, rects, new_dots))
# (5) die needs to have dots drawn
    def dots(self, pos, value):
        if value == 1:
            return [self.dot(pos)]
        if value == 2:
            return [self.dot(pos,(-6,6)),
                    self.dot(pos,(6,-6)),]
        if value == 3:
            return [self.dot(pos,(-8,8)),
                    self.dot(pos,),
                    self.dot(pos,(8,-8)),]
        if value == 4:
            return [self.dot(pos,(6,-6)),
                    self.dot(pos,(6,6)),
                    self.dot(pos,(-6,6)),
                    self.dot(pos,(-6,-6)),]
        if value == 5:
            return [self.dot(pos,(-8,8)),
                    self.dot(pos,(8,8)),
                    self.dot(pos,),
                    self.dot(pos,(-8,-8)),
                    self.dot(pos,(8,-8)),]
        if value == 6:
            return [self.dot(pos,(8,-6)),
                    self.dot(pos,(8,6)),
                    self.dot(pos,(0,6)),
                    self.dot(pos,(0,-6)),
                    self.dot(pos,(-8,6)),
                    self.dot(pos,(-8,-6)),]
        return []
    def dot(self, pos, rel=(0,0)):
        pos = add(pos,rel)
        return self.layer.add_circle(
                radius=2.7,color='#111111',pos=pos)
    def __str__(self):
        return str(list(map(lambda x: x[0], self.dice)))

dice = Dice(scene.layers[20])
print(dice)

# (4) press space to test new turn/throwing dice again
@w.event
def on_key_down(key):
    if key == w.keys.SPACE:
        dice.throw()
        print(dice)

w.run()
