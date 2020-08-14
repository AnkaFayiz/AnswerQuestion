import pygame
from pygame.locals import *
import time
import sys
import random

class Game:

	def __init__(self):
		self.w=750
		self.h=500
		self.exit=False
		self.reset=True
		self.active=False
		self.input_text=''
		self.word=0
		self.time_start=0
		self.total_time=0
		self.accuracy=0
		self.end=False
		self.results=''
		self.answer_results=''
		self.HEAD_C=(255,213,102)
		self.TEXT_C=(240,240,240)
		self.RESULT_C=(255,70,70)


		pygame.init()
		self.bg=pygame.image.load('background.jpg')
		self.bg=pygame.transform.scale(self.bg, (500,750))

		self.screen=pygame.display.set_mode((self.w, self.h))


	def draw_text(self,screen,msg,y,fsize,color):
		font=pygame.font.Font(None,fsize)
		text=font.render(msg, 1,color)
		text_rect=text.get_rect(center=(self.w/2, y))
		screen.blit(text, text_rect)
		pygame.display.update()

	def get_question(self):
		f=open('questions.txt').read()
		questions=f.split('\n')
		question=random.choice(questions)
		return question

	def get_answer(self):
		result_answer=open('answer.txt').read()
		answers=result_answer.split('\n')
		answer=random.choice(answers)
		if(self.input_text==answer):
			return answer
		else:
			for _ in range(10):
				answer=random.choice(answers)
				if(self.input_text==answer):
					return answer

	def show_results(self, screen):
		if(not self.end):
			# Calculate time
			self.total_time = time.time() - self.time_start
			
			self.results='Time : '+str(round(self.total_time))+'seconds  Answer : '+str(self.get_answer())
			print(self.results)
			pygame.display.update()

	def run(self):
		self.reset_game()

		self.running=True
		while (self.running):
			clock=pygame.time.Clock()
			self.screen.fill((0,0,0), (50,250,650,50))
			pygame.draw.rect(self.screen, self.HEAD_C, (50,250,650,50),2)
			# Update user input
			self.draw_text(self.screen, self.input_text, 274, 26,(250,250,250))
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == QUIT:
					self.running=False
					sys.exit()
				elif event.type == pygame.MOUSEBUTTONUP:
					x,y=pygame.mouse.get_pos()
					# position of input box
					if(x>=50 and x<=650 and y>=250 and y<=300):
						self.active=True
						self.input_text=''
						self.time_start=time.time()
					# position of reset box
					if(x>=310 and x<=510 and y>=390 and self.end):
						self.reset_game()
						x,y=pygame.mouse.get_pos()

				elif event.type == pygame.KEYDOWN:
					if self.active and not self.end:
						if event.key == pygame.K_RETURN:
							print(self.input_text)
							self.show_results(self.screen)
							print(self.results)
							self.draw_text(self.screen, self.results, 350, 28, self.RESULT_C)
							self.end=True

						elif event.key == pygame.K_BACKSPACE:
							self.input_text = self.input_text[:-1]
						else:
							try:
								self.input_text += event.unicode
							except:
								pass


			pygame.display.update()

		clock.tick(60)

	def reset_game(self):
		self.screen.blit(self.bg, (0,0))

		pygame.display.update()
		time.sleep(1)

		self.reset=False
		self.end=False

		self.word=''
		self.input_text=''

		# Get Random Questions
		self.word=self.get_question()
		if(not self.word):self.reset_game()
		# Drawing Heading
		self.screen.fill((0,0,0))
		self.screen.blit(self.bg,(0,0))
		msg="Answer Questions"
		self.draw_text(self.screen, msg, 80, 80, self.HEAD_C)
		# Draw the rectangle for input box
		pygame.draw.rect(self.screen, (255,192,25), (50,250,650,50),2)

		# Draw the question ring
		self.draw_text(self.screen, self.word, 200, 28, self.TEXT_C)

		pygame.display.update()


Game().run()