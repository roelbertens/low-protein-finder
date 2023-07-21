# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import logging
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
            return Measure(float(v), u)
        except AttributeError:
            pass

        # Special case where the unit is specified before the value.
        try:
            u, v = search("([a-z]+)\s*(\d+(?:\.\d+)?)$", value, IGNORECASE).groups()
            return Measure(float(v), u)
        except AttributeError:
            pass
        logging.debug(f"Failed to convert |{value}| to a Measure.")
        return None


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
    brand: str | None
    description: str | None
    price: float | None
    category: list[str] | None
    nutrition: NutritionData | None
