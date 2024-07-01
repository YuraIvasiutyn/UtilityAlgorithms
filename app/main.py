from app.process import added_and_block_cards as aabc


def main():
    object_class = aabc.AddAndBlockCards(payload=aabc.model, project_id=1) #model dynamiczny w added_and_block_cards
    card_numbers = object_class.create_cards()
    object_class.block_card_numbers(card_numbers, value_of_partial_blockade=1000)


main()
