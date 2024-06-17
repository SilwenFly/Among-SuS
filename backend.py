import argparse
import sqlite3
import random
from playsound import playsound #Bibliothèque pour jouer du son
import re

# Create the parser
parser = argparse.ArgumentParser(description="Backend of Among SuS")

# Add the arguments
parser.add_argument('Arg1', type=str, help='This is argument 1')


# Parse the arguments
args = parser.parse_args()
conn = sqlite3.connect('db.db')
c = conn.cursor()

if  args.Arg1 == "vocab":
    c.execute("SELECT COUNT(id) FROM quiz_vocabulaire")
    rows = c.fetchone()
    if rows[0] == 0:
        print("Empty Database")
        exit()
    random_number = random.randint(1,rows[0])
    c.execute("SELECT questions,choix,reponse FROM quiz_vocabulaire WHERE id = ?",(random_number,))
    rows = c.fetchone()
    result = '? '.join(map(str, rows))
    print(result)
    
elif args.Arg1 == "verbe":
    c.execute("SELECT COUNT(id) FROM quiz_verbe")
    rows = c.fetchone()
    if rows[0] == 0:
        print("Empty Database")
        exit()
    random_number = random.randint(1,rows[0])
    c.execute("SELECT questions,choix,reponse FROM quiz_verbe WHERE id = ?",(random_number,))
    rows = c.fetchone()
    result = '? '.join(map(str, rows))
    print(result)
    
elif args.Arg1 == "oral":
    c.execute("SELECT COUNT(id) FROM quiz_verbe")
    rows = c.fetchone()
    if rows[0] == 0:
        print("Empty Database")
        exit()
    random_number = random.randint(1,rows[0])
    c.execute("SELECT questions,choix,reponse,id FROM quiz_oral WHERE id = ?",(random_number,))
    rows = c.fetchone()
    result = '? '.join(map(str, rows))
    print(result)
    

elif re.match(r'^Oral\d+$', args.Arg1): #si l'argument est de la forme Oral suivi de chiffres
    s = args.Arg1 #récupère l'argument
    numbers = ''.join(i for i in s if i.isdigit()) #récupère les chiffres
    id = int(numbers) #convertit en int
    c.execute("SELECT path from quiz_oral WHERE id = ?",(id,))
    rows = c.fetchone()
    path = "src/" + rows[0]
    playsound(path)
else:
    print("GNEU,GNEU PAS COMPRIS")