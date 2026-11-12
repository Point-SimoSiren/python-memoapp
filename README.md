# SQLite-muistiinpanot

Pieni Tkinter-sovellus, jolla voi lisätä ja katsella SQLite-tietokantaan tallennettuja muistiinpanoja. Muistiinpanot säilyvät ohjelman sulkemisen jälkeen.

## Asennus ja käynnistys Windowsissa

Python 3 on asennettava tietokoneelle python.org sivulta.
Komentorivillä kansiossa minne koodi on laitettu annetaan käynnistyskomento:
python app.py


## Käyttö

Kirjoita otsikko ja sisältö oikealle ja paina **Tallenna**. Valitse muistiinpano vasemman puolen listasta nähdäksesi sen sisällön. **Päivitä lista** hakee tiedot tietokannasta uudelleen, jos niitä on muutettu ohjelman ulkopuolella.

## Tiedostot

| Tiedosto | Tehtävä |
| --- | --- |
| `app.py` | Tkinter-käyttöliittymä ja SQLite-tietokannan käsittely. |
| `notes.db` | Muistiinpanot sisältävä SQLite-tietokanta. Syntyy ensimmäisellä käynnistyksellä. |
| `README.md` | Asennus-, käynnistys- ja koodiohjeet. |

## `app.py`-tiedoston metodit ja funktiot

| Nimi | Tehtävä |
| --- | --- |
| `initialize_database()` | Luo `notes`-taulun, ellei sitä ole. |
| `get_notes()` | Lukee kaikki muistiinpanot uusimmasta vanhimpaan. |
| `add_note(title, content)` | Lisää uuden muistiinpanon tietokantaan. |
| `NotesApp.__init__()` | Rakentaa ikkunan ja sen kentät sekä lataa listan. |
| `NotesApp.load_notes()` | Päivittää näkyvän listan tietokannasta. |
| `NotesApp.show_content(content)` | Asettaa tekstin luettavaan sisältökenttään. |
| `NotesApp.show_selected_note(event)` | Näyttää listasta valitun muistiinpanon. |
| `NotesApp.save_note()` | Tarkistaa kentät, tallentaa uuden muistiinpanon ja päivittää näkymän. |
| `main()` | Alustaa tietokannan ja käynnistää sovelluksen. |

Tietokannan `notes`-taulussa on sarakkeet `id`, `title`, `content` ja `created_at`.
