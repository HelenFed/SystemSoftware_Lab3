from ShowResult import ShowResult
import tkinter as tk
from tkinter import ttk

class MMU:
    # Функція пошуку сторінки
    @staticmethod
    def find_and_update(page_reference, page_table):
        for i in range(len(page_table.pages)):
            # Перевірка чи є така сторінка в таблиці
            if page_table.pages[i].ppn == page_reference:
                # Встановлюємо біт звернення на 1, оскільки сторінка була використана
                page_table.pages[i].r = True
                return True
        return False

    # Функція заміни сторінки
    @staticmethod
    def replace_and_update(page_reference, page_table, pointer):
        while True:
            # Якщо біт біт звернення встановлений на 0 - замінюємо сторінку
            if not page_table.pages[pointer].r:
                page_table.pages[pointer].ppn = page_reference
                # Встановлюємо біт R на 1 для нової сторінки
                page_table.pages[pointer].r = True
                return (pointer + 1) % len(page_table.pages)
            # Якщо біт R встановлений на 1 - скидаємо його на 0
            page_table.pages[pointer].r = False
            pointer = (pointer + 1) % len(page_table.pages)

    # Функція визначення промахів і попадань
    @staticmethod
    def print_hits_and_faults(working_set, page_table):
        show_table = []
        pointer = 0  # вказівник (починаємо з самого початку - сторінки 0)
        pf = 0       # кількість промахів (page fault)
        ph = 0       # кількість попадань (page hits)

        t = 0
        hit = ""
        fs = ["p"] * len(page_table.pages)
        show_table.append(ShowResult("t", "ref", fs, "hit"))
        fs = [""] * len(page_table.pages)
        show_table.append(ShowResult(str(t), "", fs, hit))

        for page_reference in working_set.page_reference_stream:
            t += 1
            hit = "YES"

            # Перевірка чи є необхіжність заміни сторінки
            if not MMU.find_and_update(page_reference, page_table):
                hit = "NO"
                # Заміна сторінки
                pointer = MMU.replace_and_update(page_reference, page_table, pointer)
                pf += 1     # Інкремент значення промахів
            else:
                ph += 1     # Інкремент значення попадань

            fs = []
            for page in page_table.pages:
                if page.ppn != -1:
                    r_str = "1" if page.r else "0"
                    fs.append(f"{page.ppn}({r_str})")
                else:
                    fs.append("*")

            if hit == "NO":
                if pointer == 0:
                    fs[-1] += "<"
                else:
                    fs[pointer - 1] += "<"
            else:
                for i in range(len(fs)):
                    f_str = fs[i][:fs[i].index('(')]
                    if str(page_reference) == f_str:
                        fs[i] += "+"
                        break

            show_table.append(ShowResult(str(t), str(page_reference), fs, hit))

        MMU.out_results(show_table, ph, pf)

    @staticmethod
    def out_results(visualization, ph, pf):
        root = tk.Tk()
        root.title("Lab 3")

        table = ttk.Treeview(root)
        table["columns"] = tuple(range(len(visualization[0].fs) + 2))
        table.heading("#0", text="t")
        table.column("#0", width=50, anchor="center")
        table.heading("#1", text="ref")
        table.column("#1", width=50, anchor="center")
        for i in range(len(visualization[0].fs)):
            table.heading(f"#{i + 2}", text=f"Page {i}")
            table.column(f"#{i + 2}", width=100, anchor="center")
        table.heading(f"#{len(visualization[0].fs) + 2}", text="hit")
        table.column(f"#{len(visualization[0].fs) + 2}", width=50, anchor="center")

        for row in visualization:
            values = [row.ref] + row.fs + [row.hit]
            table.insert("", "end", text=row.t, values=values, tags=())

            for i in range(len(row.fs)):
                if "<" in row.fs[i]:
                    table.item(table.get_children()[-1], tags=("replace",))
                    break
                elif "+" in row.fs[i]:
                    table.item(table.get_children()[-1], tags=("hit",))
                    break
        table.tag_configure("replace", background="red")
        table.tag_configure("hit", background="green")

        table.pack(expand=True, fill="both")

        print(f"Total hits: {ph}\nTotal faults: {pf}")

        root.mainloop()