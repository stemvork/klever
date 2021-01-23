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
    def __init__(self, layer, ypos=25, color=None):
        super().__init__(self)
        self.layer = layer
        self.scores = []
# (17) need to keep track of req labels
        self.reqs = []
        self.color = color
        self.whites = [self.square(i, ypos) for i in range(11)]
# (7) labels for green fields in top margin
    def square(self, i, ypos):
        size = 40
        pos = (25+35*i,ypos)
        height = 60 if self.color == colors[2] else size
        self.layer.add_rect(
            color=self.color,width=size,height=height,pos=pos)
        size = height = 30
        white = self.layer.add_rect(
            color='white',width=size,height=height,pos=pos)
        if self.color == colors[2]:
            self.layer.add_label(str(int(0.5*(i+1)*(i+2))),
                    color='black',fontsize=11,align='center',
                    pos=(pos[0]+2,pos[1]-18))
# (15) labels for green field requirements
            self.reqs.append(self.layer.add_label("≥"+"12345123456"[i],
                    color='black',fontsize=11,align='center',
                    pos=(pos[0]+2,pos[1]+4)))
# (8) labels for oranges fields in squares
        if self.color == colors[3]:
            if i in [3, 6, 8, 10]:
                self.layer.add_label("x2",
                        color=colors[3],fontsize=13,align='center',
                        pos=(pos[0]+2,pos[1]+4))
# (9) less than sign polygons for purple fields
        if self.color == colors[4]:
            if i > 0:
                self.lt(pos)
        return white
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

# (13) return false if invalid move
    def play(self, value):
        if self.color == colors[2]: # green
            if len(self.scores) < 11:
                if int("12345123456"[len(self.scores)]) <= value:
                    self.scores.append(True)
                    self.cross(value)
                    print(f"Scored {len(self.scores)}")
                    return True
        if self.color == colors[3]: # orange
            if len(self.scores) < 11:
                self.scores.append(True)
                self.cross(value)
                print(f"Scored {len(self.scores)}")
                return True
        if self.color == colors[4]: # purple
            if len(self.scores) < 11:
                if len(self.scores) == 0 or value > self.scores[-1]\
                        or self.scores[-1] == 6:
                    self.scores.append(value)
                    self.cross(value)
                    print(f"Scored {len(self.scores)}")
                    return True
        return False
    def cross(self, value):
        cindex = len(self.scores)-1
        pos = self.whites[cindex].pos
        tpos = (pos[0]+2,pos[1]+4)
        if self.color == colors[2]: # green
# (16) larger cross, but also remove the label behind it 
            self.layer.add_label("X",pos=add((3,2),tpos),
                    align='center',fontsize=17, color='black')
            self.reqs[cindex].delete()
            print(len(self.reqs))
        if self.color in [colors[3], colors[4]]: # orange or purple
            self.layer.add_label(str(value),align='center',fontsize=13,
                    color='black',pos=tpos)

tops    = [scene.height-d for d in [105,65,25]] # actually ypos
greens  = Fields(scene.layers[10], ypos=tops[0], color=colors[2])
oranges = Fields(scene.layers[10], ypos=tops[1], color=colors[3])
purples = Fields(scene.layers[10], ypos=tops[2], color=colors[4])

# (2) die needs to be thrown, drawn and grouped (no dots)
class Dice(w.Group):
# (20) allow the making of empty dice object
    def __init__(self, layer, empty=False):
        super().__init__(self)
        self.layer = layer
        self.pos = (0, 0)
        # self.dice = [self.die(i) for i in range(6)]
# (18) change from dice to groups of values, rects and dots
        if not empty:
            ids, values, rects, dots = zip(*[self.die(i) for i in range(6)])
            self.ids = list(ids)
            self.values = list(values)
            self.rects = w.Group(rects)
            self.dots = w.Group(dots)
        else:
            self.ids = []
            self.values = []
            self.rects = w.Group([])
            self.dots = w.Group([])
# (19) get the bound union of all the dice bounds
    def get_bound(self):
        _bound = self.rects[0].bounds
        for rect in self.rects[1:]:
            _bound = _bound.union(rect.bounds)
        return _bound
    def die(self, i, value=None):
        rect = self.layer.add_rect(
            color=colors[i],width=30,height=30,pos=(35*i,0))
        value = random.randint(1,6) if not value else value
        dots = w.Group(self.adddots(rect.pos, value))
# (22) include the color index in the tuple
        return (i, value, rect, dots)
    def move(self, pos):
        pos = add((-self.get_bound().width/2+15,0),pos)
        self.rects.pos = pos
        self.dots.pos  = pos
    def select(self, pos): # returns index only
        # return list(filter(lambda x: x[1].bounds.collidepoint(pos), self.dice))[0]
        return [i for i, rect in enumerate(self.rects) if\
                rect.bounds.collidepoint(pos)][0]
        # return [i for i, die in enumerate(self.dice) if # TODO
        #         die[1].bounds.collidepoint(pos)][0]
# (21) use add and take for moving to dice or to silver
    def add(self, die): # color index i/c and value v
        i, v, r, d = die
        r.delete()
        d.clear()
        i, value, rect, dot = self.die(i, v)
        self.values.append(value)
        self.rects.append(rect)
        self.dots.append(dot)
    def take(self, i):
        return self.ids.pop(i), self.values.pop(i), self.rects.pop(i), self.dots.pop(i)
    def discard(self, dindex):
        self.rects[dindex].clear()
        self.dots[dindex].clear()
        self.ids.pop(dindex)
        self.values.pop(dindex)
        self.rects.pop(dindex)
        self.dots.pop(dindex)
    def throw(self, i=None):
        # values, rects, dots = zip(*self.dice)
        [dot.clear() for dot in self.dots]
        self.ids    = [0, 1, 2, 3, 4, 5]
        self.values = [random.randint(1,6) for i in range(6)]
        self.dots   = [w.Group(self.adddots(rect.pos, value)) 
                for rect, value in zip(self.rects, self.values)]
        # self.dice = list(zip(new_values, rects, new_dots))
# (5) die needs to have dots drawn
    def adddots(self, pos, value):
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
        return ", ".join([f"{i}:{v}" for i, v in zip(self.ids, self.values)])

dice = Dice(scene.layers[20])
dice.move((scene.width/2, 25))

scene.layers[30].add_rect(color='#444444',width=scene.width,
        height=40,pos=(scene.width/2, 70))
silver = Dice(scene.layers[30], empty=True)
silver.centerx = scene.width/2
# silver.move((scene.width/2, 70))

# (4) press space to test new turn/throwing dice again
@w.event
def on_key_down(key):
    if key == w.keys.SPACE:
        dice.throw()
        print(dice)

# (10) click a die to play it to a field
cdtf_expect = 0 # 0 for die, 1 for field
cdtf_die = None
def click_die_then_field(pos):
    global cdtf_expect, cdtf_die
    mx, my = pos
    if cdtf_expect == 0:
        if my < 60 and mx < 240:
            cdtf_die = dice.select(pos) # index only
            cdtf_expect = 1
    elif cdtf_expect == 1:
        if my > tops[0]-30: # actually pressing field
            play_to_field(pos)
    else:
        print("Unexpected behavior 1.")

# (12) put the value into the field if purple or orange
# (14) put an X in the field if green
def play_to_field(pos):
    global cdtf_expect, cdtf_die
    mx, my  = pos
    success = False
    value   = dice.values[cdtf_die]

    if my > tops[0]-10 and my < tops[0]+30:
        success = greens.play(value)
    elif my > tops[1] and my < tops[1]+20:
        success = oranges.play(value)
    elif my > tops[2]-20 and my < tops[2]+20:
        success = purples.play(value)
    if success:
        cdtf_expect = 0
        # dice.discard(cdtf_die) # for now, discard die, later silver platter
        silver.add(dice.take(cdtf_die))
        cdtf_die = None
    else: # do nothing if move was not valid
        cdtf_expect = 0
        cdtf_die = None

# (11) determine desired interactions through state
state = 0

@w.event
def on_mouse_down(pos):
    if state == 0:
        click_die_then_field(pos)

w.run()
