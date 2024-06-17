import argparse
import sqlite3
import random

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

else:
    print("GNEU,GNEU PAS COMPRIS")