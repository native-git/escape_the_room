#!/usr/bin/env python

from Tkinter import *
from time import sleep
import threading
import rospy
from std_msgs.msg import ColorRGBA

large_font = ('Verdana',50)
medium_font = ('Verdana',28)
small_font = ('Verdana',20)

rospy.init_node('escape_room')
pub = rospy.Publisher('/chatter2', ColorRGBA, queue_size=10)
rate = rospy.Rate(10)

alarm_active = True

def phone_thread():
	global alarm_active
	while not rospy.is_shutdown():
		if alarm_active:
			r = 255
			g = 0
			b = 0
		else:
			r = 0
			g = 255
			b = 0
		publish_color(r,g,b)

def publish_color(r,g,b):
	msg = ColorRGBA()
	msg.r = r
	msg.b = b
	msg.g = g
	pub.publish(msg)
	rate.sleep()

c_thread = threading.Thread(target=phone_thread)
c_thread.daemon = True
c_thread.start()

pin = '2758'
phrase = 'happybdaycraig!'

app = Tk()

last_message = ""

hint = "CLUE #3: The KEY to solving this puzzle is coming back to this later. In the meantime, why don't you grab a nice BOOK... might I recommend 'The One Thing', by Keller Papasan"

def check_password(p):
	global last_message
	if p == "":
		message = last_message
	elif not p.isdigit():
		message = "The pin should only contain 4-digits (0-9), you included something else: " + str(p)
	elif p == pin:
		message = "Congratulations, you have entered the correct PIN"
		#return message
	elif len(list(p))>4:
		message = "You have entered in more than four numbers: " + str(p)
		#return message
	elif len(list(p))<4:
		message = "You have entered in less than four numbers: " + str(p)
	else:
		message = "You have entered in the wrong PIN: " + str(p)
		#return message
	last_message = message
	return message

count = 0

T2 = Text(app, height=1, width=70, font=small_font,background="black",foreground="white",borderwidth=0,highlightthickness=0)
T2.place(relx=0.5,rely=0.9,anchor=CENTER)

def blink():
	global alarm_active
	T1.config(foreground="black")
	if alarm_active:
		T1.after(1000, lambda: T1.config(foreground="red"))
	else:
		T1.delete('1.0', END)
		T1.insert(END, "Alarm Status <DISABLED>")
		T1.after(1000, lambda: T1.config(foreground="green"))

def keep_blinking():
	while True:
		sleep(2)
		blink()

def show2(event):
	global alarm_active
	p = password.get()
	if p == phrase:
		print "The Alarm is disabled"
		alarm_active = False
	passEntry.delete(0,'end')
	passEntry.focus()

def round_2():
	global alarm_active
	passEntry.delete(0,'end')
	passEntry.focus()
	app.bind('<Return>', show2)
	passEntry.config(width=10)
	passEntry.place(relx=0.5,rely=0.6)
	T2.delete('1.0', END)
	T1.delete('1.0', END)
	T1.config(foreground="red",width=55)
	T.delete('1.0', END)
	T.place(relx=0.8,rely=0.1)
	T.config(font=medium_font)
	T.insert(END, 'SecuriMAX Anti-burglary Alarm Software System')
	T1.place(relx=0.7,rely=0.8)
	T1.insert(END, 'Alarm Status <ENABLED>')
	T2.place(relx=0.5,rely=0.5)
	T3 = Text(app, height=3, width=50, font=small_font,background="black",foreground="white",borderwidth=0,highlightthickness=0,wrap=WORD)
	T3.place(relx= 0.1, rely=0.2)
	T3.insert(END,hint)
	T2.insert(END, 'Please Enter your password below to disable the alarm...')
	blink_thread = threading.Thread(target=keep_blinking)
	blink_thread.daemon =True
	blink_thread.start()
	#blink()

def show(event):
	global count
	p = password.get() #get password from entry
	if p != "":
		count += 1
	if count >=3:
		T2.delete('1.0',END)
		T2.insert(END, "Remember, my favorite animals IN ORDER are -> lamb,frog,cat,rabbit...")
	#print(p)
	T1.delete('1.0',END)
	T1.insert(END, check_password(p))
	if p == pin:
		T1.config(foreground="green")
		app.after(2000, round_2)
	else:
		T1.config(foreground="white")
		passEntry.delete(0,'end')
		passEntry.focus()

def fullscreen_on(event):
	app.attributes("-fullscreen", True)

def fullscreen_off(event):
	app.attributes("-fullscreen", False)

app.bind('<Escape>',fullscreen_off)
app.bind('<F11>',fullscreen_on)
app.bind('<Return>',show)
app.configure(background="black")
app.attributes("-fullscreen",True)
password = StringVar() #Password variable
#passEntry = Entry(app, textvariable=password, show='*').pack()
passEntry = Entry(app, textvariable=password, show='*',font=large_font,width=4,justify=CENTER)
passEntry.place(relx=0.5,rely=0.5,anchor=CENTER)
T = Text(app, height=1, width=70, font=small_font,background="black",foreground="white",borderwidth=0,highlightthickness=0)
T.insert(END,"Please type in your 4-Digit PIN, then press ENTER to continue...")
T.place(relx=0.5,rely=0.25,anchor=CENTER)
T1 = Text(app, height=1, width=70, font=small_font,background="black",foreground="white",borderwidth=0,highlightthickness=0)
T1.place(relx=0.5,rely=0.75,anchor=CENTER)
passEntry.focus()

#print dir(Entry())
#submit = Button(app, text='Show Console',command=show).pack()      
app.mainloop()