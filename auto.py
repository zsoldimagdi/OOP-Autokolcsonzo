from abc import ABC, abstractmethod


class Auto(ABC):
    """
    Absztrakt autó osztály.
    Az autók közös adatait és kötelezően megvalósítandó viselkedését tartalmazza.
    """

    def __init__(self, rendszam: str, tipus: str, berleti_dij: int):
        self.rendszam = rendszam
        self.tipus = tipus
        self.berleti_dij = berleti_dij

    @property
    def rendszam(self) -> str:
        return self._rendszam

    @rendszam.setter
    def rendszam(self, rendszam: str) -> None:
        if not isinstance(rendszam, str) or len(rendszam.strip()) == 0:
            raise ValueError("A rendszám nem lehet üres.")
        self._rendszam = rendszam.strip().upper()

    @property
    def tipus(self) -> str:
        return self._tipus

    @tipus.setter
    def tipus(self, tipus: str) -> None:
        if not isinstance(tipus, str) or len(tipus.strip()) == 0:
            raise ValueError("Az autó típusa nem lehet üres.")
        self._tipus = tipus.strip()

    @property
    def berleti_dij(self) -> int:
        return self._berleti_dij

    @berleti_dij.setter
    def berleti_dij(self, berleti_dij: int) -> None:
        if not isinstance(berleti_dij, int):
            raise TypeError("A bérleti díjnak egész számnak kell lennie.")
        if berleti_dij <= 0:
            raise ValueError("A bérleti díjnak pozitívnak kell lennie.")
        self._berleti_dij = berleti_dij

    @abstractmethod
    def auto_adatok(self) -> str:
        """Az autó típusonként eltérő adatainak visszaadása."""
        pass

    def __str__(self) -> str:
        return f"{self._rendszam} - {self._tipus} - {self.auto_adatok()} - {self._berleti_dij} Ft/nap"
