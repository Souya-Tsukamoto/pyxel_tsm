#全体をapp~~関数~~ classで囲ってball.move(app())とかすることで相互に使えるようにしよう！
import pyxel


class Forcus():
    def __init__(self, App):
        self.x = App.width / 2
        self.y = App.height / 2
    def fmove(self, App):
        if pyxel.btn(pyxel.KEY_A) and self.x > 0:
            self.x -= 10
        elif pyxel.btn(pyxel.KEY_D) and self.x < App.width:
            self.x += 10
        elif pyxel.btn(pyxel.KEY_W) and self.y > 0:
            self.y -= 10
        elif pyxel.btn(pyxel.KEY_S) and self.y < App.height:
            self.y += 10

class World():
    line = 5
    def __init__(self, App):
        self.x = App.width
        self.y1 = 150
        self.z1 = 240

        self.y2 = 300
        self.z2 = 480

        self.linec = 7 #color
        self.mainc = 9

    def wdraw(self, App):
        pyxel.rect(0, App.height - self.y2, self.x, self.y2, self.mainc)
        pyxel.rect(0, App.height - self.y2, self.x, World.line, self.linec)
        pyxel.rect(0, App.height - self.y1, self.x, self.y1, self.mainc)
        pyxel.rect(0, App.height - self.y1, self.x, World.line, self.linec)


class Target():
    def __init__(self, App):
        self.x = pyxel.rndi(0, App.width)
        self.y = App.w1.y1
        self.z = App.w1.z1
        self.r = 30

    def tdraw(self):
        pyxel.circ(self.x, self.y - self.r, self.r, 7)
        App.textload(123, self.x -8, self.y - 32)

class Ball():
    colorlist = [8, 14, 15]
    def __init__(self, App):
        self.speed = 30
        self.x = 300
        self.y = 450
        self.z = 0
        self.r = 50
        self.color = Ball.colorlist[0]
        self.time = 0

        self.vx = ((App.forcus[0].x - App.width / 2) / App.width) * self.speed
        if App.forcus[0].y > 0:
            self.vy = -(1 - (App.forcus[0].y / App.height)) * self.speed * 1.2
            self.vz = pyxel.sqrt(1 - (1 - App.forcus[0].y / App.height)**2) * self.speed
        else:
            self.vy = -(1 - (1 / App.height)) * self.speed * 1.2
            self.vz = pyxel.sqrt(1 - (1 - 1 / App.height)**2) * self.speed


    def move(self, App):
        self.time += 1
        self.x += self.vx
        self.y += (self.vy + 1.2 * self.time)
        self.z += self.vz
        self.r = 50 / (self.z*0.005+1)
        self.tfrag = False
        if self.z >= 400:
            self.color = Ball.colorlist[2]
        elif self.z >= 200:
            self.color = Ball.colorlist[1]
        else:
            self.color = Ball.colorlist[0]

        i = 0
        for t in App.target:
            if abs(t.x - self.x) <= t.r and abs(t.y - self.y) <= t.r and abs(t.z - self.z)<= t.r:
                App.point += 1
                del App.target[i]
                self.tfrag = True
            else:
                self.tfrag = False
            i += 1

    def bdraw(self, y1, z1, y2, z2, App):
        if z1 < self.z and (App.height - y1) < self.y:
            pass
        elif z2 < self.z and (App.height - y2) < self.y:
            pass
            #App.point += 1
        else:
            pyxel.circ(self.x, self.y, self.r, self.color)
            


class App():
    width = 600
    height = 450
    forcus = []
    point = 0
    target = []
    w1 = 0 #world1
    def __init__(self):
        pyxel.init(App.width, App.height)
        pyxel.load("num.pyxres")
    
        self.ball = []
        App.w1 = World(App)
        App.forcus.append(Forcus(App))
        for i in range(10):
            App.target.append(Target(App))
        pyxel.run(self.update, self.draw)

    def reload(self):
        pyxel.cls(6)
        self.w1.wdraw(App)
        for t in self.target:
            t.tdraw()

    def textload(num, x, y):
        leng = len(str(num))
        for i in range(leng):
            if int(str(num)[i]) == 0:
                mapn = 9 * 8
            else:
                mapn = (int(str(num)[i]) - 1) * 8
            pyxel.blt(x + (i * 6), y, 0, mapn, 0, 9, 9, 0)

    def update(self):
        i = 0
        for b in self.ball:
            b.move(App)
            if b.tfrag:
                pass
                #App.target.append(Target(App))
            if b.y > self.height:
                del self.ball[i]
            i += 1
        self.forcus[0].fmove(App)
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.ball.append(Ball(App))

    def draw(self):
        self.reload()
        for b in self.ball:
            b.bdraw(self.w1.y1, self.w1.z1, self.w1.y2, self.w1.z2, App)
            pyxel.text(300, 200, str(b.z), 0)
        pyxel.text(300, 225, str(self.point), 0)
        pyxel.circ(self.forcus[0].x, self.forcus[0].y, 10, 0)
        

if __name__ == '__main__':
    App()