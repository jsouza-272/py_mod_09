from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
import json
import csv


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0, le=100)
    oxygen_level: float = Field(ge=0, le=100)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(None, max_length=200)

    def __str__(self) -> str:
        text = f'ID: {self.station_id}\n'
        text += f'Name: {self.name}\n'
        text += f'Crew: {self.crew_size} people\n'
        text += f'Power: {self.power_level:.1f}%\n'
        text += f'Oxygen: {self.oxygen_level:.1f}\n'
        text += f'Status: \
{"Operational" if self.is_operational else "No Operational"}\n'
        return text


def main(test: int) -> None:
    if test == 0:
        print('Space Station Data Validation')
        print('========================================')
        with open('generated_data/space_stations.json') as d_json:
            print('Valid station created:')
            try:
                space_station = SpaceStation(**json.load(d_json)[0])
                print(space_station)
            except ValidationError as error:
                print(f"{error.errors()[0].get('loc')[0]}:",
                      error.errors()[0].get('msg'))
        print("========================================")
        print('Expected validation error:')
        with open('generated_data/invalid_stations.json') as d_json:
            try:
                space_station = SpaceStation(**json.load(d_json)[0])
            except ValidationError as error:
                print(f"{error.errors()[0].get('loc')[0]}:",
                      error.errors()[0].get('msg'))
    if test == 1:
        print('Space Station Data Validation')
        print('========================================')
        with open('generated_data/space_stations.csv') as d_csv:
            print('Valid station created:')
            try:
                space_station = SpaceStation(**list(csv.DictReader(d_csv))[0])
                print(space_station)
            except ValidationError as error:
                print(f"{error.errors()[0].get('loc')[0]}:",
                      error.errors()[0].get('msg'))
        print("========================================")
        print('Expected validation error:')
        with open('generated_data/invalid_stations.csv') as d_csv:
            try:
                space_station = SpaceStation(**list(csv.DictReader(d_csv))[1])
            except ValidationError as error:
                print(f"{error.errors()[0].get('loc')[0]}:",
                      error.errors()[0].get('msg'))


if __name__ == "__main__":
    main(0)
