from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from enum import Enum
import json


class Rank(Enum):
    CADET = 'cadet'
    OFFICER = 'officer'
    LIEUTENANT = 'lieutenant'
    CAPTAIN = 'captain'
    COMMANDER = 'commander'


class CrewMenber(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True

    def __str__(self) -> str:
        return f'- {self.name} ({self.rank.value}) - {self.specialization}\n'


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMenber] = Field(min_length=1, max_length=12)
    mission_status: str = 'planned'
    budget_millions: float = Field(ge=1, le=10000)

    @model_validator(mode='after')
    def validator(self) -> 'SpaceMission':
        if self.mission_id[0] != 'M':
            raise ValueError("Mission ID must start with 'M'")
        if (Rank.CAPTAIN not in [member.rank for member in self.crew]
                or Rank.COMMANDER not in
                [member.rank for member in self.crew]):
            raise ValueError("Mission must have at least one"
                             " Commander or Captain.")
        if self.duration_days > 365:
            crew_5 = [member for member in self.crew
                      if member.years_experience > 5]
            if len(crew_5) < (len(self.crew) / 2):
                raise ValueError("For missions longer than 365 days, "
                                 "at least half the crew must have"
                                 " more than 5 years of experience.")
        if False in [member.is_active for member in self.crew]:
            raise ValueError("All crew members must be active.")
        return self

    def __str__(self) -> str:
        text = f'Mission: {self.mission_name}\n'
        text += f'ID: {self.mission_id}\n'
        text += f'Destination: {self.destination}\n'
        text += f'Duration: {self.duration_days} days\n'
        text += f'Budget: ${self.budget_millions:.1f}M\n'
        text += f'Crew size: {len(self.crew)}\n'
        members = ''
        for i in range(0, len(self.crew) - 1):
            members += str(self.crew[i])
        text += f'Crew members:\n{members}'
        return text


def main(test: int) -> None:
    if test == 0:
        print("Space Mission Crew Validation")
        print("=========================================")
        try:
            with open('generated_data/space_missions.json') as d_json:
                l_json = json.load(d_json)[0]
                crew = [CrewMenber(**member) for member in l_json.get('crew')]
                l_json.update({'crew': crew})
                print(SpaceMission(**l_json))
        except ValidationError as error:
            print(error.errors()[0].get('msg').
                  removeprefix('Value error,').strip())
        print("=========================================")
        print("Expected validation error:")
        try:
            with open('generated_data/space_missions.json') as d_json:
                l_json = json.load(d_json)[1]
                crew = [CrewMenber(**member) for member in l_json.get('crew')]
                l_json.update({'crew': crew})
                print(SpaceMission(**l_json))
        except ValidationError as error:
            print(error.errors()[0].get('msg').
                  removeprefix('Value error,').strip())


if __name__ == "__main__":
    main(0)
