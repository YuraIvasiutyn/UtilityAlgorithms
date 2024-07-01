from datetime import date
from typing import List

from app.db import db
from app.conf.configurate import config

is_db_conn = db.DB(config=db.DBConfig(**config['identitydb']))


def get_new_card_number_crud(program_variant: str, program_id: int) -> List[str]:

    today_day = f"{date.today()} 00:00:00.000"

    query = f"""
            SELECT card_number
            FROM public.cards
            where program_variant = %(program_variant)s
            and program_id = %(program_id)s
            and card_already_taken is false 
            and creation_date >= %(today_day)s
            """

    values = {
        'program_variant': program_variant,
        'program_id': program_id,
        'today_day': today_day
    }

    try:
        card_numbers = is_db_conn.fetch_all(query=query, values=values)
    except Exception as e:
        print(f"Problem with get_activation_list_id_for_program: {e}. \n{query}")
        raise

    return [card['card_number'] for card in card_numbers]


