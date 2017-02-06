import pygame as py
from random import randint as rand

# press ecape when playing to restart the game

# board size
boardLength 	= 10
boardWidth	= 10


#---------- Methods and Class ------------------------------------------

class Box:  # the box class is a template for 1 box on the board 
	x 		= 0
	y 		= 0
	clicked 	= False 
	clickable	= True
	lastClicked	= False

	def __init__(self,x,y):  # standard initialization method that creates a box object using the x and y variables given when used.
		self.x = x		
		self.y = y


def drawBox(x,y,width,colour):	# x and y are rows and columns, not pixals.
	py.draw.line(	screen,colour,
			(width * x,		width * y),	# line start (x,y)		
			((width * x)+width,	width * y),1)	# line finish... 
	py.draw.line(	screen,colour,
			(width * x,		(width * y)+width),			
			((width * x)+width,	(width * y)+width),1)
	py.draw.line(	screen,colour,
			((width * x)+width,	width * y),			
			((width * x)+width,	(width * y)+width),1)
	py.draw.line(	screen,colour,
			(width * x,		width * y),			
			(width * x,		(width * y)+width),1)

def fillBox(x,y,width,colour):
	for i in range (0,width-1):	
		py.draw.line(	screen,colour,
			((width * x)+1,		(width * y)+1+i),			
			((width * x)+width-1,	(width * y)+1+i),1)

#---------------------------------------------------------------------------------

#  	Main section

# set up board 
boxWidth	= 32
colour1		= (200,200,200)
colour2		= (100,255,255)
colour3		= (255,0,255)
colour4		= (0,255,0)
screen_width 	= (boxWidth*boardWidth)+1
screen_length 	= (boxWidth*boardLength)+1


""" pygame window """
py.init()
screen = py.display.set_mode((screen_width,screen_length))
py.display.set_caption("Horse")

myfont = py.font.SysFont("monospace", 15)

won_label = myfont.render("You Won!", 1, (255,255,255))

""" fps clock """
clock = py.time.Clock()

boxes 	= []*0									# create an array to store the box objects 
for y in range (0, boardLength ):						# loop through board width and height 
	for x in range (0, boardWidth):			
		boxes.append(Box(x,y))						# create a new box object using the grid references

	
#	Main loop	

running = True
while running:
	
	""" events """
	for evt in py.event.get():		
		if evt.type == py.QUIT:						# stop running if 'x' is clicked
			running = False
		""" keyboad events """
		if evt.type == py.KEYDOWN:
			if evt.key == py.K_ESCAPE:				# restart if escape is pressed
				for box in boxes:
					box.clicked = False
					box.clickable = True
					box.lastClicked = False

	if py.mouse.get_pressed()[0]:						# if mouse is pressed
		mouse_pos = py.mouse.get_pos() 					# get mouse position and transfer to variable
		for box in boxes:						# loop through the boxes
			if (mouse_pos[0] > box.x*boxWidth 			# if mouse position is within the current box
			and mouse_pos[0] < (box.x*boxWidth)+ boxWidth 	
			and mouse_pos[1] > box.y*boxWidth 
			and mouse_pos[1] < (box.y*boxWidth)+ boxWidth
			and box.clickable == True):				# and that box is clickable
				
				pos = []*0					# initialize an array to keep position data for new selection options
				pos.append((box.x+2,box.y-1))	
				pos.append((box.x+2,box.y+1))			
				pos.append((box.x-2,box.y-1))					
				pos.append((box.x-2,box.y+1))				
				pos.append((box.x+1,box.y-2))						
				pos.append((box.x+1,box.y+2))				
				pos.append((box.x-1,box.y-2))						
				pos.append((box.x-1,box.y+2))

				box.clicked 	= True				# set box as clicked
				box.clickable 	= False				# set box as unclickable

				for box2 in boxes:				# loop through boxes
					box2.clickable = False			 
					if box2.lastClicked:			# find the box that was last clicked
						box2.lastClicked = False	# set the lastClicked option as False

				box.lastClicked = True				# set current box as lastClicked
								
				for p in pos:					# loop through new positions
					for b in boxes:				# loop through boxes
						if( 	b.x == p[0] and 	# if new positions match box positions
							b.y == p[1] and 
							b.clicked == False):	# and if new box hasn't been clicked

							b.clickable = True	# mark new box as clickable
	
	failed 	= True								
	won 	= True
	for box in boxes:							# loop through boxes to check if player has won
		if box.clickable or box.clicked == False:			
			won = False
			break;
	for box in boxes:							# loop through boxes to check if player has lost
		if box.clickable and box.clicked == False:
			failed = False
			
			break;

	screen.fill((0,0,0))							# paint over screen with black

	for y in range (0, boardLength ):					# loop through board width and height (in blocks not pixles)
		for x in range (0, boardWidth):
			drawBox(x,y,boxWidth,colour1)				# draw box
	for box in boxes:							# loop through boxes
		if box.clicked:							# if box is clicked
			fillBox(box.x,box.y,boxWidth,colour3)			# fill box with colour3
		if box.clickable:						# if box is clickable 
			drawBox(box.x,box.y,boxWidth,(0,255,0))			# colour outline of box green (in it's raw form (0,255,0))
		if box.lastClicked:						# if box was last clicked 
			fillBox(box.x,box.y,boxWidth,colour2)			# fill box with colour2
		
	if won:									# if player has won
		failed = False							# prevent failed from running
		r1 = rand(0,255)						# random number 1
		r2 = rand(0,255)						# random number 2
		r3 = rand(0,255)						# random number 3
		screen.fill((r1,r2,r3))						# create colour with random numbers and fill screen
		tpos = won_label.get_rect()					# get rectangle of text to locate the center point
				
		screen.blit(	won_label, 					# print text to screen at center point
				((screen_length/2)-(tpos.width/2),
				screen_length/2	))

	if failed:								# if player has failed 
		screen.fill((150,0,0))							# get rectangle of text to locate the center point
		boxesLeft = 0
		for box in boxes:
			if box.clicked == False:
				boxesLeft+=1
		txt1 = "You Lost!"
		txt2 = "You have "+str(boxesLeft)+" left"
		lost_label1 = myfont.render(txt1, 1, (0,0,0))		
		lost_label2 = myfont.render(txt2, 1, (0,0,0))		
		
		tpos1 = lost_label1.get_rect()
		tpos2 = lost_label2.get_rect()
		
		screen.blit(	lost_label1, 					# print text to screen at center point
				((screen_length/2)-(tpos1.width/2),		
				screen_length/2))
		screen.blit(	lost_label2, 					# print text to screen at center point
				((screen_length/2)-(tpos2.width/2),		
				(screen_length/2)+(tpos2.height * 1.1)))
			 				

	py.display.update()							# standard pygame method to update display window

		
	clock.tick(30)								# frame rate


py.quit() 									# quit properly when loop ends
