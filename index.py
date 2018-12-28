import pygame

from modules.Spaceship import Spaceship
from modules.Planet import Planet
from modules.TextRenderer import TextRenderer
from modules.timeSpeedMultiplierReducer import timeSpeedMultiplierReducer

pygame.init()
pygame.display.set_caption('Ad Astra')
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
textRenderer = TextRenderer(screen)

SKY_COLOR = (0, 0, 0)
FRAMES_PER_SECOND = 60
FRAME_TIME = 1.0 / FRAMES_PER_SECOND

spaceship = Spaceship()
earth = Planet()

shouldCloseApp = False
isGameOver = False
timeSpeedMultiplier = 1.0

while not shouldCloseApp:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			shouldCloseApp = True
		if event.type == pygame.KEYDOWN:
			timeSpeedMultiplier = timeSpeedMultiplierReducer(timeSpeedMultiplier, event.key)
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

	# Handle spaceship rotation controls
	spaceship.stopRotation()
	if pygame.key.get_pressed()[pygame.K_LEFT]:
		spaceship.setAntiClockwiseRotation()
	if pygame.key.get_pressed()[pygame.K_RIGHT]:
		spaceship.setClockwiseRotation()

	altitude = earth.getObjectAltitude(spaceship.position)
	airDensity = earth.getAirDensityAtAltitude(altitude)

	hasCrashed = lambda ship: earth.getObjectAltitude(ship.position) <= 0
	externalSpaceshipUpdate = lambda ship: ship.applyGravityTowards(earth.gravityCoeff, earth.position)

	externalSpaceshipUpdate(spaceship)
	spaceship.applyDrag(airDensity)

	spaceship.update(FRAME_TIME * timeSpeedMultiplier)
	
	if hasCrashed(spaceship):
		isGameOver = True
		timeSpeedMultiplier = 0

	# Renders
	screen.fill(SKY_COLOR)
	spaceship.renderTrajectory(screen, spaceship.position, externalSpaceshipUpdate, hasCrashed)
	earth.render(screen, spaceship.position)
	spaceship.render(screen, spaceship.position)

	# Conditional Renders
	if spaceship.isFrozen:
		textRenderer.renderStartInstruction()
		textRenderer.renderCredits()
	elif isGameOver:
		textRenderer.renderGameOverText()
	else:
		textRenderer.renderFlightInfo(
			spaceship.getAvailableBurns(),
			spaceship.getSpeed(),
			altitude
		)

	pygame.display.flip()
	clock.tick(FRAMES_PER_SECOND)