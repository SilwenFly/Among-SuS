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
            c.execute("SELECT path, choix, reponse, questions FROM quiz_oral WHERE id = ?", (random_number,))
            rows = c.fetchone()
            result = ' | '.join(map(str, rows))
            print(result)
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
            
        elif args.Arg1 == "trou":
            c.execute("SELECT COUNT(id) FROM quiz_texte_trous")
            rows = c.fetchone()
            if rows[0] == 0:
                print("Empty Database")
                exit()
            random_number = random.randint(1, rows[0])
            c.execute("SELECT texte, q1, q2, q3, q4, rep1, rep2, rep3, rep4 FROM quiz_texte_trous WHERE id = ?", (random_number,))
            rows = c.fetchone()
            result = ' | '.join(map(str, rows))
            print(result)

        elif args.Arg1 == "comp":
            c.execute("SELECT COUNT(id) FROM quiz_compréhension")
            rows = c.fetchone()
            if rows[0] == 0:
                print("Empty Database")
                exit()
            random_number = random.randint(1, rows[0])
            c.execute("SELECT texte, questions, choix, reponse FROM quiz_compréhension WHERE id = ?", (random_number,))
            rows = c.fetchone()
            result = ' | '.join(map(str, rows))
            print(result)
except sqlite3.Error as e:
    print(f"An error occurred: {e}")
