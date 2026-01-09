from locale import LC_TIME, setlocale
import tkinter as tk
from tkinter import messagebox
from datetime import date, timedelta
import subprocess
import json
import os
import glob
import webbrowser

ARCHIV_PATH = "archiv"
SCRAPER_SCRIPT = "billa_scraper.py"


class BillaGUI(tk.Tk):    
    def __init__(self):
        # GUI base
        super().__init__()
        self.title("Billa Flugblatt Suche")
        self.geometry("700x500")

        self.create_widgets()
        self.show_date()

    def create_widgets(self):
        # Datum info
        self.date_label = tk.Label(self, font=("Arial", 12))
        self.date_label.pack(pady=10)

        # Download Button
        tk.Button(
            self,
            text="Aktuelle Flugblätter runterladen",
            command=self.download_flyers
        ).pack(pady=10)

        # Suche
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)

        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(
            search_frame,
            text="Suchen",
            command=self.search_product
        ).pack(side=tk.LEFT)

        # Ergebnisliste
        self.result_list = tk.Listbox(self, width=100, height=20)
        self.result_list.pack(pady=10)
        self.result_list.bind("<Double-Button-1>", self.open_link)

    def show_date(self):
        #  änder die Sprache auf deutsch um einen deutschen Wochentag zu bekommen
        setlocale(LC_TIME, 'de_DE')
        today = date.today()
        kw = today.isocalendar()[1]
        text = f"{today.strftime('%A, der %d.%m.%Y')} – KW {kw:02d}"
        self.date_label.config(text=text)

    def download_flyers(self):
        # aktuelle Flugblätter runterladen
        today = date.today()
        kw, year = self.get_active_flyer_week(today)

        pattern = f"**/*kw{kw}_{year}.json"
        existing = glob.glob(os.path.join(ARCHIV_PATH, pattern), recursive=True)

        # wenn die json dateien bereits im archiv vorhanden sind, zeige info
        if existing:
            messagebox.showinfo(
                "Info",
                "Sie sind bereits auf dem neuesten Stand."
            )
            return

        # wenn sie nicht vorhanden sind, versuche den scraper script zu starten
        try:
            subprocess.run(
                ["python", SCRAPER_SCRIPT],
                check=True
            )
            # wenns funktioniert
            messagebox.showinfo(
                "Fertig",
                "Flugblätter wurden erfolgreich heruntergeladen."
            )
        except subprocess.CalledProcessError:
            # wenns nicht funktioniert
            messagebox.showerror(
                "Fehler",
                "Beim Download ist ein Fehler aufgetreten."
            )

    def search_product(self):
        query = self.search_entry.get().strip().lower()
        self.result_list.delete(0, tk.END)
        today = date.today()
        kw, year = self.get_active_flyer_week(today)

        pattern = f"**/*kw{kw}_{year}.json"

        if not query:
            return

        json_files = glob.glob(
            os.path.join(ARCHIV_PATH, pattern),
            recursive=True
        )

        results = set()

        for file in json_files:
            with open(file, encoding="utf-8") as f:
                data = json.load(f)

            for entry in data:
                for product in entry.get("produkte", []):
                    if query in product.lower():
                        results.add(entry["url"])

        if not results:
            self.result_list.insert(tk.END, "Keine Treffer gefunden.")
            return

        for url in sorted(results):
            self.result_list.insert(tk.END,"Produkt gefunden: ", url)

    def get_active_flyer_week(self, today: date):
        # kleine info: die ISO Kalenderwoche startet jeden Montag neu, allerdings werden die Flugblätter nicht am Montag aktualisiert, sondern am Donnerstag
        # damit das System also die richtige Kalenderwoche zuweisen kann, muss der aktuelle Wochentag überprüft werden
        iso_year, iso_week, iso_weekday = today.isocalendar()

        # An den Wochentagen Montag, Dienstag und Mittwoch, ist nicht die aktuelle Kalenderwoche relevant, sondern die vorangegangene
        if iso_weekday <= 3:  # Mo, Di, Mi
            active_date = today - timedelta(days=7)
        # An den Wochentagen Donnerstag, Freitag, Samstag und Sonntag kann problemlos die aktuelle Kalenderwoche verwendet werden
        else: # Do, Fr, Sa, So
            active_date = today

        year, week, _ = active_date.isocalendar()
        return f"{week:02d}", year


    def open_link(self, event):
        # ermöglicht direkte Interaktion mit den URL Ergebnissen
        selection = self.result_list.curselection()
        if not selection:
            return

        url = self.result_list.get(selection[0])
        if url.startswith("http"):
            webbrowser.open(url)


if __name__ == "__main__":
    app = BillaGUI()
    app.mainloop()
