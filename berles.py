from datetime import date
from auto import Auto


class Berles:
    """
    Egy autó bérlését tárolja kezdő és vég dátummal.
    A dátumok közötti időszak zárt intervallumként értelmezett,
    tehát a kezdő és a vég dátum is beleszámít a bérlési időszakba.
    """

    def __init__(self, auto: Auto, kezdo_datum: date, veg_datum: date):
        self.auto = auto
        self.kezdo_datum = kezdo_datum
        self.veg_datum = veg_datum

    @property
    def auto(self) -> Auto:
        return self._auto

    @auto.setter
    def auto(self, auto: Auto) -> None:
        if not isinstance(auto, Auto):
            raise TypeError("A bérléshez érvényes autó objektum szükséges.")
        self._auto = auto

    @property
    def kezdo_datum(self) -> date:
        return self._kezdo_datum

    @kezdo_datum.setter
    def kezdo_datum(self, kezdo_datum: date) -> None:
        if not isinstance(kezdo_datum, date):
            raise TypeError("A kezdő dátumnak date típusúnak kell lennie.")
        self._kezdo_datum = kezdo_datum

    @property
    def veg_datum(self) -> date:
        return self._veg_datum

    @veg_datum.setter
    def veg_datum(self, veg_datum: date) -> None:
        if not isinstance(veg_datum, date):
            raise TypeError("A vég dátumnak date típusúnak kell lennie.")
        self._veg_datum = veg_datum

    def berelt_napok_szama(self) -> int:
        return (self._veg_datum - self._kezdo_datum).days + 1

    def teljes_dij(self) -> int:
        return self.berelt_napok_szama() * self._auto.berleti_dij

    def __str__(self) -> str:
        return (
            f"{self._kezdo_datum} - {self._veg_datum} | "
            f"{self._auto.rendszam} - {self._auto.tipus} | "
            f"{self.berelt_napok_szama()} nap | "
            f"{self.teljes_dij()} Ft"
        )