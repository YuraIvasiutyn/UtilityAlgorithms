import os
import time

import requests

from datetime import datetime
from typing import List
from contextlib import redirect_stdout

from app.crud.is_query import get_new_card_number_crud
from app.conf.configurate import config
from app.models import conf_models as cm
from app.models import is_api_model as iam

is_api_conf = cm.GeneralApiConf(**config["is_api"])


class AddAndBlockCards:

    def __init__(self, payload: iam.CardPayload, project_id: int):
        self.payload = payload
        self.project_id = project_id

    def create_cards(self):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file_path = os.path.join("logs", f"create_cards_log_{timestamp}.txt")
        with open(log_file_path, 'w') as f:
            with redirect_stdout(f):
                url = f"{is_api_conf.host}:{is_api_conf.port}/v1/sokp/cards/create-for-future/?project_id={self.project_id}"
                headers = {
                    "accept": "application/json",
                    "Content-Type": "application/json"
                }
                try:
                    chunks = []
                    remaining_cards = self.payload.numOfCards
                    while remaining_cards > 0:
                        chunk_size = min(remaining_cards, 500) #jeśli dobrze pamietam to max 500 kart mozna generować żeby proces się nie zawiesił
                        chunk_data = self.payload.dict()
                        chunk_data['numOfCards'] = chunk_size
                        chunks.append(chunk_data)
                        remaining_cards -= chunk_size

                    card_numbers = []

                    for chunk in chunks:
                        response = requests.request("POST", url=url, json=chunk, headers=headers)

                        if response.status_code == 200:
                            print(f"Karty zostały pomyślnie utworzone. Nowych kart - {chunk['numOfCards']}.")
                            data = response.json()
                            cards_info = data['cards']['cardsInfo']
                            for card_info in cards_info:
                                card_number = card_info['cardNumber']
                                code = card_info['infoStatus']['code']
                                message = card_info['infoStatus']['message']
                                card_numbers.append(card_number)
                                print(f"Numer karty: {card_number}")
                                if code != '03100001':
                                    print(f"Dla karty: {card_number} Kod: {code}, Wiadomość: {message}")
                        else:
                            print(f"Metoda zwróciła status code = {response.status_code}, treść: {response.text}")

                    print(f"Wszystkie karty: {card_numbers}")
                    return card_numbers
                except Exception as e:
                    print(f"Wystąpił nieoczekiwany błąd: {e}")


# zostawie ten metod może w przyszłości będzie potrzebny
    def get_new_card_number(self):

        card_numbers = get_new_card_number_crud(
            program_variant=self.payload.programVariant,
            program_id=self.payload.programId,
            )
        print(f"Pobrano {len(card_numbers)} kart z bazy")
        print(f"card {card_numbers}")

        return card_numbers

    def block_card_numbers(self, card_numbers: List[str], value_of_partial_blockade: int):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file_path = os.path.join("logs", f"block_cards_log_{timestamp}.txt")
        with open(log_file_path, 'w') as f:
            with redirect_stdout(f):
                url = f"{is_api_conf.host}:{is_api_conf.port}/v1/partial-funds-blockades"
                headers = {
                    "accept": "application/json",
                    "Content-Type": "application/json"
                }
                print(f"Ilość kart do blokady: {len(card_numbers)}")

                # Dzielimy listę kart na paczki po 50
                chunks = [card_numbers[i:i + 50] for i in range(0, len(card_numbers), 50)]

                for chunk in chunks:
                    data = [
                        {
                            "cardNumber": card_number,
                            "valueOfPartialBlockade": value_of_partial_blockade
                        }
                        for card_number in chunk
                    ]
                    print(data)
                    time.sleep(300) #timeout co 5 minut, żeby nie zawiesić proces blokady

                    try:
                        response = requests.request("POST", url=url, json=data, headers=headers)
                        print(f"Response w fornmacie json: {response.json()}")
                        if response.status_code == 201:
                            print(f"Limit został pomyślnie zmieniony dla: {len(response.json())} kart w tej paczce.")
                        else:
                            print(f"Metoda zwróciła status code = {response.status_code}, treść: {response.text}")
                    except Exception as e:
                        print(f"Wystąpił nieoczekiwany błąd: {e} {response.status_code} {response.text}")


model = iam.CardPayload(
    numOfCards=200,
    programVariant="315",
    programId=124,
    activationDateTime=datetime.now().isoformat(),
    valueLimit=1000
)
