# OOP-Autokolcsonzo
GDE OOP projektfeladat
# Autókölcsönző Rendszer

Ez a projekt egy egyszerű objektumorientált Python alkalmazás, amely egy autókölcsönző rendszer alapvető működését valósítja meg.

A rendszerben autókat lehet listázni, több napra kibérelni, meglévő jövőbeli bérlést lemondani, valamint megtekinteni az aktuális és korábbi bérléseket.

## Funkciók

- Autók listázása rendezett, oszlopos formában
- Autó bérlése kezdő és vég dátum megadásával
- A kiválasztott időszakban elérhető autók listázása
- Autó kiválasztása sorszám alapján
- Bérleti díj automatikus kiszámítása a napok száma alapján
- Bérlés lemondása sorszám alapján
- Csak lemondható, még meg nem kezdett bérlések megjelenítése
- Aktuális és korábbi bérlések listázása rendezett, oszlopos formában
- Hibakezelés és adatvalidáció
- Induló adatok automatikus betöltése

## Induló adatok

A program indulásakor automatikusan létrejön egy autókölcsönző, amely tartalmaz:

- 3 autót
- 4 bérlést

Az induló bérlések dátumai automatikusan az aktuális naphoz igazodnak:

- 1 múltbeli, lezárt bérlés
- 1 jelenleg futó bérlés
- 2 jövőbeli bérlés

Ez azért hasznos, mert a program nem fix dátumokra épül, így későbbi futtatáskor is működőképes marad.

## Fő osztályok

### `Auto`

Absztrakt ősosztály, amely az autók közös attribútumait tartalmazza:

- rendszám
- típus
- napi bérleti díj

Az osztály absztrakt metódust is tartalmaz, amelyet a leszármazott osztályok valósítanak meg.

### `Szemelyauto`

Az `Auto` osztályból származik.

A személyautók saját attribútuma:

- utasok száma

### `Teherauto`

Az `Auto` osztályból származik.

A teherautók saját attribútuma:

- teherbírás

### `Berles`

Egy autó bérlését tárolja kezdő és vég dátummal.

A bérlés képes kiszámítani:

- a bérelt napok számát
- a teljes bérleti díjat

### `Autokolcsonzo`

A rendszer központi osztálya.

Feladatai:

- autók tárolása
- bérlések tárolása
- elérhető autók keresése
- bérlés létrehozása
- bérlés lemondása
- bérlések listázása
- dátumok és időszakok ellenőrzése

## Bérlési szabályok

Új bérlés esetén a felhasználó megadja:

- a bérlés kezdő dátumát
- a bérlés vég dátumát

A rendszer ellenőrzi, hogy:

- egyik dátum sem múltbeli
- a kezdő dátum nem későbbi, mint a vég dátum
- az autó a teljes kiválasztott időszakban elérhető-e

A bérlés csak akkor rögzíthető, ha az adott autó foglalása nem ütközik másik bérléssel.

## Lemondási szabályok

A rendszer csak a lemondható bérléseket jeleníti meg.

Lemondható bérlésnek az számít, amelynek kezdő dátuma mai vagy jövőbeli.

A múltbeli bérlések lezárt történeti adatok, ezért nem mondhatók le.

A jelenleg futó bérlés szintén nem jelenik meg lemondhatóként, mert annak kezdő dátuma már múltbeli.

## OOP megoldások

A projekt tartalmazza az alábbi objektumorientált megoldásokat:

- absztrakt osztály
- öröklődés
- polimorfizmus
- egységbezárás
- non-public attribútumok
- property alapú getterek és setterek
- osztálymetódusok
- `__str__` dunder metódus
- hibakezelés `try-except` blokkal
- adatvalidáció

## Adatvalidáció

A program ellenőrzi többek között, hogy:

- a rendszám nem lehet üres
- az autó típusa nem lehet üres
- a bérleti díj pozitív egész szám legyen
- a személyautó utasainak száma pozitív egész szám legyen
- a teherautó teherbírása pozitív egész szám legyen
- a dátumok megfelelő formátumúak legyenek
- új bérlésnél ne lehessen múltbeli dátumot megadni
- a kezdő dátum ne legyen későbbi, mint a vég dátum
- csak elérhető autót lehessen kibérelni
- csak létező, lemondható bérlést lehessen lemondani

## Felhasználói felület

A program egyszerű konzolos menüvel működik.

A menüpontok:

```text
1. Autók listázása
2. Autó bérlése
3. Bérlés lemondása
4. Aktuális és korábbi bérlések listázása
0. Kilépés
