"""
This is a Py.Processing port of a beautiful
sketch by Manuel Gamboa Naon https://gist.github.com/manoloide/16ea9e1d68c6ba1700fcb008fd38aab0
"""

mm = 0

def setup():
    size(720, 720, P2D)
    generate()

def draw():
    global mx, my, mm, time
    mm *= 0.95
    # if (mm < 0.04) mm *= 0.2
    mx = mouseX - width / 2
    my = mouseY - height / 2
    time = millis() * 0.001
    background(190)

    translate(width / 2, height / 2)

    for r in rects:
        r.update()
        r.showShadow()

    for r in rects:
        r.show()


def keyPressed():
    generate()

def mouseClicked():
    sub()

def mouseMoved():
    global mm
    mm += 0.05
    sub()

def sub():
    for r in rects:
        if r.isOn(mx, my):
            r.sub()
            break


def generate():
    global rects
    rects = []
    rects.append(Rect(-300, -300, 600, color(random(256))))


class Rect:

    def __init__(self, x, y, s, c):
        self.x = x
        self.y = y
        self.ix = x
        self.iy = y
        self.s = s
        self.b = 50
        self.ncol = color(random(256))
        self.col = c

    def mouseMovement(self):
        cx = self.x + self.s * 0.5
        cy = self.y + self.s * 0.5
        maxDist = 200
        dis = dist(cx, cy, mx, my)
        ang = atan2(cy - my, cx - mx)
        if (dis < maxDist):
            dd = map(dis, 0, maxDist, 1, 0)
            dd = pow(dd, 0.9) * 20 * mm
            self.x += cos(ang) * dd
            self.y += sin(ang) * dd

    def update(self):

        self.x = lerp(self.x, self.ix, 0.09)
        self.y = lerp(self.y, self.iy, 0.09)
        self.col = lerpColor(self.col, self.ncol, 0.05)

        self.mouseMovement()

    def showShadow(self):
        noStroke()
        beginShape()
        fill(0, 40)
        vertex(self.x + self.s,
               self.y)
        vertex(self.x + self.s,
               self.y + self.s)
        fill(0, 0)
        vertex(self.x + self.s + self.b,
               self.y + self.s + self.b)
        vertex(self.x + self.s + self.b,
               self.y + self.b)
        endShape(CLOSE)
        beginShape()
        fill(0, 40)
        vertex(self.x,
               self.y + self.s)
        vertex(self.x + self.s,
               self.y + self.s)
        fill(0, 0)
        vertex(self.x + self.s + self.b,
               self.y + self.s + self.b)
        vertex(self.x + self.b,
               self.y + self.s + self.b)
        endShape(CLOSE)

    def show(self):
        stroke(255, 2)
        fill(self.col)
        rect(self.x, self.y, self.s, self.s)

    def isOn(self, mx, my):
        return (self.x + self.s > mx >= self.x and
                self.y + self.s > my >= self.y)

    def sub(self):
        ms = self.s * 0.5
        
        r = Rect(self.ix, self.iy + ms, ms, self.col)
        rects.append(r)
        
        r = Rect(self.ix, self.iy, ms, self.col)
        r.x += self.x - self.ix
        r.y += self.y - self.iy
        rects.append(r)

        r = Rect(self.ix + ms, self.iy, ms, self.col)
        r.x += self.x - self.ix
        r.y += self.y - self.iy
        rects.append(r)

        r = Rect(self.ix + ms, self.iy + ms, ms, self.col)
        r.x += self.x - self.ix
        r.y += self.y - self.iy
        rects.append(r)
 
        rects.remove(self)