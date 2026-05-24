from datetime import datetime, date, timedelta
from autokolcsonzo import Autokolcsonzo
from szemelyauto import Szemelyauto
from teherauto import Teherauto


def datum_bekerese(szoveg: str):
    """
    Bekéri és date típussá alakítja a felhasználó által megadott dátumot.
    Elvárt formátum: ÉÉÉÉ-HH-NN, például 2026-05-24.
    """

    datum_szoveg = input(szoveg)

    try:
        return datetime.strptime(datum_szoveg, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Hibás dátumformátum. Helyes formátum: ÉÉÉÉ-HH-NN, például 2026-05-24.")


def indulasi_adatok_betoltese() -> Autokolcsonzo:
    """
    Létrehozza az induló autókölcsönzőt 3 autóval és 4 előre rögzített bérléssel.

    Az induló bérlések automatikusan az aktuális naphoz igazodnak:
    - 1 múltbeli bérlés,
    - 1 jelenleg futó bérlés,
    - 2 jövőbeli bérlés.
    """

    kolcsonzo = Autokolcsonzo("SBDVQY Autókölcsönző")

    auto1 = Szemelyauto("ABC-123", "Toyota Corolla", 12000, 5)
    auto2 = Szemelyauto("XYZ-789", "Suzuki Swift", 10000, 5)
    auto3 = Teherauto("TRK-456", "Ford Transit", 18000, 1200)

    kolcsonzo.auto_hozzaadasa(auto1)
    kolcsonzo.auto_hozzaadasa(auto2)
    kolcsonzo.auto_hozzaadasa(auto3)

    mai_nap = date.today()

    # 1. múltbeli, már lezárt bérlés
    kolcsonzo.berles_hozzaadasa(
        "ABC-123",
        mai_nap - timedelta(days=10),
        mai_nap - timedelta(days=8),
        multbeli_datum_engedelyezett=True
    )

    # 2. jelenleg futó bérlés: tegnap kezdődött, holnap ér véget
    kolcsonzo.berles_hozzaadasa(
        "XYZ-789",
        mai_nap - timedelta(days=1),
        mai_nap + timedelta(days=1),
        multbeli_datum_engedelyezett=True
    )

    # 3. jövőbeli bérlés
    kolcsonzo.berles_hozzaadasa(
        "TRK-456",
        mai_nap + timedelta(days=3),
        mai_nap + timedelta(days=5),
        multbeli_datum_engedelyezett=True
    )

    # 4. jövőbeli bérlés
    kolcsonzo.berles_hozzaadasa(
        "ABC-123",
        mai_nap + timedelta(days=7),
        mai_nap + timedelta(days=9),
        multbeli_datum_engedelyezett=True
    )
    return kolcsonzo


def menu_megjelenitese() -> None:
    print("\n--- MENÜ ---")
    print("1. Autók listázása")
    print("2. Autó bérlése")
    print("3. Bérlés lemondása")
    print("4. Aktuális és korábbi bérlések listázása")
    print("0. Kilépés")


def auto_berlese(kolcsonzo: Autokolcsonzo) -> None:
    try:
        print("\n--- Autó bérlése ---")

        kezdo_datum = datum_bekerese("Add meg a bérlés kezdő dátumát ÉÉÉÉ-HH-NN formátumban: ")
        veg_datum = datum_bekerese("Add meg a bérlés vég dátumát ÉÉÉÉ-HH-NN formátumban: ")

        elerheto_autok = kolcsonzo.elerheto_autok_listaja(kezdo_datum, veg_datum)
        kolcsonzo.elerheto_autok_megjelenitese(elerheto_autok)

        if len(elerheto_autok) == 0:
            return

        sorszam_szoveg = input("Add meg a bérelni kívánt autó sorszámát: ")

        try:
            sorszam = int(sorszam_szoveg)
        except ValueError:
            raise ValueError("A sorszámnak egész számnak kell lennie.")

        kivalasztott_auto = kolcsonzo.auto_keresese_sorszam_alapjan(elerheto_autok, sorszam)

        fizetendo_dij = kolcsonzo.berles_hozzaadasa(
            kivalasztott_auto.rendszam,
            kezdo_datum,
            veg_datum
        )

        print(f"A bérlés sikeres. Fizetendő díj: {fizetendo_dij} Ft.")

    except (ValueError, TypeError) as hiba:
        print(f"Hiba: {hiba}")


def berles_lemondasa(kolcsonzo: Autokolcsonzo) -> None:
    try:
        print("\n--- Bérlés lemondása ---")

        lemondhato_berlesek = kolcsonzo.lemondhato_berlesek_listaja()
        kolcsonzo.lemondhato_berlesek_megjelenitese(lemondhato_berlesek)

        if len(lemondhato_berlesek) == 0:
            return

        sorszam_szoveg = input("Add meg a lemondani kívánt bérlés sorszámát: ")

        try:
            sorszam = int(sorszam_szoveg)
        except ValueError:
            raise ValueError("A sorszámnak egész számnak kell lennie.")

        kivalasztott_berles = kolcsonzo.berles_keresese_sorszam_alapjan(
            lemondhato_berlesek,
            sorszam
        )

        kolcsonzo.berles_lemondasa(kivalasztott_berles)

        print("A bérlés sikeresen lemondásra került.")

    except (ValueError, TypeError) as hiba:
        print(f"Hiba: {hiba}")


def main() -> None:
    kolcsonzo = indulasi_adatok_betoltese()

    print(f"Üdvözöllek a(z) {kolcsonzo.nev} rendszerében!")

    while True:
        menu_megjelenitese()
        valasztas = input("Válassz egy menüpontot: ")

        if valasztas == "1":
            kolcsonzo.autok_listazasa()

        elif valasztas == "2":
            auto_berlese(kolcsonzo)

        elif valasztas == "3":
            berles_lemondasa(kolcsonzo)

        elif valasztas == "4":
            kolcsonzo.berlesek_listazasa()

        elif valasztas == "0":
            print("Kilépés a programból. Viszlát!")
            break

        else:
            print("Érvénytelen menüpont. Kérlek, válassz a megadott lehetőségek közül.")


if __name__ == "__main__":
    main()