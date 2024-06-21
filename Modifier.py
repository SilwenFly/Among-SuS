import sqlite3
import tkinter as tk
from tkinter import messagebox, filedialog
import shutil

# Connexion à la base de données existante
def connect_db():
    return sqlite3.connect('db.db')

# Ajout d'un enregistrement
def add_record(table, columns, values):
    conn = connect_db()
    cursor = conn.cursor()
    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(values))})"
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    messagebox.showinfo("Info", f"Enregistrement ajouté dans {table} avec succès")

# Modification d'un enregistrement
def update_record(table, columns, values, record_id):
    conn = connect_db()
    cursor = conn.cursor()
    set_clause = ', '.join([f"{col}=?" for col in columns])
    query = f"UPDATE {table} SET {set_clause} WHERE id=?"
    cursor.execute(query, values + [record_id])
    conn.commit()
    conn.close()
    messagebox.showinfo("Info", f"Enregistrement mis à jour dans {table} avec succès")

# Suppression d'un enregistrement
def delete_record(app, table, record_id):
    conn = connect_db()
    cursor = conn.cursor()
    query = f"DELETE FROM {table} WHERE id=?"
    cursor.execute(query, (record_id,))
    conn.commit()

    # Mettre à jour l'ID dans l'Entry
    cursor.execute(f"SELECT COUNT(id) FROM {table}")
    new_id = cursor.fetchone()[0] + 1
    conn.close()

    app.id_entry.delete(0, tk.END)  # Efface l'ID actuel
    app.id_entry.insert(0, str(new_id))  # Insère le nouvel ID

    messagebox.showinfo("Info", f"Enregistrement supprimé de {table} avec succès")

# Affichage d'un enregistrement par ID dans une boîte de texte
def show_record_in_entry(table, record_id, entry):
    conn = connect_db()
    cursor = conn.cursor()
    query = f"SELECT * FROM {table} WHERE id=?"
    cursor.execute(query, (record_id,))
    record = cursor.fetchone()
    conn.close()
    if record:
        entry.delete(0, tk.END)  # Efface le contenu précédent de l'Entry
        entry.insert(0, ' | '.join(map(str, record)))  # Insère les données dans l'Entry
    else:
        messagebox.showinfo("Info", "Aucun enregistrement trouvé avec cet ID")

# Affichage du nombre total d'enregistrements dans une table
def count_records(table):
    conn = connect_db()
    cursor = conn.cursor()
    query = f"SELECT COUNT(id) FROM {table}"
    cursor.execute(query)
    count = cursor.fetchone()[0]
    conn.close()
    messagebox.showinfo("Info", f"Nombre total d'enregistrements dans {table}: {count}")

# Récupération des noms des tables et des colonnes
def get_tables_and_columns():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    table_info = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [info[1] for info in cursor.fetchall()]
        table_info[table_name] = columns
    conn.close()
    return table_info

# Mise à jour de l'affichage des tables et des colonnes
def update_table_info(label):
    table_info = get_tables_and_columns()
    info_text = ""
    for table, columns in table_info.items():
        info_text += f"Table: {table}\nColonnes: {', '.join(columns)}\n\n"
    label.config(text=info_text)

# Sélectionner et copier un fichier MP3
def select_and_copy_mp3(destination_folder):
    file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
    if file_path:
        shutil.copy(file_path, destination_folder)
        messagebox.showinfo("Info", f"Fichier {file_path} copié dans {destination_folder}")

# Interface graphique
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Quiz")

        self.help_button = tk.Button(root, text="Aide", command=self.show_help)
        self.help_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.table_label = tk.Label(root, text="Table")
        self.table_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.table_entry = tk.Entry(root)
        self.table_entry.grid(row=1, column=1, padx=5, pady=5)

        self.columns_label = tk.Label(root, text="Colonnes (séparées par des virgules)")
        self.columns_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.columns_entry = tk.Entry(root)
        self.columns_entry.grid(row=2, column=1, padx=5, pady=5)

        self.values_label = tk.Label(root, text="Valeurs (séparées par des virgules)")
        self.values_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.values_entry = tk.Entry(root)
        self.values_entry.grid(row=3, column=1, padx=5, pady=5)

        self.add_button = tk.Button(root, text="Ajouter", command=self.add_record)
        self.add_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.mp3_button = tk.Button(root, text="Sélectionner et copier un fichier MP3", command=self.select_and_copy_mp3)
        self.mp3_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.id_label = tk.Label(root, text="ID (pour modifier/supprimer/afficher)")
        self.id_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.id_entry = tk.Entry(root)
        self.id_entry.grid(row=6, column=1, padx=5, pady=5)

        self.update_button = tk.Button(root, text="Modifier", command=self.update_record)
        self.update_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        self.show_button = tk.Button(root, text="Afficher", command=self.show_record_in_entry)
        self.show_button.grid(row=8, column=0, columnspan=2, padx=5, pady=5)
        
        self.display_entry = tk.Entry(root, width=80)
        self.display_entry.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

        self.delete_button = tk.Button(root, text="Supprimer", command=self.delete_record_wrapper)
        self.delete_button.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

        self.count_button = tk.Button(root, text="Compter", command=self.count_records)
        self.count_button.grid(row=11, column=0, columnspan=2, padx=5, pady=5)

        self.info_label = tk.Label(root, text="", justify=tk.LEFT)
        self.info_label.grid(row=12, column=0, columnspan=2, padx=5, pady=5)

        update_table_info(self.info_label)

    def add_record(self):
        table = self.table_entry.get()
        columns = self.columns_entry.get().split(',')
        values = self.values_entry.get().split(',')
        if table and columns and values:
            add_record(table, columns, values)

    def update_record(self):
        table = self.table_entry.get()
        columns = self.columns_entry.get().split(',')
        values = self.values_entry.get().split(',')
        record_id = self.id_entry.get()
        if table and columns and values and record_id:
            update_record(table, columns, values, int(record_id))

    def delete_record_wrapper(self):
        table = self.table_entry.get()
        record_id = self.id_entry.get()
        if table and record_id:
            delete_record(self, table, int(record_id))

    def show_record_in_entry(self):
        table = self.table_entry.get()
        record_id = self.id_entry.get()
        if table and record_id:
            show_record_in_entry(table, int(record_id), self.display_entry)

    def count_records(self):
        table = self.table_entry.get()
        if table:
            count_records(table)

    def select_and_copy_mp3(self):
        destination_folder = "src/"  # Spécifiez le chemin du dossier de destination ici
        select_and_copy_mp3(destination_folder)

    def show_help(self):
        help_text = """
        Bienvenue dans l'application de gestion des Quiz !

        Pour utiliser cette application, suivez ces étapes :
        1. Remplissez les champs Table, Colonnes et Valeurs pour ajouter un nouvel enregistrement.
        2. Utilisez les boutons Ajouter, Modifier, Supprimer, Afficher et Compter pour gérer les enregistrements.
        3. Utilisez le champ ID pour spécifier l'ID de l'enregistrement à modifier, supprimer ou afficher.

        Le bouton Sélectionner et copier un fichier MP3 permet de choisir un fichier à copier et le nom du fichier est a ajouter dans la table quiz_oral dans la colonne audio.
        (Exemple: TEST_1_PART3_1.mp3)

        N'oubliez pas de sélectionner une table dans le champ Table avant d'effectuer des opérations.

        Information importante:
        Toujours mettre "&" entre chaque questions, choix ou réponses.
        (Exemple: A) share & B) shares & C) sharing & D) shared)
        """
        messagebox.showinfo("Aide", help_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
       