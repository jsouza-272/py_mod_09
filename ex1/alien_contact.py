from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from enum import Enum
import json
import csv


class ContactType(Enum):
    RADIO = 'radio'
    VISUAL = 'visual'
    PHYSICAL = 'physical'
    TELEPATHIC = 'telepathic'


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0, le=10)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode='after')
    def validation(self) -> 'AlienContact':
        if self.contact_id[:2] != 'AC':
            raise ValueError("Contact ID must start with 'AC'")
        if (self.contact_type is ContactType.PHYSICAL
                and not self.is_verified):
            raise ValueError('Physical contact reports must be verified')
        if (self.contact_type is ContactType.TELEPATHIC
                and self.witness_count < 3):
            raise ValueError('Telepathic contact requires '
                             'at least 3 witnesses')
        if (self.signal_strength > 7.0
                and self.message_received is None):
            raise ValueError('Strong signals (> 7.0) must'
                             ' include a received message')
        return self

    def __str__(self) -> str:
        text = f'ID: {self.contact_id}\n'
        text += f'Type: {self.contact_type.value}\n'
        text += f'Location: {self.location}\n'
        text += f'Signal: {self.signal_strength:.1f}/10\n'
        text += f'Duration: {self.duration_minutes} minutes\n'
        text += f'Witnesses: {self.witness_count}\n'
        text += ("" if self.message_received is None
                 else f"Message: {self.message_received}\n")
        return text


def main(test: int) -> None:
    if test == 0:
        print('Alien Contact Log Validation')
        print('======================================')
        with open('generated_data/alien_contacts.json') as d_json:
            print('Valid contact report:')
            try:
                contact = AlienContact(**json.load(d_json)[1])
                print(contact)
            except ValidationError as error:
                print(error.errors()[0].get('msg').
                      removeprefix('Value error,').strip())
        print('========================================')
        with open('generated_data/invalid_contacts.json') as d_json:
            print('Expected validation error:')
            try:
                contact = AlienContact(**json.load(d_json)[0])
                print(contact)
            except ValidationError as error:
                print(error.errors()[0].get('msg').
                      removeprefix('Value error,').strip())
    if test == 1:
        print('Alien Contact Log Validation')
        print('======================================')
        with open('generated_data/alien_contacts.csv') as d_csv:
            print('Valid contact report:')
            try:
                contact = AlienContact(**list(csv.DictReader(d_csv))[0])
                print(contact)
            except ValidationError as error:
                print(error.errors()[0].get('msg').
                      removeprefix('Value error,').strip())
        print('========================================')
        with open('generated_data/alien_contacts.csv') as d_csv:
            print('Expected validation error:')
            try:
                contact = AlienContact(**list(csv.DictReader(d_csv))[0])
                print(contact)
            except ValidationError as error:
                print(error.errors()[0].get('msg').
                      removeprefix('Value error,').strip())


if __name__ == '__main__':
    main(0)
