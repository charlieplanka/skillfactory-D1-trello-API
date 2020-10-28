import requests
import sys

auth_params = {
    "key": "65f4159f37b74da3921ca320f38d97c1",
    "token": "050f56c3607f6402e9a106f87d55392c1e12e0e931f087be65d42169aa680315"
}
board_id = "AXPZWOVS"
base_url = "https://api.trello.com/1/{}"


def read_board():
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        print(column["name"])
        card_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        if not card_data:
            print("\t" + "No cards")
            continue
        for card in card_data:
            print("\t" + card["name"])


def create_card(name, column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        if column["name"] == column_name:
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break


def move_card(name, column_name):
    column_data = requests.get(base_url.format("boards") + "/" + board_id + "/lists", params=auth_params).json()
    card_id = None
    for column in column_data:
        column_cards = requests.get(base_url.format("lists") + "/" + column["id"] + "/cards", params=auth_params).json()
        for card in column_cards:
            if card["name"] == name:
                card_id = card["id"]
                break

    for column in column_data:
        if column["name"] == column_name:
            requests.put(base_url.format('cards') + '/' + card_id + '/idList', data={'value': column['id'], **auth_params})
            break


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) <= 2:
        read_board()
    elif sys.argv[1] == "create":
        create_card(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "move":
        move_card(sys.argv[2], sys.argv[3])
