import typing

class ScreenData:


    def __init__(self, text_group: typing.List[str]):
        self.text_group = text_group

    def hasMatch(self, text:str):
        if self.__hasTextMatch(text):
            return True
        return False

    def __hasTextMatch(self, txt: str):
        if txt == '':
            return False
        for text_str in self.text_group:
            if txt in text_str:
                return True

        return False
