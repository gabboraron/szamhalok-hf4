# Feladat összefoglaló
Készíts egy netcopykliens/szerver alkalmazást, mely egy fájl átvitelét és az átvitt adat ellenőrzését teszi lehetővé CRC vagy MD5 ellenőrzőösszeg segítségével! A faladat során három komponents/programot kell elkészíteni:

1. Checksumszerver: (fájl azonosító, checksumhossz, checksum, lejárat (mp-ben)) négyesek tárolását és lekérdezését teszi lehetővé. A protokoll részletei a következő oldalon.

2. Netcopykliens: egy parancssori argumentumban megadott fájlt átküld a szervernek. Az átvitel során/végén kiszámol egy md5 checksumota fájlra, majd ezt feltölti fájl azonosítóval együtt a Checksumszerverre. A lejárati idő 60 mp. A fájl azonosító egy egész szám, amit szintén parancssori argumentumban kell megadni.

3. Netcopyszerver: Vár, hogy egy kliens csatlakozzon. Csatlakozás után fogadja az átvitt bájtokat és azokat elhelyezi a parancssori argumentumban megadott fájlba. A végén lekéri a Checksumszervertől a fájl azonosítóhoz tartozó md5 checksumotés ellenőrzi az átvitt fájl helyességét, melynek eredményét stdoutputrais kiírja. A fájl azonosító itt is parancssori argumentum kell legyen.

## Checksum szerver (TCP)
- Beszúr üzenet 
  - Formátum: szöveges
  - Felépítése: BE|<fájl azon.>|<érvényesség másodpercben>|<checksumhossza bájtszámban>|<checksumbájtjai>
  - A „|” delimiterkarakter•Példa: BE|1237671|60|12|abcdefabcdef
  - Ez esetben: a fájlazon: 1237671, 60mp az érvényességi idő, 12 bájt a checksum, abcdefabcdefmaga a checksum
  - Válasz üzenet: OK
- Kivesz üzenet
  - Formátum: szöveges
  - Felépítése: KI|<fájl azon.>
  - A „|” delimiterkarakter
  - Példa: KI|1237671
    - Azaz kérjük az 1237671 fájl azonosítóhoz tartozó checksum-ot
  - Válasz üzenet: <checksumhossza bájtszámban>|<checksumbájtjai> Péda: 12|abcdefabcdef
  - Ha nincs checksum, akkor ezt küldi: 0|
- Futtatás
  - .\checksum_srv.py <ip> <port>
  - <ip> -pl. localhosta szerver címe bindolásnál
  - <port> -ezen a portonlesz elérhető
  - A szerver végtelen ciklusban fut és egyszerre több klienst is ki tud szolgálni. A kommunikáció TCP, csak a fenti üzeneteket kezeli.
  - Lejárat utáni checksumoktörlődnek.
  
  ## Netcopy kliens (TCP)
- Működés:
  - Csatlakozik a szerverhez, aminek a címét portjátparancssori argumentumban kapja meg.
  - Fájl bájtjainak sorfolytonos átvitele a szervernek.
  - A Checksumszerverrel az ott leírt módon kommunikál.
  - A fájl átvitele és a checksumelhelyezése után bontja a kapcsolatot és terminál.
- Futtatás:
  - .\netcopy_cli.py <srv_ip> <srv_port> <chsum_srv_ip> <chsum_srv_port> <fájl azon> <fájlnév elérési úttal>
  - <fájl azon>:  egész szám
  - <srv_ip> <srv_port>: a netcopyszerver elérhetősége•<chsum_srv_ip> <chsum_srv_port>: a Checksumszerver elérhetősége
  
  ## Netcopyszerver (TCP)
- Működés:
  - Bindoljaa socketeta parancssori argumentumban megadott címre.
  - Vár egy kliensre.
  - Ha acceptálta, akkor fogadja a fájl bájtjait sorfolytonosan és kiírja a paracssoriargumentumban megadott fájlba.
  - Fájlvégejel olvasása esetén lezárja a kapcsolatot és utána ellenőrzi a fájlt a Checksumszerverrel.
  - A Checksumszerverrel az ott leírt módon kommunikál.
  - Hiba esetén a stdout-raki kell írni: CSUM CORRUPTED
  - Helyes átvitel esetén az stdout-raki kell írni: CSUM OK
  - Fájl fogadása és ellenőrzése után terminál a program.
- Futtatás:
  - .\netcopy_srv.py <srv_ip> <srv_port> <chsum_srv_ip> <chsum_srv_port> <fájl azon> <fájlnév elérési úttal>
  - <fájl azon>:  egész szám ua. mint a kliensnél –ez alapján kéri le a szervertől a checksumot
  - <srv_ip> <srv_port>: a netcopyszerver elérhetősége –bindolásnálkell
  - <chsum_srv_ip> <chsum_srv_port>: a Checksumszerver elérhetősége
  - <fájlnév> : ide írja a kapott bájtokat
