import pygame
import math

def rot_center(image, rect, angle):
	rot_image = pygame.transform.rotozoom(image, angle, 1)
	rot_rect = rot_image.get_rect(center=rect.center)
	return rot_image,rot_rect

class Spaceship:
	position = pygame.math.Vector2(0, -(2 * 256 + 12))
	velocity = pygame.math.Vector2(0, 0)
	force = pygame.math.Vector2(0, 0)
	angle = 0
	angularVelocity = 0
	isFrozen = True
	timeUntilBurnout = 0
	thrust = 370
	burns = [3.6, 0.6, 0.2, 0.1, 0.1]
	burnIndex = 0

	spaceshipImage = None
	plumeImages = []
	activePlumeIndex = 0
	plumeImageChangeCounter = 0

	def __init__(self):
		self.spaceshipImage = pygame.image.load("assets/ship.png").convert_alpha()
		self.plumeImages = list(map(
			lambda n: pygame.image.load('assets/plumes/{n}.png'.format(n = n)).convert_alpha(),
			range(1, 7)
		))

	def setClockwiseRotation(self):
		self.angularVelocity = -80

	def setAntiClockwiseRotation(self):
		self.angularVelocity = 80

	def stopRotation(self):
		self.angularVelocity = 0

	def getSpeed(self):
		return self.velocity.length()

	def fireEngine(self):
		if self.timeUntilBurnout > 0 or self.burnIndex >= len(self.burns):
			return
		self.timeUntilBurnout = self.burns[self.burnIndex]
		self.burnIndex += 1

	def getAvailableBurns(self):
		return len(self.burns) - self.burnIndex

	def applyDrag(self, airDensity):
		v2 = self.velocity.length_squared()
		if v2 == 0:
			return
		magnitude = airDensity * v2
		dragForce = magnitude * self.velocity.normalize()
		self.applyForce(-dragForce)

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
		if self.timeUntilBurnout > 0:
			self.timeUntilBurnout -= dt
			self.applyProgradeForce(self.thrust)

		if not self.isFrozen:
			self.velocity = self.velocity + self.force * dt
			self.position = self.position + self.velocity * dt
			self.angle = self.angle + self.angularVelocity * dt

		self.force = pygame.math.Vector2(0, 0)

		self.plumeImageChangeCounter -= dt
		if self.plumeImageChangeCounter <= 0:
			self.activePlumeIndex = (self.activePlumeIndex + 1) % len(self.plumeImages)
			self.plumeImageChangeCounter = 30e-3

	def render(self, surface, cameraPosition):
		image_rect = self.spaceshipImage.get_rect(center=surface.get_rect().center)
		(rotatedSpaceshipImage, rotatedSpaceshipRect) = rot_center(self.spaceshipImage, image_rect, self.angle)
		surface.blit(
			rotatedSpaceshipImage,
			rotatedSpaceshipRect.move(self.position).move(-cameraPosition)
		)
		if self.timeUntilBurnout > 0:
			self.renderPlume(surface, cameraPosition)
	
	def renderPlume(self, surface, cameraPosition):
		plumeImage = self.plumeImages[self.activePlumeIndex]
		image_rect = plumeImage.get_rect(center=surface.get_rect().center)
		(rotatedSpaceshipImage, rotatedSpaceshipRect) = rot_center(plumeImage, image_rect, self.angle)
		plumeOffsetDistance = 26
		plumeOffsetVector = (
			plumeOffsetDistance * math.sin(math.radians(self.angle)),
			plumeOffsetDistance * math.cos(math.radians(self.angle))
		)
		surface.blit(
			rotatedSpaceshipImage,
			rotatedSpaceshipRect
				.move(self.position)
				.move(plumeOffsetVector)
				.move(-cameraPosition)
		)

	def renderTrajectory(self, surface, cameraPosition):
		simulatedSpaceship = Spaceship()
		simulatedSpaceship.position = self.position
		simulatedSpaceship.velocity = self.velocity
		simulatedSpaceship.unfroze()

		t = 0
		dt = 1.0 / 60
		maxTime = 18.0
		drawCounter = 1
		while t < maxTime and not simulatedSpaceship.hasCrashed((0, 0), 512):
			t += dt
			drawCounter = (drawCounter + 1) % 6

			simulatedSpaceship.applyGravityTowards(1e8, pygame.Vector2(0, 0))
			simulatedSpaceship.update(dt)

			if drawCounter == 0:
				floatPos = simulatedSpaceship.position - cameraPosition + surface.get_rect().center
				intPos = (int(floatPos.x), int(floatPos.y))
				pygame.draw.circle(surface, (50, 50, 255), intPos, 1, 1)
