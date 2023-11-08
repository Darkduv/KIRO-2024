from KIRO.export import to_json

class Template : 
    def __init__(self, attr1, attr2, attr3):
        self.attr1 = attr1
        self.attr2 = attr2
        self.attr3 = attr3

class Template2 : 
    def __init__(self, attr1, attr2, attr3):
        self.attr1 = attr1
        self.attr2 = attr2
        self.attr3 = attr3

to_json(
    {1:1, 2:'a', 3:Template(1,2,3), 4:[Template(1,2,3), Template2(1,2,3)]}
)