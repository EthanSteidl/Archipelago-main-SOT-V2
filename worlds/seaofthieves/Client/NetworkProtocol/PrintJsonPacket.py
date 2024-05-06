
from NetUtils import ClientStatus, NetworkItem, JSONtoTextParser, JSONMessagePart, add_json_item, add_json_location, add_json_text, JSONTypes
import typing
class PrintJsonPacket:

    def __init__(self, dict):
        self.countdown: int = dict.get('countdown')
        self.tags: typing.List[str] | None = dict.get('tags')
        self.message: str | None = dict.get('message')
        self.slot: int | None = dict.get('slot')
        self.team: int | None = dict.get('team')
        self.found: bool | None = dict.get('found')
        self.receiving: int | None = dict.get('receiving')
        self.type: str | None = dict.get('type')
        self.data: typing.List[JSONMessagePart] | None = dict.get('data')
        self.item: NetworkItem | None = dict.get('item')

    def print(self):
        if self.message is not None:
            print(self.message)
