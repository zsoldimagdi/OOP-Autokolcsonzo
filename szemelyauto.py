from auto import Auto


class Szemelyauto(Auto):
    """
    Személyautó osztály.
    Az Auto absztrakt osztályból származik.
    """

    def __init__(self, rendszam: str, tipus: str, berleti_dij: int, utasok_szama: int):
        super().__init__(rendszam, tipus, berleti_dij)
        self.utasok_szama = utasok_szama

    @property
    def utasok_szama(self) -> int:
        return self._utasok_szama

    @utasok_szama.setter
    def utasok_szama(self, utasok_szama: int) -> None:
        if not isinstance(utasok_szama, int):
            raise TypeError("Az utasok számának egész számnak kell lennie.")
        if utasok_szama <= 0:
            raise ValueError("Az utasok számának pozitívnak kell lennie.")
        self._utasok_szama = utasok_szama

    def auto_adatok(self) -> str:
        return f"{self._utasok_szama} fő"
