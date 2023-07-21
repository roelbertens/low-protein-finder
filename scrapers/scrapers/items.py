# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
from re import search, IGNORECASE


@dataclass
class Measure:
    value: float
    unit: str

    @classmethod
    def from_string(cls, value: str | None) -> "Measure | None":
        if value is None:
            return None
        try:
            v, u = search("(\d+(?:\.\d+)?)\s*([a-z]+)", value, IGNORECASE).groups()
        except AttributeError:
            print(f"|{value}|")
            return None
        return Measure(v, u)


@dataclass
class NutritionData:
    reference: Measure | None = None
    energy: Measure | None = None
    carbs: Measure | None = None
    fat: Measure | None = None
    fiber: Measure | None = None
    salt: Measure | None = None
    sugar: Measure | None = None
    protein: Measure | None = None


@dataclass
class Product:
    name: str
    nutrition: NutritionData | None
