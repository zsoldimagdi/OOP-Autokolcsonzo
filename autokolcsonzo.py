from datetime import date
from auto import Auto
from berles import Berles


class Autokolcsonzo:
    """
    Az autókölcsönző rendszer központi osztálya.
    Tárolja az autókat és a bérléseket.
    """

    def __init__(self, nev: str):
        self.nev = nev
        self._autok = []
        self._berlesek = []

    @property
    def nev(self) -> str:
        return self._nev

    @nev.setter
    def nev(self, nev: str) -> None:
        if not isinstance(nev, str) or len(nev.strip()) == 0:
            raise ValueError("A kölcsönző neve nem lehet üres.")
        self._nev = nev.strip()

    def auto_hozzaadasa(self, auto: Auto) -> None:
        if not isinstance(auto, Auto):
            raise TypeError("Csak Auto típusú objektum adható hozzá.")

        if self.auto_keresese(auto.rendszam) is not None:
            raise ValueError("Ezzel a rendszámmal már létezik autó a rendszerben.")

        self._autok.append(auto)

    def auto_keresese(self, rendszam: str) -> Auto | None:
        rendszam = rendszam.strip().upper()

        for auto in self._autok:
            if auto.rendszam == rendszam:
                return auto

        return None

    def auto_keresese_sorszam_alapjan(self, elerheto_autok: list[Auto], sorszam: int) -> Auto:
        if not isinstance(sorszam, int):
            raise TypeError("A sorszámnak egész számnak kell lennie.")

        if sorszam < 1 or sorszam > len(elerheto_autok):
            raise ValueError("Nincs ilyen sorszámú autó az elérhető autók között.")

        return elerheto_autok[sorszam - 1]

    def autok_listazasa(self) -> None:
        print("\n--- Autók a rendszerben ---")

        if len(self._autok) == 0:
            print("Nincs autó a rendszerben.")
            return

        print(
            f"{'Ssz.':<6}"
            f"{'Rendszám':<12}"
            f"{'Típus':<20}"
            f"{'Adatok':<20}"
            f"{'Bérleti díj':<15}"
        )

        print("-" * 73)

        for index, auto in enumerate(self._autok, start=1):
            berleti_dij_szoveg = str(auto.berleti_dij) + " Ft/nap"

            print(
                f"{index:<6}"
                f"{auto.rendszam:<12}"
                f"{auto.tipus:<20}"
                f"{auto.auto_adatok():<20}"
                f"{berleti_dij_szoveg:<15}"
            )
            
    def elerheto_autok_listaja(self, kezdo_datum: date, veg_datum: date) -> list[Auto]:
        """
        Visszaadja azokat az autókat, amelyek a megadott időszakban elérhetők.
        """

        self._uj_berles_intervallum_ellenorzese(kezdo_datum, veg_datum)

        elerheto_autok = []

        for auto in self._autok:
            if self.elerheto_e(auto.rendszam, kezdo_datum, veg_datum):
                elerheto_autok.append(auto)

        return elerheto_autok

    def elerheto_autok_megjelenitese(self, elerheto_autok: list[Auto]) -> None:
        print("\n--- A kiválasztott időszakban elérhető autók ---")

        if len(elerheto_autok) == 0:
            print("A kiválasztott időszakban nincs elérhető autó.")
            return

        print(
            f"{'Ssz.':<6}"
            f"{'Típus':<20}"
            f"{'Ár':<12}"
        )
        print("-" * 38)

        for index, auto in enumerate(elerheto_autok, start=1):
            ar_szoveg = str(auto.berleti_dij) + " Ft/nap"

            print(
                f"{index:<6}"
                f"{auto.tipus:<20}"
                f"{ar_szoveg:<12}"
            )

    def berles_hozzaadasa(
            self,
            rendszam: str,
            kezdo_datum: date,
            veg_datum: date,
            multbeli_datum_engedelyezett: bool = False
    ) -> int:
        """
        Új bérlés rögzítése.

        Alapesetben múltbeli dátumra nem lehet új bérlést rögzíteni.
        A multbeli_datum_engedelyezett=True paraméter csak az induló,
        történeti adatok betöltéséhez használható.
        """

        auto = self.auto_keresese(rendszam)

        if auto is None:
            raise ValueError("Nincs ilyen rendszámú autó a rendszerben.")

        if multbeli_datum_engedelyezett:
            self._intervallum_tipus_es_sorrend_ellenorzese(kezdo_datum, veg_datum)
        else:
            self._uj_berles_intervallum_ellenorzese(kezdo_datum, veg_datum)

        if not self.elerheto_e(rendszam, kezdo_datum, veg_datum):
            raise ValueError("Ez az autó a kiválasztott időszakban már foglalt.")

        uj_berles = Berles(auto, kezdo_datum, veg_datum)
        self._berlesek.append(uj_berles)

        return uj_berles.teljes_dij()

    def lemondhato_berlesek_listaja(self) -> list[Berles]:
        """
        Visszaadja azokat a bérléseket, amelyek lemondhatók.
        Csak a mai vagy jövőbeli kezdő dátumú bérlések mondhatók le.
        A múltbeli bérlések lezárt történeti adatok, ezért nem módosíthatók.
        """

        lemondhato_berlesek = []

        for berles in self._berlesek:
            if berles.kezdo_datum >= date.today():
                lemondhato_berlesek.append(berles)

        return sorted(lemondhato_berlesek, key=lambda berles: berles.kezdo_datum)

    def lemondhato_berlesek_megjelenitese(self, lemondhato_berlesek: list[Berles]) -> None:
        """
        Sorszámozva megjeleníti a lemondható bérléseket.
        """

        print("\n--- Lemondható bérlések ---")

        if len(lemondhato_berlesek) == 0:
            print("Jelenleg nincs lemondható bérlés.")
            return

        print(
            f"{'Ssz.':<5}"
            f"{'Kezdő dátum':<15}"
            f"{'Vég dátum':<15}"
            f"{'Rendszám':<12}"
            f"{'Típus':<20}"
            f"{'Napok':<8}"
            f"{'Teljes díj':<12}"
        )

        print("-" * 87)

        for index, berles in enumerate(lemondhato_berlesek, start=1):
            teljes_dij_szoveg = str(berles.teljes_dij()) + " Ft"

            print(
                f"{index:<5}"
                f"{str(berles.kezdo_datum):<15}"
                f"{str(berles.veg_datum):<15}"
                f"{berles.auto.rendszam:<12}"
                f"{berles.auto.tipus:<20}"
                f"{berles.berelt_napok_szama():<8}"
                f"{teljes_dij_szoveg:<12}"
            )

    def berles_keresese_sorszam_alapjan(self, lemondhato_berlesek: list[Berles], sorszam: int) -> Berles:
        """
        A lemondható bérlések listájából sorszám alapján kiválaszt egy bérlést.
        """

        if not isinstance(sorszam, int):
            raise TypeError("A sorszámnak egész számnak kell lennie.")

        if sorszam < 1 or sorszam > len(lemondhato_berlesek):
            raise ValueError("Nincs ilyen sorszámú lemondható bérlés.")

        return lemondhato_berlesek[sorszam - 1]

    def berles_lemondasa(self, berles: Berles) -> None:
        """
        Meglévő bérlés lemondása.

        Csak mai vagy jövőbeli bérlés mondható le.
        Múltbeli bérlés nem mondható le, mert lezárt történeti adat.
        """

        if not isinstance(berles, Berles):
            raise TypeError("A lemondáshoz érvényes bérlés objektum szükséges.")

        if berles.kezdo_datum < date.today():
            raise ValueError("Múltbeli bérlés nem mondható le, mert az már lezárt történeti adat.")

        if berles not in self._berlesek:
            raise ValueError("A kiválasztott bérlés nem található a rendszerben.")

        self._berlesek.remove(berles)

    def berlesek_listazasa(self) -> None:
        print("\n--- Aktuális és korábbi bérlések ---")

        if len(self._berlesek) == 0:
            print("Jelenleg nincs bérlés a rendszerben.")
            return

        rendezett_berlesek = sorted(self._berlesek, key=lambda berles: berles.kezdo_datum)

        print(
            f"{'Ssz.':<5}"
            f"{'Kezdő dátum':<15}"
            f"{'Vég dátum':<15}"
            f"{'Rendszám':<12}"
            f"{'Típus':<20}"
            f"{'Napok':<8}"
            f"{'Teljes díj':<12}"
        )

        print("-" * 87)

        for index, berles in enumerate(rendezett_berlesek, start=1):
            teljes_dij_szoveg = str(berles.teljes_dij()) + " Ft"

            print(
                f"{index:<5}"
                f"{str(berles.kezdo_datum):<15}"
                f"{str(berles.veg_datum):<15}"
                f"{berles.auto.rendszam:<12}"
                f"{berles.auto.tipus:<20}"
                f"{berles.berelt_napok_szama():<8}"
                f"{teljes_dij_szoveg:<12}"
            )

    def elerheto_e(self, rendszam: str, kezdo_datum: date, veg_datum: date) -> bool:
        """
        Ellenőrzi, hogy az adott autó a kiválasztott időszakban szabad-e.
        Két bérlés akkor ütközik, ha van közös napjuk.
        """

        rendszam = rendszam.strip().upper()

        for berles in self._berlesek:
            if berles.auto.rendszam == rendszam:
                if self._intervallumok_atfedik_egymast(
                        kezdo_datum,
                        veg_datum,
                        berles.kezdo_datum,
                        berles.veg_datum
                ):
                    return False

        return True

    def _intervallumok_atfedik_egymast(
            self,
            kezdo1: date,
            veg1: date,
            kezdo2: date,
            veg2: date
    ) -> bool:
        return kezdo1 <= veg2 and kezdo2 <= veg1

    def _uj_berles_intervallum_ellenorzese(self, kezdo_datum: date, veg_datum: date) -> None:
        """
        Új bérlésnél:
        - egyik dátum sem lehet múltbeli,
        - a kezdő dátum nem lehet későbbi, mint a vég dátum.
        """

        self._intervallum_tipus_es_sorrend_ellenorzese(kezdo_datum, veg_datum)

        if kezdo_datum < date.today() or veg_datum < date.today():
            raise ValueError("Új bérlésnél egyik dátum sem lehet múltbeli.")

    def _intervallum_tipus_es_sorrend_ellenorzese(self, kezdo_datum: date, veg_datum: date) -> None:
        if not isinstance(kezdo_datum, date):
            raise TypeError("A kezdő dátumnak date típusúnak kell lennie.")

        if not isinstance(veg_datum, date):
            raise TypeError("A vég dátumnak date típusúnak kell lennie.")

        if kezdo_datum > veg_datum:
            raise ValueError("A kezdő dátum nem lehet későbbi, mint a vég dátum.")