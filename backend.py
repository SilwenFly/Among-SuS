import argparse
import sqlite3
import random
import pygame
import re

# Initialiser pygame mixer
pygame.mixer.init()

# Créer le parser
parser = argparse.ArgumentParser(description="Backend of Among SuS")

# Ajouter les arguments
parser.add_argument('Arg1', type=str, help='This is argument 1')

# Parser les arguments
args = parser.parse_args()

try:
    with sqlite3.connect('db.db') as conn:
        c = conn.cursor()

        if args.Arg1 == "vocab":
            c.execute("SELECT COUNT(id) FROM quiz_vocabulaire")
            rows = c.fetchone()
            if rows[0] == 0:
                print("Empty Database")
                exit()
            random_number = random.randint(1, rows[0])
            c.execute("SELECT questions, choix, reponse FROM quiz_vocabulaire WHERE id = ?", (random_number,))
            rows = c.fetchone()
            result = ' | '.join(map(str, rows))
            print(result)

        elif args.Arg1 == "verbe":
            c.execute("SELECT COUNT(id) FROM quiz_verbe")
            rows = c.fetchone()
            if rows[0] == 0:
                print("Empty Database")
                exit()
            random_number = random.randint(1, rows[0])
            c.execute("SELECT traduction, verbe, reponse FROM quiz_verbe WHERE id = ?", (random_number,))
            rows = c.fetchone()
            result = ' | '.join(map(str, rows))
            print(result)

        elif args.Arg1 == "oral":
            c.execute("SELECT COUNT(id) FROM quiz_oral")
            rows = c.fetchone()
            if rows[0] == 0:
                print("Empty Database")
                exit()
            random_number = random.randint(1, rows[0])
            c.execute("SELECT questions, choix, reponse, id FROM quiz_oral WHERE id = ?", (random_number,))
            rows = c.fetchone()
            result = ' | '.join(map(str, rows))
            print(result)

        elif re.match(r'^oral\d+$', args.Arg1):  # si l'argument est de la forme Oral suivi de chiffres
            s = args.Arg1  # récupère l'argument
            numbers = ''.join(i for i in s if i.isdigit())  # récupère les chiffres
            id = int(numbers)  # convertit en int
            c.execute("SELECT path FROM quiz_oral WHERE id = ?", (id,))
            rows = c.fetchone()
            if rows:
                path = "src/" + rows[0]
                try:
                    pygame.mixer.music.load(path)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)  # Attendre que la musique se termine
                except pygame.error as e:
                    print(f"Failed to play the audio file: {e}")
            else:
                print("No record found with the given ID.")
        else:
            print("GNEU,GNEU PAS COMPRIS")

except sqlite3.Error as e:
    print(f"An error occurred: {e}")
