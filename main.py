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
        self.v = v_value
        self.s = s
        self.s_zero = s

        self.f_hamowania = 0
        self.static_f_hamowania = f_przyspieszania/17.0
        self.f_przyspieszania = f_przyspieszania
        self.static_f_przyspieszenia = f_przyspieszania

        self.allow_simulate = True

        self.last_multiplier = 1.5
        self.brake_last_multiplier = 1.5

    @property
    def f_dzialajaca_na_pojazd(self):
        f_oporu_powietrza = sila_oporu_powietrza(self.c, self.A, self.g_powietrza, self.v)
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

def generate_charts_1(sm1, sm2, memory_delta):
    plt.subplot(3, 5, 1, title="1: v (m/s)")
    plt.plot(sm1.t, sm1.v)
    plt.subplot(3, 5, 2, title="1: s (m)")
    plt.plot(sm1.t, sm1.s)
    plt.subplot(3, 5, 3, title="1: a (m/s^2)")
    plt.plot(sm1.t, sm1.a)
    plt.subplot(3, 5, 4, title="1: przys (N)")
    plt.plot(sm1.t, sm1.przys)
    plt.subplot(3, 5, 5, title="1: ham (N)")
    plt.plot(sm1.t, sm1.ham)
    plt.subplot(3, 5, 6, title="2: v (m/s)")
    plt.plot(sm1.t, sm2.v)
    plt.subplot(3, 5, 7, title="2: s (m)")
    plt.plot(sm1.t, sm2.s)
    plt.subplot(3, 5, 8, title="2: a (m/s^2)")
    plt.plot(sm1.t, sm2.a)
    plt.subplot(3, 5, 9, title="2: przys (N)")
    plt.plot(sm1.t, sm2.przys)
    plt.subplot(3, 5, 10, title="2: ham (N)")
    plt.plot(sm1.t, sm2.ham)
    plt.subplot(3, 5, 11, title="delta s (m)")
    plt.plot(sm1.t, memory_delta)
    plt.show()


def generate_charts_2(sm1, sm2, memory_delta):
    plt.subplot(3, 5, 1, title="1: v (m/s)")
    plt.plot(sm1.t, sm1.v)
    plt.plot(sm1.t, sm2.v)
    plt.subplot(3, 5, 2, title="1: s (m)")
    plt.plot(sm1.t, sm1.s)
    plt.plot(sm1.t, sm2.s)
    plt.subplot(3, 5, 3, title="1: a (m/s^2)")
    plt.plot(sm1.t, sm1.a)
    plt.plot(sm1.t, sm2.a)
    plt.subplot(3, 5, 4, title="1: przys (N)")
    plt.plot(sm1.t, sm1.przys)
    plt.plot(sm1.t, sm2.przys)
    plt.subplot(3, 5, 5, title="1: ham (N)")
    plt.plot(sm1.t, sm1.ham)
    plt.plot(sm1.t, sm2.ham)
    plt.subplot(3, 5, 11, title="delta s (m)")
    plt.plot(sm1.t, memory_delta)
    plt.show()

def generate_charts_3(sm1, sm2, memory_delta):
    plt.subplot(3, 5, 1, title="1: v (m/s)")
    plt.plot(sm1.t, sm1.v)
    plt.subplot(3, 5, 2, title="1: s (m)")
    plt.plot(sm1.t, sm1.s)
    plt.subplot(3, 5, 3, title="1: a (m/s^2)")
    plt.plot(sm1.t, sm1.a)
    plt.subplot(3, 5, 4, title="1: przys (N)")
    plt.plot(sm1.t, sm1.przys, 'tab:green')
    plt.subplot(3, 5, 5, title="1: ham (N)")
    plt.plot(sm1.t, sm1.ham, 'tab:red')
    plt.subplot(3, 5, 6, title="2: v (m/s)")
    plt.plot(sm1.t, sm2.v, 'tab:orange')
    plt.subplot(3, 5, 7, title="2: s (m)")
    plt.plot(sm1.t, sm2.s, 'tab:orange')
    plt.subplot(3, 5, 8, title="2: a (m/s^2)")
    plt.plot(sm1.t, sm2.a, 'tab:orange')
    plt.subplot(3, 5, 9, title="2: przys (N)")
    plt.plot(sm1.t, sm2.przys, 'tab:green')
    plt.subplot(3, 5, 10, title="2: ham (N)")
    plt.plot(sm1.t, sm2.ham, 'tab:red')
    plt.subplot(3, 5, 15, title="delta s (m)")
    plt.plot(sm1.t, memory_delta, 'tab:pink')

    plt.subplot(3, 5, 13, title="1,2: v (m/s)")
    plt.plot(sm1.t, sm1.v)
    plt.plot(sm1.t, sm2.v)
    plt.subplot(3, 5, 14, title="1,2: s (m)")
    plt.plot(sm1.t, sm1.s)
    plt.plot(sm1.t, sm2.s)
    plt.show()

# def generate_charts_4(sm1, sm2, memory_delta):

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
        self.memory_delta.append(self.delta_s())

        current_ds = self.delta_s()


        self.sam_2.v = v(self.sam_2.v_zero, self.sam_2.a, 1)

        if self.sam_2.v < 0:
            self.sam_2.v = 0
            self.sam_2.a = 0
            self.sam_2.f_hamowania = 0

        # safe
        if s(self.sam_2.s_zero, self.sam_2.v_zero, 1, self.sam_2.a) < self.sam_2.s:
            raise Exception([self.sam_2.s_zero, self.sam_2.v_zero, 1, self.sam_2.a, s(self.sam_2.s_zero, self.sam_2.v_zero, 1, self.sam_2.a)])

        self.sam_2.s = s(self.sam_2.s_zero, self.sam_2.v_zero, 1, self.sam_2.a)
        self.sam_2.v_zero = self.sam_2.v
        self.sam_2.s_zero = self.sam_2.s

        if self.sam_2.v >= 0:
            self.sam_2.a = self.sam_2.delta_a
            if abs(self.sam_2.a) > 2*self.sam_2.v:
                self.sam_2.a = 2*self.sam_2.v

        if self.sam_2.v == 0 and self.sam_2.a  == 0 and self.sam_2.f_przyspieszania > 0 and self.sam_2.f_hamowania == 0:
            self.sam_2.a = self.sam_2.delta_a
            self.sam_2.v = v(0, self.sam_2.a, 1)

        # delta and memory
        self.memory_1.save(self.sam_1, t)
        self.memory_2.save(self.sam_2, t)

        # stop = input(t)
        if current_ds < 0:
            input(f"ZDERZENIE {t}")

        # estimations
        if current_ds < 90:

            if self.sam_2.v != 0:
                self.sam_2.f_przyspieszania = 0
                if len(self.memory_delta) > 1:
                    if self.sam_2.f_hamowania == 0:
                        self.sam_2.f_hamowania = self.sam_2.static_f_hamowania
                    
                    div_elem = self.memory_delta[-2]/(self.memory_delta[-1]**2)
                    # input(div_elem)
                    self.sam_2.f_hamowania *= float(2.0 + abs(div_elem))
                    if self.memory_delta[-1] < 25:
                        self.sam_2.f_hamowania += 20000

                    if self.sam_2.f_hamowania > 20000:
                        self.sam_2.f_hamowania = 20000

        elif current_ds > 150:
            self.sam_2.f_hamowania = 0
            self.sam_2.f_przyspieszania = self.sam_2.static_f_przyspieszenia
            if len(self.memory_delta) > 1:
                if self.memory_delta[-1] > self.memory_delta[-2]:
                    if v(self.sam_2.v_zero, self.sam_2.a, 1) < 45:
                        self.sam_2.f_przyspieszania *= 1.1

        else:
            self.sam_2.last_multiplier = 1.5
            self.sam_2.brake_last_multiplier = 1.5
            self.sam_2.f_przyspieszania = self.sam_2.static_f_przyspieszenia
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

    m3 = 1150.0 # -masa pojazdu
    fi3 = 0.75 # -współczynnik tarcia
    alpha3 = math.pi / 6 # -kąt nachylenia równi
    A3 = 4.0 # -powierzchnia czołowa pojazdu
    v3 = 26.5
    s3 = 55.0
    f_3_przyspieszania = 15000

    m4 = 1100.0 # -masa pojazdu
    fi4 = 0.75 # -współczynnik tarcia
    alpha4= math.pi / 6 # -kąt nachylenia równi
    A4 = 2.5 # -powierzchnia czołowa pojazdu
    v4 = 28.0
    s4 = 0.0
    f_4_przyspieszania = 12100

    sam_1 = Samochod(m1, fi1, alpha1, A1, s1, v1, f_1_przyspieszania)
    sam_2 = Samochod(m2, fi2, alpha2, A2, s2, v2, f_2_przyspieszania)
    sam_3 = Samochod(m3, fi3, alpha3, A3, s3, v3, f_3_przyspieszania)
    sam_4 = Samochod(m4, fi4, alpha4, A4, s4, v4, f_4_przyspieszania)
    r12 = Regulator(sam_1=sam_1, sam_2=sam_2)
    r34 = Regulator(sam_1=sam_3, sam_2=sam_4)

    events_1_12 = {
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
        81: {"h": 0, "p": 7000},
        89: {"h": 0, "p": 8500},
        105: {"h": 0, "p": 8900},
        112: {"h": 0, "p": 6000},
        115: {"h": 0, "p": 7000},
        120: {"h": 0, "p": 8900},
    }
    duration_1_12 = 120
    events_2_12 = {
        7: {"h": 0, "p": 6000},
        8: {"h": 0, "p": 8900},
        20: {"h": 0, "p": 6000},
        21: {"h": 0, "p": 8900},
        30: {"h": 0, "p": 6000},
    }
    duration_2_12 = 40
    events_3_12 = {
        7: {"h": 0, "p": 6000},
        8: {"h": 0, "p": 8900},
        20: {"h": 0, "p": 6000},
        21: {"h": 0, "p": 8900},
        29: {"h": 0, "p": 6000},
        32: {"h": 0, "p": 7500},
        33: {"h": 0, "p": 8000},
        41: {"h": 0, "p": 5500},
        43: {"h": 0, "p": 8500},
    }
    duration_3_12 = 50

    events_1_34 = {
        7: {"h": 0, "p": 7500},
        8: {"h": 0, "p": 15000},
        20: {"h": 0, "p": 7500},
        21: {"h": 0, "p": 15000},
        29: {"h": 0, "p": 7500},
        32: {"h": 0, "p": 7500},
        33: {"h": 0, "p": 8000},
        41: {"h": 0, "p": 5500},
        43: {"h": 0, "p": 8500},
        54: {"h": 0, "p": 7500},
        55: {"h": 0, "p": 8500},
        81: {"h": 0, "p": 7000},
        89: {"h": 0, "p": 8500},
        105: {"h": 0, "p": 15000},
        112: {"h": 0, "p": 7500},
        115: {"h": 0, "p": 7000},
        120: {"h": 0, "p": 15000}
    }
    duration_1_34 = 120
    events_2_34 = {
        7: {"h": 0, "p": 7500},
        8: {"h": 0, "p": 12500},
        20: {"h": 0, "p": 6500},
        21: {"h": 0, "p": 10000},
        30: {"h": 0, "p": 7500},
    }
    duration_2_34 = 50
    events_3_34 = {
        7: {"h": 0, "p": 7500},
        8: {"h": 0, "p": 12100},
        12: {"h": 0, "p": 8000},
        20: {"h": 0, "p": 7500},
        21: {"h": 0, "p": 15000},
        29: {"h": 0, "p": 7500},
        32: {"h": 0, "p": 12100},
        33: {"h": 0, "p": 9000},
        41: {"h": 0, "p": 7000},
        43: {"h": 0, "p": 14100},
    }
    duration_3_34 = 62


    """============SYMULACJE============"""

    """SAM 1, SAM 2"""

    # events = events_1_12
    # duration = duration_1_12
    # r = r12

    # events = events_2_12
    # duration = duration_2_12
    # r = r12

    events = events_3_12
    duration = duration_3_12
    r = r12

    """SAM 3, SAM 4"""

    # events = events_1_34
    # duration = duration_1_34
    # r = r34

    # events = events_2_34
    # duration = duration_2_34
    # r = r34

    # events = events_3_34
    # duration = duration_3_34
    # r = r34

    for t in range(duration):
        r.step(t=t)
        r.log(t=t)
        if t in events.keys():
            r.sam_1.f_hamowania = events[t]["h"]
            r.sam_1.f_przyspieszania = events[t]["p"]

    generate_charts_3(r.memory_1, r.memory_2, r.memory_delta)
    print(r.memory_delta)


if __name__ == "__main__":
    main()
