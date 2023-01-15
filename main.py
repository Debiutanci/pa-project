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
    def __init__(self, m, fi, alpha, A, s, v_value) -> None:
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
        self.f_przyspieszania = 8500

        self.allow_simulate = True

    @property
    def f_dzialajaca_na_pojazd(self):
        f_oporu_powietrza = sila_oporu_powietrza(self.c, self.A, self.g_powietrza, self.v_value)
        f_tarcia = sila_tarcia(self.fi, self.m, self.g, self.alpha)
        f_zsuwania = sila_zsuwania(self.m, self.g, self.alpha)
        f_oporu = f_oporu_powietrza + f_tarcia + f_zsuwania
        
        wynik = self.f_przyspieszania - f_oporu - self.f_hamowania

        if True:
            print(f"f_oporu_powietrza: {f_oporu_powietrza}")
            print(f"f_tarcia: {f_tarcia}")
            print(f"f_zsuwania: {f_zsuwania}")
            print(f"przyspieszanie: {self.f_przyspieszania}")
            print(f"hamowanie: {self.f_hamowania}")
            print(f"f_dzialajaca_na_pojazd {wynik}")
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
        print(f"iteracja: {t}")
        print(f"delta_s: {self.delta_s()}")
        print("sam1:")
        self.sam_1.log()
        print("sam2:")
        self.sam_2.log()


    @staticmethod
    def get_new_f_przyspieszenia(sam, t):
        start_a = sam.a
        sam.v_value = v(sam.v_zero, sam.a, t)
        while v_km_h(sam.v_value) > 145:
            sam.f_przyspieszania = sam.f_przyspieszania/2
            sam.a = start_a + sam.delta_a
            sam.v_value = v(sam.v_zero, sam.a, t)
            stop = input("++")

        return sam.f_przyspieszania

    def step(self, t):
        # sam 1:
        # if self.sam_1.allow_simulate:
        #     self.sam_1.f_przyspieszania = self.get_new_f_przyspieszenia(
        #         self.sam_1,
        #         t
        #     )
        self.sam_1.a = self.sam_1.delta_a
        self.sam_1.v = v(self.sam_1.v_zero, self.sam_1.a, 1)

        if self.sam_1.v < 0:
            self.sam_1.v = 0

        self.sam_1.s = s(self.sam_1.s_zero, self.sam_1.v_zero, 1, self.sam_1.a)
        self.sam_1.v_zero = self.sam_1.v

        # sam_2
        self.sam_2.a = self.sam_2.delta_a
        self.sam_2.v = v(self.sam_2.v_zero, self.sam_2.a, 1)

        if self.sam_2.v < 0:
            self.sam_2.v = 0

        self.sam_2.s = s(self.sam_2.s_zero, self.sam_2.v_zero, 1, self.sam_2.a)
        self.sam_2.v_zero = self.sam_2.v
        self.memory_1.save(self.sam_1, t)
        self.memory_2.save(self.sam_2, t)
        #input("123")
        print(f"delta  {self.delta_s()}")

        ds = self.delta_s()

        # delta
        self.memory_delta.append(ds)

        #if ds > 100:
        #    print("przyspieszanie=======================================")
        #    self.sam_2.f_przyspieszania = 8500
        #    self.sam_2.f_hamowania = 0
        #elif ds < 100:
        #    print("hamowanie===========================================")
        #    self.sam_2.f_przyspieszania = 0
        #    self.sam_2.f_hamowania = 0
        #if self.sam_2.a < 0:
        #    self.sam_2.a = 0
        #    stop = input("123")

        # estimations
        # if ds > 100:
        #     print("przyspieszanie=======================================")
        #     if len(self.memory_delta) > 1:
        #         if ds < self.memory_delta[-2]:
        #             self.sam_2.f_przyspieszania *= 2
        #         else:
        #             self.sam_2.f_przyspieszania = 8500
        #     else:
        #         self.sam_2.f_przyspieszania = 8500
        #     self.sam_2.f_hamowania = 0
        # elif ds < 100:
        #     print("hamowanie===========================================")
        #     self.sam_2.f_przyspieszania = 0
        #     self.sam_2.f_hamowania = 8500
        # ## stop checker
        # # safety
        # if self.sam_2.a + self.sam_2.delta_a < 0:
        #     self.sam_2.f_hamowania = 0
        #     self.sam_2.f_przyspieszania += 100
        # while self.sam_1.a + self.sam_1.delta_a < 0:
        #     self.sam_1.f_hamowania = 0
        #     self.sam_1.f_przyspieszania += 100


def main():
    m1 = 1000.0 # -masa pojazdu
    fi1 = 0.8 # -współczynnik tarcia
    alpha1 = 0 # math.pi / 6 # -kąt nachylenia równi
    A1 = 4.0 # -powierzchnia czołowa pojazdu
    v1 = 27.0
    s1 = 110.0

    m2 = 1000.0 # -masa pojazdu
    fi2 = 0.8 # -współczynnik tarcia
    alpha2= 0 # math.pi / 6 # -kąt nachylenia równi
    A2 = 4.0 # -powierzchnia czołowa pojazdu
    v2 = 29.0
    s2 = 0.0

    sam_1 = Samochod(m1, fi1, alpha1, A1, s1, v1)
    sam_2 = Samochod(m2, fi2, alpha2, A2, s2, v2)
    r = Regulator(sam_1=sam_1, sam_2=sam_2)

    events = {
        # 95: {"h": 0, "p": 0},
        #120: {"h": 5000, "p": 0},
        #125: {"h": 0, "p": 8500},
        #200: {"h": 10000, "p": 0},
        #205: {"h": 0, "p": 8500},
    }
    simulation_switch_events = [95]

    duration = 600
    for t in range(duration):
        # input("-")
        r.step(t=t)
        r.log(t=t)

        if t in events.keys():
            r.sam_1.f_hamowania = events[t]["h"]
            r.sam_1.f_przyspieszania = events[t]["p"]
        if t in simulation_switch_events:
            r.sam_1.allow_simulate = False



    generate_charts(r.memory_1, r.memory_2, r.memory_delta)
    print(r.memory_delta)

if __name__ == "__main__":
    main()
