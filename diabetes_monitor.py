import sys, pygame, os
import math
import pandas as pd
import numpy as np
from pygame.locals import *
import datetime

# Stores relevant info for a patient
class Patient:
    def __init__(self, name: str, id: str, doc_name: str, doc_phone: str, low: int, high: int):
        self.name = name
        self.id = id
        self.doc_name = doc_name
        self.doc_phone = doc_phone
        self.low = low
        self.high = high



pygame.init()

clock = pygame.time.Clock()

# set dimensions and font for display
X = 1280
Y = 720
font = pygame.font.SysFont('microsoftsansserif', 24)
tip = pygame.font.SysFont('microsoftsansserif', 16)

# create display and set window title
display = pygame.display.set_mode((X, Y))
pygame.display.set_caption("Murray, Chelsea - Glucose Monitoring System")

# set directory for help docs and results
cd = os.path.dirname(__file__)
help_dir = os.path.join(cd, 'HELP/')
res_dir = os.path.join(cd, 'Results/')

# if file path doesn't exist, make results file path
if not os.path.isdir(res_dir):
    os.makedirs(res_dir)

# set patient data
pt1 = Patient("Sara Norman", "5344-9709", "Dr. Jason Rosenberg", "579-0432", 80, 140)
pt2 = Patient("Gregg Norman", "1275-4307", "Dr. Nikhil Singh", "334-2309", 70, 120)


# Displays a message for operating the system
# Uses given text as displayed message
# x,y are the center of the text's location
def DisplayText(x, y, msg, col = "black", f = font):
	txt = f.render(msg, True, col)
	msg_box = txt.get_rect()
	msg_box.center = (x, y)
	display.blit(txt, msg_box)
	return msg_box


# Displays patient info in bottom left of display.
def DisplayPatientInfo(pt: Patient):
    DisplayText(150, Y-20, pt.name + "   " + pt.id, "midnightblue")
    return DrawButton(X-85, Y-30, 150, 50, 'slateblue', 'Log Out')
    

# Draws a button to be clicked.
def DrawButton(x, y, w, h, col: str, msg: str):
    box = pygame.Rect(x - (w/2), y - (h/2), w, h)
    pygame.draw.rect(display, col, box)
    
    DisplayText(x, y, msg)
    
    return box


# Draws a "Help"/tip button.
def DrawHelp(x, y, col="gold"):
	help = pygame.draw.circle(display, col, (x, y), 20)
	DisplayText(x, y, "i")

	return help


# Displays a login screen
# Also displays each name for patient to log in
def DisplayLoginScreen(pt1: Patient, pt2: Patient):
	# fill display with a light background
	display.fill('aliceblue')

	# basic instruction
	greet = 'Welcome! Please select your name to log in.'
	DisplayText(X/2, Y-600, greet)


	# draw each patient's login button
	first = DrawButton(X/2, Y-350, 600, 100, 'lightskyblue', pt1.name)
	second = DrawButton(X/2, Y-150, 600, 100, 'lightskyblue', pt2.name)

	# draw a "Help" icon (yellow circle with 'i' in the middle)
	#help = pygame.draw.circle(display, "gold", (X-120, 80), 20)
	help = DrawHelp(X-120, 80)

	#DisplayText(X-120, 80, "i")
	
	pygame.display.flip()

	running = True
    
	# wait for click on one of the buttons
	while running:
		pos = pygame.mouse.get_pos()
		if help.collidepoint(pos):
			tip_box = pygame.Rect(X - 230, 110,  220, 22)
			pygame.draw.rect(display, 'lavender', tip_box)
			DisplayText(X-120, 120, "Click your name to continue.", col="indigo", f=tip)
			pygame.display.flip()
		for event in pygame.event.get():
			# exit program if X is clicked
			if event.type == pygame.QUIT:
				exit()
			# if left mouse button clicks, get mouse position
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				pos = pygame.mouse.get_pos()
				# check if either login button clicked, 
    			# login that patient & move on if yes
				if first.collidepoint(pos):
					running = False
					DisplayReadingScreen(pt1)
				elif second.collidepoint(pos):
					running = False
					DisplayReadingScreen(pt2)
				elif help.collidepoint(pos):
					os.startfile(help_dir + 'LOGIN.txt')
					




# Displays a screen asking if the user has taken a glucose reading,
# then accepting a number as input
def DisplayReadingScreen(pt: Patient):
	# fill the screen to make a light background
	display.fill('aliceblue')
		
  
	# display patient info in corner & logout button
	# in other corner
	logout = DisplayPatientInfo(pt)
 
 
    # ask if patient has taken reading yet
	msg = 'Have you taken your blood sugar reading yet?'
	DisplayText(X/2, Y-600, msg)
 
	# draw buttons for each option y/n
	yes = DrawButton((X/2)-150, Y-350, 200, 100, 'springgreen', "Yes")
	no = DrawButton((X/2)+150, Y-350, 200, 100, 'lightcoral', "No")
 
	# draw "Help" tip
	help = DrawHelp(X-120, 80)

	
	pygame.display.flip()

	running = True
    
	# wait for click on one of the buttons
	while running:
		# if pt mouses over help button, display a short tip
		pos = pygame.mouse.get_pos()
		if help.collidepoint(pos):
			tip_box = pygame.Rect(X - 212, 110,  184, 44)
			pygame.draw.rect(display, 'lavender', tip_box)
			DisplayText(X-120, 120, "Click 'Yes' if you have;", col="indigo", f=tip)
			DisplayText(X-120, 142, "click 'No' if you haven't.", col="indigo", f=tip)
			pygame.display.flip()
		for event in pygame.event.get():
			# exit program if X is clicked
			if event.type == pygame.QUIT:
				exit()
			# if left mouse button clicks, get mouse position
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				pos = pygame.mouse.get_pos()
				# check if either button clicked, 
    			# request glucose levels if yes
				if yes.collidepoint(pos):
					running = False
					RequestGlucose(pt)
				# request the patient test their levels if no
				elif no.collidepoint(pos):
					running = False
					RequestTest(pt)
				# present information if help clicked
				elif help.collidepoint(pos):
					os.startfile(help_dir + 'READING.txt')
				# return to login if "logout" clicked
				elif logout.collidepoint(pos):
					DisplayLoginScreen(pt1, pt2)
					
     
     
     
     
# a screen to take in the glucose reading
# (this is called by the reading screen)
def RequestGlucose(pt: Patient):
    # fill the screen to make a light background
	display.fill('aliceblue')
 
	# display patient info in corner
	logout = DisplayPatientInfo(pt)
		
    # ask if patient has taken reading yet
	msg = 'Please enter your reading below.'
	DisplayText(X/2, Y-600, msg)
 
	# draw help/tip button
	help = DrawHelp(X-120, 80)

	pygame.display.flip()

	# create text input box 
	input = pygame.Rect((X/2)-100, Y-400, 200, 32)
	active = False

	# set default glucose value to an invalid value
	# and default input string to empty
	glucose = -1
	gl_str = ''

	running = True

	while running:
		pos = pygame.mouse.get_pos()
		if help.collidepoint(pos):
			tip_box = pygame.Rect(X - 212, 110,  184, 44)
			pygame.draw.rect(display, 'lavender', tip_box)
			DisplayText(X-120, 120, "Enter your sugar reading,", col="indigo", f=tip)
			DisplayText(X-120, 142, "in the range of 0-999.", col="indigo", f=tip)
			pygame.display.flip()
		for event in pygame.event.get():
			# exit program if X is clicked
			if event.type == pygame.QUIT:
				exit()
			# if a key is pressed while the text entry is "active":
			if event.type == pygame.KEYDOWN and active: 
				# if the key is "backspace", reduce length of input by 1
				if event.key == pygame.K_BACKSPACE:
					gl_str = gl_str[:-1]
				# if the key is "enter", attempt to convert the glucose value
				elif event.key == pygame.K_RETURN:
					try:
						glucose = int(gl_str)
						if glucose >= 0 and glucose < 1000:
							running = False
							DisplayResults(glucose, pt)
						# if outside 0-999 value range, user must try again
						else:
							err = 'Please enter a number between 0 and 999.'
							DisplayText(X/2, Y-350, err, col="darkred", f=tip)
							pygame.display.update()
							gl_str = ''
					# if string can't be casted to int, ask user to enter it again
					except:
						err = 'Please enter a number between 0 and 999.'
						DisplayText(X/2, Y-350, err, col="darkred", f=tip)
						pygame.display.update()
						gl_str = ''
				# if neither of those keys, then add the pressed key to the input string
				# input can be max 3 characters
				elif len(gl_str) < 4:
					gl_str += event.unicode
				# inform patient if they have exceeded 3 character limit
				else:
					err = 'Please enter a number between 0 and 999.'
					DisplayText(X/2, Y-350, err, col="darkred", f=tip)
					pygame.display.update()
				
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				pos = pygame.mouse.get_pos()
				# if text entry box clicked, make text entry active
				if input.collidepoint(pos):
					active = True
				else:
					active = False
				# if help/tip clicked, show full help file
				if help.collidepoint(pos):
					os.startfile(help_dir + 'READING.txt')
				# return to login if "logout" clicked
				elif logout.collidepoint(pos):
					DisplayLoginScreen(pt1, pt2)
		
		# text entry box is a darker grey if inactive/not accepting text
		if active:
			pygame.draw.rect(display, 'lightsteelblue', input)
		else:
			pygame.draw.rect(display, 'slategrey', input)

		# render currently entered input over text box
		txt = font.render(gl_str, True, 'black')
		display.blit(txt, (input.x+3, input.y+3))

		pygame.display.flip()
  
	DisplayResults(glucose, pt)



# asks patient to take a reading if they don't have one ready
# called by the reading screen
def RequestTest(pt: Patient):
    # fill the screen to make a light background
	display.fill('aliceblue')
 
	# display patient info in corner
	logout = DisplayPatientInfo(pt)
		
    # ask if patient has taken reading yet
	msg = 'Please take your blood sugar reading as soon as possible.'
	DisplayText(X/2, Y-600, msg)

	msg = 'Follow the instructions provided with your glucose monitor.'
	DisplayText(X/2, Y-400, msg)
 
	# draw 'OK' button and help button
	ok = DrawButton(X/2, Y-200, 200, 100, 'lightskyblue', "OK")
	help = DrawHelp(X-120, 80)

	pygame.display.flip()

	running = True
    
	while running:
		pos = pygame.mouse.get_pos()
		if help.collidepoint(pos):
			tip_box = pygame.Rect(X - 207, 110,  174, 22)
			pygame.draw.rect(display, 'lavender', tip_box)
			box = DisplayText(X-120, 120, "Click 'OK' to continue.", col="indigo", f=tip)
			print(box.width)
			pygame.display.flip()
		for event in pygame.event.get():
			# exit program if X is clicked
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				pos = pygame.mouse.get_pos()
				# exit this screen and return to reading screen if OK is clicked
				if ok.collidepoint(pos):
					running = False
					DisplayReadingScreen(pt)
				# open help file if help button clicked
				elif help.collidepoint(pos):
					os.startfile(help_dir + 'READING.txt')
				# return to login if "logout" clicked
				elif logout.collidepoint(pos):
					DisplayLoginScreen(pt1, pt2)


# Displays an info screen to tell player what their glucose levels mean
# Either high, normal, or low range
def DisplayResults(glucose: int, pt: Patient):
    
	reason = "N/A"
	ketones = False
    
	if glucose < pt.low:
		DisplayForLow(glucose, pt)
	elif glucose > pt.high:
		DisplayForHigh(glucose, pt)
	else:
		DisplayForNormal(glucose, pt)



# display warning for low glucose
# called by result screen
def DisplayForLow(glucose: int, pt: Patient):
    # fill the screen to make a light background
	display.fill('aliceblue')
 
	# display patient info in corner
	logout = DisplayPatientInfo(pt)
		
    # ask if patient has taken reading yet
	msg1 = 'Your blood sugar is below the acceptable threshold of ' + str(pt.low) + '.'
	DisplayText(X/2, Y-600, msg1, col="darkred")

	msg2 = 'Please eat a source of sugar, take your medications, and continue to'
	DisplayText(X/2, Y-500, msg2)
 
	msg3 = 'have regular snacks and meals as directed by your doctor.'
	DisplayText(X/2, Y-470, msg3)
 
	# draw 'Next' and help/tip buttons
	next = DrawButton(X/2, Y-300, 200, 100, 'lightskyblue', "Next")
	help = DrawHelp(X-120, 80)
	
	pygame.display.flip()

	running = True
    
	while running:
		#display tip if mouse goes over tip button
		pos = pygame.mouse.get_pos()
		if help.collidepoint(pos):
			tip_box = pygame.Rect(X - 207, 110,  174, 22)
			pygame.draw.rect(display, 'lavender', tip_box)
			box = DisplayText(X-120, 120, "Click 'Next' to continue.", col="indigo", f=tip)
			print(box.width)
			pygame.display.flip()
		for event in pygame.event.get():
			# exit program if X is clicked
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				pos = pygame.mouse.get_pos()
				# ask for reason, record data, and go to logout screen
				# if patient chooses to proceed from here
				if next.collidepoint(pos):
					running = False
					reason = DisplayAskReason(pt)
					RecordData(pt, glucose, False, reason)
					DisplayLogout(pt)
				# open help file if help button clicked
				elif help.collidepoint(pos):
					os.startfile(help_dir + 'LOW.txt')
				# return to login if "logout" clicked
				elif logout.collidepoint(pos):
					DisplayLoginScreen(pt1, pt2)
    
    
# display warning for high glucose
# called by result screen
def DisplayForHigh(glucose: int, pt: Patient):
    # fill the screen to make a light background
	display.fill('aliceblue')
 
	# display patient info in corner
	logout = DisplayPatientInfo(pt)
		
    # ask if patient has taken reading yet
	msg1 = 'Your blood sugar is above the acceptable threshold of ' + str(pt.high) + '.'
	DisplayText(X/2, Y-600, msg1, col="darkred")

	msg2 = 'Please contact your doctor immediately.'
	DisplayText(X/2, Y-500, msg2)
 
	msg3 = pt.doc_name + ": " + pt.doc_phone
	DisplayText(X/2, Y-400, msg3, col="midnightblue")
 
	# draw 'Next' and help/tip buttons
	next = DrawButton(X/2, Y-300, 200, 100, 'lightskyblue', "Next")
	help = DrawHelp(X-120, 80)
	
	pygame.display.flip()

	running = True
    
	while running:
		# display tip if mouse goes over help/tip
		pos = pygame.mouse.get_pos()
		if help.collidepoint(pos):
			tip_box = pygame.Rect(X - 207, 110,  174, 22)
			pygame.draw.rect(display, 'lavender', tip_box)
			box = DisplayText(X-120, 120, "Click 'Next' to continue.", col="indigo", f=tip)
			print(box.width)
			pygame.display.flip()
		for event in pygame.event.get():
			# exit program if X is clicked
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				pos = pygame.mouse.get_pos()
				# ask about ketones and reason for abnormal reading
				# & then go to logout screen, if patient clicks next
				if next.collidepoint(pos):
					running = False
					ketones = DisplayKetonesPrompt(pt)
					reason = DisplayAskReason(pt)
					RecordData(pt, glucose, False, reason)
					DisplayLogout(pt)
				# open help file if help button clicked
				elif help.collidepoint(pos):
					os.startfile(help_dir + 'HIGH.txt')
				# return to login if "logout" clicked
				elif logout.collidepoint(pos):
					DisplayLoginScreen(pt1, pt2)
    
    
    
# display screen notifying that sugar is normal range
# called by result screen
def DisplayForNormal(glucose: int, pt: Patient):
    # fill the screen to make a light background
	display.fill('aliceblue')
 
	# display patient info in corner
	logout = DisplayPatientInfo(pt)
		
    # ask if patient has taken reading yet
	msg1 = 'Your blood sugar is within expected levels.'
	DisplayText(X/2, Y-500, msg1)
 
	# draw 'Next' and help/tip buttons
	next = DrawButton(X/2, Y-300, 200, 100, 'lightskyblue', "Next")
	help = DrawHelp(X-120, 80)
 
	while running:
		# display tip if mouse goes over help/tip
		pos = pygame.mouse.get_pos()
		if help.collidepoint(pos):
			tip_box = pygame.Rect(X - 207, 110,  174, 22)
			pygame.draw.rect(display, 'lavender', tip_box)
			box = DisplayText(X-120, 120, "Click 'Next' to continue.", col="indigo", f=tip)
			print(box.width)
			pygame.display.flip()
		for event in pygame.event.get():
			# exit program if X is clicked
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				pos = pygame.mouse.get_pos()
				# ask about ketones and reason for abnormal reading
				# & then go to logout screen, if patient clicks next
				if next.collidepoint(pos):
					running = False
					RecordData(pt, glucose, False, "N/A - Normal Levels")
					DisplayLogout(pt)
				# open help file if help button clicked
				elif help.collidepoint(pos):
					os.startfile(help_dir + 'READING.txt')
				# return to login if "logout" clicked
				elif logout.collidepoint(pos):
					DisplayLoginScreen(pt1, pt2)

 
# Displays a screen prompting user to respond about potential
# ketones in their urine.
def DisplayKetonesPrompt(pt: Patient):
    # fill the screen to make a light background
	display.fill('aliceblue')
		
  
	# display patient info in corner & logout button
	# in other corner
	logout = DisplayPatientInfo(pt)
 
 
    # ask if patient has taken reading yet
	msg = 'Are there ketones in your urine?'
	DisplayText(X/2, Y-600, msg)
 
	# draw buttons for each option y/n
	yes = DrawButton((X/2)-150, Y-350, 200, 100, 'springgreen', "Yes")
	no = DrawButton((X/2)+150, Y-350, 200, 100, 'lightcoral', "No")
 
	# draw "Help" tip
	help = DrawHelp(X-120, 80)

	
	pygame.display.flip()

	running = True
    
	# wait for click on one of the buttons
	while running:
		# if pt mouses over help button, display a short tip
		pos = pygame.mouse.get_pos()
		if help.collidepoint(pos):
			tip_box = pygame.Rect(X - 212, 110,  184, 44)
			pygame.draw.rect(display, 'lavender', tip_box)
			DisplayText(X-120, 120, "Click 'Yes' if there are;", col="indigo", f=tip)
			DisplayText(X-120, 142, "click 'No' if there aren't.", col="indigo", f=tip)
			pygame.display.flip()
		for event in pygame.event.get():
			# exit program if X is clicked
			if event.type == pygame.QUIT:
				exit()
			# if left mouse button clicks, get mouse position
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				pos = pygame.mouse.get_pos()
				# check if either button clicked, 
    			# request glucose levels if yes
				if yes.collidepoint(pos):
					running = False
					return True
				# request the patient test their levels if no
				elif no.collidepoint(pos):
					running = False
					return False
				# present information if help clicked
				elif help.collidepoint(pos):
					os.startfile(help_dir + 'HIGH.txt')
				# return to login if "logout" clicked
				elif logout.collidepoint(pos):
					DisplayLoginScreen(pt1, pt2)


# Displays a prompt for the user to explain possible causes
# of high/low glucose levels.
def DisplayAskReason(pt: Patient):
    # fill the screen to make a light background
	display.fill('aliceblue')
 
	# display patient info in corner
	logout = DisplayPatientInfo(pt)
		
    # ask if patient has taken reading yet
	msg = 'Please enter any possible reasons for an abnormal reading.'
	DisplayText(X/2, Y-600, msg)
 
	# draw help/tip button
	help = DrawHelp(X-120, 80)

	pygame.display.flip()

	# create text input box 
	input = pygame.Rect((X/2)-200, Y-400, 400, 32)
	active = False

	# set default input string to empty
	reasons = ''

	running = True

	while running:
		pos = pygame.mouse.get_pos()
		if help.collidepoint(pos):
			tip_box = pygame.Rect(X - 212, 110,  184, 44)
			pygame.draw.rect(display, 'lavender', tip_box)
			DisplayText(X-120, 120, "Enter any likely causes", col="indigo", f=tip)
			DisplayText(X-120, 142, "in the text box.", col="indigo", f=tip)
			pygame.display.flip()
		for event in pygame.event.get():
			# exit program if X is clicked
			if event.type == pygame.QUIT:
				exit()
			# if a key is pressed while the text entry is "active":
			if event.type == pygame.KEYDOWN and active: 
				# if the key is "backspace", reduce length of input by 1
				if event.key == pygame.K_BACKSPACE:
					reasons = reasons[:-1]
				# if the key is "enter", save the reasons
				elif event.key == pygame.K_RETURN:
					return reasons
				# if neither of those keys, then add the pressed key to the input string
				elif len(reasons) <= 128:
					reasons += event.unicode
				# inform user if they are over character limit
				else:
					err = 'Please enter 128 characters or less.'
					DisplayText(X/2, Y-350, err, col="darkred", f=tip)
					pygame.display.update()
				
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				pos = pygame.mouse.get_pos()
				# if text entry box clicked, make text entry active
				if input.collidepoint(pos):
					active = True
				else:
					active = False
				# if help/tip clicked, show full help file
				if help.collidepoint(pos):
					os.startfile(help_dir + 'ABNORMAL.txt')
				# return to login if "logout" clicked
				elif logout.collidepoint(pos):
					DisplayLoginScreen(pt1, pt2)
		
		# text entry box is a darker grey if inactive/not accepting text
		if active:
			pygame.draw.rect(display, 'lightsteelblue', input)
		else:
			pygame.draw.rect(display, 'slategrey', input)

		# render currently entered input over text box
		txt = font.render(reasons, True, 'black')
		display.blit(txt, (input.x+3, input.y+3))

		pygame.display.flip()
  
	return reasons



# Displays a screen prompting the user to log out for the next reading.
def DisplayLogout(pt: Patient):
    # fill the screen to make a light background
	display.fill('aliceblue')
		
    # ask if patient has taken reading yet
	msg1 = 'Thank you.'
	DisplayText(X/2, Y-500, msg1)
 
	# draw logout button and patient info
	logout = DrawButton(X/2, Y/2, 200, 100, 'lightskyblue', "Log Out")
	DisplayText(150, Y-20, pt.name + "   " + pt.id, "midnightblue")

	running = True

	while running:
		for event in pygame.event.get():
			# exit program if X is clicked
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				pos = pygame.mouse.get_pos()
				# logout when patient clicks
				if logout.collidepoint(pos):
					DisplayLoginScreen(pt1, pt2)



# Writes out results to a file in a results directory.
def RecordData(pt: Patient, glucose: int, ketones: bool, reason: str):
    filename = pt.name + ".txt"
    f = open(res_dir + "/" + filename, "w")
    f.write("Glucose reading: " + str(glucose) + "; Ketones: " + str(ketones) + "; Reason provided for abnormal reading: " + reason)
    f.close()
    


	



# LAUNCH SYSTEM

DisplayLoginScreen(pt1, pt2)


