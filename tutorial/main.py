from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
import requests
import typing

app = FastAPI()

db: typing.List = []


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class City(BaseModel):
    """Ciudad del mundo."""

    name: str
    timezone: str


@app.get("/{variable}")
async def root(variable: str):
    """Variable tomada desde el path or endpoint."""
    return {"variable": variable}


@app.get("/cities")
def get_cities():
    results = []
    for city in db:
        r = requests.get(f"http://worldtimeapi.org/api/timezone/{city['timezone']}")
        current_time = r.json()["datetime"]
        results.append(
            {
                "name": city["name"],
                "timezone": city["timezone"],
                "current_time": current_time,
            }
        )
    return results


lista: typing.List[str] = ["sebastian"]


@app.get("/cities/{city_id}")
def get_city(city_id: int):
    return db[city_id - 1]


@app.post("/cities")
def create_city(city: City):
    db.append(city.dict())
    return db[-1]


@app.delete("/cities/{city_id}")
def delete_city(city_id: int):
    db.pop(city_id - 1)
    return {}
