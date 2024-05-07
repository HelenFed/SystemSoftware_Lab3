from MMU import MMU
from WorkingSet import WorkingSet
from PageTable import PageTable

if __name__ == "__main__":
    # Кількість сторінок
    total_pages = 5

    # Робочий набір
    page_reference_stream = [6, 4, 2, 5, 6, 50, 500, 100, 50, 3,
                             4, 2, 6, 10, 0, 1, 2, 3, 5, 4, 0, 1, 2]
    working_set = WorkingSet()
    working_set.page_reference_stream = page_reference_stream

    # Таблиця сторінок
    page_table = PageTable(total_pages)

    # Виведення hits і faults (попадань і промахів)
    # Сторінковий промах – це виключна ситуація, яка виникає під час звернення до невідображеної віртуальної сторінки
    MMU.print_hits_and_faults(working_set, page_table)