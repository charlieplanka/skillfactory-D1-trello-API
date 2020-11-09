import requests
import sys

AUTH_PARAMS = {
    "key": "..",
    "token": ".."
}
BOARD_ID = ".."
BASE_URL = "https://api.trello.com/1/{}"


class Card():
    def __init__(self, trello_id="", column=""):
        self.trello_id = trello_id
        self.column = column


def read_board():
    columns = get_board_columns()
    print_columns_with_cards(columns)


def print_columns_with_cards(columns):
    for column in columns:
        column_cards = get_column_cards(column)
        cards_qty = len(column_cards)
        column_name = column["name"]
        print(f"{column_name}, {cards_qty} card(s):")

        if not column_cards:
            print("\t —")
            continue
        print_cards(column_cards)


def print_cards(column_cards):
    counter = 1
    for card in column_cards:
        card_number = str(counter)
        card_name = card["name"]
        card_id = card["id"]
        print(f"\t {card_number}: {card_name}, id: {card_id}")
        counter += 1


def create_card(card_name, column_name):
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
    full_board_id = get_full_board_id()
    create_trello_column(column_name, full_board_id)
    print(f"Column '{column_name}' has been created")


def move_card(card_name, column_name):
    columns = get_board_columns()
    if not is_column_exist(column_name, columns):
        print(f"Sorry, there is no column named '{column_name}'")
        return

    filtered_cards = find_cards(card_name, columns)
    if not filtered_cards:
        print(f"Sorry, there is no card named '{card_name}'")
        return

    card_id = define_trello_card_id(filtered_cards, card_name, column_name)
    if not card_id:
        return

    for column in columns:
        if column["name"] == column_name:
            move_trello_card(card_id, column)
            print(f"Card '{card_name}' has been moved to '{column_name}' column")
            break


def define_trello_card_id(filtered_cards, card_name, column_name):
    if len(filtered_cards) == 1:
        card = filtered_cards[1]
        return card.trello_id
    else:
        card_number = get_card_number_from_user(filtered_cards, card_name, column_name)
        card_obj = filtered_cards.get(card_number)
        if not card_obj:
            print(f"Sorry, there is no card with number {card_number}")
            return None
        return card_obj.trello_id


def get_card_number_from_user(filtered_cards, card_name, column_name):
    print(f"There are several cards named '{card_name}':")
    for counter, card in filtered_cards.items():
        print(f"{counter}: {card_name}, column: {card.column}, id: {card.trello_id}")
    card_number = input(f"Choose a card you want to move to the '{column_name}' column and type its number (for example, 1): ")
    if not card_number:
        print("You haven't typed any number")
        sys.exit()
    return int(card_number)


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


def get_full_board_id():
    req_url = BASE_URL.format("boards") + "/" + BOARD_ID
    board = requests.get(req_url, params=AUTH_PARAMS).json()
    return board["id"]


def get_column_cards(column):
    req_url = BASE_URL.format("lists") + "/" + column["id"] + "/cards"
    return requests.get(req_url, params=AUTH_PARAMS).json()


def get_board_columns():
    req_url = BASE_URL.format("boards") + "/" + BOARD_ID + "/lists"
    return requests.get(req_url, params=AUTH_PARAMS).json()


def create_trello_card(card_name, column):
    req_url = BASE_URL.format("cards")
    requests.post(req_url, data={"name": card_name, "idList": column["id"], **AUTH_PARAMS})


def create_trello_column(column_name, board_id):
    req_url = BASE_URL.format("lists")
    requests.post(req_url, data={"name": column_name, "idBoard": board_id, "pos": "bottom", **AUTH_PARAMS})


def move_trello_card(card_id, column):
    req_url = BASE_URL.format("cards") + "/" + card_id + "/idList"
    requests.put(req_url, data={"value": column["id"], **AUTH_PARAMS})


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        get_full_board_id()
        read_board()
    elif sys.argv[1] == "create_column":
        create_column(sys.argv[2])
    elif sys.argv[1] == "create_card":
        create_card(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "move_card":
        move_card(sys.argv[2], sys.argv[3])
    else:
        print("Unknown command. Please try 'create_column', 'create_card' or 'move_card'")


