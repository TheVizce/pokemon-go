# GO Organizer – Hinweise für Claude

## Dieses Tool
- IndexedDB `pokemon-go-tool`, localStorage-Präfix `go-organizer`.
- Sync: Ordner `pokemon-go/` mit `shards: 16` (main.json + s00–s15.json, seit 11.11.2026; die Zahl nie ändern). Die alte `pokemon-go.json` im Daten-Repo wird nicht mehr benutzt. `collections: pokemon, friends, postcards (array), regionHints (map)`, Feld `xpDigits`.
- Ohne IndexedDB nur Ansicht + JSON-Export (kein Ausweichen in den gemeinsamen localStorage).
- Freunde: Resttage nur über „Prüfen“; Prüfintervall gestaffelt nach Status (`CHECK_AFTER`). Poke-Genie-Import löscht Pokémon mit eigenen Angaben nie, sondern markiert sie (`pgMissing`); eigene Formänderungen bleiben (`pgForm`).
- `SYNC.changed()` steckt in `save()`. `apply` übernimmt in `S` und ruft `save()`.
- Bilder werden nur verlinkt, nicht ins Repo kopiert: PokéAPI-HOME-Sprites (Formen, Gigadynamax) und PokeMiners/pogo_assets (Kostüme `Images/Pokemon - 256x256`, Hintergründe `Images/LocationCards`). Listen `FORMDATA`, `COSTUMES`, `BGS` sind in `index.html` eingebettet; bei neuen Events neu erzeugen.
- Pokémon-Felder für Bilder: `costumeKey` (z. B. `cJAN_2020_NOEVOLVE`), `bgKey` (z. B. `sb_GoFest2025`). Freitext `costume`/`bgName` bleibt als Fallback.

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
