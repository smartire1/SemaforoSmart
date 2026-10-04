# Benchmark video v1.3_cp

Output del modello `exp_v1_3_cp_day_001`, eseguiti con soglia `conf=0.60` e
riordinati sotto `day_001/`.

| Cartella | Video |
|---|---|
| `day_001/ambulanza_giorno/` | benchmark Ambulanza giorno |
| `day_001/ambulanza_notte/` | benchmark Ambulanza notte |
| `day_001/carabinieri_giorno/` | benchmark Carabinieri giorno |
| `day_001/carabinieri_notte/` | benchmark Carabinieri notte |
| `day_001/vdf_giorno/` | benchmark VDF giorno |
| `day_001/vdf_notte/` | benchmark VDF notte ordinario |

Lo stress test VDF notte non e' stato eseguito in questo primo ciclo. Il nome
originario errato `v1.3_cp_conf60_carab_notte-2` conteneva in realta'
Ambulanza notte ed e' stato corretto durante l'audit.

Verdetto qualitativo: miglioramento sorprendente su Carabinieri notte e lieve
beneficio sulle occlusioni Ambulanza, ma aumento dei falsi positivi; VDF resta
simile o leggermente migliore. Il compromesso non supera globalmente la v1.3.
Il feedback esteso e le cautele interpretative sono in
`../../../data/raw/v1.3_cp/README.md`.
