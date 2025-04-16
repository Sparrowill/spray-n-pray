#!/usr/bin/python

import tkinter as tk
from tkinter.ttk import *

import serial 
import time
import os
import logging

class UI():
    def __init__(self):
        self.win = tk.Tk()
        self.canvas= tk.Canvas(self.win, width= 800, height= 480, )
        self.s = Style()
        self.s.theme_use('clam')
        self.s.configure("red.Horizontal.TProgressbar", troughcolor="#efe2af", 
                    bordercolor="#efe2af",background = "#57a09e", lightcolor="#57a09e", 
                    darkcolor="#57a09e")
        self.countdownActive = False
        self.progressBarActive = False
        self.successTextActive = False


    def setup(self):
        self.win.configure(cursor='none')
        # Create the background
        self.bg = tk.PhotoImage(file = "/home/pi/Documents/spray-n-pray/ui/bg.png")
        self.canvas.create_image(0,0,anchor=tk.NW, image=self.bg)
        #Create the title
        self.canvas.create_text(750, 240, text="SPRAY 'N' PRAY ", fill="black", font=('Helvetica 35 bold'),angle=270)
        #Create the timer
        self.timer_text = self.canvas.create_text(400, 400, text="0", fill="black", font=('Helvetica 35 bold'),angle=270)
        # Create a button to exit the gui
        exit_button=tk.Button(self.win, text= "❌", command=exit, activebackground="#efe2af", bg="#efe2af",font=("Helvetica", 10),relief=tk.FLAT)
        exit_button.place(x=0, y=0)

        self.canvas.place(x=0,y=0)

         # Full Screen the widget
        self.win.overrideredirect(True)
        self.win.geometry("{0}x{1}+0+0".format(self.win.winfo_screenwidth(), self.win.winfo_screenheight()))
        self.win.attributes("-fullscreen", True) 
        self.win.update()

    def create_countdown(self):
        if not self.countdownActive:
            self.countdown_rect = self.canvas.create_rectangle(300, 10, 500, 470, outline = "#efe2af", fill = "#57a09e", width = 2)
            self.countdown_text_1 = self.canvas.create_text(450, 240, text="READY?", fill="black", font=('Helvetica 25 bold'),angle=270 )
            self.countdown_text_2 = self.canvas.create_text(400, 240, text="Your time starts in", fill="black", font=('Helvetica 25 bold'),angle=270 )
            self.countdown_text_3 = self.canvas.create_text(350, 240, text="", fill="black", font=('Helvetica 25 bold'),angle=270 )
            self.countdownActive=True
        else:
            logging.error("ERR: Cannot re-create countdown, it already exists")
    def update_countdown(self,num):
        if self.countdownActive:
            self.canvas.itemconfig(self.countdown_text_3,text=num)
        else:
            logging.error("ERR: Cannot update countdown, it doesn't exist")

    def delete_countdown(self):
        if self.countdownActive:
            # Delete countdown box
            self.canvas.delete(self.countdown_rect)
            self.canvas.delete(self.countdown_text_1)
            self.canvas.delete(self.countdown_text_2)
            self.canvas.delete(self.countdown_text_3)
            self.countdownActive = False
        else:
            logging.error("ERR: Cannot delete countdown, it doesn't exist")
    def create_progress_bar(self):
        if not self.progressBarActive:
            # add progress bar to track the serial data
            self.progress = Progressbar(self.win, style="red.Horizontal.TProgressbar", orient = tk.HORIZONTAL, length = 700, mode = 'determinate') 
            self.progress.place(x=0, y=140, height=200)
            self.progressBarActive = True
        else:
            logging.error("ERR: Cannot create progress bar, it already exists")

    def update_progress_bar(self,value):
        if self.progressBarActive:
            self.progress['value'] = int(value)   
        else:
            logging.error("ERR: Cannot update progress bar, it doesn't exist")

    def delete_progress_bar(self):
        if self.progressBarActive:
            self.progress.destroy()
            self.progressBarActive =False
        else:
           logging.error("ERR: Cannot delete progress bar, it doesn't exist") 

    def create_success_text(self,timeTaken):
        if not self.successTextActive:
            self.success_rect = self.canvas.create_rectangle(300, 10, 500, 470, outline = "#efe2af", fill = "#57a09e", width = 2)
            self.success_text_1 = self.canvas.create_text(450, 240, text="WINNER!", fill="black", font=('Helvetica 25 bold'),angle=270 )
            self.success_text_2 = self.canvas.create_text(400, 240, text="Your time was", fill="black", font=('Helvetica 25 bold'),angle=270 )
            self.success_text_3 = self.canvas.create_text(350, 240, text="{0} seconds".format(timeTaken), fill="black", font=('Helvetica 25 bold'),angle=270 )
            self.successTextActive = True
        else:
            logging.error("ERR: Cannot create success text, it already exists")


    def delete_success_text(self):
        if self.successTextActive:
            self.canvas.delete(self.success_rect)
            self.canvas.delete(self.success_text_1)
            self.canvas.delete(self.success_text_2)
            self.canvas.delete(self.success_text_3)
            self.successTextActive =False
        else:
           logging.error("ERR: Cannot delete success text, it doesn't exist") 
    def update_timer(self,timeTaken):
        self.canvas.itemconfig(self.timer_text,text=timeTaken)

    def teardown(self):
        self.delete_countdown()
        self.delete_progress_bar()
        self.delete_success_text()

    def update_gui(self):
        self.win.update()

def main():
    logging.basicConfig(filename="/home/pi/logs/{0}.log".format(time.time()), level=logging.INFO)
    logging.info("Before everything()")

    ser = serial.Serial('/dev/ttyACM0', baudrate=115200)
    ui = UI()
    ui.setup()
    firstEntry = True
    logging.info("Before while(1)")
    while(1):
        if firstEntry:
            # Effectively a soft restart
            startTime = 0
            timerActive = False
            ui.create_countdown()
            firstEntry = False
        ui.update_gui()
        if(ser.in_waiting): # If there is a message to be read
            ser_read = ser.read_until()
            val  = ser_read.decode("utf-8")
            str_val = str(val)
            if str_val == "\r\n":
                logging.info("Got new setup() func on Arduino")
            elif "RESET" in str_val:
                ui.teardown()
                firstEntry = True
            elif "COUNTDOWN" in str_val:
                if "0" in str_val:
                    ui.delete_countdown()
                    ui.create_progress_bar()
                    startTime = time.time()
                    timerActive = True
                elif "1" in str_val:
                    ui.update_countdown("1")
                elif "2" in str_val:
                    ui.update_countdown("2")   
                elif "3" in str_val:
                    ui.update_countdown("3")
                elif "4" in str_val:
                    ui.update_countdown("4")  
                elif "5" in str_val:
                    ui.update_countdown("5")
            elif int(val)  < 100:
                ui.update_progress_bar(val)
            elif int(val) >= 100:
                #Game complete
                timerActive = False
                ui.delete_progress_bar()
                timeTaken = round((time.time() - startTime),2)
                ui.create_success_text(timeTaken)
        if(timerActive):
            timeTaken = int(time.time() - startTime)   
            ui.update_timer(timeTaken) 



if __name__ == '__main__':
    main()