import pygame

from modules.Spaceship import Spaceship
from modules.Planet import Planet

pygame.init()
pygame.display.set_caption('Ad Astra')
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

mainFont = pygame.font.SysFont("arial", 40)
mainFont.set_bold(True)

normalFont = pygame.font.SysFont("arial", 20)

spaceship = Spaceship()
earth = Planet()
SKY_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 0)

shouldCloseApp = False
isGameOver = False
framesPerSecond = 60
frameTime = 1.0 / framesPerSecond
timeSpeedMultiplier = 1.0

while not shouldCloseApp:
	screen.fill(SKY_COLOR)
	spaceship.stopRotation()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			shouldCloseApp = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				shouldCloseApp = True
			if event.key == pygame.K_SPACE:
				if isGameOver:
					spaceship = Spaceship()
					isGameOver = False
					timeSpeedMultiplier = 1
				else:
					spaceship.unfroze()
					spaceship.fireEngine()
			if event.key == pygame.K_1:
				timeSpeedMultiplier = 1
			if event.key == pygame.K_2:
				timeSpeedMultiplier = 2
			if event.key == pygame.K_3:
				timeSpeedMultiplier = 4
			if event.key == pygame.K_4:
				timeSpeedMultiplier = 8

	if pygame.key.get_pressed()[pygame.K_LEFT]:
		spaceship.setAntiClockwiseRotation()
	if pygame.key.get_pressed()[pygame.K_RIGHT]:
		spaceship.setClockwiseRotation()
	
	spaceship.renderTrajectory(screen, spaceship.position)
	earth.render(screen, spaceship.position)
	spaceship.render(screen, spaceship.position)

	altitude = earth.getObjectAltitude(spaceship.position)
	airDensity = 6e-3 * (1 - 2.5e-3 * altitude) ** 8

	spaceship.applyGravityTowards(1e8, earth.position) # Gravity

	spaceship.applyDrag(0 if altitude > 250 else airDensity)

	spaceship.update(frameTime * timeSpeedMultiplier)

	if altitude <= 0:
		isGameOver = True
		timeSpeedMultiplier = 0

	if spaceship.isFrozen:
		label1 = normalFont.render("Press \"space\" to fire the engine.", 1, TEXT_COLOR)
		screen.blit(label1, (55, 50))
	elif isGameOver:
		label1 = mainFont.render("Game Over!", 1, TEXT_COLOR)
		label2 = normalFont.render("Press \"space\" to try again.", 1, TEXT_COLOR)
		label3 = normalFont.render("Press \"escape\" to quit.", 1, TEXT_COLOR)
		screen.blit(label1, (50, 50))
		screen.blit(label2, (55, 100))
		screen.blit(label3, (55, 130))
	else:
		label1 = normalFont.render("Available burns: " + str(spaceship.getAvailableBurns()), 1, TEXT_COLOR)
		label2 = normalFont.render("Speed:  " + str(round(spaceship.getSpeed())) + "m/s", 1, TEXT_COLOR)
		label3 = normalFont.render("Altitude: " + str(round(altitude)) + "m", 1, TEXT_COLOR)
		screen.blit(label1, (55, 50))
		screen.blit(label2, (55, 80))
		screen.blit(label3, (55, 110))

	pygame.display.flip()
	clock.tick(framesPerSecond)