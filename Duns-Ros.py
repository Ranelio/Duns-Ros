PressureBuf = float(input("Введите устьевое давление (МПа):"))
PressureBot = float(input("Введите забойное давление (МПа):"))
Q = float(input("Введите дебит жидкости (м3/сут):"))
WaterCont = float(input("Введите обводненность (доли ед.):"))
GasFactor = float(input("Введите газовый фактор (м3/м3):"))
DensityOil = float(input("Введите плотность нефти (кг/м3):"))
DensityWater = float(input("Введите плотность воды (кг/м3):"))
DensityGas = float(input("Введите плотность газа (кг/м3):"))
VolCoefOil = float(input("Введите объемный коэффициент нефти (м3/м3):"))
VolCoefGas = float(input("Введите объемный коэффициент газа (м3/м3):"))
ViscosityOil = float(input("Введите вязкость нефти (сП):"))
ViscosityWater = float(input("Введите вязкость воды (сП):"))
SurfTensOil = float(input("Введите поверхностоное натяжение нефти (кг/с2):"))
SurfTensWat = float(input("Введите поверхностоное натяжение воды (кг/с2):"))
Diameter = float(input("Введите диаметр скважины (м):"))
Lenght = float(input("Введите длину скважины (м):"))

Vl = Q * VolCoefOil / (3.14 * Diameter ** 2 * 0.25 * 86400)  # velocity of liquid
Vg = Q * GasFactor * VolCoefGas / (3.14 * Diameter ** 2 * 0.25 * 86400)  # velocity of gas
pl = WaterCont * (DensityWater - DensityOil) + DensityOil  # density
ml = ViscosityOil * (1 - WaterCont) + ViscosityWater * WaterCont  # viscosity of liquid
ol = SurfTensOil * (1 - WaterCont) + SurfTensWat * WaterCont  # surface tension of liquid
ql = VolCoefOil / (VolCoefOil + VolCoefOil)  # oil production per volume


Nlv = 3.178 * Vl * (pl / ol) ** 0.25
Ngv = 3.178 * Vg * (pl / ol) ** 0.25
Nd = 99.083 * Diameter * (pl / ol) ** 0.5
Nl = 0.314 * ml * (1 / (pl * ol ** 3)) ** 0.25
print("Nlv = " + str(Nlv))
print("Ngv = " + str(Ngv))
print("Nd = " + str(Nd))
print("Nl = " + str(Nl))

L1 = float(input("Введите параметр L1:"))
L2 = float(input("Введите параметр L2:"))


def define_fp():
    Nbs = L1 + L2 * Nlv
    Nstr = 50 + 36 * Nlv
    Ntrm = 75 + 84 * Nlv ** 0.75
    if (Ngv < Nbs):
        return "BUBBLE"
    if (Nbs < Ngv and Ngv < Nstr):
        return "SLUG"
    if (Ngv > Ntrm):
        return "MIST"
    if (Nstr < Ngv and Ngv < Ntrm):
        return "TRANSITION"


FlowType = define_fp()
if (FlowType == "BUBBLE"):
    F1 = float(input("Введите параметр F1:"))
    F2 = float(input("Введите параметр F2:"))
    F3 = float(input("Введите параметр F3:"))
    F4 = float(input("Введите параметр F4:"))
if (FlowType == "SLUG"):
    F5 = float(input("Введите параметр F5:"))
    F6 = float(input("Введите параметр F6:"))
    F7 = float(input("Введите параметр F7:"))
print("FlowType = " + str(FlowType))


def calc_grad_grav(FlowType):
    if (FlowType == "BUBBLE"):
        s = F1 + F2 * Nlv + (F3 - F4 / Nd) * (Ngv / (1 + Nlv)) ** 2
    if (FlowType == "SLUG"):
        s = (1 + F5) * (Ngv ** 0.982 + 0.029 * Nd + F6) / (1 + F7 * Nlv)
    if (FlowType == "MIST"):
        ps = pl * ql + DensityGas * (1 - ql)
    if (FlowType == "BUBBLE" or FlowType == "SLUG"):
        vs = (s * (ol / pl) ** 0.25) / 1.938
        D = (Vg + Vl - vs) ** 2 + 4 * vs * Vl
        Hl1 = (-(Vg + Vl - vs) + D ** 0.5) / (2 * vs)
        Hl2 = (-(Vg + Vl - vs) - D ** 0.5) / (2 * vs)
        if (Hl1 > 0 and Hl1 < 1):
            Hl = Hl1
        else:
            Hl = Hl2
        ps = pl * Hl + DensityGas * (1 - Hl)
    print("Градиент давления обусловленный гравитацией (кг/м3) = " + str(ps))


calc_grad_grav(FlowType)
a = input()


def calc_grad():
    """
    Функция, вычисляющая общий градиент давления

    :return:
    """
    pass
    # dp_dl
    # return dp_dl


def calc_grad_fric():
    """
    Функция, вычисляющая градиент давления на трение

    :return:
    """
    pass
    # dp_dl
    # return dp_dl


def calc_pressure():
    """
    Функция, определяющая давление в трубе путем интегрирования градиента

    :return:
    """
    pass
    # dp_dl
    # return dp_dl
