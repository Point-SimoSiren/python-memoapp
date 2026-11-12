"""Yksinkertainen Tkinter-sovellus SQLite-muistiinpanoille."""

import sqlite3
import tkinter as tk
from contextlib import closing
from pathlib import Path
from tkinter import messagebox


# Tietokanta luodaan samaan kansioon kuin tämä ohjelma.
DB_PATH = Path(__file__).with_name("notes.db")


def initialize_database():
    """Luo muistiinpanotaulu, jos sitä ei vielä ole."""
    with closing(sqlite3.connect(DB_PATH)) as connection:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )


def get_notes():
    """Palauta kaikki muistiinpanot uusimmasta vanhimpaan."""
    with closing(sqlite3.connect(DB_PATH)) as connection:
        return connection.execute(
            "SELECT id, title, content, created_at FROM notes ORDER BY id DESC"
        ).fetchall()


def add_note(title, content):
    """Tallenna uusi muistiinpano tietokantaan."""
    with closing(sqlite3.connect(DB_PATH)) as connection:
        with connection:
            # Paikkamerkit suojaavat kyselyä käyttäjän kirjoittamalta SQL:ltä.
            connection.execute(
                "INSERT INTO notes (title, content) VALUES (?, ?)",
                (title, content),
            )


class NotesApp:
    """Rakenna ikkuna ja yhdistä painikkeet tietokannan toimintoihin."""

    def __init__(self, root):
        self.root = root
        self.root.title("Muistiinpanot")
        self.root.geometry("650x500")
        self.notes = []

        # Vasemmalla on tietokannan muistiinpanojen lista.
        left = tk.Frame(root, padx=12, pady=12)
        left.pack(side=tk.LEFT, fill=tk.BOTH)
        tk.Label(left, text="Muistiinpanot").pack(anchor="w")
        self.note_list = tk.Listbox(left, width=28)
        self.note_list.pack(fill=tk.BOTH, expand=True)
        self.note_list.bind("<<ListboxSelect>>", self.show_selected_note)
        tk.Button(left, text="Päivitä lista", command=self.load_notes).pack(
            fill=tk.X, pady=(8, 0)
        )

        # Oikealla näkyy valittu sisältö ja lomake uuden lisäämistä varten.
        right = tk.Frame(root, padx=12, pady=12)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Label(right, text="Valittu muistiinpano").pack(anchor="w")
        self.selected_content = tk.Text(right, height=8, state=tk.DISABLED)
        self.selected_content.pack(fill=tk.BOTH, expand=True)

        tk.Label(right, text="Uusi otsikko").pack(anchor="w", pady=(12, 0))
        self.title_entry = tk.Entry(right)
        self.title_entry.pack(fill=tk.X)
        tk.Label(right, text="Uusi sisältö").pack(anchor="w", pady=(8, 0))
        self.content_entry = tk.Text(right, height=6)
        self.content_entry.pack(fill=tk.BOTH, expand=True)
        tk.Button(right, text="Tallenna", command=self.save_note).pack(
            anchor="e", pady=(8, 0)
        )

        self.load_notes()

    def load_notes(self):
        """Hae muistiinpanot uudelleen ja täytä lista."""
        self.notes = get_notes()
        self.note_list.delete(0, tk.END)
        self.show_content("")
        for _note_id, title, _content, _created_at in self.notes:
            self.note_list.insert(tk.END, title)

    def show_content(self, content):
        """Näytä teksti vain luettavassa sisältökentässä."""
        self.selected_content.config(state=tk.NORMAL)
        self.selected_content.delete("1.0", tk.END)
        self.selected_content.insert("1.0", content)
        self.selected_content.config(state=tk.DISABLED)

    def show_selected_note(self, _event):
        """Näytä listasta valitun muistiinpanon sisältö."""
        selection = self.note_list.curselection()
        if selection:
            _note_id, _title, content, created_at = self.notes[selection[0]]
            self.show_content(f"Luotu: {created_at}\n\n{content}")

    def save_note(self):
        """Tarkista syöte, tallenna muistiinpano ja päivitä lista."""
        title = self.title_entry.get().strip()
        content = self.content_entry.get("1.0", tk.END).strip()
        if not title or not content:
            messagebox.showwarning("Puuttuva tieto", "Kirjoita otsikko ja sisältö.")
            return

        add_note(title, content)
        self.title_entry.delete(0, tk.END)
        self.content_entry.delete("1.0", tk.END)
        self.load_notes()
        self.note_list.selection_set(0)
        self.show_selected_note(None)


def main():
    """Valmistele tietokanta ja käynnistä Tkinter-ikkuna."""
    initialize_database()
    root = tk.Tk()
    NotesApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
