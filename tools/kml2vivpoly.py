#!/usr/bin/env python3
"""Rechnet die KML der Community-Karte „Vivillon Pattern Distribution Borders“ in die Liste VIV_POLY für index.html um.

Aufruf:  python3 tools/kml2vivpoly.py karte.kml > vivpoly.js
Danach die Zeile `const VIV_POLY = …;` in index.html durch die Ausgabe ersetzen und das Datum im Kommentar anpassen.

- Nur Flächen mit „Best Estimate“ im Namen werden übernommen.
- Längengrade werden je Ring fortlaufend gemacht (Datumsgrenze). Läuft ein Ring einmal um die Erde, ist es ein Ring um den Nordpol (Flag 1).
- Koordinaten auf 2 Nachkommastellen (~1 km) gerundet.
"""
import json, re, sys
import xml.etree.ElementTree as ET
NS = {'k': 'http://www.opengis.net/kml/2.2'}
KEY = {'High Plains': 'highplains', 'Icy Snow': 'icysnow'}

def unwrap(r):
    out = [list(r[0])]
    for x, y in r[1:]:
        px = out[-1][0]
        while x - px > 180: x -= 360
        while x - px < -180: x += 360
        out.append([x, y])
    return out

res = []
for pm in ET.parse(sys.argv[1]).getroot().iter('{%s}Placemark' % NS['k']):
    name = pm.find('k:name', NS).text.strip()
    if 'Best Estimate' not in name: continue
    key = KEY.get(re.sub(r'\s*\d+\s*Best Estimate', '', name), re.sub(r'\s*\d+\s*Best Estimate', '', name).lower())
    for pg in pm.iter('{%s}Polygon' % NS['k']):
        rings = []
        for tag in ('outerBoundaryIs', 'innerBoundaryIs'):
            for b in pg.findall('k:' + tag, NS):
                pts = [[float(c.split(',')[0]), float(c.split(',')[1])] for c in b.find('.//k:coordinates', NS).text.split()]
                rings.append(unwrap(pts))
        pole = 1 if round((rings[0][-1][0] - rings[0][0][0]) / 360) else 0
        res.append([key, pole] + [[round(v, 2) for p in r for v in p] for r in rings])
print('const VIV_POLY = ' + json.dumps(res, separators=(',', ':')) + ';')
