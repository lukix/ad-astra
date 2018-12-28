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
	if pygame.key.get_pressed()[pygame.K_UP]:
		spaceship.applyProgradeForce(360)
	
	spaceship.renderTrajectory(screen, spaceship.position)
	earth.render(screen, spaceship.position)
	spaceship.render(screen, spaceship.position)

	altitude = earth.position.distance_to(spaceship.position) - (2 * 256)
	airDensity = 6e-3 * (1 - 2.5e-3 * altitude) ** 8

	spaceship.applyGravityTowards(1e8, earth.position) # Gravity

	spaceship.applyDrag(0 if altitude > 250 else airDensity)

	spaceship.update(frameTime * timeSpeedMultiplier)

	if spaceship.hasCrashed(earth.position, 2 * 256):
		isGameOver = True
		timeSpeedMultiplier = 0

	if isGameOver:
		label1 = mainFont.render("Game Over!", 1, (255,255,0))
		label2 = normalFont.render("Press \"space\" to try again.", 1, (255,255,0))
		label3 = normalFont.render("Press \"escape\" to quit.", 1, (255,255,0))
		screen.blit(label1, (50, 50))
		screen.blit(label2, (55, 100))
		screen.blit(label3, (55, 130))

	pygame.display.flip()
	clock.tick(framesPerSecond)