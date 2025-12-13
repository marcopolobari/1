import pygame
from classi_gioco import Gioco

gioco = Gioco()

while gioco.running:
    
    gioco.muovibarra()
    gioco.muovipallina()
    
pygame.quit()
