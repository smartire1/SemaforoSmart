# Sincronizzazione manuale Windows/macOS

Finche' il progetto non usa una soluzione centralizzata, evitare modifiche
parallele agli stessi file. Prima di ogni sessione stabilire quale computer e'
la copia autorevole; al termine riportare sull'altro soltanto gli elementi
modificati.

## Copiare sempre quando cambiano

- `README.md` e `requirements.txt`;
- `scripts/` escluso `__pycache__/`;
- `docs/project/`, `docs/guides/` e `docs/handoff/`;
- nuovi log sotto `docs/logs/`;
- README, manifest e configurazioni di un dataset modificato;
- report prodotti sotto `experiments/Test/`;
- `best.pt`, `args.yaml`, `results.csv` e grafici di un nuovo training che deve
  essere consultabile su entrambe le macchine.

Se cambia realmente il contenuto di un dataset, copiarne l'intera cartella
versionata oppure verificare con hash che le due copie siano identiche. Non
ricostruire parzialmente un dataset copiando file isolati senza manifest.

## Non sincronizzare normalmente

- `.venv/`, che e' specifica del sistema operativo;
- `runs/` e `weights/yolo26n.pt`, cache rigenerabili;
- `scripts/__pycache__/`, `*.cache`, `.DS_Store`, `._*` e `__MACOSX/`;
- video predetti gia' presenti su entrambi i computer;
- ZIP raw storici, salvo che l'altra macchina debba diventare un archivio
  completo.

## Procedura breve

1. Chiudere training e inferenze sulla macchina sorgente.
2. Annotare quali file sono cambiati.
3. Copiarli mantenendo gli stessi percorsi relativi.
4. Controllare `docs/project/STATO_PROGETTO.md` e il README interessato.
5. Per pesi o dataset importanti, confrontare dimensione e SHA-256.
6. Riprendere il lavoro soltanto dopo aver scelto nuovamente la copia autorevole.

I path nei documenti e negli script devono restare relativi alla root, così gli
stessi comandi funzionano sia su Windows sia su macOS.
