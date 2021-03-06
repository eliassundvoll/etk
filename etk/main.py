import tkinter as tk
import os
import random

KEY_SENSETIVITY = 20
OAR_FREQUENCY = 20
COURSE_LENGHT = 20000
SKY_HEIGHT = 250
CLOUD_AMOUNT = 50
COURSE_MOVE_LEFT_LIMIT = 600
COURSE_MOVE_RIGHT_LIMIT = 1000


class Course(object):
    def __init__(self):
        window = tk.Tk()
        window.attributes("-fullscreen", True)
        
        greeting = tk.Label(text="Welcome to Escape the Kraken!")
        greeting.pack()

        self.course = tk.Canvas(window, bg="white")
        self.course.create_rectangle(0, 0, COURSE_LENGHT, SKY_HEIGHT, fill="lightblue")
        self.course.pack(fill=tk.BOTH, expand=True)        
        
        dirname = os.path.dirname(__file__)
        boat_img = tk.PhotoImage(file=os.path.join(dirname, "graphics\kayakBoatBrownT.png")).subsample(3,3)

        oars = [
            tk.PhotoImage(file=os.path.join(dirname, "graphics\Oar_1.png")).subsample(3,3),
            tk.PhotoImage(file=os.path.join(dirname, "graphics\Oar_2.png")).subsample(3,3),
            tk.PhotoImage(file=os.path.join(dirname, "graphics\Oar_3.png")).subsample(11,11),
            tk.PhotoImage(file=os.path.join(dirname, "graphics\Oar_4.png")).subsample(3,3),
        ]

        cloud_imgs = [
            tk.PhotoImage(file=os.path.join(dirname, "graphics\cloud_1.png")).subsample(2),
            tk.PhotoImage(file=os.path.join(dirname, "graphics\cloud_1.png")).subsample(3),
            tk.PhotoImage(file=os.path.join(dirname, "graphics\cloud_1.png")).subsample(4),
            tk.PhotoImage(file=os.path.join(dirname, "graphics\cloud_2.png")).subsample(2),
            tk.PhotoImage(file=os.path.join(dirname, "graphics\cloud_2.png")).subsample(3),
            tk.PhotoImage(file=os.path.join(dirname, "graphics\cloud_2.png")).subsample(4),
            # tk.PhotoImage(file=os.path.join(dirname, "graphics\cloud_3.png")).subsample(2),
            # tk.PhotoImage(file=os.path.join(dirname, "graphics\cloud_3.png")).subsample(3),
            # tk.PhotoImage(file=os.path.join(dirname, "graphics\cloud_3.png")).subsample(4),
        ]

        self.create_clouds(cloud_imgs)

        position_var = tk.StringVar()
        label = tk.Label(window, textvariable=position_var)
        label.pack()


        Line(self.course)
        boat = Boat(self.course, boat_img, oars, position_var)

        window.bind("<Left>", boat.left)
        window.bind("<Right>", boat.right)

        window.mainloop()

    def create_clouds(self, cloud_imgs):
        self.clouds = []
        for i in range(CLOUD_AMOUNT):
            random_x = random.randint(0, COURSE_LENGHT)
            random_y = random.randint(0, SKY_HEIGHT)
            random_cloud_idx = random.randint(0, len(cloud_imgs) - 1)
            self.clouds.append(self.course.create_image(random_x, random_y, image=cloud_imgs[random_cloud_idx], anchor=tk.SW, tags="background"))


class Line(object):
    def __init__(self, course):
        self.course = course
        self.course.create_line(0, SKY_HEIGHT, COURSE_LENGHT, SKY_HEIGHT, fill="blue", width=5)


class Boat(object):
    def __init__(self, course: tk.Canvas, img, oars, position):
        self.course = course
        self.boat_img = self.course.create_image(0, 215, image=img, anchor=tk.NW, tags="vessel")
        self.oars = [
            self.course.create_image(40, 170, image=oars[0], anchor=tk.NW, tags="vessel"),
            self.course.create_image(40, 170, image=oars[1], anchor=tk.NW, tags="vessel"),
            self.course.create_image(40, 165, image=oars[2], anchor=tk.NW, tags="vessel"),
            self.course.create_image(120, 170, image=oars[3], anchor=tk.NW, tags="vessel"),
        ]
        self.position_label = position
        self.position_label.set("0")
        self.position = 0
        self.screen_positon = 0
        for oar in self.oars:
            self.course.itemconfig(oar, state=tk.HIDDEN)

        self.course_offset = 0


    def left(self, e):
        delta_x = -KEY_SENSETIVITY
        self.move_vessel(delta_x)

    def right(self, e):
        delta_x = KEY_SENSETIVITY
        self.move_vessel(delta_x)

    def move_vessel(self, delta_x):
        if self.position + delta_x < 0:
            return
        self.position += delta_x
        self.position_label.set(self.position)
        index = int((self.position / OAR_FREQUENCY) % 4)
        for oar in self.oars:
            self.course.itemconfig(oar, state=tk.HIDDEN)
        self.course.itemconfig(self.oars[index], state=tk.NORMAL)

        if self.screen_positon + delta_x > COURSE_MOVE_RIGHT_LIMIT and delta_x > 0 :  # Moving right in to right zone
            self.course_offset += delta_x
            self.course.move("background", -delta_x, 0)
        elif self.position < COURSE_MOVE_LEFT_LIMIT:
            self.course.move("vessel", delta_x, 0)
            self.screen_positon += delta_x
        elif self.screen_positon - delta_x < COURSE_MOVE_LEFT_LIMIT and delta_x < 0:  # Moving left in to left zone
            self.course_offset -= delta_x
            self.course.move("background", -delta_x, 0)
        else:  # Moving in midle zone
            self.course.move("vessel", delta_x, 0)
            self.screen_positon += delta_x  


course = Course()
