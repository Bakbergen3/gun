from random import randrange as rnd
from random import choice
import tkinter as tk
import math
import time

#Global params
WIDTH = 800
HEIGHT = 600


def main():
    """
    Executes the application
    """
    global root, canvas
    global bullet, target, text_screen, gun, number_of_shots, bullets

    root = tk.Tk()
    frame = tk.Frame(root)
    root.geometry(str(WIDTH) + 'x' + str(HEIGHT))
    canvas = tk.Canvas(root, bg='white')
    canvas.pack(fill=tk.BOTH, expand=1)

    target = Target()
    text_screen = canvas.create_text(400, 300, text='To be filled',
                                    font='Times 28')
    gun = Gun()
    number_of_shots = 0
    bullets = []


def time_handler():
    """
    Updates the canvas
    """
    global root, canvas
    global bullet, target, text_screen, gun, number_of_shots, bullets

    canvas.bind('<Button-1>', gun.load)
    canvas.bind('<ButtonRelease-1>', gun.shoot)
    canvas.bind('<Motion>', gun.targetting)

    target.life = 1
    while target.life or bullets:
        for bullet in bullets:
            bullet.move()
            #Add target hit
        
        canvas.update()
        time.sleep(0.03)
        gun.targetting()
        gun.power_up()
    canvas.itemconfig(text_screen, text='')
    canvas.delete(gun)
    root.after(1000, time_handler)


class Bullet:
    """
    Bullet, which hits the targets.
    """
    global canvas

    def __init__(self, x=40, y=450):
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 1
        self.vy = 1
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.bullet_id = canvas.create_oval(
                        self.x - self.r,
                        self.y - self.r,
                        self.x + self.r,
                        self.y + self.r,
                        fill=self.color
        )
        self.life = 30

    def set_coords(self):
        """
        Changes the xy coordinates of the bullet
        """
        canvas.coords(
                self.bullet_id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
        )

    def move(self):
        """
        Moves bullet as time passes
        """
        self.x += self.vx
        self.y -= self.vy
        self.set_coords()
    #FIXME: Add collision motion with other bullets 


class Gun:
    global canvas

    def __init__(self):
        self.gun_on = False
        self.angle = 1
        self.power = 10
        self.gun_id = canvas.create_line(20, 450, 50, 420, width=7)

    def load(self, event):
        """
        Loads the gun to prepare the gun to shoot stronger.
        """
        self.gun_on = True

    def shoot(self, event):
        """
        Shoots the gun with the bullet.
        """
        global bullets, number_of_shots

        number_of_shots += 1
        new_bullet = Bullet(20 + max(self.power, 20) * math.cos(self.angle),
                            450 + max(self.power, 20) * math.sin(self.angle))
        new_bullet.r += 5
        self.angle = math.atan((event.y - new_bullet.y)
                                / (event.x - new_bullet.x))
        new_bullet.vx = self.power * math.cos(self.angle)
        new_bullet.vy = - self.power * math.sin(self.angle)
        bullets += [new_bullet]
        self.gun_on = False
        self.power = 10

    def targetting(self, event=0):
        """
        Targetting the gun depending on the mouse pointer.
        """
        if event:
            self.angle = math.atan((event.y - 450) / (event.x - 20))
        if self.gun_on:
            canvas.coords(self.gun_id, 20, 450,
                        20 + max(self.power, 20) * math.cos(self.angle),
                        450 + max(self.power, 20) * math.sin(self.angle))

    def power_up(self):
        """
        Adjusts the power of shooting depending on seconds
        pressed on the button.
        """
        if self.gun_on:
            if self.power < 100:
                self.power += 1
            canvas.itemconfig(self.gun_id, fill='orange')
        else:
            canvas.itemconfig(self.gun_id, fill='black')


class Target:
    global canvas

    def __init__(self):
        self.points = 0
        self.life = 1
        self.r = rnd(5, 50)
        self.x = rnd(600, WIDTH - self.r)
        self.y = rnd(300, HEIGHT - self.r)
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.target_id = canvas.create_oval(self.x - self.r, self.y - self.r,
                                        self.x + self.r, self.y + self.r,
                                        fill=self.color, width=0)

    def hit(self, points=1):
        """
        When the bullet hits the target.
        """
        canvas.coords(self.target_id, -10, -10, -10, -10)
        #FIX: Add points counter

if __name__ == __name__:
    main()
    time_handler()
    root.mainloop()
