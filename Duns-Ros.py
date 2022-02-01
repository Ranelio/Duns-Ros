from typing import Any

import math as m
import matplotlib.pyplot as plt
import numpy as np

# PressureBuf = float(input("Введите устьевое давление (бар):"))
PressureBuf = 0
# Lenght = float(input("Введите длину скважины (м):"))
Lenght = 3000


def DunsRos(Q):
    # WaterCont = float(input("Введите обводненность (доли ед.):"))
    WaterCont = 0.1
    # GasFactor = float(input("Введите газовый фактор (м3/м3):"))
    GasFactor = 100
    # DensityOil = float(input("Введите плотность нефти (кг/м3):"))
    DensityOil = 800
    # DensityWater = float(input("Введите плотность воды (кг/м3):"))
    DensityWater = 1100
    # DensityGas = float(input("Введите плотность газа (кг/м3):"))
    DensityGas = 90
    # VolCoefOil = float(input("Введите объемный коэффициент нефти (м3/м3):"))
    VolCoefOil = 1.1
    # VolCoefGas = float(input("Введите объемный коэффициент газа (м3/м3):"))
    VolCoefGas = 0.09
    # ViscosityOil = float(input("Введите вязкость нефти (Па*с/сП = Па*С*10-3):"))
    ViscosityOil = 0.003
    # ViscosityWater = float(input("Введите вязкость газа (Па*с/сП = Па*С*10-3):"))
    ViscosityGas = 0.00001
    # ViscosityWater = float(input("Введите вязкость воды (Па*с/сП = Па*С*10-3):"))
    ViscosityWater = 0.001
    # SurfTensOil = float(input("Введите поверхностоное натяжение нефти (кг/с2):"))
    SurfTensOil = 0.002
    # SurfTensWat = float(input("Введите поверхностоное натяжение воды (кг/с2):"))
    SurfTensWat = 0.007
    # Diameter = float(input("Введите диаметр скважины (м):"))
    Diameter: Any = 0.15
    # Roughness = float(input("Введите шероховатость трубы (м):"))
    Roughness = 0.00002

    Vl = Q * VolCoefOil / (3.14 * Diameter ** 2 * 0.25 * 86400)  # velocity of liquid
    Vg = Q * GasFactor * VolCoefGas / (3.14 * Diameter ** 2 * 0.25 * 86400)  # velocity of gas
    pl = WaterCont * (DensityWater - DensityOil) + DensityOil  # density
    ml = ViscosityOil * (1 - WaterCont) + ViscosityWater * WaterCont  # viscosity of liquid
    ol = SurfTensOil * (1 - WaterCont) + SurfTensWat * WaterCont  # surface tension of liquid
    ql = VolCoefOil / (VolCoefOil + VolCoefGas)  # oil production per volume

    Nlv = 3.178 * Vl * (pl / ol) ** 0.25
    Ngv = 3.178 * Vg * (pl / ol) ** 0.25
    Nd = 99.083 * Diameter * (pl / ol) ** 0.5
    Nl = 0.314 * ml * (1 / (pl * ol ** 3)) ** 0.25

    def interpolation(filename, Parameter, Parameter2, Parameter3):  # creating x and y massive
        arr1 = []
        arr2 = []
        abs_arr1 = []
        j = 0
        i = 0
        with open(filename) as f:
            for pair in f:
                x, y = pair.split()
                arr1.append(x)
                arr2.append(y)
                arr1 = [float(elem) for elem in arr1]
                arr2 = [float(elem) for elem in arr2]
                maxarr1 = max(arr1)
                minarr1 = min(arr1)
            # print(arr1)

            if Parameter >= maxarr1:
                Parameter2 = ((Parameter - arr1[-1]) * (arr2[-2] - arr2[-1]) / (arr1[-2] - arr1[-1] + 0.0001)) + arr2[
                    -1]
            if Parameter <= minarr1:
                Parameter2 = ((Parameter - arr1[0]) * (arr2[1] - arr2[0]) / (arr1[1] - arr1[0] + 0.0001)) + arr2[0]
            else:
                for i, elem in enumerate(arr1):  # creating new massive for estimating value of differences
                    arr1[i] = arr1[i] - Parameter
                    i += 1
                    # print(arr1)
                    abs_arr1 = list(map(abs, arr1))  # abs value of massive
                    # print(abs_arr1)
                    minim = abs_arr1[0]
                j = 0
                for i, elem in enumerate(abs_arr1):  # estimating min value and number of string
                    if abs_arr1[i] < minim:
                        minim = abs_arr1[i]
                        j += 1
                    i += 1
                mini = arr1[j]
                # print(mini, j)
                if mini <= 0:
                    Parameter2 = ((Parameter - (arr1[j] + Parameter)) * (arr2[j - 1] - arr2[j]) / (
                            (arr1[j - 1] + Parameter) - (arr1[j] + Parameter) + 0.0001)) + arr2[j]
                else:
                    Parameter2 = ((Parameter - (arr1[j - 1] + Parameter)) * (arr2[j] - arr2[j - 1]) / (
                            (arr1[j] + Parameter) - (arr1[j - 1] + Parameter) + 0.0001)) + arr2[j - 1]
            return Parameter2

    def MUDI(RoughCoef):
        a = [0.00001, 0.00005, 0.0001, 0.0002, 0.0004, 0.0006, 0.0008, 0.001, 0.002, 0.004, 0.006, 0.008, 0.01, 0.015,
             0.02,
             0.03, 0.04, 0.05]
        for i, elem in enumerate(a):
            a[i] = a[i] - RoughCoef
            i += 1
        # print(arr1)
        abs_a = list(map(abs, a))
        # print(abs_arr1)
        minim = abs_a[0]
        j = 0
        for i, elem in enumerate(abs_a):
            if abs_a[i] < minim:
                minim = abs_a[i]
                j += 1
            i += 1
        minim = a[j]
        return j

    L1 = interpolation("L1.txt", Ngv, "L1", "Ngv")
    L2 = interpolation("L2.txt", Ngv, "L2", "Ngv")

    Nbs = L1 + L2 * Nlv
    Nstr = 50 + 36 * Nlv
    Ntr = 75 + 84 * Nlv ** 0.75

    def define_fp():
        if Ngv < Nbs:
            return "BUBBLE"
        if Nbs < Ngv and Ngv < Nstr:
            return "SLUG"
        if Ngv > Ntr:
            return "MIST"
        if Nstr < Ngv and Ngv < Ntr:
            return "TRANSITION"

    FlowType = define_fp()
    #print(FlowType)
    if FlowType == "BUBBLE":
        F1 = interpolation("F1.txt", Nl, "F1", "Nl")
        F2 = interpolation("F2.txt", Nl, "F2", "Nl")
        F3 = interpolation("F3.txt", Nl, "F3", "Nl")
        F4 = interpolation("F4.txt", Nl, "F4", "Nl")
    if FlowType == "SLUG" or FlowType == "TRANSITION":
        F5 = interpolation("F5.txt", Nl, "F5", "Nl")
        F6 = interpolation("F6.txt", Nl, "F6", "Nl")
        F7 = interpolation("F7.txt", Nl, "F7", "Nl")

    def calc_grad_grav(FlowType):
        if (FlowType == "BUBBLE"):
            s = F1 + F2 * Nlv + (F3 - F4 / Nd) * (Ngv / (1 + Nlv)) ** 2
        if (FlowType == "SLUG"):
            s = (1 + F5) * (Ngv ** 0.982 + 0.029 * Nd + F6) / (1 + F7 * Nlv)
        if (FlowType == "MIST"):
            ps = pl * ql + DensityGas * (1 - ql)
            return ps
        if FlowType == "BUBBLE" or FlowType == "SLUG":
            vs = (s * (ol / pl) ** 0.25) / 1.938
            D = (Vg + Vl - vs) ** 2 + 4 * vs * Vl
            Hl1 = (-(Vg + Vl - vs) + D ** 0.5) / (2 * vs)
            Hl2 = (-(Vg + Vl - vs) - D ** 0.5) / (2 * vs)
            if (Hl1 > 0 and Hl1 < 1):
                Hl = Hl1
            else:
                Hl = Hl2
            ps = pl * Hl + DensityGas * (1 - Hl)
            return ps

    def calc_grad_fric(FlowType):
        if (FlowType == "BUBBLE" or FlowType == "SLUG"):
            Nre = pl * Vl * Diameter / ml
            RoughCoef = Roughness / Diameter
            f1 = interpolation(str(MUDI(RoughCoef)) + ".txt", Nre, "f1", "Nre")
            f2coef = (f1 * Vg * Nd ** (2 / 3)) / 4 * Vl
            f2 = interpolation("f1-f2.txt", f2coef, "f2", "f2coef")
            f3 = 1 + f1 * 0.25 * (Vg / (50 * Vl)) ** 0.5
            f = f1 * f2 / f3
            Pfriction = f * pl * Vl * (Vl + Vg) / (2 * Diameter)
        if (FlowType == "MIST"):
            pg = DensityGas * Ngv / Ntr
            Nre = pg * Vg * Diameter / ViscosityGas
            RoughCoef = Roughness / Diameter
            if RoughCoef < 0.05:
                f = interpolation(str(MUDI(RoughCoef)) + ".txt", Nre, "f1", "Nre")
            else:
                f = 4 * (1 / (((4 * m.log10(0.27 * RoughCoef)) ** 2) + 0.067 * RoughCoef ** 1.73))
            Pfriction = f * pg * (Vg ** 2) / (2 * Diameter)
        return (Pfriction)

    def calc_grad(FlowType):
        if (FlowType == "BUBBLE" or FlowType == "SLUG"):
            return (round(calc_grad_fric(FlowType) + calc_grad_grav(FlowType), 2))
        if (FlowType == "MIST"):
            Ek = (Vg + Vl) * Vg * calc_grad_grav("MIST") / pl
            return (round(calc_grad_fric("MIST") + calc_grad_grav("MIST") + Ek, 2))
        if (FlowType == "TRANSITION"):
            Ek = (Vg + Vl) * Vg * calc_grad_grav("MIST") / pl
            A = (Ntr - Ngv) / (Ntr - Nstr)
            return (A * (calc_grad_fric("SLUG") + calc_grad_grav("SLUG")) + (1 - A) * (
                    calc_grad_fric("MIST") + calc_grad_grav("MIST") + Ek))

    return (calc_grad(FlowType))


def calc_pressure():
    x, y = 20, 2
    a = [[0 for j in range(y)] for i in range(x)]
    Q = 100
    i = 0
    while Q <= 2000:
        a[i][0] = Q
        Q += 100
        i += 1
    i = 0
    for i, elem in enumerate(a):
        a[i][1] = DunsRos(a[i][0]) * 0.00000987 * Lenght + PressureBuf
        i += 1
    np.savetxt("VLP.txt", a)
    return ()


def plotVLP():
    qx = []
    py = []
    with open("VLP.txt") as f:
        for pair in f:
            x, y = pair.split()
            qx.append(x)
            py.append(y)
            arr1 = [float(elem) for elem in qx]
            arr2 = [float(elem) for elem in py]

    plt.title("Vertical Lift Pressure")
    plt.xlabel("Q, m3")
    plt.ylabel("Pressure, MPa")
    plt.plot(arr1, arr2, label="VLP", marker="o")
    plt.legend()
    plt.show()
    return ()


calc_pressure()
plotVLP()
