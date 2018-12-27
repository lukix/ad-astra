import pygame

from modules.Spaceship import Spaceship
from modules.Planet import Planet

pygame.init()
pygame.display.set_caption('Ad Astra')
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

spaceship = Spaceship()
earth = Planet()
SKY_COLOR = (0, 0, 0)

shouldCloseApp = False
framesPerSecond = 60
frameTime = 1.0 / framesPerSecond

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
				spaceship.unfroze()

	if pygame.key.get_pressed()[pygame.K_LEFT]:
		spaceship.setAntiClockwiseRotation()
	if pygame.key.get_pressed()[pygame.K_RIGHT]:
		spaceship.setClockwiseRotation()
	if pygame.key.get_pressed()[pygame.K_UP]:
		spaceship.applyProgradeForce(360)
	
	spaceship.renderTrajectory(screen, spaceship.position)
	earth.render(screen, spaceship.position)
	spaceship.render(screen, spaceship.position)

	pygame.display.flip()

	spaceship.applyGravityTowards(1e8, earth.position) # Gravity

	spaceship.update(frameTime)

	clock.tick(framesPerSecond)