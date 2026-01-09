# Angebot Scraper
Ein Simples Webscraping Script, welches Informationen aus dem HTML Code von Supermarkt Flugblättern in JSON-Dateien abspeichert um anschließend eine Produktsuche zu ermöglichen
## [angebote_GUI.py](angebote_GUI.py)
Das Frontend des Projekts. Ein Simples User Interface das die Ausführung von anderen Scripts und die Durchsuchung der JSON-Dateien ermöglicht.
## [billa_scraper.py](billa_scraper.py)
Ein Webscraping script, welches die aktuellen Flugblätter von Billa Wien und Billa Plus Wien als JSON-Dateien im archiv speichert. Durch das aktuelle Datum wird immer der derzeit aktuelle Angebotskatalog untersucht. <br> 
Prozessablauf:
<ul>
  <li>Es wird ausgelesen, wie viel Seiten das Flugblatt insgesamt hat.</li>
  <li>Eine Schleife wird gestartet die die gesamte Seitenanzahl inkrementiert</li>
  <li>Die Schleife ruft über die URL die einzelnen Katalogseiten auf</li>
  <li>Ein Timeout counter versichert dass der HTML Code vollständig geladen wird und dass Server Überlastung seitens Billa minimiert werden.</li>
  <li>Der Alt-Text, welcher die Produktinformationen enthält, wird gespeichert</li>
  <li>Das Script differenziert auf welcher Seite man sich aktuell befindet; Um redundante Informationen zu vermeiden, ist es wichtig zu wissen...</li>
  <ul>
    <li>ob die aktuelle Ansicht nur die rechte Seite des Flugblatts zeigt (ergo die erste Seite vom Angebotskatalog)</li>
    <li>ob die aktuelle Ansicht nur die linke Seite des Flugblatts zeigt (ergo die letzte Seite vom Angebotskatalog)</li>
    <li>ob die aktuelle Ansicht eine Doppelseite zeigt (ergo alles dazwischen)</li>
  </ul>
  <li>Doppelseiten werden nur einmal aufgerufen, da z.B. sowohl der Aufruf von Seite 2 als auch von Seite 3 die Doppelseiten 2-3 anzeigt und ein doppelter Aufruf für redundante Daten sorgt</li>
</ul><br>
Nach dem Prozessablauf wird der Alt-Text und die URL in eine JSON Datei eingetragen, welche im Archiv gespeichert wird.
