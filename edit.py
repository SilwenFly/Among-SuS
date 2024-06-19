import pygame
import sys
import sqlite3
import random
# Initialiser Pygame
pygame.init()

# Créer une fenêtre
window = pygame.display.set_mode((800, 600))

# Créer une connexion à la base de données
conn = sqlite3.connect('db.db')
cursor = conn.cursor()

# Créer une fonction pour éditer la base de données
def edit_database():
    print("lol")
    pass

def get_all_tables():
    tables_return=[]
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table_name in tables:
        tables_return.append(table_name[0])  # table_name est un tuple, donc nous utilisons l'index 0 pour obtenir le nom de la table
    return tables_return

#Boucle pour afficher les tables
def button_pressed(name_table):
    # Réduire la taille du bouton "back" et le centrer dans le rectangle
    back_button_rect = pygame.Rect(window_width // 2 - 50, window_height - 100, 100, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    return  # Retourner au menu principal si le bouton de retour est cliqué

        # Dessiner le menu
        window.fill((0, 0, 0))
        pygame.draw.rect(window, (255, 255, 255), back_button_rect)
        text_surface = font.render('Back', True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=back_button_rect.center)  # Centrer le texte dans le rectangle
        window.blit(text_surface, text_rect)

        pygame.display.flip()
        
#Fonction pour dessiner un rectangle avec des coins arrondis
def draw_rounded_rect(surface, rect, color, corner_radius):
    """Draw a rectangle with rounded corners on the specified surface. 
    The corner_radius parameter is the radius of the circles at the corners."""
    
    pygame.draw.circle(surface, color, (rect.left + corner_radius, rect.top + corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (rect.right - corner_radius, rect.top + corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (rect.left + corner_radius, rect.bottom - corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (rect.right - corner_radius, rect.bottom - corner_radius), corner_radius)

    pygame.draw.rect(surface, color, rect.inflate(-2*corner_radius, 0))
    pygame.draw.rect(surface, color, rect.inflate(0, -2*corner_radius))
    
tables_return = get_all_tables()

# Obtenir la taille de la fenêtre
window_width, window_height = window.get_size()

# Créer les rectangles centrés
button_rects = [pygame.Rect(window_width // 2 - 200, 50 + i*120, 400, 50) for i in range(len(tables_return))]

# Créer une police de caractères
font = pygame.font.Font(None, 36)

# Charger une image de fond
background_image = pygame.image.load('etoile.jpg')
background_x = 0  # Position x de l'image de fond
background_y = 0  # Position y de l'image de fond

# Initialiser move_direction et move_counter
move_direction = None
move_counter = 0

# Initialiser la vitesse
speed = 1000

# Initialiser l'horloge
clock = pygame.time.Clock()

# Créer une boucle principale
while True:
    dt = clock.tick(60) / 1000  # Retourne le temps écoulé en secondes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Vérifier si l'utilisateur a cliqué sur l'un des boutons
            for i, rect in enumerate(button_rects):
                if rect.collidepoint(event.pos):
                    print(f"Button {i} clicked. Corresponding table: {tables_return[i]}")
                    button_pressed(tables_return[i])
    
    if move_counter == 0:
        # Choisir une nouvelle direction et réinitialiser le compteur
        move_direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        move_counter = 20
    
    # Dessiner le menu de départ
    #window.blit(background_image, (background_x, background_y))
    #window.blit(background_image, (background_x - background_image.get_width(), background_y))

    # Déplacer l'image de fond
    background_x += move_direction[0] * speed * dt
    background_y += move_direction[1] * speed * dt
    
    # Vérifier si l'image de fond est sortie de la fenêtre et la ramener si nécessaire
    if background_x < -background_image.get_width():
        background_x = 0
    elif background_x > 0:
        background_x = -background_image.get_width()

    if background_y < -background_image.get_height():
        background_y = 0
    elif background_y > 0:
        background_y = -background_image.get_height()

    window.blit(background_image, (background_x, background_y))
    # Décrémenter le compteur de mouvement
    move_counter -= 1
        
    for i, rect in enumerate(button_rects):
        draw_rounded_rect(window, rect, (255, 255, 255), 20)
        text_surface = font.render(tables_return[i], True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=rect.center)
        window.blit(text_surface, text_rect)

    pygame.display.flip()