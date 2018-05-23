from tkinter import *


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
