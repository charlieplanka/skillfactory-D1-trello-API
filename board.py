import requests
import sys

auth_params = {
    "key": "65f4159f37b74da3921ca320f38d97c1",
    "token": "050f56c3607f6402e9a106f87d55392c1e12e0e931f087be65d42169aa680315"
}
board_id = "5f9844c16b5b362d8328c244"
base_url = "https://api.trello.com/1/{}"


class Card():
    def __init__(self, trello_id, column):
        self.trello_id = trello_id
        self.column = column


def read_board():
    column_data = requests.get(base_url.format("boards") + "/" + board_id + "/lists", params=auth_params).json()
    for column in column_data:
        card_data = requests.get(base_url.format("lists") + "/" + column["id"] + "/cards", params=auth_params).json()
        card_qty = len(card_data)
        print(f"{column['name']}, {card_qty} card(s):")
        if not card_data:
            print(f"\t —")
            continue
        custom_id = 1
        for card in card_data:
            print(f"\t {str(custom_id)} {card['name']}, id: {card['id']}")
            custom_id += 1


def create_card(name, column_name):
    column_data = requests.get(base_url.format("boards") + "/" + board_id + "/lists", params=auth_params).json()
    for column in column_data:
        if column["name"] == column_name:
            requests.post(base_url.format("cards"), data={"name": name, "idList": column["id"], **auth_params})
            print(f"Card '{name}' has been created in '{column_name}' column")
            break


def create_column(column_name):
    r = requests.post(base_url.format("lists"), data={"name": column_name, "idBoard": board_id, "pos": "bottom", **auth_params})
    print(r.text)
    print(f"Column '{column_name}' has been created")
    # check if column is already existed


def move_card(name, column_name):
    column_data = requests.get(base_url.format("boards") + "/" + board_id + "/lists", params=auth_params).json()
    card_id = None
    filtered_cards = {}
    custom_id = 1
    for column in column_data:
        column_cards = requests.get(base_url.format("lists") + "/" + column["id"] + "/cards", params=auth_params).json()
        for card in column_cards:
            if card["name"] == name:
                filtered_cards[custom_id] = Card(card["id"], column["name"])
                custom_id += 1
    if len(filtered_cards) == 1:
        card_id = filtered_cards[1].trello_id
    else:
        print(f"There are several cards named '{name}':")
        for custom_id, card in filtered_cards.items():
            print(f"{custom_id}: {name}, column: {card.column}, id: {card.trello_id}")
        card_number = int(input(f"Choose a card you want to move to the '{column_name}' column and type its number (for example, 1): "))
        card_id = filtered_cards[card_number].trello_id

    for column in column_data:
        if column["name"] == column_name:
            requests.put(base_url.format("cards") + "/" + card_id + "/idList", data={"value": column["id"], **auth_params})
            print(f"Card '{name}' has been moved to '{column_name}' column")
            break


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read_board()
    elif sys.argv[1] == "create_column":
        create_column(sys.argv[2])
    elif sys.argv[1] == "create_card":
        create_card(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "move_card":
        move_card(sys.argv[2], sys.argv[3])
