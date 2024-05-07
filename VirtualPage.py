class VirtualPage:
    def __init__(self, ppn):
        self.p = False  # біт присутності
        self.r = False  # біт звернення
        self.m = False  # біт права модифікації вмісту
        self.ppn = ppn  # номер фізичної сторінки в яку відображена віртуальна сторінка.