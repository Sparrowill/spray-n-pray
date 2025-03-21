
import tkinter as tk
from tkinter.ttk import *

import serial 
import time
import os, sys

# Create an instance of tkinter frame or widget
win = tk.Tk()


def restart():
    print("User Reset")
    python = sys.executable
    os.execl(python, python, * sys.argv)

def exit():
    global win
    print("User Quit")
    win.destroy()
    sys.exit()

def main():
    # Setup Serial port - probably ACM0
    ser = serial.Serial('/dev/ttyACM0', baudrate=115200)

    start_time = time.time()

    global win
    win.configure(cursor="none")
    # Full Screen the widget
    win.attributes("-fullscreen", True) 

    # Create a canvas to hold all the stuff apart from the progress bar
    canvas= tk.Canvas(win, width= 800, height= 480, )
    #Create the background
    bg=tk.PhotoImage(file = "bg.png")
    canvas.create_image(0,0,anchor=tk.NW, image=bg)
    #Create the title

    canvas.create_text(750, 240, text="SPRAY 'N' PRAY ", fill="black", font=('Helvetica 35 bold'),angle=270)
    timer_text = canvas.create_text(400, 400, text="1", fill="black", font=('Helvetica 35 bold'),angle=270)


    canvas.place(x=0,y=0)

    # # Blue #57a09e
    # # Red #d94c26
    # # Fawn #efe2af



    s = Style()
    s.theme_use('clam')
    s.configure("red.Horizontal.TProgressbar", troughcolor="#efe2af", 
                    bordercolor="#efe2af",background = "#57a09e", lightcolor="#57a09e", 
                    darkcolor="#57a09e")

    # print("Height (px) = {0}".format(win.winfo_screenheight())) #480
    # print("Width (px) = {0}".format(win.winfo_screenwidth())) #800

    # add progress bar to track the serial data
    progress = Progressbar(win, style="red.Horizontal.TProgressbar", orient = tk.HORIZONTAL, length = 700, mode = 'determinate') 
    progress.place(x=0, y=140, height=200)

    # Create a button to exit the gui
    exit_button=tk.Button(win, text= "❌", command=exit, activebackground="#efe2af", bg="#efe2af",font=("Helvetica", 10),relief=tk.FLAT)
    exit_button.place(x=0, y=0)
    # Create a button to restart the gui
    rst_button=tk.Button(win, text= "⟳", command=restart, activebackground="#efe2af", bg="#efe2af",font=("Helvetica", 10),relief=tk.FLAT)
    rst_button.place(x=0, y=30)




    while(1):
        win.update()
        if(ser.in_waiting): # If there is a message to be read
            val  = int(ser.read_until().decode("utf-8"))
            progress['value'] = val
            if val  >= 100:
                progress.destroy()
                canvas.create_rectangle(300, 10, 500, 470, outline = "#efe2af", fill = "#57a09e", width = 2)
                canvas.create_text(450, 240, text="WINNER!", fill="black", font=('Helvetica 25 bold'),angle=270 )
                canvas.create_text(400, 240, text="Your time was", fill="black", font=('Helvetica 25 bold'),angle=270 )
                canvas.create_text(350, 240, text="{0} seconds".format(round((time.time() - start_time),2)), fill="black", font=('Helvetica 25 bold'),angle=270 )
                win.update()
                while(1):
                    win.update()
                    if(ser.in_waiting):
                        data = str(ser.read_until().decode("utf-8"))
                        if "RESET" in data:
                            restart() # Restarts the program
                        else:
                            print(data)
        timer = int(time.time() - start_time)
        #timer = round((time.time() - start_time),2)
        canvas.itemconfig(timer_text,text=timer) # display th value from the Mega
        # Update time since program start




if __name__ == '__main__':
    main()