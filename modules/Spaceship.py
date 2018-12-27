import pygame

def rot_center(image, rect, angle):
	rot_image = pygame.transform.rotozoom(image, angle, 0.25)
	rot_rect = rot_image.get_rect(center=rect.center)
	return rot_image,rot_rect

class Spaceship:
	position = pygame.math.Vector2(0, -(2 * 256 + 18))
	velocity = pygame.math.Vector2(0, 0)
	force = pygame.math.Vector2(0, 0)
	angle = 0
	angularVelocity = 0
	engineOn = False
	isFrozen = True

	spaceshipImage = None

	def __init__(self):
		self.spaceshipImage = pygame.image.load("assets/ship.png").convert_alpha()

	def setClockwiseRotation(self):
		self.angularVelocity = -60

	def setAntiClockwiseRotation(self):
		self.angularVelocity = 60

	def stopRotation(self):
		self.angularVelocity = 0

	def applyProgradeForce(self, magnitude):
		forceVector = pygame.math.Vector2(0, -magnitude).rotate(-self.angle)
		self.applyForce(forceVector)

	def applyGravityTowards(self, massProduct, target):
		direction = pygame.math.Vector2(self.position.x - target.x, self.position.y - target.y).normalize()
		r2 = self.position.distance_squared_to(target)
		magnitude = massProduct / r2
		self.applyForce(-direction * magnitude)

	def applyForce(self, force):
		self.force = self.force + force

	def unfroze(self):
		self.isFrozen = False
	
	def hasCrashed(self, planetPosition, planetRadius):
		distance = self.position.distance_to(planetPosition)
		return distance < planetRadius

	def update(self, dt):
		if not self.isFrozen:
			self.velocity = self.velocity + self.force * dt
			self.position = self.position + self.velocity * dt
			self.angle = self.angle + self.angularVelocity * dt

		self.force = pygame.math.Vector2(0, 0)

	def render(self, surface, cameraPosition):
		image_rect = self.spaceshipImage.get_rect(center=surface.get_rect().center)
		(rotatedSpaceshipImage, rotatedSpaceshipRect) = rot_center(self.spaceshipImage, image_rect, self.angle)
		surface.blit(
			rotatedSpaceshipImage,
			rotatedSpaceshipRect.move(self.position).move(-cameraPosition)
		)

	def renderTrajectory(self, surface, cameraPosition):
		simulatedSpaceship = Spaceship()
		simulatedSpaceship.position = self.position
		simulatedSpaceship.velocity = self.velocity
		simulatedSpaceship.unfroze()

		t = 0
		dt = 1.0 / 60
		maxTime = 15.0
		drawCounter = 1
		while t < maxTime and not simulatedSpaceship.hasCrashed((0, 0), 512):
			t += dt
			drawCounter = (drawCounter + 1) % 5

			simulatedSpaceship.applyGravityTowards(1e8, pygame.Vector2(0, 0))
			simulatedSpaceship.update(dt)

			if drawCounter == 0:
				floatPos = simulatedSpaceship.position - cameraPosition + surface.get_rect().center
				intPos = (int(floatPos.x), int(floatPos.y))
				pygame.draw.circle(surface, (255, 0, 0), intPos, 2, 1)
