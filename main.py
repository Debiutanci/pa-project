import math
import matplotlib.pyplot as plt


def v_km_h(vms):
    return vms*3.6

def sila_tarcia(fi, m, g, alpha):
    return fi*m*g*math.cos(alpha)

def sila_zsuwania(m, g, alpha):
    return m*g*math.sin(alpha)

def sila_oporu_powietrza(c, A, g_powietrza, v_value):
    return c*A*g_powietrza*((v_value*v_value)/2)

def v(v_zero, a, t):
    return v_zero + a*t

def s(s_zero, v_zero, t, a):
    return s_zero + v_zero*t + (a*t*t)/2


class Samochod:
    def __init__(self, m, fi, alpha, A, s, v_value, f_przyspieszania) -> None:
        # static vars
        self.g = 9.81
        self.c = 0.3
        self.g_powietrza = 1.1225

        # dynamic vars
        self.m = m
        self.fi = fi
        self.alpha = alpha
        self.A = A

        self.a = 0.0
        self.v_zero = v_value
        self.v_value = v_value
        self.s = s
        self.s_zero = s

        self.f_hamowania = 0
        self.f_przyspieszania = f_przyspieszania

        self.allow_simulate = True

        self.last_multiplier = 1.5
        self.brake_last_multiplier = 1.5

    @property
    def f_dzialajaca_na_pojazd(self):
        f_oporu_powietrza = sila_oporu_powietrza(self.c, self.A, self.g_powietrza, self.v_value)
        f_tarcia = sila_tarcia(self.fi, self.m, self.g, self.alpha)
        f_zsuwania = sila_zsuwania(self.m, self.g, self.alpha)
        f_oporu = f_oporu_powietrza + f_tarcia + f_zsuwania
        
        wynik = self.f_przyspieszania - f_oporu - self.f_hamowania

        if False:
            print(f"f_oporu_powietrza: {f_oporu_powietrza}")
            print(f"f_tarcia: {f_tarcia}")
            print(f"f_zsuwania: {f_zsuwania}")
            print(f"przyspieszanie: {self.f_przyspieszania}")
            print(f"hamowanie: {self.f_hamowania}")
            print(f"f_dzialajaca_na_pojazd {wynik}")

        print(f"======================================================================= {wynik}")
        return wynik

    @property
    def delta_a(self):
        return self.f_dzialajaca_na_pojazd/self.m

    def log(self):
        print(f"v: {self.v} ; s: {self.s} ; a: {self.a} p: {self.f_przyspieszania} ; h: {self.f_hamowania}")

def generate_charts(sm1, sm2, memory_delta):
    plt.subplot(3, 5, 1, title="1: v")
    plt.plot(sm1.t, sm1.v)
    plt.subplot(3, 5, 2, title="1: s")
    plt.plot(sm1.t, sm1.s)
    plt.subplot(3, 5, 3, title="1: a")
    plt.plot(sm1.t, sm1.a)
    plt.subplot(3, 5, 4, title="1: przys")
    plt.plot(sm1.t, sm1.przys)
    plt.subplot(3, 5, 5, title="1: ham")
    plt.plot(sm1.t, sm1.ham)
    plt.subplot(3, 5, 6, title="2: v")
    plt.plot(sm1.t, sm2.v)
    plt.subplot(3, 5, 7, title="2: s")
    plt.plot(sm1.t, sm2.s)
    plt.subplot(3, 5, 8, title="2: a")
    plt.plot(sm1.t, sm2.a)
    plt.subplot(3, 5, 9, title="2: przys")
    plt.plot(sm1.t, sm2.przys)
    plt.subplot(3, 5, 10, title="2: ham")
    plt.plot(sm1.t, sm2.ham)
    plt.subplot(3, 5, 10, title="2: ham")
    plt.plot(sm1.t, sm2.ham)

    plt.subplot(3, 5, 11, title="delta s")
    plt.plot(sm1.t, memory_delta)
    plt.show()

class SamMemory:
    def __init__(self) -> None:
        self.t = []
        self.v = []
        self.s = []
        self.a = []
        self.przys = []
        self.ham = []

    def save(self, sam, t):
        self.t.append(t)
        self.v.append(sam.v)
        self.s.append(sam.s)
        self.a.append(sam.a)
        self.przys.append(sam.f_przyspieszania)
        self.ham.append(sam.f_hamowania)


class Regulator:
    def __init__(self, sam_1, sam_2) -> None:
        self.sam_1 = sam_1
        self.sam_2 = sam_2

        self.memory_1 = SamMemory()
        self.memory_2 = SamMemory()
        self.memory_delta = []

        self.warnings = 0

    def delta_s(self):
        return self.sam_1.s - self.sam_2.s

    def log(self, t):
        print(f"-------------------------------------------------------------------------------------------------------------iteracja: {t}")
        print(f"delta_s: {self.delta_s()}")
        print("sam1:")
        self.sam_1.log()
        print("sam2:")
        self.sam_2.log()


    @staticmethod
    def get_new_f_przyspieszenia(sam, vmax=145):
        print("///////////////////////////////////////////////////////////////////////////////////////////////")
        start_a = sam.a
        sam.v_value = v(sam.v_zero, sam.a, 1)
        while v_km_h(sam.v_value) > vmax:
            sam.f_przyspieszania = sam.f_przyspieszania/2
            sam.a = sam.delta_a
            sam.v_value = v(sam.v_zero, sam.a, 1)
            stop = input("++")

        return sam.f_przyspieszania

    def step(self, t):
        self.sam_1.v = v(self.sam_1.v_zero, self.sam_1.a, 1)
        if self.sam_1.v < 0:
            self.sam_1.v = 0
            self.sam_1.a = 0
        else:
            self.sam_1.a = self.sam_1.delta_a
        self.sam_1.s = s(self.sam_1.s_zero, self.sam_1.v_zero, 1, self.sam_1.a)
        self.sam_1.v_zero = self.sam_1.v
        self.sam_1.s_zero = self.sam_1.s
        self.sam_1.a = self.sam_1.delta_a
        

        self.sam_2.v = v(self.sam_2.v_zero, self.sam_2.a, 1)
        if self.sam_2.v < 0:
            self.sam_2.v = 0
            self.sam_2.a = 0
        self.sam_2.s = s(self.sam_2.s_zero, self.sam_2.v_zero, 1, self.sam_2.a)
        self.sam_2.v_zero = self.sam_2.v
        self.sam_2.s_zero = self.sam_2.s
        self.sam_2.a = self.sam_2.delta_a
        if abs(self.sam_2.a) > 2*self.sam_2.v:
            self.sam_2.a = 2*self.sam_2.v

        # delta and memory
        self.memory_1.save(self.sam_1, t)
        self.memory_2.save(self.sam_2, t)

        current_ds = self.delta_s()
        self.memory_delta.append(current_ds)
        if current_ds < 0:
            input(f"ZDERZENIE {t}")
            # raise Exception("X")

        # estimations
        if current_ds < 90:
            self.sam_2.f_przyspieszania = 0
            if len(self.memory_delta) > 1:
                if self.sam_2.f_hamowania == 0:
                    self.sam_2.f_hamowania = 500
                
                div_elem = self.memory_delta[-2]/(self.memory_delta[-1]**2)
                self.sam_2.f_hamowania *= float(2.0 + abs(div_elem))
                if self.memory_delta[-1] < 25:
                    self.sam_2.f_hamowania += 10000

                if self.sam_2.f_hamowania > 20000:
                    self.sam_2.f_hamowania = 20000

        elif current_ds > 120:
            self.sam_2.f_hamowania = 0
            self.sam_2.f_przyspieszania = 8500
            # if len(self.memory_delta) > 1:
            #     if self.memory_delta[-1] > self.memory_delta[-2]:
            #         if v(self.sam_2.v_zero, self.sam_2.a, 1) < 35:
            #             self.sam_2.f_przyspieszania *= 1.1
        else:
            self.sam_2.last_multiplier = 1.5
            self.sam_2.brake_last_multiplier = 1.5
            self.sam_2.f_przyspieszania = 8500
            self.sam_2.f_hamowania = 0


def main():
    m1 = 1000.0 # -masa pojazdu
    fi1 = 0.8 # -współczynnik tarcia
    alpha1 = 0 # math.pi / 6 # -kąt nachylenia równi
    A1 = 4.0 # -powierzchnia czołowa pojazdu
    v1 = 27.0
    s1 = 110.0
    f_1_przyspieszania = 8500

    m2 = 1000.0 # -masa pojazdu
    fi2 = 0.8 # -współczynnik tarcia
    alpha2= 0 # math.pi / 6 # -kąt nachylenia równi
    A2 = 2 # -powierzchnia czołowa pojazdu
    v2 = 29.0
    s2 = 0.0
    f_2_przyspieszania = 8500

    sam_1 = Samochod(m1, fi1, alpha1, A1, s1, v1, f_1_przyspieszania)
    sam_2 = Samochod(m2, fi2, alpha2, A2, s2, v2, f_2_przyspieszania)
    r = Regulator(sam_1=sam_1, sam_2=sam_2)

    events_1 = {
        7: {"h": 0, "p": 6000},
        8: {"h": 0, "p": 8900},
        20: {"h": 0, "p": 6000},
        21: {"h": 0, "p": 8900},
        29: {"h": 0, "p": 6000},
        32: {"h": 0, "p": 7500},
        33: {"h": 0, "p": 8000},
        41: {"h": 0, "p": 5500},
        43: {"h": 0, "p": 8500},
        54: {"h": 0, "p": 7500},
        55: {"h": 0, "p": 8500},
        81: {"h": 0, "p": 6000},
        89: {"h": 0, "p": 8500},
        100: {"h": 0, "p": 6000},
        105: {"h": 0, "p": 8900},
        112: {"h": 0, "p": 6000},
        115: {"h": 0, "p": 7000},
        120: {"h": 0, "p": 8900},
        135: {"h": 0, "p": 6000},
        137: {"h": 0, "p": 8900},
    }
    duration_1 = 140

    events_2 = {
        7: {"h": 0, "p": 6000},
        8: {"h": 0, "p": 8900},
        20: {"h": 0, "p": 6000},
        21: {"h": 0, "p": 8900},
        30: {"h": 0, "p": 6000},
    }
    duration_2 = 45

    events_3 = {
        7: {"h": 0, "p": 6000},
        8: {"h": 0, "p": 8335},
    }
    duration_3 = 140

    events = events_1
    duration = duration_1
    for t in range(duration):
        r.step(t=t)
        r.log(t=t)
        #stop = input(t)
        if t in events.keys():
            r.sam_1.f_hamowania = events[t]["h"]
            r.sam_1.f_przyspieszania = events[t]["p"]

    generate_charts(r.memory_1, r.memory_2, r.memory_delta)
    print(r.memory_delta)

if __name__ == "__main__":
    main()
