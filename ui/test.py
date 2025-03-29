#!/usr/bin/python

import tkinter as tk
from tkinter.ttk import *

import serial 
import time
import os, sys
time.sleep(2)
# Create an instance of tkinter frame or widget
win = tk.Tk()
win.configure(cursor="none")


# Create a canvas to hold all the stuff apart from the progress bar
canvas= tk.Canvas(win, width= 800, height= 480, )

def restart():
    print("User Reset")
    # Destroy and then re-set up
    python = sys.executable
    os.execl(python, python, * sys.argv)

def exit():
    global win
    print("User Quit")
    win.destroy()
    sys.exit()

def main():
    ser = serial.Serial('/dev/ttyACM0', baudrate=115200)

    global win 
    global canvas
    #Create the background
    bg=tk.PhotoImage(file = "bg.png")
    canvas.create_image(0,0,anchor=tk.NW, image=bg)
    #Create the title
    canvas.create_text(750, 240, text="SPRAY 'N' PRAY ", fill="black", font=('Helvetica 35 bold'),angle=270)
    timer_text = canvas.create_text(400, 400, text="1", fill="black", font=('Helvetica 35 bold'),angle=270)
    countdown_rect = canvas.create_rectangle(300, 10, 500, 470, outline = "#efe2af", fill = "#57a09e", width = 2)
    countdown_text_1 = canvas.create_text(450, 240, text="READY?", fill="black", font=('Helvetica 25 bold'),angle=270 )
    countdown_text_2 = canvas.create_text(400, 240, text="Your time starts in", fill="black", font=('Helvetica 25 bold'),angle=270 )
    countdown_text_3 = canvas.create_text(350, 240, text="5", fill="black", font=('Helvetica 25 bold'),angle=270 )

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

    # Create a button to exit the gui
    exit_button=tk.Button(win, text= "❌", command=exit, activebackground="#efe2af", bg="#efe2af",font=("Helvetica", 10),relief=tk.FLAT)
    exit_button.place(x=0, y=0)
    # Create a button to restart the gui
    rst_button=tk.Button(win, text= "⟳", command=restart, activebackground="#efe2af", bg="#efe2af",font=("Helvetica", 10),relief=tk.FLAT)
    rst_button.place(x=0, y=30)

    time.sleep(2)
    # Full Screen the widget
    win.overrideredirect(True)
    win.geometry("{0}x{1}+0+0".format(win.winfo_screenwidth(), win.winfo_screenheight()))
    win.attributes("-fullscreen", True) 
    win.update()
    timer_active = False
    while(1):
        win.update()
        if(ser.in_waiting): # If there is a message to be read
            val  = ser.read_until().decode("utf-8")
            str_val = str(val)
            if "RESET" in str_val:
                canvas_items = canvas.find_all()
                for tag in canvas_items:
                    canvas.delete(tag)
                ser.close()
                main()
                #restart() # Restarts the program
            elif "COUNTDOWN" in str_val:
                if "0" in str_val:
                    # Delete countdown box
                    canvas.delete(countdown_rect)
                    canvas.delete(countdown_text_1)
                    canvas.delete(countdown_text_2)
                    canvas.delete(countdown_text_3)
                    # add progress bar to track the serial data
                    progress = Progressbar(win, style="red.Horizontal.TProgressbar", orient = tk.HORIZONTAL, length = 700, mode = 'determinate') 
                    progress.place(x=0, y=140, height=200)
                    start_time = time.time()
                    timer_active = True
                elif "1" in str_val:
                    canvas.itemconfig(countdown_text_3,text="1");
                elif "2" in str_val:
                    canvas.itemconfig(countdown_text_3,text="2");    
                elif "3" in str_val:
                    canvas.itemconfig(countdown_text_3,text="3");
                elif "4" in str_val:
                    canvas.itemconfig(countdown_text_3,text="4");    
                elif "5" in str_val:
                    canvas.itemconfig(countdown_text_3,text="5");         
            elif int(val)  < 102:
                progress['value'] = int(val) 
                if int(val)  >= 100:
                    timer_active = False
                    progress.destroy()
                    canvas.create_rectangle(300, 10, 500, 470, outline = "#efe2af", fill = "#57a09e", width = 2)
                    canvas.create_text(450, 240, text="WINNER!", fill="black", font=('Helvetica 25 bold'),angle=270 )
                    canvas.create_text(400, 240, text="Your time was", fill="black", font=('Helvetica 25 bold'),angle=270 )
                    canvas.create_text(350, 240, text="{0} seconds".format(round((time.time() - start_time),2)), fill="black", font=('Helvetica 25 bold'),angle=270 )
        if timer_active:
            timer = int(time.time() - start_time)
            #timer = round((time.time() - start_time),2)
            canvas.itemconfig(timer_text,text=timer) # display the value from the Mega
            # Update time since program start




if __name__ == '__main__':
    main()