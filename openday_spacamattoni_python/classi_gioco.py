import pygame

class Colori:
    """Classe per gestire i colori del gioco"""
    NERO = (0, 0, 0)
    BIANCO = (255, 255, 255)
    ROSSO = (255, 0, 0)
    VERDE = (0, 255, 0)
    BLU = (0, 100, 255)


class Barra:
    """Classe per gestire la barra/racchetta"""
    def __init__(self, x, y, larghezza_schermo):
        self.x = x
        self.y = y
        self.larghezza = 80
        self.altezza = 10
        self.velocita = 6
        self.larghezza_schermo = larghezza_schermo
    
    def muovi_sinistra(self):
        if self.x > 0:
            self.x -= self.velocita
    
    def muovi_destra(self):
        if self.x < self.larghezza_schermo - self.larghezza:
            self.x += self.velocita
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.larghezza, self.altezza)
    
    def disegna(self, screen):
        pygame.draw.rect(screen, Colori.BIANCO, (self.x, self.y, self.larghezza, self.altezza))


class Pallina:
    """Classe per gestire la pallina"""
    def __init__(self, x, y, larghezza_schermo, altezza_schermo):
        self.x = x
        self.y = y
        self.dx = 3
        self.dy = -3
        self.raggio = 5
        self.larghezza_schermo = larghezza_schermo
        self.altezza_schermo = altezza_schermo
    
    def muovi(self):
        """Muove la pallina e gestisce automaticamente i bordi"""
        self.x += self.dx
        self.y += self.dy
        
        # Gestione bordi integrata
        self.gestione_bordi()
    
    def gestione_bordi(self):
        """Gestisce il rimbalzo sui bordi e il game over"""
        # Rimbalzo sui bordi laterali
        if self.x <= 0 or self.x >= self.larghezza_schermo:
            self.rimbalzo_orizzontale()
        
        # Rimbalzo sul bordo superiore
        if self.y <= 0:
            self.rimbalzo_verticale()
        
        # Game over se la pallina cade
        if self.y > self.altezza_schermo:
            self.reset()
    
    def rimbalzo_orizzontale(self):
        self.dx = -self.dx
    
    def rimbalzo_verticale(self):
        self.dy = -self.dy
    
    def reset(self):
        self.x = 300
        self.y = 200
        self.dy = -3
    
    def get_rect(self):
        return pygame.Rect(self.x - self.raggio, self.y - self.raggio, 
                          self.raggio * 2, self.raggio * 2)
    
    def disegna(self, screen):
        pygame.draw.circle(screen, Colori.BIANCO, (int(self.x), int(self.y)), self.raggio)


class Mattone:
    """Classe per gestire un singolo mattone"""
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 55, 15)
    
    def disegna(self, screen):
        pygame.draw.rect(screen, Colori.VERDE, self.rect)


class GruppoMattoni:
    """Classe per gestire tutti i mattoni"""
    def __init__(self):
        self.mattoni = []
        self.crea_mattoni()
    
    def crea_mattoni(self):
        for riga in range(5):
            for col in range(10):
                mattone = Mattone(col * 60, riga * 20 + 50)
                self.mattoni.append(mattone)
    
    def rimuovi_mattone(self, mattone):
        self.mattoni.remove(mattone)
    
    def controlla_collisione(self, pallina_rect):
        for mattone in self.mattoni[:]:
            if pallina_rect.colliderect(mattone.rect):
                self.rimuovi_mattone(mattone)
                return True
        return False
    
    def tutti_distrutti(self):
        return len(self.mattoni) == 0
    
    def disegna(self, screen):
        for mattone in self.mattoni:
            mattone.disegna(screen)


class Punteggio:
    """Classe per gestire il punteggio"""
    def __init__(self):
        self.punti = 0
        self.font = pygame.font.Font(None, 30)
    
    def incrementa(self):
        self.punti += 1
    
    def disegna(self, screen):
        testo = self.font.render(f"Punteggio: {self.punti}", True, Colori.BIANCO)
        screen.blit(testo, (10, 10))


class Gioco:
    """Classe principale che gestisce tutto il gioco"""
    def __init__(self):
        pygame.init()
        self.larghezza = 600
        self.altezza = 400
        self.screen = pygame.display.set_mode((self.larghezza, self.altezza))
        pygame.display.set_caption("Breakout Semplice")
        self.clock = pygame.time.Clock()
        
        # Inizializza gli oggetti del gioco (DOPO aver definito larghezza e altezza)
        #self.barra = Barra(250, 350)
        self.larghezza_schermo = 600
        self.barra = Barra(350, 350, self.larghezza_schermo) 
        self.pallina = Pallina(300, 200, self.larghezza, self.altezza)
        self.mattoni = GruppoMattoni()
        self.punteggio = Punteggio()
        
        self.running = True
        self.font = pygame.font.Font(None, 30)
    
    def gestione_eventi(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                print("applicazione chiusa")
                
                
    def muovibarra(self):
        self.gestione_eventi()
        # Movimento barra
        tasti = pygame.key.get_pressed()
        if tasti[pygame.K_LEFT]:
            self.barra.muovi_sinistra()
        if tasti[pygame.K_RIGHT]:
            self.barra.muovi_destra()
        
    def muovipallina(self):    
        # Movimento pallina con gestione bordi automatica
        self.pallina.muovi()
    
        # Collisioni
        self.gestione_collisioni()
        
        # Disegna tutto
        self.disegna()
        
        # Aggiorna schermo
        self.aggiorna()
        
    def gestione_collisioni(self):
        """Gestisce tutte le collisioni del gioco"""
        # Rimbalzo sulla barra
        if self.barra.y < self.pallina.y < self.barra.y + self.barra.altezza:
            if self.barra.x < self.pallina.x < self.barra.x + self.barra.larghezza:
                self.pallina.rimbalzo_verticale()
        
        # Collisione con i mattoni
        pallina_rect = self.pallina.get_rect()
        if self.mattoni.controlla_collisione(pallina_rect):
            self.pallina.rimbalzo_verticale()
            self.punteggio.incrementa()
    
    def disegna(self):
        # Sfondo nero
        self.screen.fill(Colori.NERO)
        
        # Disegna tutti gli elementi
        self.barra.disegna(self.screen)
        self.pallina.disegna(self.screen)
        self.mattoni.disegna(self.screen)
        self.punteggio.disegna(self.screen)
        
        # Messaggio vittoria
        if self.mattoni.tutti_distrutti():
            testo_vinto = self.font.render("HAI VINTO!", True, Colori.VERDE)
            screen_rect = self.screen.get_rect()
            testo_rect = testo_vinto.get_rect(center=(screen_rect.centerx, screen_rect.centery))
            self.screen.blit(testo_vinto, testo_rect)
    
    def aggiorna(self):
        pygame.display.flip()
        self.clock.tick(60)


