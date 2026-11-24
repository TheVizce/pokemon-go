# GO Organizer – Hinweise für Claude

## Dieses Tool
- IndexedDB `pokemon-go-tool`, localStorage-Präfix `go-organizer`.
- Sync: Ordner `pokemon-go/` mit `shards: 16` (main.json + s00–s15.json, seit 11.11.2026; die Zahl nie ändern). Die alte `pokemon-go.json` im Daten-Repo wird nicht mehr benutzt. `collections: pokemon, friends, postcards (array), regionHints, places, vivCards (map)`, Feld `xpDigits`.
- Ohne IndexedDB nur Ansicht + JSON-Export (kein Ausweichen in den gemeinsamen localStorage).
- Freunde: Resttage nur über „Prüfen“. Zwei getrennte Status in `activity()`: „Spielt“ (aus `xpChanged`, nicht bei Lv 80) und „Freundschaft“ (aus `friendChanged`, stockt ab `FR_STALL` = 7 Tagen, nicht beim Allerbesten Freund); „Spielt, interagiert nicht“ = EP aktiv + Freundschaft stockt. Prüfintervall = kürzerer Wert aus beiden (`CHECK_AFTER`). Pro Freund fest um ±25 % gestreut (`CHECK_SPREAD`, `spreadDays()` aus der id), damit nicht alle am selben Tag fällig werden.
- Entfernen-Vorschlag: `removeScore()` (Punkte aus Aktivität, Freundeslevel, Glücksfreund, Muster-Einzigartigkeit; Liste ab `REMOVE_MIN`), Filter „Eher entfernen“. Nie bei `irl` (Reallife-Freund, Haken im Dialog) und nicht ohne Prüfung in den letzten `REMOVE_FRESH` Tagen. Das Tool löscht nie selbst.
- Geschenke öffnen (seit 24.11.2026): `f.giftWaiting` (Geschenk vorgemerkt), `f.giftOpened` (Datum letzte Öffnung). Filter „🎁 Geschenke öffnen“ sortiert nach `giftScore()` (Freundschaft steigt, kurz vor Level, am längsten nicht geöffnet, Reallife, fehlendes Muster; Entfernen-Kandidaten ganz oben, damit ihr Geschenk vor dem Entfernen geöffnet wird). Erfassen-Liste (`renderGiftCapture`, `FF.capture`): alle Freunde kompakt nach Name (`nameCmp`) wie die Freundesliste im Spiel, Tipp schaltet `giftWaiting`. Tageslimit nur lokal in `localStorage['go-organizer-giftlimit']` (Standard 20). Nicht verwechseln mit dem am 2026-11 entfernten „Geschenk geschickt“-Knopf (`giftSent`, wird weiter beim Start entfernt).
- Postkarten-Liste entfernt (24.11.2026): Herkunft (`region`) und Vivillon-Muster (`viv`) stehen beim Freund. Alte `postcards` wurden per `migratePostcards()` in die Freunde übernommen (`moved: true`), bleiben aber in den Daten und im Sync (kein Massenlöschen). Vivillon-Tab: Stand wie in der Medaille (Fortschritt bis zur nächsten Purmel-Begegnung, z. B. 4 / 15) in `vivCards` (Map Muster → `{p, goal, date}`, goal 3/9/15, synchronisiert; alte `{n}` = Gesamtzahl werden per `migrateVivCards()` umgerechnet). Muster-Namen und Reihenfolge in `VIV` wie im deutschen Pokémon GO (Schlüssel englisch, nie ändern). Beste IV / beste Shiny pro Muster werden aus den Pokémon der Purmel-Linie (`VIV_LINE`) mit gesetztem `viv` berechnet – kein eigenes Feld; Poke Genie exportiert das Muster nicht.
- Herkunft (seit 24.11.2026): `country` = ISO-Code (Name/Flagge per `Intl.DisplayNames`, Liste `countryList()`), `region` = Freitext (Bundesland, Staat, Stadt). Alter Freitext wird per `migrateOrigin()`/`parseOrigin()` zerlegt, Original in `originOld`. Mögliche Muster pro Land in `VIV_COUNTRY` (Quelle friend-codes.com, nur Vorschlag/Plausibilität, keine Unterregionen); bei genau einem Muster wird es gesetzt, wenn `viv` leer ist. `regionHints` und `postcards` bleiben in den Daten, werden aber nicht mehr benutzt.
- „+1 Postkarte“ auf der Freundeskachel (`vivPlus`): zählt `vivCards[f.viv]` hoch, Rückmeldung per `toast()` mit Rückgängig; bei Erreichen des Ziels Purmel-Begegnung und neuer Zähler 0 / nächstes Ziel (3 → 9 → 15 → 15). „+1 andere…“ (Kachel) bzw. „+1 Postkarte von Ort…“ (Vivillon-Tab) → `vivOther()`: Ort suchen (Nominatim, auf Knopfdruck), Muster per `vivAt`, Muster wählbar, dann `vivPlus`. Speichert keine Orte.
- Musterkarte (seit 24.11.2026): `VIV_POLY` = Flächen der Community-Karte „Vivillon Pattern Distribution Borders“ (KML, nur „Best Estimate“), erzeugt mit `tools/kml2vivpoly.py` (Datumsgrenze/Pol-Ringe beachtet). `vivAt(lat, lon)` → Muster. Herkunftsorte (`Region, Land`) werden nur auf Knopfdruck über Nominatim gesucht und in `places` mit `kind: 'origin'` gespeichert (nicht in der Fangort-Liste/Karte). Karte hat Vorrang vor `VIV_COUNTRY`; vorhandene `viv` werden nie überschrieben, nur leere ergänzt.
- Poke Genie nur über den **Abgleich**: Backup wird dem Stand gegenübergestellt, jede Änderung einzeln entschieden (nichts vorausgewählt, nichts automatisch zusammengeführt), erst „Ausgewählte übernehmen“ schreibt. Prüf-Stand im IndexedDB-Eintrag `pgReview` (Store `kv`, nicht synchronisiert, wird nach Abschluss gelöscht). Wiedererkennung über `pgKey` (Scan-Datum + IVs + Geschlecht), Gegenstücke über Entwicklungsreihe (`EVO`). `pgForm` = zuletzt aus Poke Genie übernommene Form. Alte `pgMissing`-Markierungen landen in „Nicht mehr im Backup“.
- Orte: `location` = Fangort (bei `remote` = Raid-Ort), `myLocation` = eigener Standort beim Fern-Raid. Koordinaten einmal pro Ort im Verzeichnis `places` (Map, Schlüssel = Ortsname klein, synchronisiert). Ortssuche nur auf Knopfdruck über OpenStreetMap/Nominatim; Karte-Tab mit Leaflet 1.9.4 (cdnjs) und OSM-Kacheln.
- Abenteuereffekt wird aus den Lade-Attacken abgeleitet (`ADV_MOVES`, Namen wie im Poke-Genie-Export) – kein eigenes Feld; neue Abenteuereffekte dort ergänzen.
- `SYNC.changed()` steckt in `save()`. `apply` übernimmt in `S` und ruft `save()`.
- Bilder werden nur verlinkt, nicht ins Repo kopiert: PokéAPI-HOME-Sprites (Formen, Gigadynamax) und PokeMiners/pogo_assets (Hintergründe `Images/LocationCards`). Listen `FORMDATA`, `BGS` sind in `index.html` eingebettet; bei neuen Events neu erzeugen.
- Kostüme sind reiner Text (`costume`). Kostüm-Bilder wurden am 23.11.2026 auf Wunsch zurückgebaut (uneinheitlich: nicht alle vorhanden, anderer Stil/andere Größe) – nicht wieder einführen. Alte `costumeKey` werden beim Start in Text umgewandelt.
- Hintergrund: Bild `bgKey` (z. B. `sb_GoFest2025`), Freitext `bgName` bleibt als Fallback.
- Mega-/Proto-Level pro Pokémon: Feld `mega` (1 Basis, 2 Hoch, 3 Max, 4 Super-Max, leer = noch nie). Nur bei Arten aus `MEGA` (PokéAPI, inkl. Megas, die es in GO noch nicht gibt), nicht bei Crypto. Poke Genie exportiert es nicht → eigene Angabe, der Abgleich fasst es nicht an. Keine Mega-Bilder.

## Gemeinsame Regeln für alle Tools unter thevizce.github.io

Alle Tools laufen unter derselben Adresse und teilen sich Speicher. Übersicht, Speicheranzeige und Sync-Einstellungen: Repo `startseite` (https://thevizce.github.io/startseite/).

**Speicher**
- localStorage ist für alle Tools gemeinsam (~5 MB). Nur kleine Daten (deutlich unter 500 KB) mit dem eigenen Präfix, nie `localStorage.clear()`.
- Größere Daten in die eigene IndexedDB (Name unten). Fremde Datenbanken nie beschreiben.
- Speicherfehler sichtbar anzeigen. JSON-Export/Import muss weiter funktionieren.
- Formatänderungen: alte Daten beim Start automatisch übernehmen, alte Schlüssel erst danach entfernen.
- Vor Änderungen am Speicher dem Nutzer kurz Befund und empfohlene Variante nennen, danach eine kurze Umstiegs-Anleitung gegen Datenverlust geben.

**GitHub-Sync (`/startseite/sync-v1.js`)**
- Das Tool gleicht über `ToolSync.create({...})` mit dem privaten Repo `TheVizce/tool-daten` ab. Token und Repo trägt der Nutzer nur auf der Startseite ein (`localStorage["toolsync.config"]`). Keine eigenen Token-Felder oder eigenen GitHub-Uploads bauen.
- Nach jedem erfolgreichen Speichern muss `SYNC.changed()` aufgerufen werden (Stelle unten). Neue Speicherwege ebenfalls daran anschließen.
- Neue Datenfelder oder Listen müssen in `get`/`apply` und in `collections`/`fields` ergänzt werden, sonst werden sie nicht abgeglichen oder gehen beim Übernehmen aus der Cloud verloren.
- Einträge in Listen brauchen eine stabile `id` (bzw. das angegebene ID-Feld). IDs nie neu vergeben, nicht umbenennen.
- Ein Eintrag gelöscht = Löschung wird gemerkt. Daten nicht durch Löschen + Neuanlegen „umbauen“.
- `sync-v1.js` nicht kopieren und nicht im Tool-Repo ändern. Änderungen daran nur im Repo `startseite`, abwärtskompatibel; Inkompatibles als `sync-v2.js`.
- Das ☁︎-Feld unten links (mit ⌂ zur Startseite) kommt aus dem Sync. Keinen eigenen Zurück-Knopf bauen, der dort kollidiert.

**Sonst**
- iPhone: Kopfzeilen mit `env(safe-area-inset-top)` und `viewport-fit=cover` beibehalten.
- Direkte Pushes auf `main` sind erlaubt. Nicht gleichzeitig aus zwei Chats am selben Tool arbeiten.
- Neue Tools oder neue Datenbanken in `startseite/index.html` (Liste `TOOLS`) eintragen.
