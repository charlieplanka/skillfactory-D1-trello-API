import requests
import sys

auth_params = {
    "key": "65f4159f37b74da3921ca320f38d97c1",
    "token": "050f56c3607f6402e9a106f87d55392c1e12e0e931f087be65d42169aa680315"
}
board_id = "5f9844c16b5b362d8328c244"
base_url = "https://api.trello.com/1/{}"


class Card():
    def __init__(self, trello_id="", column=""):
        self.trello_id = trello_id
        self.column = column


def read_board():
    columns = get_board_columns()
    for column in columns:
        column_cards = get_column_cards(column)
        cards_qty = len(column_cards)
        column_name = column["name"]
        print(f"{column_name}, {cards_qty} card(s):")

        if not column_cards:
            print("\t —")
            continue

        counter = 1
        for card in column_cards:
            card_number = str(counter)
            card_name = card["name"]
            card_id = card["id"]
            print(f"\t {card_number}: {card_name}, id: {card_id}")
            counter += 1


def create_card(card_name, column_name):

    def create_trello_card(card_name, column):
        requests.post(base_url.format("cards"), data={"name": card_name, "idList": column["id"], **auth_params})

    columns = get_board_columns()
    if not is_column_exist(column_name, columns):
        print(f"Sorry, there is no column named '{column_name}'")
        return
    for column in columns:
        if column["name"] == column_name:
            create_trello_card(card_name, column)
            print(f"Card '{card_name}' has been created in '{column_name}' column")
            break


def create_column(column_name):
    requests.post(base_url.format("lists"), data={"name": column_name, "idBoard": board_id, "pos": "bottom", **auth_params})
    print(f"Column '{column_name}' has been created")


def move_card(card_name, column_name):

    def define_trello_card_id(filtered_cards):
        if len(filtered_cards) == 1:
            card = filtered_cards[1]
            return card.trello_id
        else:
            print(f"There are several cards named '{card_name}':")
            for counter, card in filtered_cards.items():
                print(f"{counter}: {card_name}, column: {card.column}, id: {card.trello_id}")
            card_number = int(input(f"Choose a card you want to move to the '{column_name}' column and type its number (for example, 1): "))
            card_obj = filtered_cards.get(card_number)
            if not card_obj:
                print(f"Sorry, there is no card with number {card_number}")  # может, можно возвращать управление инпуту в цикле?
                return None
            return card_obj.trello_id

    def move_trello_card(card_id, column):
        requests.put(base_url.format("cards") + "/" + card_id + "/idList", data={"value": column["id"], **auth_params})

    columns = get_board_columns()
    if not is_column_exist(column_name, columns):
        print(f"Sorry, there is no column named '{column_name}'")  # код повторяется в двух местах (create card)
        return
    filtered_cards = find_cards(card_name, columns)
    if not filtered_cards:
        print(f"Sorry, there is no card named '{card_name}'")
        return
    card_id = define_trello_card_id(filtered_cards)
    if not card_id:
        return
    for column in columns:
        if column["name"] == column_name:
            move_trello_card(card_id, column)
            print(f"Card '{card_name}' has been moved to '{column_name}' column")
            break


def find_cards(card_name, columns):
    filtered_cards = {}
    counter = 1
    for column in columns:
        column_cards = get_column_cards(column)
        for card in column_cards:
            if card["name"] == card_name:
                filtered_cards[counter] = Card(card["id"], column["name"])
                counter += 1
    return filtered_cards


def is_column_exist(column_name, columns):
    for column in columns:
        if column["name"] == column_name:
            return True
    return False


def get_column_cards(column):
    return requests.get(base_url.format("lists") + "/" + column["id"] + "/cards", params=auth_params).json()


def get_board_columns():
    return requests.get(base_url.format("boards") + "/" + board_id + "/lists", params=auth_params).json()


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read_board()
    elif sys.argv[1] == "create_column":
        create_column(sys.argv[2])
    elif sys.argv[1] == "create_card":
        create_card(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "move_card":
        move_card(sys.argv[2], sys.argv[3])
    else:
        print("Unknown command. Please try 'create_column', 'create_card' or 'move_card'")
