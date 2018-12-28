import pygame

def timeSpeedMultiplierReducer(currentMultiplier, eventKey):
	if eventKey == pygame.K_1: return 1
	elif eventKey == pygame.K_2: return 2
	elif eventKey == pygame.K_3: return 4
	elif eventKey == pygame.K_4: return 8
	elif eventKey == pygame.K_5: return 16
	return currentMultiplier