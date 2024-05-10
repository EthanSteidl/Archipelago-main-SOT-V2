import typing

class ScreenData:


    def __init__(self, text_group: typing.List[str]):
        self.text_group = text_group
        for i in range(len(self.text_group)):
            self.text_group[i] = self.text_group[i].lower()

    def hasMatch(self, text:str):
        if self.__hasTextMatch(text):
            return True
        return False

    def __hasTextMatch(self, txt: str):
        if txt == '':
            return False
        for text_str in self.text_group:
            if text_str in txt:
                return True

        return False
