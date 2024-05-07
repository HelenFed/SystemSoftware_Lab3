class ShowResult:
    def __init__(self, t, ref, fs, hit):
        self.t = t          # номер доступу до сторінки
        self.ref = ref      # значення сторінки, до якої треба доступитися
        self.fs = fs        # номера сторінок зі значенням біта звернення
        self.hit = hit      # значення YES або NO чи було попадання чи ні (промах)