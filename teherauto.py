from auto import Auto


class Teherauto(Auto):
    """
    Teherautó osztály.
    Az Auto absztrakt osztályból származik.
    """

    def __init__(self, rendszam: str, tipus: str, berleti_dij: int, teherbiras: int):
        super().__init__(rendszam, tipus, berleti_dij)
        self.teherbiras = teherbiras

    @property
    def teherbiras(self) -> int:
        return self._teherbiras

    @teherbiras.setter
    def teherbiras(self, teherbiras: int) -> None:
        if not isinstance(teherbiras, int):
            raise TypeError("A teherbírásnak egész számnak kell lennie.")
        if teherbiras <= 0:
            raise ValueError("A teherbírásnak pozitívnak kell lennie.")
        self._teherbiras = teherbiras

    def auto_adatok(self) -> str:
        return f"{self._teherbiras} kg teherbírás"
