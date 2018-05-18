from tkinter import *
import random
import time
import threading

# Create window
tk = Tk()
tk.title("Bounce!")
tk.wm_resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=1000, height=700, highlightthickness=5,
                highlightbackground='green')
canvas.pack()

# Divide the window by drawing rectangle + draw dark-red floor
canvas.create_rectangle(0, 705, 702, 702, fill='firebrick', width=0)
canvas.create_rectangle(700, 0, 705, 705, fill='green', width=0)

button1 = Button(text="HELP?", anchor=W, font=('Comic Sans MS', 30), padx=50)
button1.configure(width=5, activebackground="#33B5E5", relief=GROOVE)
button1_window = canvas.create_window(740, 550, anchor=NW, window=button1)

# Create photos (don't show them yet)
pic1 = PhotoImage(file='tut1.gif')
pic2 = PhotoImage(file='tut2.gif')
pic3 = PhotoImage(file='tut3.gif')

# Variables
lvl = 1
default_timer = 15  # Default time for each lvl
timer = default_timer  # Storing current time
bottom = False  # True when ball hits bottom of the screen
run = True  # Running game_loop()
epsilon = 0.75  # Used when preventing ball to go straight up at the beginning
slomo = False  # Slow motion
slow_timer_default = 20  # Default slow motion cooldown
slow_timer = slow_timer_default  # Current slow motion cooldown
slomo_amount = 0  # Amount of slow motion actions available
slow_timer2_default = 75  # Default value of slow_timer2
slow_timer2 = slow_timer2_default  # Current value of available "length" of
# slow motion
death_counter = 0  # Value used to limit time of game communicates
clock_run = True  # False to pause the timer


# Clock and level info
class Clock:
    def __init__(self, place, color):
        self.canvas = place
        self.color = color
        self.id = place.create_text(850, 100, text=int(timer), fill=color,
                                    font=('Comic Sans MS', 80), tags='clock')
        self.lvl_info = place.create_text(850, 250,
                                          text='Level: {}'.format(lvl),
                                          fill=color, font=('Comic Sans MS',
                                                            20))
        self.slomo_info = place.create_text(850, 400,
                                            text='Slow motion: {}'.format(
                                                slow_timer), fill=color,
                                            font=('Comic Sans MS', 20))
        self.slomo_time = place.create_text(850, 460, text=slomo_amount,
                                            fill=color,
                                            font=('Comic Sans MS', 25))


# Ball
class Ball:
    def __init__(self, place, color):
        self.canvas = place
        self.color = color
        self.id = place.create_oval(0, 0, 20, 20, fill=color, tags='ball')
        self.canvas.move(self.id, 340, 600)
        self.x = 0
        self.y = -3.5 - 0.12 * lvl
        while abs(
                self.x) < epsilon:  # Prevent ball from going almost
            # straight up at the beginning
            self.x = random.uniform(-3.5 - 0.12 * lvl, 3.5 + 0.12 * lvl)

    # Bounce the ball if it hits end of the screen
    def border(self):
        global bottom
        # pos[0] - left
        # pos[1] - up
        # pos[2] - right
        # pos[3] - down
        pos = self.canvas.coords(self.id)
        if pos[0] <= 1 or pos[0] >= 680:
            self.x = self.x * -1
        elif pos[1] <= 1:
            self.y = self.y * -1
        elif pos[1] >= 685:
            bottom = True

    # Move the ball
    def move_ball(self):
        self.canvas.move(self.id, self.x, self.y)


# Paddle
class Paddle:
    def __init__(self, place, color):
        self.canvas = place
        self.color = color
        self.id = place.create_rectangle(250 + 1.6 * lvl, 702, 450 - 1.6 * lvl,
                                         682, fill=color, tags='paddle')
        self.x = 0

    # Move the paddle
    def move_paddle(self):
        # pos[0] - left
        # pos[1] - up
        # pos[2] - right
        # pos[3] - down
        paddle_pos = self.canvas.coords(self.id)
        self.canvas.move(self.id, self.x, 0)
        if paddle_pos[0] <= 3:
            self.x = 3 - (lvl * 0.01)
            self.canvas.move(self.id, 3 - (lvl * 0.01), 0)
        elif paddle_pos[2] >= 700:
            self.x = -3 + (lvl * 0.01)
            self.canvas.move(self.id, -3 + (lvl * 0.01), 0)

    # Move paddle while pressing <Left>
    def move_left(self, event):
        self.x = -3 + (lvl * 0.01)

    # Move paddle while pressing <Right>
    def move_right(self, event):
        self.x = 3 - (lvl * 0.01)


# Binding functions to the arrow keys
def bindings():
    paddle.canvas.bind_all('<Right>', paddle.move_right)
    paddle.canvas.bind_all('<Left>', paddle.move_left)
    paddle.canvas.bind_all('<d>', paddle.move_right)
    paddle.canvas.bind_all('<a>', paddle.move_left)
    button1.bind('<Button-1>', show_help)
    paddle.canvas.bind_all('<space>', pause)
    paddle.canvas.bind_all('<Control_L>', slo_mo)
    paddle.canvas.bind_all('<Control_R>', slo_mo)


# Show help window
def show_help(event):
    global run
    help_window = Toplevel()
    help_window.title("Help")
    help_window.wm_resizable(0, 0)
    help_window.wm_attributes("-topmost", 1)
    canvas2 = Canvas(help_window, width=500, height=365, highlightthickness=5,
                     highlightbackground='green')
    canvas2.pack()
    canvas2.create_text(20, 20, anchor=NW, fill='black', font=('Courier', 11),
                        width=500,
                        text='Game difficulty will be adjusted by '
                             'manipulating\n1) Ball speed\n2) Paddle '
                             'speed\n3) '
                             'Paddle size\n4) '
                             'Game speed itself')
    canvas2.create_text(20, 140, anchor=NW, fill='black',
                        font=('Courier bold', 15), width=500,
                        text='- Use <A/D> or <Left/Right> to control the '
                             'paddle\n- Press <Spacebar> to pause the game\n'
                             '- Press <Ctrl> to activate slow motion\nYou '
                             'can save your slow motions and use them '
                             'later!')
    canvas2.create_image(-20, 260, image=pic1, anchor=NW)
    canvas2.create_image(160, 260, image=pic2, anchor=NW)
    canvas2.create_image(340, 260, image=pic3, anchor=NW)

    # Pause the game when help window is active
    if run:
        pause('<space>')


# Pause / unpause the game
def pause(event):
    global run
    if run:
        run = False
        canvas.create_text(350, 120, text='PAUSED', fill='red',
                           font=('Comic Sans MS', 60), tags='text')
    elif not run:
        run = True
        canvas.delete('text')
        game_loop()


# Bounce the ball when it hits the paddle
def hit_paddle():
    # pos[0] - left
    # pos[1] - up
    # pos[2] - right
    # pos[3] - down
    ball_pos = ball.canvas.coords(ball.id)
    paddle_pos = paddle.canvas.coords(paddle.id)

    if ball_pos[3] >= paddle_pos[1] and \
            ((paddle_pos[0] <= ball_pos[2] <= paddle_pos[2]) or
             (paddle_pos[2] >= ball_pos[0] >= paddle_pos[0])):
        if 688 <= ball_pos[3]:
            ball.x += 0.5 * paddle.x
        else:
            ball.y = ball.y * -1

            # Change ball's direction slightly when it hits flank of the paddle
            if ball_pos[2] < (
                    paddle_pos[0] + 0.25 * (paddle_pos[2] - paddle_pos[0])):
                ball.x -= 0.75
            elif ball_pos[0] > (
                    paddle_pos[0] + 0.75 * (paddle_pos[2] - paddle_pos[0])):
                ball.x += 0.75

            # Change ball's direction slightly according to the movement of
            # the paddle
            if paddle.x < 0:
                ball.x -= 0.5
            elif paddle.x > 0:
                ball.x += 0.5

            # Change ball's direction even more when it hits the very edge
            # of the paddle
            if ball_pos[0] <= paddle_pos[0] <= ball_pos[2]:
                ball.x -= 0.75
                ball.y /= 1.2
            elif ball_pos[0] <= paddle_pos[2] <= ball_pos[2]:
                ball.x += 0.75
                ball.y /= 1.2


# Ball hits the bottom of the screen.
def hit_bottom():
    global death_counter, bottom, lvl, clock_run
    if bottom:
        clock_run = False
        canvas.delete('text')
        canvas.create_text(350, 300, text='YOU MISSED', fill='black',
                           font=('Comic Sans MS', 50), tags='text')
        tk.update()
        time.sleep(1)
        death_counter += 1
        if death_counter == 4:
            lvl -= 1
            restart()


# Restarts the game, resets objects, etc.
def restart():
    global death_counter, bottom, timer, lvl, default_timer, clock_run
    death_counter = 0
    timer = default_timer
    clock_run = True
    canvas.delete('text')
    ball.canvas.coords(ball.id, (330, 590, 350, 610))
    ball.x = 0
    paddle.x = 0
    ball.y = -3.5 - 0.12 * lvl
    while abs(
            ball.x) < epsilon:  # Prevent ball from going almost straight up
        #  at the beginning
        ball.x = random.uniform(-3.5 - 0.12 * lvl, 3.5 + 0.12 * lvl)
    tk.update()
    bottom = False
    paddle.canvas.coords(paddle.id,
                         (250 + 1.6 * lvl, 702, 450 - 1.6 * lvl, 682))


# Starts next level
def next_lvl():
    global death_counter, bottom, timer, lvl, clock_run
    if timer <= 0 and not bottom:
        timer = 0
        canvas.delete('text')
        canvas.create_text(350, 300, text='GOOD JOB', fill='green',
                           font=('Comic Sans MS', 50), tags='text')
        tk.update()
        clock_run = False
        time.sleep(1)
        death_counter += 1
        if death_counter == 3:
            lvl += 1
            restart()


# Player wants to use slow motion.
def slo_mo(event):
    global slomo, slomo_amount
    if slomo_amount > 0 and timer > 0 and not bottom:
        slomo = True


# Activates slow motion.
def slo_motion():
    global timer, slow_timer2, slow_timer, slomo, slomo_amount
    if slomo:
        if slow_timer2 > 0 and timer >= 0 and not bottom:
            canvas.delete('text')
            canvas.create_text(350, 500, text=slow_timer2, fill='PaleGreen3',
                               font=('Comic Sans MS', 30), tags='text')
            time.sleep(0.03)
            slo_mo('<Control_L>')
            slow_timer2 -= 1
        else:
            slow_timer = slow_timer_default
            slow_timer2 = slow_timer2_default
            slomo = False
            slomo_amount -= 1
            canvas.delete('text')


# Handle all time-related things in background
def clock_update():
    global timer, slow_timer, slow_timer2_default, slomo_amount, clock_run
    time.sleep(1)
    if run and clock_run:
        # Slow down time when in slow motion
        if slomo:
            timer -= 0.3
        elif not bottom:
            timer -= 1
        if timer > 0 and not bottom and not slomo:
            if slow_timer > 0:
                slow_timer -= 1
            else:
                slomo_amount += 1
                slow_timer = slow_timer_default
    clock_update()


# Run clock_update() in background
t1 = threading.Thread(target=clock_update)
t1.start()

# Create object instances
ball = Ball(canvas, 'red')
paddle = Paddle(canvas, 'blue')
clock = Clock(canvas, 'black')


# Game loop
def game_loop():
    global run, slomo_amount, clock_run
    while run:
        tk.update()
        ball.move_ball()
        ball.border()
        hit_paddle()
        paddle.move_paddle()
        bindings()
        hit_bottom()
        time.sleep(0.005 - 0.00015 * lvl)
        slo_motion()
        canvas.itemconfigure(clock.id, text=int(timer))
        canvas.itemconfigure(clock.lvl_info, text='Level: {}'.format(lvl))
        canvas.itemconfigure(clock.slomo_time, text=slomo_amount,
                             justify=CENTER)
        canvas.itemconfigure(clock.slomo_info,
                             text='Slow motion: {}'.format(slow_timer))
        next_lvl()
        if slomo_amount > 0:
            canvas.itemconfigure(clock.slomo_time, fill='purple',
                                 font=('Comic Sans MS', 45))
            canvas.config(highlightbackground='purple')
        else:
            canvas.itemconfigure(clock.slomo_time, fill=clock.color,
                                 font=('Comic Sans MS', 25))
            canvas.config(highlightbackground='green')
        tk.update()
        tk.update_idletasks()


game_loop()

tk.mainloop()
