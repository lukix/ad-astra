import pygame

def rot_center(image, rect, angle):
	rot_image = pygame.transform.rotozoom(image, angle, 2)
	rot_rect = rot_image.get_rect(center=rect.center)
	return rot_image,rot_rect

class Planet:
	position = pygame.math.Vector2(0, 0)
	angle = 0
	radius = 512
	gravityCoeff = 1e8

	image = None

	def __init__(self):
		self.image = pygame.image.load("assets/earth.png").convert_alpha()

	def getObjectAltitude(self, targetPosition):
		return self.position.distance_to(targetPosition) - self.radius

	def getAirDensityAtAltitude(self, altitude):
		densityAtSeaLevel = 6e-3
		density = densityAtSeaLevel * (1 - 2.5e-3 * altitude) ** 8
		return 0 if altitude > 250 else density

	def render(self, surface, cameraPosition):
		image_rect = self.image.get_rect(center=surface.get_rect().center)
		(rotatedImage, rotatedRect) = rot_center(self.image, image_rect, self.angle)
		surface.blit(
			rotatedImage,
			rotatedRect.move(self.position).move(-cameraPosition)
		)
