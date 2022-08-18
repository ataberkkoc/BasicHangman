import os


class Types:

    BASE_PATH = os.path.join(os.path.abspath(os.curdir), "sentences")
    TYPE_COUNT = 3
    TYPE_PROGRAMMING_LANG = 1
    TYPE_MOVIES = 2
    TYPE_FOODS = 3
    type_dict = {
        1: os.path.join(BASE_PATH,"programminglanguages.txt"),
        2: os.path.join(BASE_PATH,"movies.txt"),
        3: os.path.join(BASE_PATH,"foods.txt")
    }

    @classmethod
    def get_type(cls, type_code):
        return cls.type_dict[type_code]
