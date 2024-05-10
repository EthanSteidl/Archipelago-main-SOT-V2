import typing
import cv2
import numpy as np
import PIL

class ScreenData:


    def __init__(self, text_group: typing.List[str] | None = None, image_group: typing.List[str] | None = None):
        self.text_group = text_group if text_group is not None else []
        for i in range(len(self.text_group)):
            self.text_group[i] = self.text_group[i].lower()

        self.image_group = image_group if image_group is not None else []

    def hasMatch(self, text: str = None, image = None):
        if text is not None and self.__hasTextMatch(text):
            return True
        if image is not None and self.__hasImageMatch(image):
            return True
        return False

    def __hasTextMatch(self, txt: str):
        if txt == '':
            return False
        for text_str in self.text_group:
            if text_str in txt:
                return True

        return False

    def __hasImageMatch(self, image_scr) -> bool:

        found = False
        for file_prefix in self.image_group:
            filename = "{}{}{}".format('..\\Items\\Images\\', file_prefix, ".png")
            try:
                template = cv2.imread(filename)
                template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                #cv2.imshow('img',template)
                #cv2.waitKey(0)
            except Exception as e:
                print("ERROR: File image recognition failed to find path {}".format((filename)), e)
                continue


            #w, h = template.shape[:-1]
            try:
                image_scr = cv2.imread("screen_cap.png")
                image_scr = cv2.cvtColor(image_scr, cv2.COLOR_RGB2GRAY)
                w, h = template.shape[::-1]
                #cv2.imshow('img', image_scr)
                #cv2.waitKey()
                res = cv2.matchTemplate(image_scr, template, cv2.TM_CCOEFF_NORMED)


                threshold = .9
                loc = np.where(res >= threshold)
                #resS = cv2.resize(loc, (960, 540))
                #cv2.imshow(file_prefix, resS)
                #cv2.waitKey(0)

                found_in_loop = False
                for pt in zip(*loc[::-1]):
                    cv2.rectangle(image_scr, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                    found_in_loop = True
                    break



                if found_in_loop:


                    #cv2.imshow('img',template)
                    #cv2.waitKey(0)
                    #cv2.imshow('Detected', image_scr)
                    #cv2.waitKey()
                    #print("Found image = YES")
                    return True
                    #cv2.imwrite('result.png', image_scr)
            except Exception as e:
                print("Error: Image compare failed. ", e)

        return found