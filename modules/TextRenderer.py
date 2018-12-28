import pygame

TEXT_COLOR = (255, 255, 0)

class TextRenderer:
	def __init__(self, screen):
		self.screen = screen
		self.mainFont = pygame.font.SysFont("arial", 40)
		self.normalFont = pygame.font.SysFont("arial", 20)
		self.creditsFont = pygame.font.SysFont("arial", 15)
		self.mainFont.set_bold(True)

	def renderGameOverText(self):
		label1 = self.mainFont.render("Game Over!", 1, TEXT_COLOR)
		label2 = self.normalFont.render("Press \"space\" to try again.", 1, TEXT_COLOR)
		label3 = self.normalFont.render("Press \"escape\" to quit.", 1, TEXT_COLOR)
		self.screen.blit(label1, (50, 50))
		self.screen.blit(label2, (55, 100))
		self.screen.blit(label3, (55, 130))

	def renderStartInstruction(self):
		label1 = self.normalFont.render("Press \"space\" to fire the engine.", 1, TEXT_COLOR)	
		self.screen.blit(label1, (55, 50))

	def renderFlightInfo(self, burns, speed, altitude):
		label1 = self.normalFont.render("Available burns: " + str(burns), 1, TEXT_COLOR)
		label2 = self.normalFont.render("Speed:  " + str(round(speed)) + "m/s", 1, TEXT_COLOR)
		label3 = self.normalFont.render("Altitude: " + str(round(altitude)) + "m", 1, TEXT_COLOR)
		self.screen.blit(label1, (55, 50))
		self.screen.blit(label2, (55, 80))
		self.screen.blit(label3, (55, 110))

	def renderCredits(self):
		text = "Planet and Ship graphics made by Freepik from www.flaticon.com"
		pos = (
			self.screen.get_rect().bottomright[0] - 400,
			self.screen.get_rect().bottomright[1] - 50
		)
		label1 = self.creditsFont.render(text, 1, TEXT_COLOR)
		self.screen.blit(label1, pos)