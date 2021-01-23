import wasabi2d as w
import random # needed for die
from functools import reduce # for bounds union

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
        self.color = color
        self.whites = [self.square(i, ypos) for i in range(11)]
# (23) the field object also keeps its own scores # TODO: move
        self.scores = []
# (27) proto square function to separate some logic
    def _square(self, pos, color='white', size=30):
        return self.layer.add_rect(
                color=color,width=size,height=size,pos=pos)
# (24) colored square behind white square, try to move labels away
    def square(self, i, ypos):
        pos   = (25+35*i,ypos)
        bg    = self._square(pos, color=self.color, size=40)
        white = self._square(pos)
        return white
# (13) return false if invalid move
    def play(self, value):
# (30) move these color specific checks in play and cross out of field class
        if self.color == colors[2]: # green
            if len(self.scores) < 11:
                if int("12345123456"[len(self.scores)]) <= value:
                    self.scores.append(True)
                    self.cross(value)
                    # print(f"Scored {len(self.scores)}")
                    return True
        if self.color == colors[3]: # orange
            if len(self.scores) < 11:
                self.scores.append(True)
                self.cross(value)
                # print(f"Scored {len(self.scores)}")
                return True
        if self.color == colors[4]: # purple
            if len(self.scores) < 11:
                if len(self.scores) == 0 or value > self.scores[-1]\
                        or self.scores[-1] == 6:
                    self.scores.append(value)
                    self.cross(value)
                    # print(f"Scored {len(self.scores)}")
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
            # print(len(self.reqs))
        if self.color in [colors[3], colors[4]]: # orange or purple
            self.layer.add_label(str(value),align='center',fontsize=13,
                    color='black',pos=tpos)

# (25) separately draw green margin
scene.layers[10].add_rect(color=colors[2],width=scene.width-10,height=15,
        pos=(scene.width/2,scene.height-130))

tops    = [scene.height-d for d in [105,65,25]] # actually ypos
greens  = Fields(scene.layers[10], ypos=tops[0], color=colors[2])
oranges = Fields(scene.layers[10], ypos=tops[1], color=colors[3])
purples = Fields(scene.layers[10], ypos=tops[2], color=colors[4])

# (26) function to write green labels
def green_labels(greens):
# (7) labels for green fields in top margin
    for i, green in enumerate(greens.whites):
        greens.layer.add_label(str(int(0.5*(i+1)*(i+2))),
                color='black',fontsize=11,align='center',
                pos=(green.pos[0]+2,green.pos[1]-19))
# (15) labels for green field requirements, saved in greens group
# (17) in order to delete the label as the greens are filled
        if 'reqs' not in greens.__dict__: greens.reqs = []
        greens.reqs.append(greens.layer.add_label("≥"+"12345123456"[i],
                color='black',fontsize=11,align='center',
                pos=(green.pos[0]+2,green.pos[1]+4)))
green_labels(greens)

# (28) function to write oranges labels
def orange_labels(oranges):
# (8) labels for oranges fields in squares
    for i, orange in enumerate(oranges.whites):
        if i in [3, 6, 8, 10]:
            oranges.layer.add_label("x2",
                    color=colors[3],fontsize=13,align='center',
                    pos=(orange.pos[0]+2,orange.pos[1]+4))
orange_labels(oranges)

# (29) function to write purples less than signs
def purple_labels(purples):
    def lt(self, pos):
        _lt_bg = self.layer.add_polygon(color=colors[4], fill=True, vertices=\
                        [(-5,0), (+8,-9), (+8,+9)], pos=(pos[0]-20,pos[1]))
        _lt_fg = self.layer.add_polygon(color='white', fill=True, vertices=\
                        [(-1,0), (+6,-5), (+6,+5)], pos=(pos[0]-20,pos[1]))
        return (_lt_bg, _lt_fg)
# (9) less than sign polygons for purple fields
    for i, purple in enumerate(purples.whites):
        if i > 0:
            lt(purples, purple.pos)
purple_labels(purples)

# (22) include the color index in the tuple
# (31) in fact, contain color-value-rect-dots in one object
class Die():
    def __init__(self, layer, color=0, value=None): # layer required
        self.color = color
        self.value = value if value else self._throw()
        self.layer = layer
# (32) draws rect and dots to layer
        self.rect  = self._rect()
        self.dots  = w.Group(self._dots())
        self.bounds = self.rect.bounds
# (38) getters and setters for color and value
    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, color):
        self._color = color
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, value):
        self._value = value
# (39) proto function for adding square
    def _rect(self):
        return self.layer.add_rect(color=colors[self.color],width=30,height=30)
# (5) die needs to have dots drawn
    def _dots(self):
        pos = self.rect.pos
        if self.value == 1:
            return [self._dot(pos)]
        if self.value == 2:
            return [self._dot(pos,(-6,6)),
                    self._dot(pos,(6,-6)),]
        if self.value == 3:
            return [self._dot(pos,(-8,8)),
                    self._dot(pos,),
                    self._dot(pos,(8,-8)),]
        if self.value == 4:
            return [self._dot(pos,(6,-6)),
                    self._dot(pos,(6,6)),
                    self._dot(pos,(-6,6)),
                    self._dot(pos,(-6,-6)),]
        if self.value == 5:
            return [self._dot(pos,(-8,8)),
                    self._dot(pos,(8,8)),
                    self._dot(pos,),
                    self._dot(pos,(-8,-8)),
                    self._dot(pos,(8,-8)),]
        if self.value == 6:
            return [self._dot(pos,(8,-6)),
                    self._dot(pos,(8,6)),
                    self._dot(pos,(0,6)),
                    self._dot(pos,(0,-6)),
                    self._dot(pos,(-8,6)),
                    self._dot(pos,(-8,-6)),]
        return []
    def _dot(self, pos, rel=(0,0)):
        pos = add(pos,rel)
        return self.layer.add_circle(radius=2.7,color='#111111',pos=pos)
    def move(self, pos):
        self.rect.pos = pos
        self.dots.pos = pos
# (41) throw the die and refresh the sprites
    def _throw(self):
        return random.randint(1,6)
    def throw(self):
        self.value = self._throw()
        self.dots.delete()
        self.dots = w.Group(self._dots())
        return self.dots

# (2) die needs to be thrown, drawn and grouped (no dots)
class Dice(w.Group):
    def __init__(self, layer, dice=[], ypos=25):
        super().__init__(self)
        self.layer = layer
        self.ypos  = ypos
# (18) change from dice to groups of values, rects and dots
# (33) in fact, change to list of Die instances
        if dice == []:
            self.dice = [Die(layer=self.layer, color=i) for i in range(6)]
# (20) allow the making of empty dice object
        else:
            self.dice = dice
        self.rects = w.Group([die.rect for die in self.dice])
        self.dots  = w.Group([die.dots for die in self.dice])
        self.arrange()
# (19) get the bound union of all the dice bounds
# (35) write the bound union function in the newer fashion
    def get_bound(self): 
        bounds = [die.bounds for die in self.dice]
        return reduce(lambda a, b: a.union(b), bounds)
        # _bound = bounds[0]
        # for bound in bounds[1:]:
        #     _bound = _bound.union(bound)
        # return _bound
# (37) arrange the dice in a smart way
    def arrange(self):
        n = len(self.dice)
        [die.move((20+(i-n/2)*35+self.pos[0], self.pos[1]))
            for i, die in enumerate(self.dice)]
        self.move((scene.width/2, self.ypos))
    def move(self, pos):
# (36) rewrite the die class to fit the following usage
        self.rects.pos = pos
        self.dots.pos = pos
        # pos = add((-self.get_bound().width/2+15,0),pos)
        # self.rects.pos = pos
        # self.dots.pos  = pos
    def select(self, pos): # returns index only
        return [i for i, die in enumerate(self.dice) if\
                die.rect.bounds.collidepoint(pos)][0]
# (21) use add and take for moving to dice or to silver
    def add(self, die): 
        die.rect.delete()
        die.dots.clear()
        print(self.layer)
        _die = Die(layer=self.layer, color=die.color, value=die.value)
        print(len(self.rects))
        self.rects.append(_die.rect)
        self.dots.append(_die.dots)
        self.dice.append(_die)
        print(len(self.rects))
        self.arrange()
    def take(self, i):
        _list1 = self.rects.explode()
        _list2 = self.dots.explode()
        _subl1 = _list1[0:i]+_list1[i+1:]
        _subl2 = _list2[0:i]+_list2[i+1:]
        self.rects = w.Group(_subl1)
        self.dots  = w.Group(_subl2)
        self.arrange()
        return self.dice.pop(i)
    def discard(self, dindex): # TODO
        self.rects[dindex].clear()
        self.dots[dindex].clear()
        self.ids.pop(dindex)
        self.values.pop(dindex)
        self.rects.pop(dindex)
        self.dots.pop(dindex)
    def throw(self, i=None):
        for die in self.dice:
            dots = die.throw() 
            self.dots.append(dots)
        # self.arrange()
        # # values, rects, dots = zip(*self.dice)
        # [dot.clear() for dot in self.dots]
        # self.ids    = [0, 1, 2, 3, 4, 5]
        # self.values = [random.randint(1,6) for i in range(6)]
        # self.dots   = [w.Group(self.adddots(rect.pos, value)) 
        #         for rect, value in zip(self.rects, self.values)]
        # # self.dice = list(zip(new_values, rects, new_dots))
    def __str__(self):
        return ", ".join([f"{die.color}:{die.value}" for die in self.dice])

dice = Dice(scene.layers[20])

# (34) draw silver plate and its dice in the newer fashion
scene.layers[10].add_rect(color='#444444',width=scene.width,
        height=40,pos=(scene.width/2, 70))
silver = None

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
            # print(f'selected {cdtf_die}')
            cdtf_expect = 1
    elif cdtf_expect == 1:
        if my > tops[0]-30: # actually pressing field
            play_to_field(pos)
    else:
        print("Unexpected behavior 1.")

# (12) put the value into the field if purple or orange
# (14) put an X in the field if green
def play_to_field(pos):
    global cdtf_expect, cdtf_die, silver
    mx, my  = pos
    success = False
    value   = dice.dice[cdtf_die].value

    if my > tops[0]-10 and my < tops[0]+30:
        success = greens.play(value)
    elif my > tops[1] and my < tops[1]+20:
        success = oranges.play(value)
    elif my > tops[2]-20 and my < tops[2]+20:
        success = purples.play(value)
    if success:
        cdtf_expect = 0
        if silver is None:
# (40) layer index not working #FIXME 
            silver = Dice(scene.layers[30], dice=[dice.take(cdtf_die)],
                    ypos=70)
        else:
            silver.add(dice.take(cdtf_die)) 
        dice.arrange()
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
