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
    def __init__(self, layer):
        super().__init__(self)
        self.layer = layer
        [self.square((25+35*i,65)) for i in range(11)]
    def square(self, pos):
        self.layer.add_rect(
            color='white',width=30,height=30,pos=pos)

greens = Fields(scene.layers[10])

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
