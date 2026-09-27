# caiet-laborator

Caiet de laborator pentru cursul „Uscarea lemnului”, publicat cu GitHub Pages.

## Sursa și paginile generate

Paginile `index.html` și `lucrarea-1.html` … `lucrarea-4.html` **se generează** din `src/` — nu le editați direct.

- `src/app.html` — aplicația (o singură copie a codului)
- `src/labs/lucrarea-N/lab.json` — conținutul lucrării N (text, întrebări, barem)
- `src/labs/lucrarea-N/img/*.webp` — figurile lucrării N

După orice modificare în `src/`, rulați (necesită Node.js):

```
node build.js
```

și publicați atât `src/`, cât și paginile regenerate. `node build.js --check` verifică doar dacă paginile corespund sursei.
