# Metadata immagini v1, v1.1, v1.2 e v1.3

Compila ogni riga dopo la freccia. È sufficiente una valutazione rapida; usa `UNKNOWN`, `MIXED` o `REVIEW` nei casi dubbi.

Formato consigliato:

```text
NOME_FILE -> FAR|MID|CLOSE|MIXED, DAY|NIGHT|DUSK|UNKNOWN, CLEAR|RAIN|FOG|SNOW|UNKNOWN, ON|OFF|UNKNOWN, FRONT|REAR|SIDE|OBLIQUE|MIXED|UNKNOWN, LOW|STREET|ELEVATED|TOP_DOWN|UNKNOWN, OK|BLUR|OCCLUDED|PARTIAL|UNKNOWN, S|M
```

Per le immagini negative:

```text
NOME_FILE -> NULL
```

La distanza è già calcolata automaticamente dall'area normalizzata delle bounding box:

- `FAR`: meno del 10% dell'immagine
- `MID`: dal 10% al 30%
- `CLOSE`: oltre il 30%
- `MIXED`: nell'immagine sono presenti bounding box appartenenti a fasce diverse

Legenda sintetica:

- distanza:         `FAR`, `MID`, `CLOSE`, `MIXED`
- luce:             `DAY`, `NIGHT`, `DUSK`, `UNKNOWN`
- meteo:            `CLEAR`, `RAIN`, `FOG`, `SNOW`, `UNKNOWN`
- lampeggianti:     `ON`, `OFF`, `UNKNOWN`
- angolazione:      `FRONT`, `REAR`, `SIDE`, `OBLIQUE`, `MIXED`, `UNKNOWN`
- altezza ripresa:  `LOW`, `STREET`, `ELEVATED`, `TOP_DOWN`, `UNKNOWN`
- visibilità:       `OK`, `BLUR`, `OCCLUDED`, `PARTIAL`, `UNKNOWN` (se coesistono, usa `+`)
- quantità:         `S` (single), `M` (multiple)
- dubbio: aggiungi  `REVIEW`

Note da rivedere (separate dai campi per mantenere uniforme il formato):

- `amb_old_series_008_view_002`: quantità `M` indicata come incerta.
- `car_video_006_frame_001`: presenti tre classi. Le tre bounding box sono tutte `FAR` secondo la soglia corrente; più classi non significa necessariamente distanza `MIXED`.

## TRAIN (319)

- `amb_diverso_001_png.rf.82b5a1d313d004a490f8e70271606c47.jpg` -> MID, DAY, CLEAR, ON, SIDE, STREET, OK, S
- `amb_diverso_002_png.rf.48e251b4029b617cba26e2584c861ede.jpg` -> FAR, DAY, CLEAR, ON, REAR, STREET, OK, S 
- `amb_diverso_003_png.rf.0579021afbd333bc66e09ab308d4f405.jpg` -> FAR, DAY, CLEAR, ON, MIXED, STREET, OK, S
- `amb_diverso_005_png.rf.d427587aa9a7874729662904e0ea7147.jpg` -> FAR, DAY, CLEAR, ON, REAR, STREET, OK, S
- `amb_old_series_001_view_001_jpeg.rf.fe0c43cce9ab8b8b5d04c1c6ab51970e.jpg` -> CLOSE, DAY, CLEAR, OFF, REAR, STREET, OK, S
- `amb_old_series_004_view_001_jpeg.rf.407b642fbb0b035da9deab2849cab7d7.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `amb_old_series_004_view_002_jpeg.rf.33a63566f4f786e4ce440a2a2a98b3a4.jpg` -> CLOSE, DAY, CLEAR, OFF, SIDE, STREET, OK, S
- `amb_old_series_005_view_001_jpeg.rf.adacf1ea6a5a481c0ee24d94b3e2e093.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `amb_old_series_005_view_002_jpeg.rf.adf6f74f612c0ad6044ba15eb41d40e6.jpg` -> MIXED, DAY, CLEAR, OFF, OBLIQUE, LOW, OK, M
- `amb_old_series_006_view_001_jpg.rf.2ea42b104510c538b4f0f247b308628e.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `amb_old_series_007_view_001_jpeg.rf.2d117b6dfa83c2233847d4e14e0e3bfe.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `amb_old_series_008_view_001_jpeg.rf.f87df391705c6691b0db699e79169e09.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `amb_old_series_008_view_002_jpeg.rf.94f343eae11e9ca1ceaef8537d5b3653.jpg` -> MIXED, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, M
- `amb_old_series_009_view_001_jpg.rf.5d742b37404b600adbe30209d9cc80e7.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `amb_old_series_009_view_002_jpg.rf.bcdcd29d5ad7a83ed8b2083222ca267d.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `amb_old_single_001_jpg.rf.ac9094d0f1cfada81ae75aa19039630b.jpg` -> MIXED, DAY, CLEAR, OFF, OBLIQUE, STREET, OCCLUDED, M
- `amb_old_single_002_jpeg.rf.9cc2445fce5a4bbd15f1920d9bb2425f.jpg` -> CLOSE, DAY, CLEAR, OFF, REAR, STREET, OK, S
- `amb_old_single_003_jpeg.rf.a4c26d95ecba2c15274f7284a6b6d167.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `amb_old_single_005_jpeg.rf.ce7952445b82c0970b524e6b656f44dc.jpg` -> MIXED, NIGHT, SNOW, ON, OBLIQUE, STREET, OK, M
- `amb_old_single_006_jpg.rf.b95afa58e8433e206e2df7cbdd911bd1.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `amb_old_video_001_frame_001_png.rf.e719ae13d26215e85e06de64759348de.jpg` -> CLOSE, DAY, CLEAR, UNKNOWN, MIXED, STREET, OCCLUDED, S
- `amb_old_video_001_frame_002_png.rf.a11b1b84bf7f648d689b3008d084e131.jpg` -> MID, DAY, CLEAR, ON, MIXED, STREET, OCCLUDED, S
- `amb_old_video_001_frame_003_png.rf.38aa1a5e50c8e0d9aa74be987ebd1b06.jpg` -> MID, DAY, CLEAR, OFF, MIXED, STREET, OK, S
- `amb_old_video_001_frame_004_png.rf.4607c6cecf413b783e1341971777c1a1.jpg` -> MID, DAY, CLEAR, OFF, MIXED, STREET, OCCLUDED, S
- `amb_old_video_001_frame_005_png.rf.d1e7b266378fae34ad18e0143aa74ebd.jpg` -> MID, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `amb_old_video_001_frame_006_png.rf.9564fbd00aa1b5418ee4e8b922255967.jpg` -> MIXED, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `amb_old_video_001_frame_007_png.rf.aab1c092fcfa9ea2ed63cac633c0ea4c.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `amb_old_video_001_frame_008_png.rf.91931d9312ebca4d602f4c4488ddd8f8.jpg` -> CLOSE, DAY, CLEAR, ON, OBLIQUE, STREET, OK, S
- `amb_old_video_001_frame_009_png.rf.910daa3e99e9114a9634d31a988db5c4.jpg` -> CLOSE, DAY, CLEAR, ON, SIDE, STREET, OK, S
- `amb_old_video_001_frame_010_png.rf.ab1a07758f28942f1c71fc5195f0cf50.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `amb_old_video_001_frame_011_png.rf.19869622939c6415001cd47dc5d76769.jpg` -> CLOSE, DAY, CLEAR, OFF, REAR, STREET, OCCLUDED, S
- `amb_old_video_001_frame_012_png.rf.d7af138c64e750e92b8a693eec227d00.jpg` -> CLOSE, DAY, CLEAR, OFF, REAR, STREET, OCCLUDED, S
- `amb_old_video_001_frame_013_png.rf.bc6ed02aa759700992edcdefa22ee9e5.jpg` -> CLOSE, DAY, CLEAR, OFF, MIXED, STREET, OK, S
- `amb_old_video_002_frame_001_png.rf.f363ab241b714c455d11a0bd34ad1405.jpg` -> CLOSE, DAY, CLEAR, ON, MIXED, STREET, OK, S
- `amb_old_video_002_frame_002_png.rf.3e4ed55036f45515283e776ed531279b.jpg` -> CLOSE, DAY, CLEAR, ON, MIXED, STREET, OK, S
- `amb_old_video_002_frame_003_png.rf.fb02a208c4b9262056aff971d1137204.jpg` -> CLOSE, DAY, CLEAR, OFF, MIXED, STREET, OK, S
- `amb_old_video_002_frame_004_png.rf.c674613bf764abf8ec84775be3154e34.jpg` -> CLOSE, DAY, CLEAR, OFF, REAR, STREET, OK, S
- `amb_old_video_003_frame_001_png.rf.5230103dadb29a198c01f5de40c95c33.jpg` -> CLOSE, DAY, CLEAR, ON, MIXED, STREET, OK, S
- `amb_old_video_003_frame_002_png.rf.01afd91961171b0570885cb85fab86da.jpg` -> CLOSE, DAY, CLEAR, ON, MIXED, STREET, OK, S
- `amb_video_002_frame_001_png.rf.844d7294992dad624937991000d40c41.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OK, S 
- `amb_video_002_frame_002_png.rf.8286ffb98210d13a804d69556006f23e.jpg` -> FAR, DAY, CLEAR, ON, MIXED, STREET, OK, S
- `amb_video_002_frame_003_png.rf.d047dc5e72d58a9d08da9d1078c4ba96.jpg` -> FAR, DAY, CLEAR, ON, REAR, STREET, OK, S
- `amb_video_003_frame_001_png.rf.58024ebb89f397ce568176e1491d3c6b.jpg` -> FAR, DAY, CLEAR, ON, MIXED, STREET, OK, S
- `amb_video_003_frame_002_png.rf.90742a386d7eb8bb3ec6437c8eb933d7.jpg` -> MID, DAY, CLEAR, ON, MIXED, STREET, OK, S
- `amb_video_004_frame_001_png.rf.800a3592ca09ba9421314535d8f93d62.jpg` -> FAR, NIGHT, CLEAR, ON, REAR, STREET, OK, S
- `amb_video_004_frame_002_png.rf.56e321b8f086e3d7957abf1a7ad35597.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, BLUR, S
- `amb_video_004_frame_003_png.rf.9ab472dbf45995d1772206a3bd5c18f0.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, BLUR, S
- `amb_video_004_frame_004_png.rf.a912f608b678ba624dcb46d1510e4d4a.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, BLUR, S
- `amb_video_004_frame_005_png.rf.ae7247ec36192e79b618df598eeb1d7b.jpg` -> MID, NIGHT, CLEAR, ON, SIDE, STREET, OK, S
- `amb_video_004_frame_006_png.rf.af2ffa6b7b763eb5755d5a6bbd826f8c.jpg` -> FAR, NIGHT, CLEAR, ON, OBLIQUE, STREET, OK, S
- `amb_video_004_frame_007_png.rf.215bd97938b314a4d5e71d8017b8a3bc.jpg` -> FAR, NIGHT, CLEAR, ON, REAR, STREET, OK, S
- `amb_video_005_frame_001_png.rf.dfe5c08c7b473af81cf417e5189a4293.jpg` -> FAR, DAY, CLEAR, OFF, REAR, STREET, OK, S
- `amb_video_005_frame_002_png.rf.143a643be99bb4e44dbd2a251cf2c08d.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `amb_video_007_frame_001_png.rf.11ba913c0946db6c5b451b6d96ff17eb.jpg` -> FAR, NIGHT, CLEAR, ON, REAR, STREET, OK, S
- `amb_video_007_frame_002_png.rf.34ba64635fddda8896cac49a610fb81b.jpg` -> FAR, NIGHT, CLEAR, ON, REAR, STREET, OK, S
- `amb_video_007_frame_003_png.rf.16a33a7750a8233cebfd9cde9e160493.jpg` -> CLOSE, NIGHT, CLEAR, ON, SIDE, STREET, BLUR, S
- `amb_video_008_frame_001_png.rf.67ca5e9a3a9dbd07fb9c5af38a9abf95.jpg` -> FAR, DAY, CLEAR, OFF, REAR, STREET, OK, S
- `amb_video_008_frame_002_png.rf.788b2eed183feb7b61f1f8bf8a21e2fd.jpg` -> MIXED, DAY, CLEAR, ON, FRONT, ELEVATED, BLUR, M
- `amb_video_008_frame_003_png.rf.67254b9cb1667e6fe80ceaea9f481cf5.jpg` -> FAR, DAY, CLEAR, ON, FRONT, ELEVATED, OK, S
- `amb_video_008_frame_004_png.rf.34f005fff346ea810f00ada796cba2ad.jpg` -> FAR, DAY, CLEAR, ON, FRONT, ELEVATED, OK, S
- `amb_video_008_frame_005_png.rf.af820fa936c70f29967d21aab6f58ea4.jpg` -> FAR, DAY, CLEAR, ON, REAR, LOW, OK, S
- `amb_video_011_frame_001_png.rf.e92b2cb51c050a048f86ccb17f6f5c66.jpg` -> MID, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `amb_video_011_frame_002_png.rf.d89e2f3856d2c7f633c1fe70f2f27ae8.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `amb_video_012_frame_001_png.rf.d70670ca868424f1fd218067765a46b9.jpg` -> FAR, DAY, CLEAR, ON, REAR, STREET, OK, M
- `amb_video_012_frame_002_png.rf.da1adf462433f703a3a1df6e449af23b.jpg` -> FAR, DAY, CLEAR, ON, MIXED, STREET, OK, M
- `amb_video_012_frame_003_png.rf.fd9d02990ed4c033a761b281e8a1ede2.jpg` -> MIXED, DAY, CLEAR, UNKNOWN, MIXED, STREET, OK, M
- `amb_video_012_frame_004_png.rf.3cf7548d44d45aa08e579fbb00e809b2.jpg` -> FAR, DAY, CLEAR, UNKNOWN, MIXED, STREET, OK, M
- `amb_video_013_frame_001_png.rf.95a2a813564c7e68e37e86e64e201cf1.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `amb_video_013_frame_002_png.rf.c5f6d09fd4b32e3401363b62a659e710.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OCCLUDED, S
- `amb_video_014_frame_001_png.rf.3abf63223d12efa84b59b82f4d255334.jpg` -> FAR, NIGHT, CLEAR, ON, REAR, STREET, OK, S
- `amb_video_014_frame_002_png.rf.22c9697713aabf018028bc162eefe3c1.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `amb_video_014_frame_003_png.rf.22da9766b18afd7e7bd89cff40c9265c.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `amb_video_016_frame_001_png.rf.51e62a5d3e1bea1e3816901c39333f68.jpg` -> MID, DAY, CLEAR, OFF, MIXED, ELEVATED, PARTIAL, S
- `amb_video_016_frame_002_png.rf.02d35bc284e5c324f280b9e94650a660.jpg` -> FAR, DAY, CLEAR, OFF, MIXED, ELEVATED, OK, S
- `amb_video_016_frame_003_png.rf.8012fa7434d25e832c90a5f89d7f5797.jpg` -> FAR, DAY, CLEAR, OFF, MIXED, ELEVATED, OK, S
- `amb_video_016_frame_004_png.rf.97203a44ad7bbc05a65c979f5c47b9ca.jpg` -> FAR, DAY, CLEAR, OFF, MIXED, ELEVATED, OK, S
- `amb_video_019_frame_001_png.rf.94e153ad83b40d864f404d18995ccb16.jpg` -> MID, DAY, CLEAR, ON, MIXED, STREET, OK, S
- `amb_video_019_frame_002_png.rf.1d8901b4d5f938b861c3e8d088473338.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `amb_video_019_frame_003_png.rf.255abdfc6890b1093c97b8587b3b7d26.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `amb_video_019_frame_004_png.rf.447614cb4beac626d233b9c4dd6b7a58.jpg` -> FAR, DAY, CLEAR, ON, MIXED, STREET, OK, S
- `amb_video_020_frame_001_png.rf.07fac40782503712855d9a756a4986da.jpg` -> CLOSE, DAY, CLEAR, ON, MIXED, TOP_DOWN, PARTIAL, S
- `amb_video_020_frame_002_png.rf.cfecf8ff848a3c8fbff27dd8be7b83bb.jpg` -> FAR, DAY, CLEAR, ON, FRONT, ELEVATED, OK, S
- `amb_video_020_frame_003_png.rf.4cd94796a221ebd2f3f4e2b4791a9fc8.jpg` -> FAR, DAY, CLEAR, ON, MIXED, ELEVATED, OK, S
- `amb_video_021_frame_001_png.rf.aa277b23488810e38fec9055f9f02cf1.jpg` -> FAR, DAY, CLEAR, ON, FRONT, ELEVATED, OK, M
- `amb_video_021_frame_002_png.rf.cf31c7ddeba0a33511a2e60e77d0802e.jpg` -> FAR, DAY, CLEAR, UNKNOWN, FRONT, ELEVATED, OK, M
- `amb_video_021_frame_003_png.rf.1fb4da6831ef99bc5e15b211d9a40c33.jpg` -> MID, DAY, CLEAR, UNKNOWN, FRONT, ELEVATED, OK, M
- `car_diverso_001_png.rf.d748470a0eb344d6acfd2dbbea65e889.jpg` -> MID, NIGHT, CLEAR, ON, SIDE, STREET, OK, S
- `car_diverso_002_png.rf.4b314d7c6e82f53e73c7b24b39e4ec74.jpg` -> MID, DAY, CLEAR, ON, REAR, STREET, OK, S
- `car_old_single_001_jpg.rf.1200ae2059997e08631fbf823db7143f.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `car_old_single_002_jpg.rf.68dd9cb20f886685e0e75b76dacf9e04.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `car_old_single_003_jpg.rf.0a5655fb055fcf99f1d6d89a56e28fd8.jpg` -> MID, NIGHT, CLEAR, ON, SIDE, STREET, OK, S
- `car_old_single_004_jpg.rf.2b1942925e44e4a09cdda0c7d00aee7a.jpg` -> CLOSE, DAY, CLEAR, OFF, SIDE, STREET, OK, S
- `car_old_single_005_jpg.rf.82008c8a8ba842d2e3f47c14963b44af.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `car_old_single_006_jpg.rf.9ee2ddb415056c6fb3db1600ffc35eca.jpg` -> CLOSE, DAY, CLEAR, OFF, SIDE, STREET, OK, S
- `car_old_single_008_jpg.rf.c55803840162b0f27c462be44ed2601b.jpg` -> CLOSE, DAY, CLEAR, ON, OBLIQUE, STREET, OK, S
- `car_old_single_010_jpg.rf.0ba0c1d7a7cf19ff43f4e8cc838e0ca4.jpg` -> CLOSE, DAY, CLEAR, ON, OBLIQUE, STREET, OK, S
- `car_old_single_012_jpg.rf.81b1d40580e78c8894f2fb8efb89683b.jpg` -> MIXED, NIGHT, CLEAR, ON, OBLIQUE, STREET, OK, M
- `car_old_single_015_jpg.rf.94c94b049bc39df53bc6920cca8c8d88.jpg` -> CLOSE, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `car_old_video_001_frame_003_png.rf.f671cdff8f8daad6c29b6cb3f5ec3362.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `car_old_video_001_frame_004_png.rf.70e0b35f8235b18bf3217f119daf30c3.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `car_old_video_001_frame_005_png.rf.b8997f9da9b9d89014910eaa7cb2f884.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `car_old_video_002_frame_001_png.rf.bcaf4b0098efb6be2de4b7d1b6287205.jpg` -> CLOSE, DAY, CLEAR, ON, REAR, STREET, OK, S
- `car_old_video_002_frame_002_png.rf.fb612973ef7b8f88a46b31a4493f8eba.jpg` -> CLOSE, DAY, CLEAR, ON, OBLIQUE, STREET, OK, S
- `car_old_video_002_frame_003_png.rf.bead93d8130a5ba52ba24864c77b9710.jpg` -> CLOSE, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `car_old_video_004_frame_001_png.rf.71e1916eb31f2175d0d6a9b23a76ece9.jpg` -> MID, DAY, CLEAR, ON, SIDE, STREET, OK, S
- `car_old_video_004_frame_002_png.rf.46da219ac350c031a36a98e1c87207ca.jpg` -> MID, DAY, CLEAR, ON, OBLIQUE, STREET, OK, S
- `car_old_video_004_frame_003_png.rf.97c04627404bcbc939bf745cc170f8ae.jpg` -> MID, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `car_old_video_004_frame_004_png.rf.866e0c30d98c67473cbbf86aac11b259.jpg` -> MID, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `car_old_video_004_frame_005_png.rf.c3520087e42bde320f8ceebba505b27e.jpg` -> MID, DAY, CLEAR, ON, OBLIQUE, STREET, OK, S
- `car_old_video_005_frame_001_png.rf.73cb79866bfbb929def5afaed29f2a27.jpg` -> CLOSE, DAY, CLEAR, ON, REAR, STREET, OK, S
- `car_old_video_005_frame_002_png.rf.7749934b695c0ed841ea4e865582247c.jpg` -> CLOSE, DAY, CLEAR, ON, SIDE, STREET, PARTIAL, S
- `car_old_video_005_frame_003_png.rf.3480cc410a5409154c64d5a008450e08.jpg` -> MID, DAY, CLEAR, OFF, MIXED, STREET, OK, S
- `car_old_video_006_frame_001_png.rf.22ab42f3d6fe6abd36383e4ed437680d.jpg` -> CLOSE, DAY, CLEAR, ON, MIXED, STREET, BLUR, S
- `car_old_video_006_frame_002_png.rf.0513979bc79d122bd1dc1648795508ca.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, BLUR, S
- `car_old_video_007_frame_001_png.rf.11433b17d08da508c7f657819a001948.jpg` -> CLOSE, DAY, CLEAR, OFF, REAR, STREET, PARTIAL, S
- `car_old_video_008_frame_001_png.rf.3be29f35fbc7ba06c6d90e72f4063dac.jpg` -> FAR, DUSK, CLEAR, OFF, MIXED, TOP_DOWN, PARTIAL, S
- `car_old_video_008_frame_002_png.rf.361f2c9c32d2ab566795471cda1ce2df.jpg` -> MID, DUSK, CLEAR, OFF, MIXED, TOP_DOWN, OK, S
- `car_old_video_009_frame_001_png.rf.3b06cce58f6595585d53d1cacf2674ee.jpg` -> CLOSE, DAY, CLEAR, OFF, MIXED, TOP_DOWN, OK, S
- `car_old_video_010_frame_001_png.rf.722f767cfa88e56c16047b45c00b8263.jpg` -> FAR, DUSK, CLEAR, OFF, MIXED, ELEVATED, OK, S
- `car_old_video_010_frame_002_png.rf.db4c4a5adae30132b0a05b5fd2fb246c.jpg` -> MID, DUSK, CLEAR, OFF, MIXED, ELEVATED, PARTIAL, S
- `car_old_video_010_frame_003_png.rf.e16709d9393f5de7359305870e3300aa.jpg` -> FAR, DUSK, CLEAR, OFF, MIXED, ELEVATED, OK, S
- `car_video_001_frame_001_png.rf.968ddd303b84b3245eec7adb1f0aa079.jpg` -> MIXED, DAY, CLEAR, ON, MIXED, STREET, OK, M
- `car_video_001_frame_002_png.rf.7e2e9994321fdb5ae1b61250d197d267.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OCCLUDED, S
- `car_video_001_frame_003_png.rf.8c69528396f69ffc7075bd9575422223.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `car_video_001_frame_004_png.rf.529d14ebd2b2c42419abd0894136e1a1.jpg` -> MIXED, DAY, CLEAR, ON, OBLIQUE, STREET, OK, M
- `car_video_001_frame_005_png.rf.4ba1937a1778f4b666191ed51232ac19.jpg` -> MIXED, DAY, CLEAR, ON, OBLIQUE, STREET, OK, M
- `car_video_001_frame_006_png.rf.a531c679de25f0fecc3ae9f4c8c3c5da.jpg` -> MID, DAY, CLEAR, ON, OBLIQUE, STREET, OK, S
- `car_video_003_frame_001_png.rf.bf8ad107262663f3b42d6512b990caf1.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `car_video_003_frame_002_png.rf.9d4e69d79318c2d3dde67f9b7b0ad7a0.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, BLUR, S
- `car_video_004_frame_001_png.rf.35571ed547334a6b5d8027debe5305d5.jpg` -> FAR, DAY, CLEAR, ON, REAR, STREET, OK, S
- `car_video_004_frame_002_png.rf.3b4c34e9cd875338dfbab0889dc4c52d.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `car_video_004_frame_003_png.rf.04af9a5aff455573fb6b4e3569ab2a41.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `car_video_004_frame_004_png.rf.d786267c9841b173d3fe2b8b04b71c3f.jpg` -> FAR, DAY, CLEAR, ON, MIXED, STREET, OK, S
- `car_video_004_frame_005_png.rf.855f3777e93ebf7ed2ed4d559909b178.jpg` -> FAR, DAY, CLEAR, ON, REAR, STREET, BLUR, S
- `car_video_004_frame_006_png.rf.f73cd579c498a82e2bdeb92cf99f6568.jpg` -> FAR, DAY, CLEAR, ON, REAR, STREET, OK, S
- `car_video_005_frame_001_png.rf.ef1f1b99fa62f5df1abe85cce724dc2a.jpg` -> FAR, NIGHT, CLEAR, ON, REAR, STREET, BLUR, S
- `car_video_005_frame_002_png.rf.6070408d3aecc96b6a234b28f85c8bbb.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, BLUR, S
- `car_video_005_frame_003_png.rf.07d2844560cc20fe9bbf1b08ecb5fdf2.jpg` -> MID, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `car_video_005_frame_004_png.rf.dd5d3af3365681f78f6bf3d6de29d38d.jpg` -> CLOSE, NIGHT, CLEAR, ON, SIDE, STREET, OK, S
- `car_video_005_frame_005_png.rf.6334f10d7b91ed43543e15f6e533adde.jpg` -> FAR, NIGHT, CLEAR, ON, OBLIQUE, STREET, BLUR, S
- `car_video_006_frame_001_png.rf.5790d1a09d2e13b08436490c5a661410.jpg` -> FAR, DAY, RAIN, OFF, REAR, STREET, OK, S
- `car_video_006_frame_002_png.rf.4cdb87725c6c7b9ca9221aa360d9fc46.jpg` -> FAR, DAY, RAIN, ON, SIDE, STREET, OCCLUDED, S
- `car_video_006_frame_003_png.rf.20f7aaf28776a646cd140c8b22167f4a.jpg` -> FAR, DAY, RAIN, ON, FRONT, STREET, OK, S
- `car_video_006_frame_004_png.rf.b5c5e457b303716067dcbb94ea227254.jpg` -> CLOSE, DAY, RAIN, ON, SIDE, STREET, OK, S
- `car_video_009_frame_001_png.rf.53494b1fd075c14295dffc2d9bb7b612.jpg` -> MID, DAY, CLEAR, OFF, SIDE, STREET, OK, S
- `car_video_009_frame_002_png.rf.9885ae630113aacc7ecb85d8e0a8c563.jpg` -> MID, DAY, CLEAR, ON, MIXED, STREET, OK, S
- `car_video_010_frame_001_png.rf.b4326ecfb9b29a354b6249300234088c.jpg` -> FAR, NIGHT, CLEAR, ON, MIXED, ELEVATED, BLUR, M
- `car_video_010_frame_002_png.rf.600b041490d58e9945828feb8741ba17.jpg` -> FAR, NIGHT, RAIN, ON, MIXED, ELEVATED, BLUR, S
- `car_video_010_frame_003_png.rf.139659a7f1ad8b92a4148a295c338ed3.jpg` -> MIXED, NIGHT, CLEAR, ON, SIDE, TOP_DOWN, OK, S
- `car_video_011_frame_001_png.rf.1be1d6f61e2c2e8ef7ce70282e3f984c.jpg` -> FAR, NIGHT, CLEAR, ON, MIXED, ELEVATED, BLUR, S
- `car_video_011_frame_002_png.rf.ecbd27ba4ef2f684957c754cf9a7059c.jpg` -> FAR, NIGHT, CLEAR, ON, REAR, ELEVATED, BLUR, S
- `car_video_012_frame_001_png.rf.d9b529b100d5161669ed6844923d5a2d.jpg` -> FAR, DAY, CLEAR, OFF, REAR, STREET, OK, S
- `car_video_012_frame_002_png.rf.71dcac06ed1b74f577553f1cbb8ef4e7.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, BLUR, S
- `car_video_012_frame_003_png.rf.ddb6f79f29bded1663ab3bf3e026ba25.jpg` -> FAR, DAY, CLEAR, ON, MIXED, STREET, OK, S
- `car_video_013_frame_001_png.rf.390d0f77d84509a2c36eff72bbe7cc10.jpg` -> FAR, DAY, CLEAR, ON, MIXED, STREET, OK, S
- `car_video_013_frame_002_png.rf.2d7d40ee03eac530194687e95c718f6b.jpg` -> CLOSE, DAY, CLEAR, OFF, SIDE, STREET, OK, S
- `car_video_014_frame_001_png.rf.cf1fc45808229fe315a0eebd1d4dbe93.jpg` -> MID, DAY, CLEAR, ON, MIXED, ELEVATED, PARTIAL, S
- `car_video_014_frame_002_png.rf.174657db447dd51d24ba376272df010a.jpg` -> FAR, DAY, CLEAR, ON, MIXED, ELEVATED, OK, S
- `neg_context_car_001_png.rf.cefb4f58d34bf03368d82abae04c8a68.jpg` -> NULL
- `neg_hard_amb_001_png.rf.82ddadfed553930e1c2be5d102705aa3.jpg` -> NULL
- `neg_hard_car_001_png.rf.e65fadda16067b9a5b396926fd755dd1.jpg` -> NULL
- `neg_hard_car_003_png.rf.c907f75c6b289b26a4f8476fd369019f.jpg` -> NULL
- `neg_hard_vdf_001_png.rf.971be468a4b820c9b9c17284451fe961.jpg` -> NULL
- `neg_hard_vdf_002_png.rf.b6d0a2ea9e17bc5d9ca12514831bb46c.jpg` -> NULL
- `neg_scene_001_jpg.rf.4fc1a1b2442e88407879a9d5f6764aab.jpg` -> NULL
- `neg_scene_002_jpg.rf.094867027b4b5d10ee5187f966fabfea.jpg` -> NULL
- `neg_scene_003_jpg.rf.1544638797bfda2758bbb29f8adf0c57.jpg` -> NULL
- `neg_scene_004_jpg.rf.043e7e8f3e1d52714a71831c40a80f5d.jpg` -> NULL
- `neg_scene_005_jpg.rf.d63e55f7f4ec7a557074489bd80a3e4d.jpg` -> NULL
- `neg_scene_006_jpg.rf.e12d18095c02a2c517c05eee1d7f0ebe.jpg` -> NULL
- `neg_scene_007_jpg.rf.4b2f6182bf54cc84f231839f2447f4ec.jpg` -> NULL
- `neg_scene_009_png.rf.6326e3fc5eca4a0fba8953b6e4ecbeb8.jpg` -> NULL
- `neg_scene_010_png.rf.477a09b2e5d567d56dc3341007da3866.jpg` -> NULL
- `neg_scene_011_png.rf.62a4a45ac33ee012191c093a3f9382c4.jpg` -> NULL
- `neg_scene_012_png.rf.7234c0cc339934b8ff41f9bd17c86642.jpg` -> NULL
- `neg_scene_013_png.rf.173407538484f6a25cde47d81c8cfe40.jpg` -> NULL
- `neg_scene_014_png.rf.6e9b8cff4d172030e07123457dcc30ef.jpg` -> NULL
- `neg_scene_017_png.rf.b74d1c25693bb5a950df82175ab88d5c.jpg` -> NULL
- `neg_scene_018_png.rf.6d53a981c044db9d690b3adc8bb2d9b0.jpg` -> NULL
- `neg_scene_019_png.rf.624956313f561c94fedd44f9b4619f33.jpg` -> NULL
- `neg_scene_020_png.rf.c371bb003db4d51faad8c491a08f2c80.jpg` -> NULL
- `neg_scene_021_png.rf.ebe63afaf7727b41d40fae9c9434d3e3.jpg` -> NULL
- `neg_scene_022_png.rf.528881bd059d99f05f64cb06ec5f8a3e.jpg` -> NULL
- `neg_scene_025_png.rf.c6d6e8fad09d416c5991eb2c6335f0dc.jpg` -> NULL
- `neg_scene_026_png.rf.018e9f7521555186983d55db1946d6f9.jpg` -> NULL
- `neg_scene_027_png.rf.16755b6d7c61c361e5c50b39d3991008.jpg` -> NULL
- `neg_scene_029_png.rf.826d9285bae4ec20ae4e891a10167978.jpg` -> NULL
- `neg_scene_031_png.rf.965867fe5b9c4eac5e515537b588935c.jpg` -> NULL
- `neg_scene_033_png.rf.adddf3cbce95fea4a1d4766c14936055.jpg` -> NULL
- `neg_scene_034_jpeg.rf.5b6868ba151cfc1e17ba01d41b673b65.jpg` -> NULL
- `neg_scene_036_jpeg.rf.66c4111ddd618a8fcaae16e1c0640575.jpg` -> NULL
- `vdf_diverso_001_png.rf.f91415b69fe5d5ee41369113c3a6e83e.jpg` -> FAR, NIGHT, CLEAR, ON, MIXED, TOP_DOWN, OK, M  
- `vdf_diverso_002_png.rf.509c8c183e614136cebb1868e2f5dc17.jpg` -> FAR, DAY, CLEAR, OFF, SIDE, LOW, OK, S
- `vdf_diverso_003_png.rf.55e963d813809300c5daed788b16765b.jpg` -> MID, DAY, CLEAR, ON, SIDE, STREET, OCCLUDED+OK, S
- `vdf_diverso_004_png.rf.09007b912c8de7dd01a3ea9e22d7b375.jpg` -> MID, DAY, CLEAR, ON, REAR, STREET, OCCLUDED+OK, S
- `vdf_diverso_005_png.rf.46a0bfdec9faf2dd393a52982d66a4b8.jpg` -> FAR, DAY, CLEAR, ON, REAR, STREET, OK, S
- `vdf_diverso_006_png.rf.200603783a54cec8fc0a3898b67345f9.jpg` -> MID, DAY, CLEAR, ON, FRONT, STREET, OCCLUDED, S
- `vdf_diverso_008_png.rf.cb8f22a74cbd16d5ee68142890f7e523.jpg` -> MID, DAY, CLEAR, ON, SIDE, STREET, OCCLUDED, S
- `vdf_diverso_009_png.rf.e7734f0c81bdffdcade7d1272fe17846.jpg` -> FAR, DAY, CLEAR, ON, FRONT, LOW, OK, M
- `vdf_diverso_010_png.rf.b84799964a8207fe03c097b94b39cbc5.jpg` -> FAR, DAY, CLEAR, ON, MIXED, STREET, OK, M
- `vdf_old_single_001_jpg.rf.58336207b65d490064e26a506f9882c2.jpg` -> MID, NIGHT, RAIN, ON, MIXED, STREET, OK, M
- `vdf_old_single_002_jpg.rf.6b0f7edbb98eac9233eb9df44db69096.jpg` -> CLOSE, DAY, CLEAR, OFF, MIXED, LOW, OK, S
- `vdf_old_single_004_png.rf.b8cf237cbaf75a579eb7c544997307f0.jpg` -> CLOSE, DAY, CLEAR, OFF, MIXED, TOP_DOWN, OK, S
- `vdf_old_single_007_jpg.rf.859de14e24529848cfd158a05e704b2d.jpg` -> MIXED, DAY, CLEAR, OFF, MIXED, STREET, OK, S
- `vdf_old_single_008_jpg.rf.0ef17f81bc4bff4a33ca144e02648dc7.jpg` -> CLOSE, DAY, CLEAR, OFF, MIXED, LOW, OK, S
- `vdf_old_single_010_jpg.rf.6a95d6a7df984c0766e6b2edc9287ae8.jpg` -> CLOSE, DAY, CLEAR, OFF, MIXED, STREET, PARTIAL, S
- `vdf_old_single_011_jpg.rf.4839c6248f36eacdc657da80b9a6d49e.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `vdf_old_single_012_jpg.rf.18daa96c2b9ebf774bff35c17008a09b.jpg` -> MID, DAY, CLEAR, ON, SIDE, STREET, OK, S
- `vdf_old_single_013_jpg.rf.fbdd95ff6619d5b51c8ef4502c433315.jpg` -> CLOSE, DAY, CLEAR, OFF, FRONT, STREET, OK, S
- `vdf_old_single_014_jpg.rf.1f6d44e871ff29c9152a6b10e5e3c4a0.jpg` -> CLOSE, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_old_single_015_jpg.rf.cbec18615753264faab708bf5eae7bd9.jpg` -> CLOSE, DAY, CLEAR, ON, OBLIQUE, STREET, OK, S
- `vdf_old_single_016_jpg.rf.c822202e22a9af5d5f41a87b1720e9c4.jpg` -> CLOSE, DAY, CLEAR, ON, OBLIQUE, STREET, OK, S
- `vdf_old_single_017_jpg.rf.78669c04ee8fa39d67713d469c7179bf.jpg` -> CLOSE, NIGHT, CLEAR, ON, OBLIQUE, STREET, OK, S
- `vdf_old_single_019_jpg.rf.e889ec2f76ee35342d156b481fc40b74.jpg` -> CLOSE, DAY, CLEAR, ON, OBLIQUE, STREET, OK, S
- `vdf_old_single_022_jpg.rf.4e050f853d8491c0bde5595a2431ba98.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `vdf_old_single_024_jpg.rf.9f7648e8caf13fca167096975a99b257.jpg` -> MID, DAY, CLEAR, ON, SIDE, STREET, OK, S
- `vdf_old_single_025_jpeg.rf.e2056ba808bf46a0318de9609cebeb50.jpg` -> CLOSE, DAY, CLEAR, UNKNOWN, MIXED, STREET, PARTIAL, S
- `vdf_old_single_027_jpg.rf.740c84979baf996cb204090ac02d23aa.jpg` -> CLOSE, DAY, CLEAR, OFF, SIDE, STREET, PARTIAL, S
- `vdf_old_single_028_jpg.rf.c5c8d667e60214368d7429d81f7f2357.jpg` -> CLOSE, DAY, CLEAR, ON, OBLIQUE, STREET, OK, S
- `vdf_old_single_029_jpg.rf.b9d1fe141843deaf733bab7dcf567de8.jpg` -> CLOSE, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_old_single_030_jpg.rf.5d1eefaf2c7f65c5d39ee7ea06af085d.jpg` -> CLOSE, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_old_single_031_jpg.rf.34ad9c1f719d8f51e78f24782b110608.jpg` -> CLOSE, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_old_single_032_jpg.rf.1a3aefca3fd317bb36df918321694217.jpg` -> CLOSE, DAY, CLEAR, OFF, MIXED, STREET, PARTIAL, S
- `vdf_old_single_033_jpg.rf.8546cd8c731c65010139b6b417e38afb.jpg` -> MIXED, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_old_single_034_jpg.rf.e59b2db002a552b2eca0d1ffd5cc7e46.jpg` -> MID, DUSK, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_old_single_035_jpg.rf.c7db2d095d71306db3f8c316d1efde23.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `vdf_old_single_036_jpg.rf.ed6d1b0a083add194811f6e557624fac.jpg` -> MID, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_old_single_037_jpg.rf.c42868eb9933a71eeafe95beec37a6fd.jpg` -> MID, DAY, RAIN, ON, OBLIQUE, STREET, OK, M
- `vdf_old_single_038_jpg.rf.a705cee54f3a505c7d165c0aed8c5d2a.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `vdf_old_single_039_jpg.rf.31d51bc2a38e0083c12540f21f2452e3.jpg` -> CLOSE, DAY, UNKNOWN, OFF, OBLIQUE, STREET, BLUR, S
- `vdf_old_single_040_jpg.rf.bea9fbc08e0a0036ccc0685c2e495dd7.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `vdf_old_single_041_jpg.rf.a1d3627f4770f52002913de8afdb87d3.jpg` -> CLOSE, DAY, CLEAR, ON, MIXED, ELEVATED, OK, S
- `vdf_old_single_042_jpg.rf.152b0f8245fb3c2f90bc725cc1182435.jpg` -> CLOSE, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_old_single_043_jpg.rf.9f8b457056814acb2a0f32a577d8bb2c.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `vdf_old_single_044_jpg.rf.2ea18596a6ff906316546da7183e169c.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, M
- `vdf_old_single_045_jpg.rf.347551ef72719a2980f6491aa3de3f73.jpg` -> CLOSE, DAY, CLEAR, ON, OBLIQUE, STREET, OK, S
- `vdf_old_single_046_jpg.rf.793cccb4bf99a3cf517b9a4fb6056d86.jpg` -> CLOSE, DAY, CLEAR, ON, OBLIQUE, STREET, OK, S
- `vdf_old_single_049_jpg.rf.615127214870019ee0f555991851a5a0.jpg` -> CLOSE, DAY, CLEAR, ON, OBLIQUE, STREET, OK, S
- `vdf_old_single_050_jpg.rf.631255723eb06264079a3729d202d302.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `vdf_old_single_051_jpg.rf.ef306f8182322b3f988e578a538b6417.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `vdf_old_single_052_jpg.rf.422c88dd053bdab9586cc6d18291fb1a.jpg` -> MID, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `vdf_old_single_053_jpg.rf.d84d257102f4f0a75e4f0a268da19cf7.jpg` -> CLOSE, DAY, CLEAR, ON, OBLIQUE, STREET, OK, S
- `vdf_old_single_056_jpeg.rf.68144ec55ce68ed12eafd665a4660214.jpg` -> CLOSE, DAY, CLEAR, OFF, REAR, STREET, OK, S
- `vdf_old_single_057_jpeg.rf.1f7d1df9aa1091ab8834aab1a47491e7.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OCCLUDED, S
- `vdf_old_single_058_png.rf.e72969c31459f8c4141c63aba1c10d76.jpg` -> FAR, DUSK, CLEAR, ON, REAR, STREET, OK, S
- `vdf_old_video_001_frame_001_png.rf.3941ecdad4797be2cf4991c771ae80c6.jpg` -> MID, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `vdf_old_video_001_frame_002_png.rf.105cffd1e2e710fa41db7ba7d541da37.jpg` -> FAR, DAY, CLEAR, OFF, FRONT, STREET, OK, M
- `vdf_old_video_001_frame_003_png.rf.635940570d54055fcc2d6bea83f256ef.jpg` -> FAR, DAY, CLEAR, OFF, FRONT, STREET, OK, M
- `vdf_old_video_001_frame_004_png.rf.6e99f2d86946f9dfa893358f9a06697c.jpg` -> FAR, DAY, CLEAR, OFF, FRONT, STREET, OK, M
- `vdf_old_video_002_frame_001_png.rf.2aeb5d4d8e2dce6d0156be72d326c7fa.jpg` -> MID, DAY, CLEAR, OFF, FRONT, STREET, OK, S
- `vdf_old_video_002_frame_002_png.rf.a3d18e4a6aa4a1f110c16bf1e5f65fe6.jpg` -> FAR, DAY, CLEAR, OFF, OBLIQUE, STREET, OCCLUDED, S
- `vdf_old_video_002_frame_003_png.rf.2329475ab4c75915ee88bc44ecc8eb55.jpg` -> FAR, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `vdf_old_video_003_frame_001_png.rf.626eac22b59800d5bbf4029d0491c49e.jpg` -> CLOSE, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_old_video_003_frame_002_png.rf.407d71cfe668c8c910e53aac8d4842e5.jpg` -> MID, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_old_video_003_frame_003_png.rf.30af004c07d5d9d4e585b70a14eb488c.jpg` -> CLOSE, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_old_video_005_frame_001_png.rf.428852ace1776bb862695f8327b1dd11.jpg` -> MID, DAY, CLEAR, OFF, SIDE, STREET, OK, S
- `vdf_old_video_005_frame_002_png.rf.3baaee7f3106f9f6e81f211212eb8c05.jpg` -> FAR, DAY, CLEAR, ON, OBLIQUE, STREET, OK, M
- `vdf_old_video_005_frame_003_png.rf.202b8e9f5cb2266ef38d29c393e32961.jpg` -> FAR, DAY, CLEAR, ON, OBLIQUE, STREET, OK, M
- `vdf_old_video_005_frame_004_png.rf.499cf887a2ce3f2b66724c0f98b4b51d.jpg` -> FAR, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `vdf_video_001_frame_001_png.rf.27d81a898e80cd195c2e4dd79807df9f.jpg` -> FAR, DAY, CLEAR, OFF, REAR, STREET, OK, S
- `vdf_video_001_frame_002_png.rf.d851d1527f2c93a0f58a97515f4022c5.jpg` -> FAR, DAY, CLEAR, OFF, FRONT, STREET, OK, S
- `vdf_video_001_frame_003_png.rf.ad51856dc7cd3a949b3dd20b7fc22aa6.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_video_001_frame_004_png.rf.150468ee7e1b02f1a64bb83e74532fb6.jpg` -> MID, DAY, CLEAR, ON, REAR, STREET, OK, S
- `vdf_video_001_frame_005_png.rf.1dd6efc29054a67cc4332bf9383bfc83.jpg` -> FAR, DAY, CLEAR, ON, REAR, STREET, OK, S
- `vdf_video_002_frame_001_png.rf.b45f05e803876dd53a682bf73128d740.jpg` -> FAR, DAY, CLEAR, OFF, MIXED, TOP_DOWN, OCCLUDED, M
- `vdf_video_002_frame_002_png.rf.c4cf65a649981e6947ec7d937e5e09c9.jpg` -> FAR, DAY, CLEAR, OFF, MIXED, TOP_DOWN, OK, S
- `vdf_video_002_frame_003_png.rf.3a61b9b9b4d6f15a0f52ac14edb6f670.jpg` -> FAR, DAY, CLEAR, ON, MIXED, TOP_DOWN, OK, M
- `vdf_video_002_frame_004_png.rf.ccaa97e5f6f5d831751d7b42041a4688.jpg` -> FAR, DAY, CLEAR, OFF, MIXED, TOP_DOWN, OCCLUDED, S
- `vdf_video_003_frame_001_png.rf.29443dbf78150d280614be232e4311c4.jpg` -> FAR, DAY, CLEAR, ON, REAR, STREET, OK, S
- `vdf_video_003_frame_002_png.rf.e91606e283cdcbf782b5e5ac099e0251.jpg` -> FAR, DAY, RAIN, ON, REAR, STREET, OK, S
- `vdf_video_004_frame_001_png.rf.800fb2ae0e67e9e6156351dcec9b629f.jpg` -> FAR, DAY, CLEAR, OFF, OBLIQUE, STREET, OCCLUDED, S
- `vdf_video_004_frame_002_png.rf.6cceb15b5ad6373a6a45b5d737bf798f.jpg` -> MID, DAY, CLEAR, OFF, OBLIQUE, STREET, OCCLUDED, S
- `vdf_video_005_frame_001_png.rf.dc8c190c23ad0503bef14c777d39cabd.jpg` -> MID, NIGHT, CLEAR, OFF, FRONT, STREET, OK, S
- `vdf_video_005_frame_002_png.rf.166b551365d6f39bc6bfa15417a76769.jpg` -> MID, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_video_005_frame_003_png.rf.7f9da6cb8b688dce604b57e47a66c115.jpg` -> MID, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_video_007_frame_001_png.rf.2282b9a042d9f307d5d52f5f6c9c2902.jpg` -> MID, DAY, CLEAR, ON, REAR, STREET, OK, S
- `vdf_video_007_frame_002_png.rf.76551e779f82dc01f32f17033b0834e9.jpg` -> MID, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_video_007_frame_003_png.rf.8589cbb8ffa76005fb6186158efffee2.jpg` -> MID, DAY, CLEAR, OFF, FRONT, STREET, OK, S
- `vdf_video_007_frame_004_png.rf.15bc409a2ecbaa245ce9759dab412fc4.jpg` -> FAR, DAY, CLEAR, OFF, REAR, STREET, OK, S
- `vdf_video_009_frame_001_png.rf.a0d00e4c18723005eae8395b6defc2e5.jpg` -> FAR, DAY, CLEAR, OFF, REAR, STREET, OK, S
- `vdf_video_009_frame_002_png.rf.87989312bff2c86a3efabad2cb2b0541.jpg` -> MID, DAY, FOG, ON, FRONT, STREET, OCCLUDED, S
- `vdf_video_010_frame_001_png.rf.0611cbd809aa4b7f7684edb4a1e258b6.jpg` -> CLOSE, NIGHT, CLEAR, ON, REAR, STREET, OCCLUDED, S
- `vdf_video_010_frame_002_png.rf.444683408fae824fb49b8cf25067ba06.jpg` -> FAR, NIGHT, CLEAR, ON, REAR, STREET, OK, S
- `vdf_video_011_frame_001_png.rf.727bb2fdf18b7a979dbebf346484409f.jpg` -> FAR, DAY, CLEAR, OFF, REAR, STREET, OK, S
- `vdf_video_011_frame_002_png.rf.ef2510205ae169b1533425d1e92d267f.jpg` -> FAR, DAY, CLEAR, ON, REAR, STREET, OK, S
- `vdf_video_012_frame_001_png.rf.69e2126f741ffa7b90b4d87ce14ddffa.jpg` -> FAR, DAY, CLEAR, OFF, REAR, STREET, OCCLUDED, S
- `vdf_video_012_frame_002_png.rf.3872e099db4001125c4a354b5abba4a8.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OCCLUDED, S
- `vdf_video_012_frame_003_png.rf.0b002d16d29b6ae3433a63789cc55f62.jpg` -> FAR, DAY, CLEAR, OFF, FRONT, STREET, OK, S
- `vdf_video_012_frame_004_png.rf.847a268b9ce47d2f3d54846dc1cef813.jpg` -> CLOSE, DAY, CLEAR, ON, SIDE, STREET, OK, S
- `vdf_video_014_frame_001_png.rf.8df6238e44d4e331383249a4d410fe66.jpg` -> MID, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_video_014_frame_002_png.rf.5b8aa74a7c3d2e6014970002fece50de.jpg` -> MID, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_video_015_frame_001_png.rf.2d1d67f839bbb997d87388326eb71d6c.jpg` -> FAR, DAY, CLEAR, OFF, REAR, STREET, OCCLUDED, S
- `vdf_video_015_frame_002_png.rf.05e66e710254eabbbf3471176ec5d806.jpg` -> MID, DAY, CLEAR, OFF, FRONT, STREET, OCCLUDED, S
- `vdf_video_015_frame_003_png.rf.04e02f1619368db401d3e4005e1923ad.jpg` -> MID, DAY, CLEAR, OFF, SIDE, STREET, OCCLUDED, S
- `vdf_video_018_frame_001_png.rf.6a616c63537b6d7c73265a4f6cf5582e.jpg` -> MIXED, DAY, CLEAR, ON, REAR, STREET, OCCLUDED, M
- `vdf_video_018_frame_002_png.rf.624f7f18e816076eb716abfd25641a4d.jpg` -> FAR, DAY, CLEAR, OFF, FRONT, STREET, OK, S
- `vdf_video_018_frame_003_png.rf.e0b9bff37eacd0f4086eae0434ca432a.jpg` -> MID, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `vdf_video_018_frame_004_png.rf.457245ebe9077efae200a13ab01c1a4b.jpg` -> MIXED, DAY, CLEAR, OFF, REAR, STREET, OK, M
- `vdf_video_021_frame_001_png.rf.3e5d9e80e78354126288c6c6eac22910.jpg` -> FAR, DAY, CLEAR, OFF, REAR, STREET, OK, M
- `vdf_video_021_frame_002_png.rf.e59e7c286369c6703354aa747a3af04b.jpg` -> FAR, DAY, CLEAR, OFF, FRONT, STREET, OK, M
- `vdf_video_022_frame_001_png.rf.425e309536724f24ddf6f458ed34a162.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_video_022_frame_002_png.rf.a09eb594db08a37927a9440b2fe21840.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, ELEVATED, OK, S
- `vdf_video_022_frame_003_png.rf.15a0556ddcc1123b6c84919034caefb9.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, OK, M
- `vdf_video_022_frame_004_png.rf.7a0fbf237a0de12ed88488d8c625a554.jpg` -> MID, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_video_022_frame_005_png.rf.87ffaaa6c1b3025653ee89660fc6ed3e.jpg` -> MIXED, NIGHT, FOG, ON, OBLIQUE, STREET, PARTIAL, S
- `vdf_video_023_frame_001_png.rf.5d0b593bfe08f10a9897e2561b367bd4.jpg` -> MID, DAY, CLEAR, OFF, OBLIQUE, STREET, OCCLUDED, S
- `vdf_video_023_frame_002_png.rf.b4112faac9271b0f4cc49f3ed8c7d98d.jpg` -> FAR, DAY, CLEAR, OFF, FRONT, STREET,OK, S
- `vdf_video_023_frame_003_png.rf.f4d90005736860f897e78a1997e2156f.jpg` -> FAR, DAY, CLEAR, OFF, FRONT, STREET, OK, S 
- `vdf_video_024_frame_001_png.rf.e4b46993e8207790a7fdaae947ac7dc9.jpg` -> MID, DAY, CLEAR, ON, REAR, STREET, OK, S
- `vdf_video_024_frame_002_png.rf.385a2e49e25a755b296f577e26f8b268.jpg` -> FAR, DAY, CLEAR, OFF, FRONT, STREET, OK, S
- `vdf_video_024_frame_003_png.rf.41c7a9934dc843eb8e6e3e7d86b989d9.jpg` -> MID, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `vdf_video_024_frame_004_png.rf.aae9c1a513900581bb2c0cffe20e7753.jpg` -> FAR, DUSK, CLEAR, OFF, REAR, STREET, OK, S
- `vdf_video_024_frame_005_png.rf.a2495e37936384529d2231a9c1a6edab.jpg` -> FAR, DUSK, CLEAR, OFF, FRONT, STREET, OK, S
- `vdf_video_024_frame_006_png.rf.26eacb758baef93ffb5cf473f14c11a4.jpg` -> FAR, DUSK, CLEAR, OFF, FRONT, STREET, OK, S
- `vdf_video_024_frame_007_png.rf.11f17f0e5c1979c86a73f13aa02c27d5.jpg` -> MID, DUSK, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `vdf_video_025_frame_001_png.rf.594c70c2ef87673280191c4c0a97d778.jpg` -> MID, DAY, CLEAR, OFF, REAR, STREET, OK, S
- `vdf_video_025_frame_002_png.rf.c7ac3cd38ac7885bec7d4339fd51478f.jpg` -> FAR, DAY, CLEAR, OFF, FRONT, STREET, OK, S
- `vdf_video_025_frame_003_png.rf.09537886f63074669087f657a4f01215.jpg` -> FAR, DAY, CLEAR, OFF, FRONT, STREET, OK, S
- `vdf_video_025_frame_004_png.rf.b8b149fcb8fe84403e93f033fa4fb757.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S

## VALID (64)

- `amb_old_series_002_view_001_jpeg.rf.09a057072fd082c1451dbe20c73f7e11.jpg` -> MIXED, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `amb_old_series_002_view_002_jpeg.rf.3ff8aea7917d94396e3bac8cc40ab1d8.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `amb_old_single_004_jpg.rf.ecd48df2e990eea1abf2c83446d32b61.jpg` -> MIXED, DAY, CLEAR, OFF, FRONT, STREET, OK, S
- `amb_video_006_frame_001_png.rf.d1fa72ce9b82e9e632f30df0edbafc95.jpg` -> FAR, DAY, CLEAR, ON, FRONT, ELEVATED, OK, S
- `amb_video_009_frame_001_png.rf.e2afa3a3e1d031b438760748f0365955.jpg` -> FAR, DAY, CLEAR, OFF, MIXED, STREET, OK, S
- `amb_video_009_frame_002_png.rf.9aaa5472b4db4ecf61f44cf8d4e4c76a.jpg` -> FAR, DAY, CLEAR, UNKNOWN, MIXED, STREET, OCCLUDED, S
- `amb_video_009_frame_003_png.rf.7eeab964991fc25273101b29e32d9c13.jpg` -> FAR, DAY, CLEAR, UNKNOWN, MIXED, STREET, OCCLUDED, S
- `amb_video_009_frame_004_png.rf.0ef70e8243f22426feae512bdec8ca8d.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `amb_video_010_frame_001_png.rf.5044230f3534107e8e4d57d8a55be187.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `amb_video_010_frame_002_png.rf.d530b8654eb029ecb9970706bd09ffc1.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `amb_video_015_frame_001_png.rf.2f9590078904cd43c373a6ea114f38b7.jpg` -> FAR, DAY, CLEAR, OFF, REAR, STREET, OK, S
- `amb_video_015_frame_002_png.rf.b03c44e267dc1c64d17bf081b0d2ffed.jpg` -> FAR, DAY, CLEAR, OFF, FRONT, STREET, OK, S
- `amb_video_015_frame_003_png.rf.ce4e8cffcf85e05d3eeeee65e79506c3.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `amb_video_015_frame_004_png.rf.391e16cffadf9681f8f806c7162f84f3.jpg` -> MID, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `amb_video_018_frame_001_png.rf.2a02d5c5cc733bcc8de8a67ef12f23dd.jpg` -> FAR, NIGHT, CLEAR, OFF, SIDE, STREET, OK, S
- `amb_video_018_frame_002_png.rf.f1c5f1b90e65505a9069c29cdf4543ef.jpg` -> FAR, NIGHT, CLEAR, ON, OBLIQUE, STREET, OK, S
- `amb_video_018_frame_003_png.rf.7b7f896de4435717d9f9a69e3d6475a1.jpg` -> FAR, NIGHT, CLEAR, ON, OBLIQUE, STREET, OK, S
- `car_old_single_014_jpg.rf.66761252805e6d9743174d73234c6831.jpg` -> MIXED, NIGHT, CLEAR, ON, SIDE, STREET, PARTIAL, S
- `car_old_video_003_frame_001_png.rf.c67ed4da3f1b5ea29e4fbc9b281f9c07.jpg` -> FAR, DAY, CLEAR, OFF, REAR, STREET, OK, M
- `car_old_video_003_frame_002_png.rf.a64d5b054bf53aec2058b0ee23e7e80f.jpg` -> MID, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `car_old_video_003_frame_003_png.rf.4781a95e462529dbbfd3b4b7d1ef93f4.jpg` -> MID, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `car_old_video_003_frame_004_png.rf.197cd8f56d35f6c0ead605343a3efaea.jpg` -> MID, DAY, CLEAR, ON, MIXED, STREET, OK, S
- `car_old_video_003_frame_006_png.rf.3911325dfb011774154a509f85cacbce.jpg` -> CLOSE, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `car_old_video_003_frame_007_png.rf.6fba624c1b9f8e6a47382d669f42da2e.jpg` -> MIXED, DAY, CLEAR, OFF, REAR, STREET, OK, S
- `car_old_video_003_frame_008_png.rf.f8d3b8992d740600d2b5096ffa2789ca.jpg` -> FAR, DAY, CLEAR, ON, REAR, STREET, OK, S
- `car_old_video_011_frame_001_png.rf.07606530d5248933875254eede366535.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OCCLUDED, S
- `car_video_002_frame_001_png.rf.cb26c42d176fe064196257200b414c35.jpg` -> FAR, NIGHT, FOG, ON, MIXED, TOP_DOWN, BLUR, S
- `car_video_002_frame_002_png.rf.d5a1902b3b2a25099bcd11a83b061b12.jpg` -> FAR, NIGHT, CLEAR, ON, MIXED, TOP_DOWN, OK, S
- `car_video_002_frame_003_png.rf.0010818cd787712a2287291cbf83e846.jpg` -> FAR, NIGHT, CLEAR, ON, SIDE, TOP_DOWN, OK, S
- `car_video_002_frame_004_png.rf.482b42b11699f99a519b470d8fb3c27f.jpg` -> FAR, NIGHT, CLEAR, ON, MIXED, TOP_DOWN, OK, S
- `car_video_002_frame_005_png.rf.d12d82d84e22b84482fc570977763463.jpg` -> FAR, NIGHT, CLEAR, OFF, MIXED, TOP_DOWN, OK, S
- `neg_hard_amb_002_png.rf.45e92fad5fc99f02d9678033fda146bd.jpg` -> NULL
- `neg_hard_car_002_png.rf.0c29a7a1ffae9c3b80216b01f2fdefc2.jpg` -> NULL
- `neg_scene_015_png.rf.f8536cb74649f7b38948fe17f19ec9cf.jpg` -> NULL
- `neg_scene_023_png.rf.3a33e2dbed1830d46d723279cffe326f.jpg` -> NULL
- `neg_scene_024_png.rf.019dd45e294cee609f0fac3b2b6dd9b5.jpg` -> NULL
- `neg_scene_028_png.rf.06707053878fcebc63dbd297a707689e.jpg` -> NULL
- `neg_scene_035_jpeg.rf.4e7fbfdf18f3a645e8d0e98c3fbb94b1.jpg` -> NULL
- `vdf_old_single_003_jpg.rf.4795f8c3cb4d6cae25224c3f49b838ca.jpg` -> CLOSE, NIGHT, CLEAR, ON, MIXED, STREET, OK, S
- `vdf_old_single_005_jpg.rf.cd7abba67dc31c70d27a5f7cb66509a2.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `vdf_old_single_006_jpeg.rf.db3171d4d0b3e75031f75428c7d14c46.jpg` -> MIXED, DAY, CLEAR, OFF, MIXED, TOP_DOWN, OK, S
- `vdf_old_single_018_jpg.rf.613abbb55103c0e4bac9026d545076bf.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `vdf_old_single_023_jpg.rf.7d175695be0def68bab0520a879da834.jpg` -> CLOSE, DAY, CLEAR, OFF, REAR, STREET, OK, S
- `vdf_old_single_026_jpg.rf.cae838a5c13bffa87321852fbd474312.jpg` -> CLOSE, DAY, CLEAR, ON, FRONT, ELEVATED, OK, S
- `vdf_old_single_047_jpg.rf.9d879cc6f9a5a4621e25557519805789.jpg` -> CLOSE, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_old_single_048_jpg.rf.f789bd8fcce89468ef845c13a2f753d5.jpg` -> CLOSE, DAY, CLEAR, ON, MIXED, ELEVATED, OK, S
- `vdf_old_single_055_jpeg.rf.1130761a66f4ed696bfc257eb3d53523.jpg` -> CLOSE, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_old_video_004_frame_001_png.rf.ecda5c3c59be58239b3f6cd9301fd6dd.jpg` -> FAR, DAY, CLEAR, OFF, FRONT, STREET, OK, S
- `vdf_old_video_004_frame_002_png.rf.cf0f1a49e2d54109b69770f78ea91bd9.jpg` -> FAR, DAY, CLEAR, OFF, FRONT, STREET, OK, S
- `vdf_video_013_frame_001_png.rf.4c83590c3018459aa1308faaa96804f5.jpg` -> MID, NIGHT, FOG, ON, REAR, STREET, OK, S
- `vdf_video_013_frame_002_png.rf.a28f22ad7064a7b61204a9c431168039.jpg` -> FAR, NIGHT, UNKNOWN, ON, FRONT, STREET, OK, S
- `vdf_video_013_frame_003_png.rf.40586640d31328813b465c9a6a2a3b25.jpg` -> FAR, NIGHT, FOG, ON, FRONT, STREET, OK, S
- `vdf_video_013_frame_004_png.rf.b00ddde7c7523cd04f5ec179c1b4e285.jpg` -> FAR, NIGHT, FOG, ON, FRONT, STREET, OK, S
- `vdf_video_013_frame_005_png.rf.7494e23185d428afc0e05d7fd7fd06c4.jpg` -> MID, NIGHT, CLEAR, ON, MIXED, STREET, OK, M
- `vdf_video_016_frame_001_png.rf.09ebc32a274836cfab081d50b125e608.jpg` -> FAR, DAY, RAIN, ON, REAR, STREET, BLUR, S
- `vdf_video_016_frame_002_png.rf.58db21cb1f2a82df147721a88db0282e.jpg` -> FAR, DAY, RAIN, ON, FRONT, STREET, OCCLUDED, S
- `vdf_video_016_frame_003_png.rf.c14b360bf609441a9ffd8491ad35fdf3.jpg` -> FAR, DAY, RAIN, ON, FRONT, STREET, OK, S
- `vdf_video_016_frame_004_png.rf.a31e224042d37c9f1dc6266254ca4a91.jpg` -> MID, DAY, RAIN, ON, FRONT, STREET, OK, S
- `vdf_video_017_frame_001_png.rf.b21961c49d4aa6afe69fb6e85b113127.jpg` -> FAR, DAY, CLEAR, ON, REAR, STREET, OK, S
- `vdf_video_017_frame_002_png.rf.34848a1c32e42bd3b705d3d702b08a82.jpg` -> FAR, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `vdf_video_017_frame_003_png.rf.e38e47e17ea3a9ed5261c59e86ed290b.jpg` -> FAR, DAY, CLEAR, UNKNOWN, FRONT, STREET, OK, M
- `vdf_video_017_frame_004_png.rf.40618f6b6fc7640bd4311f42593786fa.jpg` -> MID, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_video_020_frame_001_png.rf.196db43bf7a47735669d6abc2ab87536.jpg` -> MID, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_video_020_frame_002_png.rf.097c1e3f147cd0901f31866402c66b1e.jpg` -> FAR, DAY, CLEAR, OFF, FRONT, STREET, OK, S

## TEST (43)

- `amb_diverso_004_png.rf.f3d6b4703ab9d966763a709c910840d4.jpg` -> FAR, DAY, CLEAR, ON, REAR, STREET, OK, S
- `amb_old_series_003_view_001_jpeg.rf.17f0548c5388408ceab5ef1d9c9edd59.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `amb_old_series_003_view_002_jpeg.rf.cee3331d78c5020c56b97807187e4547.jpg` -> MIXED, DAY, CLEAR, OFF, SIDE, STREET, OK, S
- `amb_video_001_frame_001_png.rf.dbe30704a2c32aac8200fa82cc943986.jpg` -> MID, DAY, CLEAR, ON, SIDE, STREET, OK, S
- `amb_video_001_frame_002_png.rf.80dcff23d7b3c684f81b2c5ab0d444b5.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `amb_video_001_frame_003_png.rf.0172479e76f3fe382220c92890990397.jpg` -> MID, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `amb_video_001_frame_004_png.rf.b9b3938d44397592cc6883938fc4a594.jpg` -> MID, DAY, CLEAR, ON, REAR, STREET, OK, S
- `amb_video_017_frame_001_png.rf.ee37a67936c9b09f21824023870c5504.jpg` -> MID, DAY, CLEAR, OFF, MIXED, TOP_DOWN, OK, S
- `amb_video_017_frame_002_png.rf.38dfad3eab54c8e760bad5b7ebad1cde.jpg` -> MID, DAY, CLEAR, OFF, MIXED, TOP_DOWN, PARTIAL, S
- `amb_video_017_frame_003_png.rf.422bac2adbfd13b59d6d4837c8c38429.jpg` -> CLOSE, DAY, CLEAR, OFF, MIXED, TOP_DOWN, OCCLUDED, S
- `amb_video_017_frame_004_png.rf.6debd6cbc29380d31b520cd3e4465c78.jpg` -> CLOSE, DAY, CLEAR, OFF, MIXED, TOP_DOWN, PARTIAL, S
- `amb_video_017_frame_005_png.rf.7d2d9268b4f0be192ccc044f508811e1.jpg` -> CLOSE, DAY, CLEAR, OFF, MIXED, TOP_DOWN, PARTIAL, S
- `car_diverso_003_png.rf.720e9c525febbb021008e273e9571c61.jpg` -> MID, DAY, CLEAR, OFF, SIDE, STREET, OK, S 
- `car_old_single_007_jpeg.rf.1374974ea718a1f8c88fcd5c571ce2f8.jpg` -> CLOSE, DAY, CLEAR, OFF, MIXED, STREET, OK, S
- `car_old_single_009_jpg.rf.d572af2cb546505abd87fe7df1448d59.jpg` -> CLOSE, DAY, CLEAR, OFF, SIDE, STREET, OK, S
- `car_old_single_011_jpg.rf.6fc63901c2ed216ed032a6b2a008f907.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `car_old_single_013_jpg.rf.be8121ac00372d91e5e647b6467f3b16.jpg` -> MID, NIGHT, CLEAR, ON, SIDE, STREET, OK, S
- `car_video_007_frame_001_png.rf.96225317220ccf060a30b360e74272d6.jpg` -> FAR, NIGHT, UNKNOWN, ON, UNKNOWN, ELEVATED, BLUR, S
- `car_video_007_frame_002_png.rf.4eeed1d4187b7f55c9daaedd30d1fa1e.jpg` -> FAR, NIGHT, UNKNOWN, ON, UNKNOWN, ELEVATED, BLUR, S
- `car_video_007_frame_003_png.rf.ec3d2e8019755c8195066f3d43d47db5.jpg` -> MID, NIGHT, UNKNOWN, ON, UNKNOWN, ELEVATED, BLUR, S
- `car_video_008_frame_001_png.rf.3374debdae80227a4b66d67452c0e1aa.jpg` -> FAR, NIGHT, UNKNOWN, ON, UNKNOWN, ELEVATED, BLUR, S
- `car_video_008_frame_002_png.rf.5a014b37c08b7ea92ecf163af8148f7c.jpg` -> FAR, NIGHT, UNKNOWN, ON, UNKNOWN, ELEVATED, BLUR, S
- `neg_scene_008_png.rf.4eb0e6b2577446bc4e0a1a9ca9805168.jpg` -> NULL
- `neg_scene_016_png.rf.eb264dd00d91020a24b2f5377525c81d.jpg` -> NULL
- `neg_scene_030_png.rf.0d9ed47b968370d78da1fddb2250f6cf.jpg` -> NULL
- `neg_scene_032_png.rf.173ac97e80ff7f44ee85ed9924bd6c8c.jpg` -> NULL
- `vdf_diverso_007_png.rf.e5842196291bb5b24e021cf366bd0792.jpg` -> MID, DAY, CLEAR, OFF, FRONT, STREET, OCCLUDED, S
- `vdf_old_single_009_jpg.rf.87c5756047bad7aced47de8e21cb299e.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `vdf_old_single_020_jpg.rf.8dd6c15af82ceef2b1af540e8d58cd4b.jpg` -> CLOSE, DAY, CLEAR, OFF, SIDE, STREET, OK, S
- `vdf_old_single_021_jpg.rf.122f3c666fd0901e45c4e1cd0538cb0b.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `vdf_old_single_054_jpeg.rf.af3637c777688a5a84d8763b0d39024d.jpg` -> CLOSE, DAY, CLEAR, OFF, FRONT, STREET, OK, S
- `vdf_video_006_frame_001_png.rf.c5991057f8ca1d74bd68e7ae9f8f1ab0.jpg` -> MID, DAY, CLEAR, ON, REAR, STREET, OK, S
- `vdf_video_006_frame_002_png.rf.ff3d03bd65cbb23dbfb21d63449e2e2e.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_video_006_frame_003_png.rf.5edcb6419bbf1c3b30d5446ef7bdb1d7.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_video_006_frame_004_png.rf.2172ad4abbfaa66d948d94b81295ec3e.jpg` -> MID, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_video_006_frame_005_png.rf.583927f85206c5137eb2febba46b11c0.jpg` -> CLOSE, DAY, CLEAR, ON, REAR, STREET, BLUR, S
- `vdf_video_008_frame_001_png.rf.8e2d33f6d04c7e47089344dc8777ebba.jpg` -> MIXED, NIGHT, CLEAR, ON, OBLIQUE, STREET, OK, S
- `vdf_video_008_frame_002_png.rf.6ac72c651668f48c95c223c53e19a06d.jpg` -> CLOSE, NIGHT, CLEAR, ON, SIDE, STREET, OCCLUDED, S
- `vdf_video_008_frame_003_png.rf.ec17b8d25c6c57e50f997bf64b0df6eb.jpg` -> MID, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_video_008_frame_004_png.rf.2bfd22266a7ddd2b94f695190bc596a2.jpg` -> MID, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `vdf_video_008_frame_005_png.rf.854ae5d35e682699b1e84d26bc83618d.jpg` -> FAR, NIGHT, CLEAR, ON, MIXED, STREET, OK, S
- `vdf_video_019_frame_001_png.rf.9225eff6f82f299b286f4f511e625fc9.jpg` -> FAR, DAY, CLEAR, ON, REAR, STREET, OK, S
- `vdf_video_019_frame_002_png.rf.5f3224d193c95e15f49f6b7edfbeb58c.jpg` -> FAR, DAY, CLEAR, OFF, FRONT, STREET, OK, S

<!-- INIZIO AGGIUNTE v1.1: solo immagini non presenti nel dataset v1 -->
## Aggiunte v1.1 (91)

Queste righe provengono dal manifest v1.1: 79 positive e 12 negative. Distanza e `S/M` sono calcolati dalle label YOLO; luce, meteo e altezza derivano da `data/raw/v1.1/batches/2026-09-13/fonti.txt` a livello di video, quindi vanno corretti se un singolo frame fa eccezione. Nessuna immagine e' stata aperta per compilare questi campi. `UNKNOWN` indica un dato non documentato, non un difetto dell'immagine.

- `v11_amb_video_004`: altezza descritta come TOP_DOWN/ELEVATED; resta `UNKNOWN` finche' non scegli la categoria del singolo frame.
- `v11_car_video_007`: altezza descritta come LOW/STREET; resta `UNKNOWN` finche' non scegli la categoria del singolo frame.
- `v11_car_source_unknown_video_001`: due frame della stessa fonte con link perso; condizioni non documentate.
- `car_old_video_001_frame_001`: Portrait parziale da `v1/images/Annotate/Carabinieri`; `PARTIAL` segue la descrizione dell'utente, gli altri contesti non sono documentati.
- I 12 `v11_null_*` sono `NULL`; i due reject non figurano nello split e quindi non sono elencati qui.

### Nuove in TRAIN (78)

- `car_old_video_001_frame_001_png.rf.6c6711103b6b0f3a034a5f22f722b02a.jpg` -> CLOSE, DAY, CLEAR, OFF, SIDE, STREET, PARTIAL, S
- `v11_amb_video_001_frame_001_png.rf.1c7a661cce52c1906456eebe5402e0ae.jpg` -> FAR, NIGHT, CLEAR, ON, REAR, STREET, BLUR, S
- `v11_amb_video_001_frame_002_png.rf.0eb573320b0d51ca0f72a0f8033b9171.jpg` -> FAR, NIGHT, CLEAR, ON, MIXED, STREET, OCCLUDED, S
- `v11_amb_video_001_frame_003_png.rf.694e1f2cca9acc3ff23db8cc63c8cb3d.jpg` -> FAR, NIGHT, CLEAR, ON, OBLIQUE, STREET, OK, S
- `v11_amb_video_001_frame_004_png.rf.195a774e1610d140d5e102865f7621e7.jpg` -> FAR, NIGHT, CLEAR, ON, MIXED, STREET, OK, S
- `v11_amb_video_001_frame_005_png.rf.89dff8ac1308dd0ce44a693a1309a6b3.jpg` -> MID, NIGHT, CLEAR, ON, SIDE, STREET, OK, S
- `v11_amb_video_001_frame_006_png.rf.65ce5e861a9a8b370efa51dbefb418f1.jpg` -> MID, NIGHT, CLEAR, ON, SIDE, STREET, OCCLUDED, S
- `v11_amb_video_001_frame_007_png.rf.fc9a38c6d2b15aff977b9a40f5c22ecb.jpg` -> FAR, NIGHT, CLEAR, OFF, OBLIQUE, STREET, OK, S
- `v11_amb_video_002_frame_001_png.rf.7f6a5005e62ac4d93a669cb5a022cfce.jpg` -> CLOSE, NIGHT, CLEAR, ON, SIDE, STREET, PARTIAL, S
- `v11_amb_video_002_frame_002_png.rf.719f9d34ce1e7bcf303ea78b48e21613.jpg` -> FAR, NIGHT, CLEAR, ON, REAR, STREET, OK, S
- `v11_amb_video_002_frame_003_png.rf.2d37cb49cb5e69834b326713bdad1d65.jpg` -> FAR, NIGHT, CLEAR, ON, OBLIQUE, STREET, BLUR, S
- `v11_amb_video_004_frame_001_png.rf.dc104b91a215c6ebd3fbaa7bce7ed57f.jpg` -> MID, NIGHT, CLEAR, OFF, REAR, ELEVATED, OK, S
- `v11_amb_video_004_frame_002_png.rf.c9ac9f46ee2cb4e14b3ad7361cb3f713.jpg` -> MID, NIGHT, CLEAR, ON, MIXED, ELEVATED, PARTIAL, S
- `v11_amb_video_004_frame_003_png.rf.d79c4aaf9629c4ce4e5a3170393e210a.jpg` -> MID, NIGHT, CLEAR, ON, FRONT, ELEVATED, OK, S
- `v11_amb_video_004_frame_004_png.rf.4cb3aa1adeab20d8eba8fb393426d484.jpg` -> CLOSE, NIGHT, CLEAR, ON, MIXED, TOP_DOWN, PARTIAL, S
- `v11_amb_video_005_frame_001_png.rf.7061cea7c0595bf22a012f6058c06020.jpg` -> MID, NIGHT, CLEAR, ON, SIDE, STREET, OK, S
- `v11_amb_video_005_frame_002_png.rf.bc54e0d0e9be49922769ffef136b9856.jpg` -> FAR, NIGHT, CLEAR, ON, OBLIQUE, STREET, OK, S
- `v11_amb_video_005_frame_003_png.rf.7bdf293946bba57882a29dbde5833fd5.jpg` -> FAR, NIGHT, CLEAR, ON, OBLIQUE, STREET, OCCLUDED, S
- `v11_amb_video_005_frame_004_png.rf.c112f5292c114666a04133b3a663ce6b.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, BLUR, S
- `v11_amb_video_006_frame_001_png.rf.ac31791a3cace787469e17e01c76062e.jpg` -> FAR, DAY, CLEAR, OFF, SIDE, TOP_DOWN, OCCLUDED, S
- `v11_amb_video_006_frame_002_png.rf.235d6bf2d9b166b327e14898662ea9fe.jpg` -> FAR, DAY, CLEAR, ON, SIDE, TOP_DOWN, OK, S
- `v11_amb_video_006_frame_003_png.rf.b432543e3d1f67a3586224cfd68ae435.jpg` -> FAR, DAY, CLEAR, OFF, SIDE, TOP_DOWN, OCCLUDED, S
- `v11_amb_video_007_frame_001_png.rf.2fb7c0c3c189171a009e66bc12534f4d.jpg` -> MID, DAY, CLEAR, ON, REAR, STREET, OK, S
- `v11_amb_video_007_frame_002_png.rf.bef19e1db5b2ceab8927952cf7f71181.jpg` -> FAR, DAY, CLEAR, OFF, FRONT, STREET, OCCLUDED, S
- `v11_amb_video_007_frame_003_png.rf.9339898fdd74b2c80b3e196d44ee6399.jpg` -> MID, DAY, CLEAR, OFF, SIDE, STREET, OCCLUDED, S
- `v11_amb_video_007_frame_004_png.rf.e3b8c06b273b40ba0e8a035befe52c87.jpg` -> FAR, DAY, CLEAR, ON, REAR, STREET, OK, S
- `v11_amb_video_008_frame_001_png.rf.8be62089a5370d6542e09ae12353ae09.jpg` -> MID, DAY, CLEAR, OFF, SIDE, STREET, PARTIAL, S
- `v11_amb_video_008_frame_002_png.rf.7370da3829f42bc8f49510f767ec7ce3.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `v11_car_source_unknown_video_001_frame_001_png.rf.ea5e161c54efa2a8d7e99a459e3295ae.jpg` -> FAR, NIGHT, CLEAR, ON, REAR, STREET, BLUR, S
- `v11_car_source_unknown_video_001_frame_002_png.rf.4a6a9fba33d21f1a8b03dcebc7ad94f8.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, BLUR, S
- `v11_car_video_001_frame_001_png.rf.8652c50de356a9c526842ca8c4d49f92.jpg` -> FAR, DAY, CLEAR, OFF, MIXED, TOP_DOWN, OK, S
- `v11_car_video_001_frame_002_png.rf.a4a62268e08c9bb94b365e29ac7090ce.jpg` -> FAR, DAY, CLEAR, OFF, FRONT, TOP_DOWN, OK, S
- `v11_car_video_001_frame_003_png.rf.41541e8777fff43b354739ef297c1359.jpg` -> FAR, DAY, CLEAR, OFF, OBLIQUE, TOP_DOWN, OK, S
- `v11_car_video_001_frame_004_png.rf.cd6a9ab0be0988e942a43aade4d26f73.jpg` -> FAR, DAY, CLEAR, OFF, SIDE, TOP_DOWN, OK, S
- `v11_car_video_001_frame_005_png.rf.3883358a4b93a93fcc09242878702ecd.jpg` -> FAR, DAY, CLEAR, OFF, OBLIQUE, TOP_DOWN, OK, S
- `v11_car_video_002_frame_001_png.rf.191224ebcaaf16c76862c583f2e968ff.jpg` -> FAR, DAY, CLEAR, UNKNOWN, SIDE, STREET, OCCLUDED, S
- `v11_car_video_002_frame_002_png.rf.5a4f41cd22c08c5ba3e30d0b1eb31967.jpg` -> FAR, DAY, CLEAR, ON, SIDE, STREET, OCCLUDED, S
- `v11_car_video_002_frame_003_png.rf.4ef3d5ced9f6616222a62b4fe50b6571.jpg` -> FAR, DAY, CLEAR, OFF, SIDE, STREET, OK, S
- `v11_car_video_003_frame_001_png.rf.0a0e6a97099a89691a8758f29de6a584.jpg` -> FAR, DAY, CLEAR, ON, OBLIQUE, STREET, BLUR, S
- `v11_car_video_003_frame_002_png.rf.b966196eafa1100bf51328ef568988ef.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `v11_car_video_005_frame_001_png.rf.a3d9ff418680f0943ed8c7fc89e28418.jpg` -> FAR, NIGHT, CLEAR, ON, SIDE, ELEVATED, OCCLUDED, S
- `v11_car_video_006_frame_001_png.rf.cfb3e2dad21cc3789ce6acbeb7a13d66.jpg` -> CLOSE, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `v11_car_video_007_frame_001_png.rf.85f867ac59da3004059a6dd19fb80314.jpg` -> MID, NIGHT, CLEAR, OFF, REAR, STREET, OCCLUDED, S
- `v11_car_video_007_frame_002_png.rf.c9bdf8acb0ab92154a0ac69c9df4ca65.jpg` -> FAR, NIGHT, CLEAR, ON, REAR, LOW, BLUR, S
- `v11_car_video_007_frame_003_png.rf.4212fdebbce2f2fe2a6ee989efe86c57.jpg` -> MID, NIGHT, CLEAR, OFF, REAR, STREET, OK, S
- `v11_car_video_008_frame_001_png.rf.d54aaa7fb6dd329bd0598ed33c49259c.jpg` -> MID, NIGHT, CLEAR, ON, SIDE, STREET, OK, S
- `v11_car_video_008_frame_002_png.rf.29cfcad7f0c37e8a9cb70b6065e1df1f.jpg` -> FAR, NIGHT, CLEAR, ON, OBLIQUE, STREET, OK, S
- `v11_car_video_008_frame_003_png.rf.04a40e2419aca5ad1ca46f82a578a6f2.jpg` -> MID, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `v11_car_video_009_frame_002_png.rf.0f3bbd8ec20eb50c71d75b03eb7c2b0f.jpg` -> MID, NIGHT, CLEAR, OFF, REAR, STREET, OK, S
- `v11_car_video_010_frame_001_png.rf.25f264f73df383690b65993948040cca.jpg` -> MID, NIGHT, CLEAR, ON, MIXED, STREET, PARTIAL, S
- `v11_car_video_012_frame_001_png.rf.fb454b41486ebea219d1cfb404a39832.jpg` -> MID, DAY, CLEAR, ON, REAR, STREET, OCCLUDED, S
- `v11_car_video_012_frame_002_png.rf.33471ae24a0d76a4d2456918464bd083.jpg` -> MID, DAY, CLEAR, ON, SIDE, STREET, OCCLUDED, S
- `v11_car_video_012_frame_003_png.rf.a2a67c9c99cb9171fdcf55e4a87ecd23.jpg` -> MID, DAY, CLEAR, ON, MIXED, STREET, OK, S
- `v11_car_video_012_frame_004_png.rf.01568aaae855b32b560dbde17238e783.jpg` -> FAR, DAY, CLEAR, ON, REAR, STREET, OK, S
- `v11_car_video_012_frame_005_png.rf.f1533cba212cc22ccfd7f32fa6b6921d.jpg` -> MID, DAY, CLEAR, ON, REAR, STREET, OK, S
- `v11_null_001_png.rf.7308f8f02d6102260d5cdc024047053f.jpg` -> NULL
- `v11_null_002_png.rf.33b2a6a0715ca7ca86dcf136f870994d.jpg` -> NULL
- `v11_null_003_png.rf.f6b3b5b8e87bef0e4ad83013bf6d951c.jpg` -> NULL
- `v11_null_004_png.rf.d5aa69f026f0aa9de712c9345e8351a2.jpg` -> NULL
- `v11_null_005_png.rf.7a567f5feb1eddde5e9a40574622ed27.jpg` -> NULL
- `v11_null_006_png.rf.c325e7385a707d00a981bfc09c7bbea6.jpg` -> NULL
- `v11_null_007_png.rf.2bb933976fffb75eebdbcde55db8afcc.jpg` -> NULL
- `v11_null_008_png.rf.fc734bdd08816baba0c65a6927953ed8.jpg` -> NULL
- `v11_null_009_png.rf.9e9eeb8d13f640b77bd9dff39e64429f.jpg` -> NULL
- `v11_null_010_png.rf.134fe5c8bd69a900e819eed3c55a061d.jpg` -> NULL
- `v11_null_011_png.rf.1dbbc823599eac94f6d0082224d1f2e4.jpg` -> NULL
- `v11_null_012_png.rf.b697bd838df8644e603a0a30da5eb58c.jpg` -> NULL
- `v11_vdf_video_001_frame_001_png.rf.ad57a68d83da818461ffd895333b9029.jpg` -> FAR, NIGHT, CLEAR, ON, OBLIQUE, STREET, OK, S
- `v11_vdf_video_001_frame_002_png.rf.509d6c8d6bd7d6f271b02f75068d6bdd.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, OCCLUDED, S
- `v11_vdf_video_001_frame_003_png.rf.72b267dcac707ba93c70b7bf508a4168.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `v11_vdf_video_001_frame_004_png.rf.711421b33b332cdcae32af46ac11443a.jpg` -> MID, NIGHT, CLEAR, ON, OBLIQUE, STREET, OK, S
- `v11_vdf_video_001_frame_005_png.rf.a91d1409b0abb53ca4a3f3c76e8160e6.jpg` -> FAR, NIGHT, CLEAR, ON, OBLIQUE, STREET, OK, S
- `v11_vdf_video_001_frame_006_png.rf.2712c981fb23975a2a2718173dae535a.jpg` -> FAR, NIGHT, CLEAR, ON, SIDE, STREET, OK, S
- `v11_vdf_video_003_frame_001_png.rf.f99361795b54d65fb00d7d169a60d68c.jpg` -> FAR, DAY, CLEAR, OFF, SIDE, STREET, OK, S
- `v11_vdf_video_003_frame_002_png.rf.e9ed2187b58f9691eced261a4138a19e.jpg` -> MID, DAY, CLEAR, OFF, SIDE, STREET, OK, S
- `v11_vdf_video_003_frame_003_png.rf.c6a1a7a0de1564af0a9403de03dcd57d.jpg` -> MID, DAY, CLEAR, OFF, SIDE, STREET, OK, S
- `v11_vdf_video_003_frame_004_png.rf.020c1fc47f7ea6d01acdb1ddb5cfc9d4.jpg` -> MID, DAY, CLEAR, OFF, REAR, STREET, OCCLUDED, S
- `v11_vdf_video_003_frame_005_png.rf.1c19da9994fb8722815f5b583bf5aa2f.jpg` -> FAR, DAY, CLEAR, OFF, SIDE, STREET, OK, S

### Nuove in VALID (13)

- `v11_amb_video_003_frame_001_png.rf.20dc450a0e6fb1e937a8eadd9ee51e7d.jpg` -> FAR, NIGHT, CLEAR, ON, SIDE, STREET, OCCLUDED, S
- `v11_amb_video_003_frame_002_png.rf.bf734a3c38f0d9bd348e1d29e412c183.jpg` -> FAR, NIGHT, CLEAR, ON, OBLIQUE, STREET, OK, S
- `v11_amb_video_003_frame_003_png.rf.0b4819d2348b4b230055af0441ae6e09.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `v11_amb_video_003_frame_004_png.rf.8d2f25f3c2e328d37c989f54db56136e.jpg` -> CLOSE, NIGHT, CLEAR, ON, SIDE, STREET, PARTIAL, S
- `v11_amb_video_003_frame_005_png.rf.f93a3b02d09897c5b3774135e9e26588.jpg` -> FAR, NIGHT, CLEAR, ON, REAR, STREET, OCCLUDED, S
- `v11_car_video_004_frame_001_png.rf.4115d6f27483c7e22db0bbaeb76e4d5a.jpg` -> MID, NIGHT, CLEAR, ON, REAR, STREET, BLUR, S
- `v11_car_video_011_frame_001_png.rf.529938d2a19f178feb303b7c56717345.jpg` -> FAR, NIGHT, CLEAR, ON, REAR, STREET, BLUR, S
- `v11_car_video_011_frame_002_png.rf.0d238954d70a98937d5369a8a5efdfb2.jpg` -> MID, NIGHT, CLEAR, ON, REAR, STREET, OK, S
- `v11_car_video_011_frame_003_png.rf.5de4a542b18b5673d7630bb6ad5b5611.jpg` -> MID, NIGHT, CLEAR, OFF, FRONT, STREET, OK, S
- `v11_car_video_011_frame_004_png.rf.b20c060aa8e92badfb086f5dd8cb9dc8.jpg` -> FAR, NIGHT, CLEAR, ON, REAR, STREET, OK, S
- `v11_vdf_video_002_frame_001_png.rf.2960f05acfe0a60112776731bba69b3a.jpg` -> FAR, DAY, CLEAR, ON, REAR, STREET, BLUR, S
- `v11_vdf_video_002_frame_002_png.rf.e55f22c216c1550affe0804ea5b56bf1.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `v11_vdf_video_002_frame_003_png.rf.37e2a533b0201f3e38eafbfa2edf3cd8.jpg` -> FAR, DAY, CLEAR, ON, REAR, STREET, OK, S

Nessuna nuova immagine in TEST: resta identico al test v1.

<!-- FINE AGGIUNTE v1.1 -->

## Aggiunte v1.2 (69)

Le distanze sono calcolate dalle bounding box esportate. Le circostanze delle
immagini YouTube derivano dalla compilazione temporanea v1.2, successivamente
consolidata e rimossa; quelle del recupero storico derivano dalla revisione
descrittiva dell'utente. `UNKNOWN` indica un
campo non documentato senza riesaminare visivamente l'immagine.

### Nuove in TRAIN (61)

- `v12_amb_comp_001_clip_001_frame_001_png.rf.511cb33e380921465e9e4f84f93e55e0.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, BLUR, S
- `v12_amb_comp_001_clip_001_frame_002_png.rf.8dfe230e9ee87d3f1447f76f8ed6de95.jpg` -> FAR, NIGHT, CLEAR, ON, MIXED, STREET, OCCLUDED, S
- `v12_amb_comp_001_clip_001_frame_003_png.rf.bfa364845dfe2dfa605843fc626c6656.jpg` -> MID, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `v12_amb_comp_001_clip_001_frame_004_png.rf.032df2e95fb2e55c1c09b3e20c4017d6.jpg` -> MID, NIGHT, CLEAR, ON, SIDE, STREET, OK, S
- `v12_amb_comp_001_clip_002_frame_001_png.rf.a1215ebefaec7e2402f37ae0795f82ab.jpg` -> FAR, NIGHT, RAIN, ON, OBLIQUE, ELEVATED, BLUR+OCCLUDED, S
- `v12_amb_comp_001_clip_002_frame_002_png.rf.771a775f05ec335feafc15ff84f24f3e.jpg` -> MID, NIGHT, RAIN, ON, FRONT, STREET, OCCLUDED, S
- `v12_amb_comp_002_clip_001_frame_001_png.rf.1c079d4b2ef7a52e3003ee21f11563f9.jpg` -> FAR, NIGHT, RAIN, ON, REAR, STREET, OK, S
- `v12_amb_comp_002_clip_001_frame_002_png.rf.22ad9fdff9e3098dcc395a2a9dae0911.jpg` -> FAR, NIGHT, CLEAR, UNKNOWN, REAR, STREET, OCCLUDED, S
- `v12_amb_comp_002_clip_001_frame_003_png.rf.e4df780ca2887985697b0f6fbe17e972.jpg` -> MID, NIGHT, RAIN, ON, FRONT, ELEVATED, OK, S
- `v12_amb_comp_002_clip_001_frame_004_png.rf.59035c79e83634b41b8c9974ecc07330.jpg` -> MID, NIGHT, RAIN, ON, FRONT, STREET, OCCLUDED, S
- `v12_amb_old_recovery_002_jpeg.rf.8b141804a1dda4cf90c36ee260d79691.jpg` -> CLOSE, DAY, CLEAR, ON, REAR, STREET, PARTIAL, S
- `v12_amb_old_recovery_003_jpeg.rf.e9c0ad31865585dc8651344d6e7e6b80.jpg` -> CLOSE, DAY, CLEAR, ON, FRONT, STREET, PARTIAL, S
- `v12_amb_old_recovery_004_jpeg.rf.8af8e05c799962a8fd227d57d8ae9efe.jpg` -> CLOSE, DAY, CLEAR, OFF, REAR, STREET, OCCLUDED+PARTIAL, M
- `v12_amb_old_recovery_006_jpg.rf.a76ca931cb88b391683084b6de26e0cc.jpg` -> MIXED, DAY, CLEAR, OFF, FRONT, STREET, OCCLUDED+PARTIAL, M
- `v12_amb_old_recovery_007_jpg.rf.53a1ba1c20158acb36cdc60cacc148c3.jpg` -> MIXED, DAY, CLEAR, OFF, OBLIQUE, STREET, PARTIAL, M
- `v12_amb_old_recovery_008_jpg.rf.5f39b5d876070682c49a86205cebef65.jpg` -> CLOSE, NIGHT, CLEAR, ON, OBLIQUE, STREET, OCCLUDED, S
- `v12_amb_old_recovery_009_jpg.rf.3c1890b0407a1af2ef20bfb6f0b49562.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, PARTIAL, M
- `v12_amb_old_recovery_010_jpg.rf.df3c2c7ad120419118fe893e47f22444.jpg` -> MIXED, DAY, CLEAR, OFF, OBLIQUE, STREET, OCCLUDED+PARTIAL, M
- `v12_amb_old_recovery_013_jpg.rf.7f3495b5ff0f0698e828d226200677f6.jpg` -> MID, DAY, CLEAR, OFF, SIDE, STREET, OCCLUDED, M
- `v12_car_comp_002_frame_001_png.rf.e2effdbea9316e5a39a0c4138fdb4278.jpg` -> MID, DAY, CLEAR, OFF, REAR, STREET, OCCLUDED, S
- `v12_car_comp_002_frame_002_png.rf.c91c2066fba1648f9c49891cbeae7b5c.jpg` -> MID, DAY, CLEAR, OFF, FRONT, STREET, OCCLUDED, S
- `v12_car_comp_002_frame_003_png.rf.c33e7274fdf0f30178e0ff7f3d050230.jpg` -> MID, DAY, CLEAR, OFF, OBLIQUE, STREET, OCCLUDED, S
- `v12_car_video_001_frame_001_png.rf.841ea71f67a7107211bcea42c8f8413e.jpg` -> FAR, DAY, CLEAR, ON, REAR, STREET, OCCLUDED, S
- `v12_car_video_001_frame_002_png.rf.548a825e3a0b3ad1083dd9b605621143.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OCCLUDED, M
- `v12_car_video_003_frame_001_png.rf.b5e335c19c61befcdd23935262f3a3ee.jpg` -> FAR, NIGHT, CLEAR, OFF, SIDE, STREET, OCCLUDED, S
- `v12_car_video_003_frame_002_png.rf.477c96109451e6c67e23f99a192f1472.jpg` -> FAR, NIGHT, CLEAR, ON, SIDE, STREET, OCCLUDED, S
- `v12_car_video_004_frame_001_png.rf.cb3b023ae2493f9845690624165d84ed.jpg` -> FAR, DAY, CLEAR, OFF, MIXED, TOP_DOWN, OK, S
- `v12_multiclass_source_unknown_001_png.rf.1090f05a07a063fc88d3cabd2a590def.jpg` -> MIXED, DUSK, CLEAR, ON, FRONT, STREET, OK, M
- `v12_null_roma_centro_part_001_frame_001_png.rf.a1228c5328831b458b85c7ca4359b51c.jpg` -> NULL
- `v12_null_roma_centro_part_001_frame_002_png.rf.54412dc9c0c9be77c9372955366be3e5.jpg` -> NULL
- `v12_null_roma_centro_part_001_frame_003_png.rf.c43951d58b74ca33210aef312dc15e9f.jpg` -> NULL
- `v12_null_roma_centro_part_001_frame_004_png.rf.2ad3d1a42e5af552ba42ab83efb16ff6.jpg` -> NULL
- `v12_null_roma_centro_part_001_frame_005_png.rf.1df9606fe7681b6961524e80ecb1a56c.jpg` -> NULL
- `v12_null_roma_centro_part_001_frame_006_png.rf.161928cd23ab9d0ccab0f2b04ddc2814.jpg` -> NULL
- `v12_null_roma_centro_part_001_frame_007_png.rf.2860ba5e48ed5ca3cd8f25ddbd309e76.jpg` -> NULL
- `v12_null_roma_centro_part_001_frame_008_png.rf.62a49de6aa583a54d9607c09e39ee9ad.jpg` -> NULL
- `v12_null_roma_centro_part_001_frame_009_png.rf.7d097e7afe9eff0231b0a8cbd53dc7a5.jpg` -> NULL
- `v12_null_roma_centro_part_002_frame_001_png.rf.d46e02591cb761a9dfa0a31c0e46a099.jpg` -> NULL
- `v12_null_roma_centro_part_002_frame_002_png.rf.938a1d7de7f0e9aeada1f4ffc15f571e.jpg` -> NULL
- `v12_null_roma_centro_part_002_frame_003_png.rf.0092aa9a41f3c6b1ac6f68334a5c7159.jpg` -> NULL
- `v12_null_roma_centro_part_002_frame_004_png.rf.022e37a487d6250b1c8fd474914dafe5.jpg` -> NULL
- `v12_null_roma_centro_part_002_frame_005_png.rf.c900fe0a7140d90995d55bdcabb27086.jpg` -> NULL
- `v12_null_roma_centro_part_002_frame_006_png.rf.a66ce2734abeee7515c419587d2864da.jpg` -> NULL
- `v12_null_roma_centro_part_002_frame_007_png.rf.5ed24d717b4acc5730e53cb00f1d2939.jpg` -> NULL
- `v12_null_roma_centro_part_002_frame_008_png.rf.2c8a4b6d767665d415570be1167a7703.jpg` -> NULL
- `v12_null_roma_centro_part_002_frame_009_png.rf.db08207db07b6483833f88f3720746ba.jpg` -> NULL
- `v12_vdf_comp_001_clip_001_frame_001_png.rf.7335ec137cc00d89b9eb1d9c00c17433.jpg` -> FAR, NIGHT, CLEAR, ON, REAR, STREET, OCCLUDED, S
- `v12_vdf_comp_001_clip_001_frame_002_png.rf.60b64465bbaf473b30a9e989916773ad.jpg` -> CLOSE, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `v12_vdf_comp_001_clip_001_frame_003_png.rf.9b407185a17d4bc17ccea7797069c3ba.jpg` -> FAR, NIGHT, CLEAR, ON, REAR, STREET, OK, S
- `v12_vdf_comp_002_clip_001_frame_001_png.rf.08ed44713f598a5107f64daf269cb7fd.jpg` -> FAR, DAY, CLEAR, OFF, REAR, ELEVATED, OK, M
- `v12_vdf_comp_002_clip_001_frame_002_png.rf.e8de8d991ab9f8df8796b242135c2b54.jpg` -> FAR, DAY, CLEAR, ON, MIXED, STREET, OCCLUDED, S
- `v12_vdf_comp_002_clip_001_frame_003_png.rf.b1bcfe4533c648566c3acabd8f0171c5.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OK, S
- `v12_vdf_comp_002_clip_001_frame_004_png.rf.6e3af9b06bea1a72cd949b6fb7789624.jpg` -> CLOSE, DAY, CLEAR, OFF, SIDE, STREET, OK, S
- `v12_vdf_comp_002_clip_001_frame_005_png.rf.2eb39c55a2b30d478562c985c3c0ca6f.jpg` -> MID, DAY, CLEAR, OFF, REAR, STREET, OCCLUDED, S
- `v12_vdf_comp_002_clip_002_frame_001_png.rf.4f973ddd0386c2c994fe7224e422b7f9.jpg` -> FAR, NIGHT, RAIN, ON, REAR, STREET, OCCLUDED, S
- `v12_vdf_comp_002_clip_002_frame_002_png.rf.7970579c9561404b7316ddd9023cc144.jpg` -> MID, NIGHT, RAIN, ON, SIDE, STREET, OCCLUDED, S
- `v12_vdf_comp_002_clip_002_frame_003_png.rf.e9da657900d7677c7065cdd8f763f47b.jpg` -> FAR, NIGHT, RAIN, ON, FRONT, STREET, OK, S
- `v12_vdf_video_001_frame_001_png.rf.ac6933123641a8173616c305cf40e16b.jpg` -> MIXED, NIGHT, CLEAR, ON, SIDE, STREET, OK, M
- `v12_vdf_video_001_frame_002_png.rf.524430bb48fd61fa8f1e5cdc64bf4e94.jpg` -> MID, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `v12_vdf_video_003_frame_001_png.rf.66905f109a676860401941cceadf1f2d.jpg` -> FAR, DAY, CLEAR, OFF, OBLIQUE, STREET, OK, M
- `v12_vdf_video_003_frame_002_png.rf.eef1b03321a9d2ae2c327296134197b0.jpg` -> MID, DAY, CLEAR, ON, SIDE, STREET, OK, S

### Nuove in VALID (8)

- `v12_amb_old_recovery_005_jpeg.rf.f2376e0b2631b36318d53214d772c62b.jpg` -> MIXED, DAY, CLEAR, OFF, FRONT, STREET, OCCLUDED+PARTIAL, M
- `v12_amb_old_recovery_011_jpg.rf.00f690ad4413b3da502df48f35fa6bfb.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, OCCLUDED, S
- `v12_amb_old_recovery_014_jpg.rf.5901b62b4d480f6fba461845cd5e1ac1.jpg` -> CLOSE, DAY, CLEAR, OFF, OBLIQUE, STREET, OCCLUDED, S
- `v12_car_video_002_frame_001_png.rf.e704daedf67b7e5acccb32c20dadfca3.jpg` -> FAR, NIGHT, CLEAR, ON, SIDE, STREET, BLUR, M
- `v12_car_video_002_frame_002_png.rf.4dec606ab13348aa6d486ba00cf461d0.jpg` -> FAR, NIGHT, CLEAR, ON, REAR, STREET, OCCLUDED, M
- `v12_vdf_video_002_frame_001_png.rf.f96fe743bbdea5212f0e86046b01a737.jpg` -> CLOSE, DUSK, CLEAR, ON, SIDE, STREET, OCCLUDED, S
- `v12_vdf_video_002_frame_002_png.rf.4f2bb217be21c37e5ec13db281513b00.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `v12_vdf_video_004_frame_001_png.rf.78290cdea75b0941c823330c51b0f453.jpg` -> FAR, DAY, CLEAR, ON, FRONT, STREET, OK, S

Nessuna nuova immagine in TEST: resta identico al test v1/v1.1.

<!-- FINE AGGIUNTE v1.2 -->

<!-- INIZIO AGGIUNTE v1.3 -->

## V1.3 — metadata preliminare (SUPERSEDED)

> Questa prima sezione usa i canonical stem solo come appunto. Per il riferimento
> operativo usare la sezione corretta per split riportata piu' avanti.

Le righe usano il `canonical_stem` (senza il suffisso Roboflow `.rf...`).
Il nome esportato completo e lo split corrispondente sono in
`data/datasets/v1.3/split_manifest.csv`.

La distanza e' stata ricavata dalle label esportate usando le soglie definite
all'inizio del documento: FAR <10%, MID 10–30%, CLOSE >30%. I campi non
deducibili dalla fonte sono `UNKNOWN` e vanno completati manualmente.

### Ambulanza

- `v13_amb_video_001_frame_001` -> MID, DAY, CLEAR, ON, FRONT, STREET, UNKNOWN, S
- `v13_amb_video_001_frame_002` -> CLOSE, DAY, CLEAR, ON, REAR, STREET, UNKNOWN, S
- `v13_amb_video_002_frame_001` -> CLOSE, DAY, CLEAR, ON, SIDE, STREET, OCCLUDED, S
- `v13_amb_video_002_frame_002` -> FAR, DAY, CLEAR, ON, REAR, STREET, OCCLUDED, S
- `v13_amb_video_003_frame_001` -> MID, DAY, CLEAR, ON, UNKNOWN, STREET, OCCLUDED, S
- `v13_amb_video_004_frame_001` -> MID, DAY, CLEAR, ON, UNKNOWN, STREET, OCCLUDED, S
- `v13_amb_video_004_frame_002` -> MID, DAY, CLEAR, ON, UNKNOWN, STREET, OCCLUDED, S
- `v13_amb_video_004_frame_003` -> MID, DAY, CLEAR, ON, UNKNOWN, STREET, OCCLUDED, S
- `v13_amb_video_004_frame_004` -> MID, DAY, CLEAR, ON, UNKNOWN, STREET, OCCLUDED, S
- `v13_amb_video_005_frame_001` -> FAR, DAY, CLEAR, ON, UNKNOWN, STREET, OCCLUDED, S
- `v13_amb_video_005_frame_002` -> FAR, DAY, CLEAR, ON, UNKNOWN, STREET, OCCLUDED, S
- `v13_amb_video_005_frame_003` -> MID, DAY, CLEAR, ON, UNKNOWN, STREET, OCCLUDED, S
- `v13_amb_video_005_frame_004` -> FAR, DAY, CLEAR, ON, UNKNOWN, STREET, OCCLUDED, S

Nota: i frame 001–002 sono clip 1; 003–004 sono clip 2.

### Carabinieri

- `v13_car_video_001_frame_001` -> NULL
- `v13_car_video_001_frame_002` -> FAR, DAY, CLEAR, ON, FRONT, ELEVATED, UNKNOWN, S
- `v13_car_video_001_frame_003` -> FAR, DAY, CLEAR, ON, FRONT, ELEVATED, UNKNOWN, S
- `v13_car_video_001_frame_004` -> FAR, DAY, CLEAR, ON, FRONT, ELEVATED, UNKNOWN, S
- `v13_car_video_002_frame_001` -> FAR, NIGHT, CLEAR, ON, UNKNOWN, STREET, OK, S
- `v13_car_video_002_frame_002` -> FAR, NIGHT, CLEAR, ON, UNKNOWN, STREET, OK, S
- `v13_car_video_002_frame_003` -> MIXED, NIGHT, CLEAR, ON, UNKNOWN, STREET, OK, S
- `v13_car_video_002_frame_004` -> CLOSE, NIGHT, CLEAR, ON, UNKNOWN, STREET, OK, S
- `v13_car_video_002_frame_005` -> MIXED, NIGHT, CLEAR, ON, UNKNOWN, STREET, OK, S
- `v13_car_video_003_frame_001` -> FAR, NIGHT, CLEAR, ON, SIDE, STREET, OCCLUDED, S
- `v13_car_video_004_frame_001` -> FAR, NIGHT, CLEAR, ON, UNKNOWN, STREET, REVIEW, S
- `v13_car_video_004_frame_002` -> MIXED, NIGHT, CLEAR, ON, MIXED, STREET, OK, M
- `v13_car_video_004_frame_003` -> FAR, NIGHT, CLEAR, ON, MIXED, STREET, OK, M
- `v13_car_video_004_frame_004` -> MID, NIGHT, CLEAR, ON, UNKNOWN, STREET, REVIEW, S
- `v13_car_video_005_frame_001` -> FAR, NIGHT, CLEAR, ON, UNKNOWN, ELEVATED, OCCLUDED, S
- `v13_car_video_005_frame_002` -> FAR, NIGHT, CLEAR, ON, UNKNOWN, ELEVATED, OCCLUDED, S
- `v13_car_video_005_frame_003` -> FAR, NIGHT, CLEAR, ON, UNKNOWN, ELEVATED, OCCLUDED, S
- `v13_car_video_005_frame_004` -> FAR, NIGHT, CLEAR, ON, UNKNOWN, ELEVATED, OCCLUDED, S
- `v13_car_video_005_frame_005` -> FAR, NIGHT, CLEAR, ON, UNKNOWN, ELEVATED, OCCLUDED, S
- `v13_car_video_006_frame_001` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `v13_car_video_006_frame_002` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, OK, S

Nota: nei frame 001 e 004 della fonte 004 e' visibile soltanto l'Ambulanza;
restano marcati `REVIEW` e non devono essere considerati esempi positivi di
Carabinieri. Il frame 001 della fonte 001 e' NULL.

### VDF

- `v13_vdf_video_001_frame_001` -> FAR, NIGHT, CLEAR, ON, MIXED, STREET, OK, M
- `v13_vdf_video_001_frame_002` -> CLOSE, NIGHT, CLEAR, ON, MIXED, STREET, OK, M
- `v13_vdf_video_001_frame_003` -> MID, NIGHT, CLEAR, ON, MIXED, STREET, OK, M
- `v13_vdf_video_001_frame_004` -> MID, NIGHT, CLEAR, ON, MIXED, STREET, OK, M
- `v13_vdf_video_002_frame_001` -> FAR, NIGHT, CLEAR, ON, MIXED, STREET, OK, S
- `v13_vdf_video_002_frame_002` -> FAR, NIGHT, CLEAR, ON, MIXED, STREET, OK, S
- `v13_vdf_video_002_frame_003` -> MID, NIGHT, CLEAR, ON, MIXED, STREET, OK, S
- `v13_vdf_video_002_frame_004` -> CLOSE, NIGHT, CLEAR, ON, MIXED, STREET, OK, S
- `v13_vdf_video_003_frame_001` -> FAR, NIGHT, CLEAR, ON, UNKNOWN, STREET, OK, S
- `v13_vdf_video_003_frame_002` -> MID, NIGHT, CLEAR, ON, UNKNOWN, STREET, OK, S
- `v13_vdf_video_003_frame_003` -> FAR, NIGHT, CLEAR, ON, UNKNOWN, STREET, OK, S
- `v13_vdf_video_003_frame_004` -> FAR, NIGHT, CLEAR, ON, UNKNOWN, STREET, OK, S
- `v13_vdf_video_003_frame_005` -> MIXED, NIGHT, CLEAR, ON, UNKNOWN, STREET, OK, S
- `v13_vdf_video_003_frame_006` -> MID, NIGHT, CLEAR, ON, UNKNOWN, STREET, OK, S
- `v13_vdf_video_003_frame_007` -> FAR, DAY, CLEAR, ON, UNKNOWN, STREET, OK, S
- `v13_vdf_video_003_frame_008` -> FAR, DAY, CLEAR, ON, UNKNOWN, STREET, OK, S
- `v13_vdf_video_004_frame_001` -> FAR, NIGHT, CLEAR, ON, UNKNOWN, STREET, OK, S
- `v13_vdf_video_004_frame_002` -> MID, NIGHT, CLEAR, ON, UNKNOWN, STREET, OK, S
- `v13_vdf_video_004_frame_003` -> MIXED, NIGHT, CLEAR, ON, UNKNOWN, STREET, OK, S

Nota: VDF fonte 003 e' divisa in tre clip: 001–002, 003–006 e 007–008.

### NULL / hard negative

- `v13_null_hn_002` ... `v13_null_hn_026` -> NULL

`v13_null_hn_001` era uno screen di riferimento e non e' presente nell'export.
Il frame `v13_car_video_001_frame_001` e' elencato nella relativa fonte
Carabinieri, ma va trattato come NULL.

<!-- FINE AGGIUNTE v1.3 -->

## V1.3 — compilazione operativa per split

Qui si segue la convenzione storica del documento: nome completo esportato da
Roboflow, seguito dal contesto. La distanza e' calcolata dalle bounding box;
gli altri campi derivano dalle fonti e restano `UNKNOWN` quando non verificabili.

### Nuove in TRAIN (66)

- `v13_amb_video_001_frame_001_png.rf.08cac3cfcf6f957a6dbcb0c72f6c1735.jpg` -> MID, DAY, CLEAR, ON, FRONT, STREET, PARTIAL, S
- `v13_amb_video_001_frame_002_png.rf.aa494783786baa46e4f99722c912a91a.jpg` -> CLOSE, DAY, CLEAR, ON, REAR, STREET, OCCLUDED, S
- `v13_amb_video_003_frame_001_png.rf.0f762074cef2899b7c18e988df4396c9.jpg` -> MID, DAY, CLEAR, ON, UNKNOWN, STREET, OCCLUDED, S
- `v13_amb_video_004_frame_001_png.rf.9c9a2cf92db5890000047ee8dcf54ee0.jpg` -> MID, DAY, CLEAR, ON, UNKNOWN, STREET, OCCLUDED, S
- `v13_amb_video_004_frame_002_png.rf.483781992b1c0ffac24c8c8ee0fc9c3b.jpg` -> MID, DAY, CLEAR, ON, UNKNOWN, STREET, OCCLUDED, S
- `v13_amb_video_004_frame_003_png.rf.9ed273fa37de15bfae835bb3320c2ced.jpg` -> MID, DAY, CLEAR, ON, UNKNOWN, STREET, OCCLUDED, S
- `v13_amb_video_004_frame_004_png.rf.649050dd6967dea0e4069427dadc9c79.jpg` -> MID, DAY, CLEAR, ON, UNKNOWN, STREET, OCCLUDED, S
- `v13_amb_video_005_frame_001_png.rf.dae10a8d73289bbb68c956e6fed921f6.jpg` -> FAR, DAY, CLEAR, ON, UNKNOWN, STREET, OCCLUDED, S
- `v13_amb_video_005_frame_002_png.rf.d3e245d7d121cba877746b8a30b6c02c.jpg` -> FAR, DAY, CLEAR, ON, UNKNOWN, STREET, OCCLUDED, S
- `v13_amb_video_005_frame_003_png.rf.7516a3dc6cfee9a6d51313e5da79d613.jpg` -> MID, DAY, CLEAR, ON, UNKNOWN, STREET, OCCLUDED, S
- `v13_amb_video_005_frame_004_png.rf.0f3d74a153c550fd7f86dc7c557fcddb.jpg` -> FAR, DAY, CLEAR, ON, UNKNOWN, STREET, OCCLUDED, S
- `v13_car_video_001_frame_001_png.rf.3feb25ca606bd81d3c1bc5e5d9120c64.jpg` -> NULL
- `v13_car_video_001_frame_002_png.rf.2820ef5f844b204601878e8324c4b181.jpg` -> FAR, DAY, CLEAR, ON + OFF, FRONT, ELEVATED, OK + OCCLUDED, M
- `v13_car_video_001_frame_003_png.rf.5e751efe5e9d1db0272d22e692f1a1f0.jpg` -> FAR, DAY, CLEAR, ON, FRONT, ELEVATED, OCCLUDED, M
- `v13_car_video_001_frame_004_png.rf.a837fc05afa8598650cfa72561d937e7.jpg` -> FAR, DAY, CLEAR, ON, FRONT, ELEVATED, OK + OCCLUDED, M
- `v13_car_video_002_frame_001_png.rf.52372a2b0bca9e781b300737998d06ed.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, BLUR, S
- `v13_car_video_002_frame_002_png.rf.977ee5e8056fa66842aef36d4f8a4a9f.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, OK, M
- `v13_car_video_002_frame_003_png.rf.5b54b7659b24f594e189e26b40536d60.jpg` -> MIXED, NIGHT, CLEAR, ON, MIXED, STREET, OK, M
- `v13_car_video_002_frame_004_png.rf.270e2a54de7aa7a7e5a83f7f8193bfae.jpg` -> CLOSE, NIGHT, CLEAR, ON, SIDE, STREET, PARTIAL, S
- `v13_car_video_002_frame_005_png.rf.579ad9be5e393673442465f98d9c6f9c.jpg` -> MIXED, NIGHT, CLEAR, ON, REAR, STREET, OK, M
- `v13_car_video_004_frame_001_png.rf.f876ff1208688697caeaeebef8a8f2db.jpg` -> FAR, NIGHT, CLEAR, ON, REAR, STREET, OCCLUDED, S (AMBULANZA)
- `v13_car_video_004_frame_002_png.rf.9069e99d02da1eae775d90e731f7f42e.jpg` -> MIXED, NIGHT, CLEAR, ON, MIXED, STREET, OK + OCCLUDED, M
- `v13_car_video_004_frame_003_png.rf.c40c19c8be85bd929c5011f4d50ad388.jpg` -> FAR, NIGHT, CLEAR, ON, MIXED, STREET, OK + OCCLUDED, M
- `v13_car_video_004_frame_004_png.rf.a45aec57b2d5b127f7265f82a90471a9.jpg` -> MID, NIGHT, CLEAR, ON, REAR, STREET, OCCLUDED, S (AMBULANZA)
- `v13_car_video_005_frame_001_png.rf.9ebe60b0764291fc8cd1b37c350ed0ec.jpg` -> FAR, NIGHT, CLEAR, ON, MIXED, ELEVATED, OCCLUDED, S
- `v13_car_video_005_frame_002_png.rf.53afc7e5d7455c19c04b4ab244325cce.jpg` -> FAR, NIGHT, CLEAR, ON, SIDE, ELEVATED, OCCLUDED, S
- `v13_car_video_005_frame_003_png.rf.7f20cf6cd32095afe04d12767ccca104.jpg` -> FAR, NIGHT, CLEAR, ON, MIXED, ELEVATED, OK, S
- `v13_car_video_005_frame_004_png.rf.e35dfa0b257ce4ca9549cd742438329b.jpg` -> FAR, NIGHT, CLEAR, ON, MIXED, ELEVATED, OCCLUDED, S
- `v13_car_video_005_frame_005_png.rf.1be2c29f174398e77f95d82ffd437de0.jpg` -> FAR, NIGHT, CLEAR, ON, MIXED, ELEVATED, OCCLUDED + BLUR, S
- `v13_null_hn_003_png.rf.fa610f9ac87f4e4126ce27d0721e9316.jpg` -> NULL
- `v13_null_hn_004_png.rf.cfdbe1e8d4f555ef46b1bbc7be10ee6b.jpg` -> NULL
- `v13_null_hn_005_png.rf.3633d57eef5c1cdd4c1fe95f6a16941e.jpg` -> NULL
- `v13_null_hn_006_png.rf.3e02490881dc30a5d466a6433f71fa2c.jpg` -> NULL
- `v13_null_hn_007_png.rf.8f6026fb2fe740e16009b9211aded34a.jpg` -> NULL
- `v13_null_hn_008_png.rf.5ec7af0c191e7838d9704344393b2831.jpg` -> NULL
- `v13_null_hn_009_png.rf.032fb35763677bacd5655dc39c7ec258.jpg` -> NULL
- `v13_null_hn_010_png.rf.6afe2decae2ce1914d7c597029b4daf7.jpg` -> NULL
- `v13_null_hn_011_png.rf.bc8927ae7b4b362373a9ac28a3cb4365.jpg` -> NULL
- `v13_null_hn_012_png.rf.9f9dabd049d22533410af31658c8b276.jpg` -> NULL
- `v13_null_hn_013_png.rf.12cbf603c52cb5dee740c143b3220129.jpg` -> NULL
- `v13_null_hn_015_png.rf.f86c2c4387b191cafae4a44b85933260.jpg` -> NULL
- `v13_null_hn_016_png.rf.1e1cb8b37b428f675e376c315446b3f5.jpg` -> NULL
- `v13_null_hn_017_png.rf.7528a64064ee3ca956bb34c8973316a8.jpg` -> NULL
- `v13_null_hn_018_png.rf.3f0b3feaec0aba8846f77ac284e4e62e.jpg` -> NULL
- `v13_null_hn_019_png.rf.83f2338ca868a49d316034c68a72662f.jpg` -> NULL
- `v13_null_hn_021_png.rf.2f8fd3b4da8c1ec4c18f1135b05cef29.jpg` -> NULL
- `v13_null_hn_023_png.rf.5f5f5da99966007d266512822b262d8e.jpg` -> NULL
- `v13_null_hn_024_png.rf.b47986b0dd85e212dfc51b8747e1e2f8.jpg` -> NULL
- `v13_null_hn_025_png.rf.04d1be3745f8b5ae5cd344c95db3e2ec.jpg` -> NULL
- `v13_null_hn_026_png.rf.249a55bfaef4de6004454358eec80920.jpg` -> NULL
- `v13_vdf_video_001_frame_001_png.rf.a3d61a952b32a20f14d6f626311e6e93.jpg` -> FAR, NIGHT, CLEAR, ON, MIXED, STREET, OK, S
- `v13_vdf_video_001_frame_002_png.rf.3a3b63603e27784cc08823ec323767dc.jpg` -> CLOSE, NIGHT, CLEAR, ON, MIXED, STREET, PARTIAL + BLUR, S
- `v13_vdf_video_001_frame_003_png.rf.5e4bd88893ed037ff95c51a2d111b93c.jpg` -> MID, NIGHT, CLEAR, ON, MIXED, STREET, OCCLUDED, S
- `v13_vdf_video_001_frame_004_png.rf.9b63ae3c96b8599910d9015703a35082.jpg` -> MID, NIGHT, CLEAR, ON, MIXED, STREET, OK, S
- `v13_vdf_video_002_frame_001_png.rf.1a35ff90e9ea1ae68e6336ea877728f4.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `v13_vdf_video_002_frame_002_png.rf.de129673f1e31c77931ff4127504ca47.jpg` -> FAR, NIGHT, CLEAR, ON, MIXED, STREET, PARTIAL, S
- `v13_vdf_video_002_frame_003_png.rf.2338539e6e960d725280ac611cdf42e4.jpg` -> MID, NIGHT, CLEAR, ON, SIDE, STREET, OK, S
- `v13_vdf_video_002_frame_004_png.rf.bc87f32c58e8e324b7c7c41dc0f8b824.jpg` -> CLOSE, NIGHT, CLEAR, ON, SIDE, STREET, OCCLUDED + PARTIAL, S
- `v13_vdf_video_003_frame_001_png.rf.9c2095c870ac23d859cb1d7d54f7b7ca.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, OCCLUDED, S
- `v13_vdf_video_003_frame_002_png.rf.40cd6f84f10ca5291b66af68514423e4.jpg` -> MID, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `v13_vdf_video_003_frame_003_png.rf.1074370285b7b4098d61417d5912eae5.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, OK, M
- `v13_vdf_video_003_frame_004_png.rf.760f0f3c563a0ac38ecafb98a656ebb8.jpg` -> FAR, NIGHT, CLEAR, ON, MIXED, STREET, OK, M 
- `v13_vdf_video_003_frame_005_png.rf.32451a562b40277b614a5eb85ad5b22b.jpg` -> MIXED, NIGHT, CLEAR, ON, OBLIQUE, STREET, PARTIAL + OK, M
- `v13_vdf_video_003_frame_006_png.rf.89eb8cca463498c923660f0cb95becf4.jpg` -> MID, NIGHT, CLEAR, ON, OBLIQUE, STREET, OCCLUDED + OK, M
- `v13_vdf_video_003_frame_007_png.rf.193b807ec916ac9c247121f01a523015.jpg` -> FAR, DAY, CLEAR, ON, OBLIQUE, STREET, OK + OCCLUDED, M
- `v13_vdf_video_003_frame_008_png.rf.a76cdca53dc319882f8296b9eef06422.jpg` -> FAR, DAY, CLEAR, ON, UNKNOWN, STREET, OK, M

### Nuove in VALID (12)

- `v13_amb_video_002_frame_001_png.rf.5ef1003f0d65afd5f92a313b61198385.jpg` -> CLOSE, DAY, CLEAR, ON, SIDE, STREET, OCCLUDED, S
- `v13_amb_video_002_frame_002_png.rf.a9bac9b52ec0bfa42b685f079eb3d928.jpg` -> FAR, DAY, CLEAR, ON, REAR, STREET, OCCLUDED, S
- `v13_car_video_003_frame_001_png.rf.bcca5359dc79247150c4aa007162dbef.jpg` -> FAR, NIGHT, CLEAR, ON, SIDE, STREET, OCCLUDED, S
- `v13_car_video_006_frame_001_png.rf.bbf0290914b5e037aa652ae9b75358aa.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `v13_car_video_006_frame_002_png.rf.53f95ddcedc1d59edca507350a345e00.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `v13_null_hn_002_png.rf.1a5eef37a66180fed3605a6aaae3851a.jpg` -> NULL
- `v13_null_hn_014_png.rf.c73e2507a37139509d44e2f458c529d1.jpg` -> NULL
- `v13_null_hn_020_png.rf.0ec5cb0fc18e869aa6a58871ba7bf7fb.jpg` -> NULL
- `v13_null_hn_022_png.rf.bf1c374be7da1ae5adeb130391ca8c44.jpg` -> NULL
- `v13_vdf_video_004_frame_001_png.rf.1fb6c15896eff6895e4dd92ca77961d7.jpg` -> FAR, NIGHT, CLEAR, ON, FRONT, STREET, OK, S
- `v13_vdf_video_004_frame_002_png.rf.2097f13340827dc7185095fea3dc2a4c.jpg` -> MID, NIGHT, CLEAR, ON, FRONT, STREET, OCCLUDED, S
- `v13_vdf_video_004_frame_003_png.rf.a55d5034598db7865abc110a8cabcb76.jpg` -> MIXED, NIGHT, CLEAR, ON, OBLIQUE, STREET, OCCLUDED, S

### Nuove in TEST

Nessuna immagine v1.3: il test congelato resta quello storico di 43 immagini.

<!-- FINE METADATA OPERATIVO v1.3 -->
