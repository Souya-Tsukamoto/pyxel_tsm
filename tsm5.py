#全体をapp~~関数~~ classで囲ってball.move(app())とかすることで相互に使えるようにしよう！
import pyxel


class Forcus():
    def __init__(self, App, user):
        self.x = App.width / 2
        self.y = App.height / 2
        self.user = user
    def fmove(self, App):
        if self.user == 0:
            if pyxel.btn(pyxel.KEY_A) and self.x > 0:
                self.x -= 10
            elif pyxel.btn(pyxel.KEY_D) and self.x < App.width:
                self.x += 10
            elif pyxel.btn(pyxel.KEY_W) and self.y > 0:
                self.y -= 10
            elif pyxel.btn(pyxel.KEY_S) and self.y < App.height:
                self.y += 10
        elif self.user == 1:
            if pyxel.btn(pyxel.KEY_LEFT) and self.x > 0:
                self.x -= 10
            elif pyxel.btn(pyxel.KEY_RIGHT) and self.x < App.width:
                self.x += 10
            elif pyxel.btn(pyxel.KEY_UP) and self.y > 0:
                self.y -= 10
            elif pyxel.btn(pyxel.KEY_DOWN) and self.y < App.height:
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

    def wdraw_b(self, App):
        pyxel.rect(0, App.height - self.y2, self.x, self.y2, self.mainc)
        pyxel.rect(0, App.height - self.y2, self.x, World.line, self.linec)
    #    pyxel.rect(0, App.height - self.y1, self.x, self.y1, self.mainc)
    #    pyxel.rect(0, App.height - self.y1, self.x, World.line, self.linec)
    
    def wdraw_f(self, App):
    #    pyxel.rect(0, App.height - self.y2, self.x, self.y2, self.mainc)
    #    pyxel.rect(0, App.height - self.y2, self.x, World.line, self.linec)
        pyxel.rect(0, App.height - self.y1, self.x, self.y1, self.mainc)
        pyxel.rect(0, App.height - self.y1, self.x, World.line, self.linec)


class Target(): #動かない
    def __init__(self, App, no, max, world, dan):
        self.vx = 0
        self.vy = 0
        self.goal_x = 0
        self.goal_y = 0
        self.no = no
        self.world = world
        self.dan = dan
        self.x = (self.no * (App.width/max)) + ((App.width / (2 * max)) )
        self.r = 20

        self.goal_x = self.x
        #self.x = 0
        self.y = App.height
        if(world == 1):
            if(dan == 1):
                self.goal_y = App.w1.y1 + pyxel.rndi(-20, 0)
                self.y = App.w1.y1 + self.r
                self.z = App.w1.z1
            elif(dan == 2):
                self.goal_y = App.w1.y2 + pyxel.rndi(-20, 0)
                self.y = App.w1.y2 + self.r
                self.z = App.w1.z2
        self.r = 20 + (self.z * 0.02)
        self.leng = pyxel.sqrt(((self.x - (App.width / 2)) ** 2) + ((self.y - App.height) ** 2) + ((600 - self.z) ** 2))
        self.point = 200 * (int(self.leng) // 100)

    def tmove(self):
        #self.goal_x = self.x
#        if self.x >= self.goal_x:
#            self.vx = 0
#        else:
#            self.vx = 10
#        self.x += self.vx
        if self.y <= self.goal_y:
            self.vy = 0
        else:
            self.vy = 3
        self.y -= self.vy



    def tdraw(self):
        pyxel.circ(self.x, self.y - self.r, self.r, 7)
        App.textload(self.point, self.x, self.y - self.r*1.1, 1, 0)


class M_Target(): #動くやつ
    def __init__(self, App, world, dan, start, vx):
        self.vx = vx
        #self.vy = 0
        self.world = world
        self.dan = dan
        self.x = start
        self.y = App.height
        self.r = 0
#        self.goal_y = 0

        if(world == 1):
            if(dan == 1):
                self.y = App.w1.y1 + pyxel.rndi(-20, 0) - 80
                #self.y = App.w1.y1 + self.r
                self.z = App.w1.z1
            elif(dan == 2):
                self.y = App.w1.y2 + pyxel.rndi(-20, 0) - 80
                #self.y = App.w1.y2 + self.r
                self.z = App.w1.z2
        self.r = 10 + (self.z * 0.02)
        self.leng = pyxel.sqrt(((self.x - (App.width / 2)) ** 2) + ((self.y - App.height) ** 2) + ((600 - self.z) ** 2))
        self.point = 300 * (int(self.leng) // 100)

    def tmove(self):
        self.x += self.vx
        self.y += pyxel.sin(pyxel.frame_count * 30) * 2



    def tdraw(self):
        pyxel.circ(self.x, self.y - self.r, self.r, 10)
        App.textload(self.point, self.x, self.y - self.r*1.1, 1, 0)
        if(self.x > App.width + 100 and self.vx > 0):
            self.x = -100
        elif(self.x < -100 and self.vx < 0):
            self.x = App.width + 100



class Ball():
    colorlist = [8, 14, 15, 1, 5, 12]
    lostlist = []
    def __init__(self, App, user):
        self.speed = 30
        self.user = user
        if self.user == 0:
            self.x = 0
            self.y = App.height
        elif self.user == 1:
            self.x = App.width
            self.y = App.height
        self.z = 0
        self.r = 50
        self.color = Ball.colorlist[0]
        self.time = 0
        
        if self.user == 0:
            self.vx = ((App.forcus[0].x) / App.width) * self.speed
            if App.forcus[0].y > 0:
                self.vy = -(1 - (App.forcus[0].y / App.height)) * self.speed * 1.2
                self.vz = pyxel.sqrt(1 - (1 - App.forcus[0].y / App.height)**2) * self.speed
            else:
                self.vy = -(1 - (1 / App.height)) * self.speed * 1.2
                self.vz = pyxel.sqrt(1 - (1 - 1 / App.height)**2) * self.speed
        elif self.user == 1:
            self.vx = ((App.forcus[1].x - App.width) / App.width) * self.speed
            if App.forcus[1].y > 0:
                self.vy = -(1 - (App.forcus[1].y / App.height)) * self.speed * 1.2
                self.vz = pyxel.sqrt(1 - (1 - App.forcus[1].y / App.height)**2) * self.speed
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
        if self.user == 0:
            if self.z >= 400:
                self.color = Ball.colorlist[2]
            elif self.z >= 200:
                self.color = Ball.colorlist[1]
            else:
                self.color = Ball.colorlist[0]
        elif self.user == 1:
            if self.z >= 400:
                self.color = Ball.colorlist[5]
            elif self.z >= 200:
                self.color = Ball.colorlist[4]
            else:
                self.color = Ball.colorlist[3]


        i = 0
        for t in App.target_b:
            if abs(t.x - self.x) <= t.r and abs(t.y - self.y) <= t.r and abs(t.z - self.z)<= t.r:
                if self.user == 0:
                    App.totalpoint_l += t.point
                elif self.user == 1:
                    App.totalpoint_r += t.point
                Ball.lostlist.append([App.target_b[i].no, App.target_b[i].world, App.target_b[i].dan])
                #App.target.append(Target(App, App.target[i].no, 10, App.target[i].world, App.target[i].dan))
                del App.target_b[i]
                self.tfrag = True
            else:
                self.tfrag = False
            i += 1

        j = 0
        for t in App.target_f:
            if abs(t.x - self.x) <= t.r and abs(t.y - self.y) <= t.r and abs(t.z - self.z)<= t.r:
                if self.user == 0:
                    App.totalpoint_l += t.point
                elif self.user == 1:
                    App.totalpoint_r += t.point
                Ball.lostlist.append([App.target_f[j].no, App.target_f[j].world, App.target_f[j].dan])
                #App.target.append(Target(App, App.target[i].no, 10, App.target[i].world, App.target[i].dan))
                del App.target_f[j]
                self.tfrag = True
            else:
                self.tfrag = False
            j += 1
        
        k = 0
        for t in App.target_m:
            if abs(t.x - self.x) <= t.r and abs(t.y - self.y) <= t.r and abs(t.z - self.z)<= t.r:
                if self.user == 0:
                    App.totalpoint_l += t.point
                elif self.user == 1:
                    App.totalpoint_r += t.point
                Ball.lostlist.append([0, App.target_m[k].world, 0])
                #App.target.append(Target(App, App.target[i].no, 10, App.target[i].world, App.target[i].dan))
                del App.target_m[k]
                self.tfrag = True
            else:
                self.tfrag = False
            k += 1

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
    totalpoint_l = 0
    totalpoint_r = 0
    target_b = []
    target_f = []
    target_m = []
    start_time = 0
    start_frag = False
    w1 = 0 #world1
    def __init__(self):
        pyxel.init(App.width, App.height)
        pyxel.load("num.pyxres")
    
        self.ball = []
        App.w1 = World(App)
        App.forcus.append(Forcus(App, 0))
        App.forcus.append(Forcus(App, 1))
        for i in range(10):
            App.target_b.append(Target(App, i, 10, 1, 1))
            App.target_f.append(Target(App, i, 10, 1, 2))
        for i in range(3):
            App.target_m.append(M_Target(App, 1, 2, 0 + i * -200, 2))
        pyxel.run(self.update, self.draw)

    def reload(self):
        pyxel.cls(6)
        for t in self.target_b:
            t.tdraw()
        self.w1.wdraw_b(App)
        for t in self.target_f:
            t.tdraw()
        for t in self.target_m:
            t.tdraw()
        self.w1.wdraw_f(App)
        

    def textload(num, x, y, size, col):
        if size == 1:
            x = x - (3 * len(str(num)))
            leng = len(str(num))
            for i in range(leng):
                if int(str(num)[i]) == 0:
                    mapn = 9 * 8
                else:
                    mapn = (int(str(num)[i]) - 1) * 8
                pyxel.blt(x + (i * 6), y, 0, mapn, 0, 9, 9, 0)
        elif size == 2:
            x = x - (6 * len(str(num)))
            leng = len(str(num))
            for i in range(leng):
                if int(str(num)[i]) == 0:
                    mapn = 9 * 16
                else:
                    mapn = (int(str(num)[i]) - 1) * 16
                pyxel.blt(x + (i * 12), y, 0, mapn, 17, 17, 17, 0)

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE) and App.start_frag != True:
            App.start_time = pyxel.frame_count
            App.start_frag = True
        if pyxel.frame_count - App.start_time < 600 and App.start_frag:
            i = 0
            for b in self.ball:
                b.move(App)
                if b.tfrag:
                    pass
                    #App.target.append(Target(App))
                if b.y > self.height:
                    del self.ball[i]
                i += 1

            for f in self.forcus:
                f.fmove(App)

            if pyxel.btnp(pyxel.KEY_SPACE):
                self.ball.append(Ball(App, 0))
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.ball.append(Ball(App, 1))

            if pyxel.frame_count % 60 == 0:
                for l in  range(len(Ball.lostlist)):
                    if Ball.lostlist[l][2] == 1:
                        App.target_b.append(Target(App, Ball.lostlist[l][0], 10, Ball.lostlist[l][1], Ball.lostlist[l][2]))
                    elif Ball.lostlist[l][2] == 2:
                        App.target_f.append(Target(App, Ball.lostlist[l][0], 10, Ball.lostlist[l][1], Ball.lostlist[l][2]))
                    elif Ball.lostlist[l][2] == 0:
                        App.target_m.append(M_Target(App, 1, 2, 0, 2))

                Ball.lostlist = []
            
            for t in App.target_b:
                t.tmove()
            for t in App.target_f:
                t.tmove()
            for t in App.target_m:
                t.tmove()


    def draw(self):
        if not App.start_frag:
            pyxel.rect(245, 98, 75, 10, 5)
            pyxel.rect(265, 98, 22, 10, 8)
            pyxel.text(250, 100, "FIT STORY MANIA!!", 10)
            pyxel.text(50, 200, "Left User: WASD & SPACE", 8)
            pyxel.text(400, 200, "Right USER: UP, LEFT, DOWN, RIGHT & ENTER", 6)
            pyxel.text(250, 350, "Push SPACE KEY to Start!!", 11)
        elif pyxel.frame_count - App.start_time < 600 and App.start_frag:
            self.reload()
            for b in self.ball:
                b.bdraw(self.w1.y1, self.w1.z1, self.w1.y2, self.w1.z2, App)
            #    pyxel.text(300, 200, str(b.z), 0)
            #pyxel.text(300, 225, str(self.totalpoint), 0)
            if pyxel.frame_count - App.start_time > 450:
                App.textload((600 - pyxel.frame_count + App.start_time)//30+1, 300, 30, 2, 0)
                App.textload((600 - pyxel.frame_count + App.start_time)//30+1, 300, App.height - 100, 2, 0)
            #pyxel.text(300, 0, str(pyxel.frame_count), 0)
            for f in self.forcus:
                if f.user == 0:
                    pyxel.circ(f.x, f.y, 10, 2)
                elif f.user == 1:
                    pyxel.circ(f.x, f.y, 10, 3)
        else:
            pyxel.cls(6)
            App.textload(self.totalpoint_l, 100, 225, 2, 0)
            pyxel.text(140, 225, "point!!", 7)     
            App.textload(self.totalpoint_r, 500, 225, 2, 0)
            pyxel.text(540, 225, "point!!", 7)     

if __name__ == '__main__':
    App()
