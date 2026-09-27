# Caiet de Laborator

Caiet de laborator digital pentru disciplina **Uscarea lemnului**. Studenții completează fișele de lucru pe telefon sau pe laptop, iar cadrul didactic le primește, le corectează și calculează nota finală, totul dintr-o singură pagină web.

**Aplicația:** https://sergiugeorgescu-ai.github.io/caiet-laborator/

## Lucrări incluse

| Lucrare | Titlu | Pagină separată |
|---|---|---|
| 1 | Prezentarea generală a unei instalații de uscare | [lucrarea-1.html](https://sergiugeorgescu-ai.github.io/caiet-laborator/lucrarea-1.html) |
| 2 | Stivuirea cherestelei, amplasarea stivelor în instalație și determinarea capacității de uscare | [lucrarea-2.html](https://sergiugeorgescu-ai.github.io/caiet-laborator/lucrarea-2.html) |
| 3 | Determinarea și monitorizarea umidității lemnului înainte, pe parcursul și la sfârșitul procesului de uscare | [lucrarea-3.html](https://sergiugeorgescu-ai.github.io/caiet-laborator/lucrarea-3.html) |
| 4 | Metode și aparatură pentru măsurarea temperaturii, umidității relative a aerului și a umidității de echilibru | [lucrarea-4.html](https://sergiugeorgescu-ai.github.io/caiet-laborator/lucrarea-4.html) |

`index.html` conține toate lucrările; fiecare `lucrarea-N.html` este aceeași aplicație, cu figurile unei singure lucrări (se încarcă mai repede pe telefon).

## Pentru studenți

1. Scanează codul QR al lucrării (sau deschide linkul primit).
2. Scrie numele și grupa. Din ele se generează setul tău de date numerice, diferit de al colegilor.
3. Răspunde la întrebări. Fișa se salvează automat, deci poți închide pagina și relua mai târziu.
4. Apasă **Finalizează**, apoi **Trimite profesorului** (e-mail, WhatsApp, Teams).
5. Dacă nu ai semnal, apasă **Arată codul QR** și lasă profesorul să-l scaneze de pe ecran.

## Pentru cadrul didactic

1. **Intrarea în modul profesor:** apasă insigna **LAB** din stânga sus și introdu codul PIN (îl alegi la prima intrare). Pe calculatoarele din laborator nu bifa „Ține minte pe acest calculator”.
2. **Cheile de criptare:** în fila *Acces studenți*, apasă **Generează cheile**. Fișierul `cheie-profesor-XXXXXX.json` descărcat atunci este singura copie a cheii private; păstrează-l în două locuri sigure.
3. **Editorul:** în fila *Editor* creezi sau modifici lucrări (antet, figuri, grile, aplicații numerice cu date individuale, întrebări cu răspuns liber).
4. **Ora de laborator:** proiectează codul QR al lucrării din fila *Acces studenți*.
5. **Corectarea:** lipește în fila *Catalog* tot ce ai primit (un e-mail întreg, o conversație). Aplicația găsește singură codurile, corectează automat grilele și aplicațiile numerice; tu punctezi răspunsurile libere.
6. **Nota finală:** fila *Note finale* face media lucrărilor predate, cu export CSV/Excel și clasament pe grupe.

Ghidul complet se găsește în aplicație, în modul profesor.

## Detalii tehnice

- Site static pe GitHub Pages, fără pas de build și fără dependențe de instalat.
- Datele stau în browser (IndexedDB, cu localStorage ca rezervă); nu există server.
- Fișele trimise sunt criptate cu cheia publică a profesorului.
- Codul PIN ține studenții departe de editor și catalog, dar nu ascunde codul-sursă: răspunsurile corecte sunt vizibile pentru cine citește pagina. Protecția reală la lucrările notate este faptul că fiecare student primește alte date numerice.

---

## English summary

**Caiet de Laborator** is a digital lab notebook for the *Wood Drying* (Uscarea lemnului) course, hosted on GitHub Pages at https://sergiugeorgescu-ai.github.io/caiet-laborator/. It ships four labs; `index.html` holds all of them and `lucrarea-1…4.html` each hold a single lab.

- **Students** open a lab via QR code, enter name and group (which seeds their personal numeric data), fill in the worksheet (autosaved), and submit it by e-mail/messaging app or by showing a QR code.
- **Teachers** unlock teacher mode with a PIN (tap the **LAB** badge), generate an encryption key pair, edit labs, paste received submissions into the *Catalog* for automatic grading, and export final grades.

It is a single static page with no build step and no backend; data lives in the browser, and submissions are encrypted with the teacher's public key.
