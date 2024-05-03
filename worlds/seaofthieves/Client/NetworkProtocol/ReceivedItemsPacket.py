from NetUtils import ClientStatus, NetworkItem, JSONtoTextParser, JSONMessagePart, add_json_item, add_json_location, add_json_text, JSONTypes


class ReceivedItemsPacket:

    def __init__(self, dict: dict):
        self.index: int | None = dict.get('index')
        self.items: list[NetworkItem] | None = dict.get('items')
