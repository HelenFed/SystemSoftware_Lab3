from VirtualPage import VirtualPage
class PageTable:
    def __init__(self, num_pages):
        self.pages = [VirtualPage(i) for i in range(num_pages)]