import pygame
import sys
import sqlite3
import random
import textwrap

# Initialiser Pygame
pygame.init()

# Créer une fenêtre
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Edit | Among SuS')
pygame.display.set_icon(pygame.image.load('./edit/dab.png'))

hacker_font = pygame.font.Font('./edit/HACKED_Title.ttf', 50)
desc_font = pygame.font.Font('./edit/whitrabt.ttf', 18)

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
        if table_name[0] != "sqlite_sequence":
            tables_return.append(table_name[0])  # table_name est un tuple, donc nous utilisons l'index 0 pour obtenir le nom de la table
    return tables_return

#Boucle pour afficher les tables
def button_pressed(name_table):
    
    
    # Créer des rectangles pour les boutons
    back_button_rect = pygame.Rect(window_width // 2 - 50, window_height - 50, 100, 30)
    add_button_rect = pygame.Rect(window_width // 2 - 100, window_height - 150, 200, 60)  # Nouveau bouton "Ajouter"
    modify_button_rect = pygame.Rect(window_width // 2 - 100, window_height - 250, 200, 60)  # Nouveau bouton "Modifier"
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    return  # Retourner au menu principal si le bouton de retour est cliqué
                elif add_button_rect.collidepoint(event.pos):
                    print("Bouton Ajouter cliqué")  # Remplacer par votre code pour le bouton "Ajouter"
                    
                elif modify_button_rect.collidepoint(event.pos):
                    print("Bouton Modifier cliqué")  # Remplacer par votre code pour le bouton "Modifier"
        
        # Dessiner le menu
        window.fill((0, 0, 0))
        
        # Dessiner le nom de la table en haut au milieu
        table_name_surface = hacker_font.render(name_table, True, (0, 255, 0))
        table_name_rect = table_name_surface.get_rect(center=(window_width // 2, 50))
        window.blit(table_name_surface, table_name_rect)
        
        #Récupérer description du quiz
        quiz_description = ""
        with open('./edit/description.txt', 'r') as file:
            # Lire ligne par ligne
            for line in file.readlines():
                # Si la ligne contient le nom du quiz
                if name_table in line:
                    # Stocker le contenu de la ligne dans une variable
                    quiz_description = line
                    quiz_description = quiz_description.split(":")
                    quiz_description = quiz_description[1]
                    quiz_description = quiz_description.replace(".", ".\n \n")
                    break  # Arrêter la lecture du fichier
            if quiz_description == "":
                quiz_description = "Mystere, Mystere..."
        
            # Diviser le texte en paragraphes
        paragraphs = quiz_description.split('\n')

        # Diviser chaque paragraphe en lignes de 60 caractères
        lines = []
        for paragraph in paragraphs:
            if paragraph:  # Si le paragraphe n'est pas vide
                lines.extend(textwrap.wrap(paragraph, width=60))
            lines.append('')  # Ajouter un saut de ligne

        # Dessiner chaque ligne séparément
        y = 150  # Ajustez la position y initiale comme vous le souhaitez
        for line in lines:
            if line:  # Si la ligne n'est pas vide
                line_surface = desc_font.render(line, True, (255, 255, 255))
                line_rect = line_surface.get_rect(topleft=(50, y))
                window.blit(line_surface, line_rect)
                y += desc_font.get_height() + 10  # Passer à la ligne suivante
            else:  # Si la ligne est vide (saut de ligne)
                y +=(desc_font.get_height()+10)  # Sauter deux lignes
        
        # Dessiner un rectangle vert autour du nom de la table
        pygame.draw.rect(window, (0, 255, 0), table_name_rect, 2)  # Le dernier argument est l'épaisseur de la ligne

        #dessiner les boutons
        draw_rounded_rect(window, back_button_rect, (255, 255, 255), 10)  # Dessiner le bouton "Retour"
        draw_rounded_rect(window, add_button_rect, (255, 255, 255), 10)  # Dessiner le bouton "Ajouter"
        draw_rounded_rect(window, modify_button_rect, (255, 255, 255), 10)  # Dessiner le bouton "Modifier"
        
        # Ajouter du texte aux boutons
        for button_rect, button_text in [(back_button_rect, 'Back'), (add_button_rect, 'Ajouter'), (modify_button_rect, 'Modifier')]:
            text_surface = font.render(button_text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=button_rect.center)  # Centrer le texte dans le rectangle
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
button_rects = []
button_width = 300
button_height = 50
button_spacing = 20  # Espace entre les boutons
for i in range(len(tables_return)):
    if i % 2 == 0:  # Bouton à gauche
        x = (window_width - button_spacing - 2 * button_width) // 2
    else:  # Bouton à droite
        x = window_width // 2 + button_spacing // 2
        
    # Si c'est le dernier bouton et que le nombre total de boutons est impair, alors le centrer
    if i == len(tables_return) - 1 and len(tables_return) % 2 == 1:
        x = (window_width - button_width) // 2
    y = 400 + (i // 2) * (button_height + button_spacing)
    button_rects.append(pygame.Rect(x, y, button_width, button_height))

# Créer une police de caractères
font = pygame.font.Font(None, 36)

# Charger une image de fond
background_image = pygame.image.load('etoile.jpg')
background_x = 0  # Position x de l'image de fond
background_y = 0  # Position y de l'image de fond

# Créer une boucle principale
while True:
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
    
    
    #Dessiner le menu de départ
    window.blit(background_image, (background_x, background_y))
    window.blit(background_image, (background_x - background_image.get_width(), background_y))

    # Déplacer l'image de fond
    background_x = random.randrange(window.get_width() - background_image.get_width(), 0)
    background_y = random.randrange(window.get_height() - background_image.get_height(), 0)
    
    # Ajouter logo INSUS
    logo = pygame.image.load('./edit/logo.png')
    window_width = window.get_size()[0]
    # Obtenir la taille de l'image
    logo_width = logo.get_size()[0]
    # Calculer la position x pour centrer l'image
    x = window_width // 2 - logo_width // 2
    # Dessiner l'image
    window.blit(logo, (x, 0))  # Remplacez 'y' par la coordonnée y où vous voulez dessiner l'image
        
    for i, rect in enumerate(button_rects):
        draw_rounded_rect(window, rect, (255, 255, 255), 20)
        text_surface = font.render(tables_return[i], True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=rect.center)
        window.blit(text_surface, text_rect)

    pygame.display.flip()