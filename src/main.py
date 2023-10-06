"""
External Dependencies:
- numpy
- pandas
- matplotlib
- pygame
- openpyxl (not required)
- pyinstaller (required for compiling)
"""
import math
import multiprocessing
from time import time

from submodules import graph, visualizer
from submodules.data import DataHolder, euler
from submodules.inputparser import InputParser

# Constants:
g = 9.81


def main():
    ip = InputParser()
    ip.start()
    print("\nFollowing constants are set to: g = 9.81")
    print("\nIf units are not specified, they are measured in SI-units.")
    model = ip.get_input(
        question="Specify Model",
        input_description=(
            "1: Mass on a incline",
            "2: Pendulum attached to a mass on a incline",
        ),
        possible_inputs=("1", "2"),
    )
    if model == "1":
        answer = ip.get_input(
            question="Include air resistance and friction?",
            input_description=(
                "y: yes",
                "n: no",
            ),
            possible_inputs=("y", "n"),
        )
        if answer == "y":
            model1_w_external_forces(ip)
        else:
            model1_wo_external_forces(ip)
    else:
        model2(ip)


def model1_wo_external_forces(ip: InputParser):
    t = ip.get_type_input("Specify time t in seconds to run.", float)
    samples = ip.get_type_input("Specify number of samples to take in the time t", int)
    a = ip.get_type_input(
        "Specify angle with floor between 0 and pi", float, interval=(0, math.pi)
    )
    R0 = ip.get_type_input("Specify start displacement R0", float)
    Rd0 = ip.get_type_input("Specify start velocity Rd0", float)

    k = g * math.sin(a)

    dh = DataHolder(t, samples)
    dh.set_val(0, "R", R0)
    dh.set_val(0, "Rd", Rd0)
    dh.set_val(0, "Rdd", k)

    i = 1
    l = dh.length

    t0 = time()
    while i < l:
        t = dh.get_val(i, "t")
        dh.set_val(i, "Rdd", k)
        dh.set_val(i, "Rd", k * t + Rd0)
        dh.set_val(i, "R", 1 / 2 * k * t**2 + Rd0 * t + R0)
        i += 1
    t1 = time() - t0
    print(f"\nCalculated following:")
    print(dh.data)
    print(f"\nTime taken: {t1} s.")
    answer = ip.get_input(
        question="Save data?",
        input_description=(
            "y: yes",
            "n: no",
        ),
        possible_inputs=("y", "n"),
    )
    answer = ip.get_input(
        question="Show graph?",
        input_description=(
            "y: yes",
            "n: no",
        ),
        possible_inputs=("y", "n"),
    )
    p1 = multiprocessing.Process(target=graph.three_axes, args=(dh.data,))
    p2 = multiprocessing.Process(target=visualizer.animate, args=(dh, samples / t, a))

    if answer == "y":
        p1.start()
    answer = ip.get_input(
        question="Show animation?",
        input_description=(
            "y: yes",
            "n: no",
        ),
        possible_inputs=("y", "n"),
    )
    if answer == "y":
        p2.start()


def model1_w_external_forces(ip: InputParser):
    answer = ip.get_input(
        question="Use analytic solution for calculation?",
        input_description=(
            "y: yes",
            "n: no",
        ),
        possible_inputs=("y", "n"),
    )
    use_analytic_solution = answer == "y"
    t = ip.get_type_input("Specify time t in seconds to run.", float)
    samples = ip.get_type_input("Specify number of samples to take in the time t", int)
    m = ip.get_type_input("Specify the mass of the point mass:", float)
    a = ip.get_type_input(
        "Specify angle with floor between 0 and pi", float, interval=(0, math.pi)
    )
    R0 = ip.get_type_input("Specify start displacement R0", float)
    Rd0 = ip.get_type_input("Specify start velocity Rd0", float)
    k = ip.get_type_input(
        "Specify the constant k associated with the drag equation F=kv^2", float
    )
    u = ip.get_type_input("Specify the coefficient u", float)

    if use_analytic_solution:
        k1 = g * math.sin(a) - u * math.cos(a)
        k2 = k / m
        k1sqr = math.sqrt(k1)
        k2sqr = math.sqrt(k2)
        k1k2sqrt = k1sqr * k2sqr

        dh = DataHolder(t, samples)
        dh.set_val(0, "R", R0)
        dh.set_val(0, "Rd", Rd0)
        dh.set_val(0, "Rdd", k1 - k2 * Rd0**2)

        i = 1
        l = dh.length

        t0 = time()
        while i < l:
            t = dh.get_val(i, "t")
            dh.set_val(i, "R", R0 + math.log(math.cosh((Rd0 + t) * k1k2sqrt)) / k2)
            Rd = k1k2sqrt * math.tanh((Rd0 + t) * k1k2sqrt) / k2sqr
            dh.set_val(i, "Rd", Rd)
            dh.set_val(i, "Rdd", k1 - k2 * Rd**2)

            i += 1
        t1 = time() - t0
    else:
        k1 = g * math.sin(a) - u * math.cos(a)
        k2 = k / m

        dh = DataHolder(t, samples)
        dh.set_val(0, "R", R0)
        dh.set_val(0, "Rd", Rd0)
        dh.set_val(0, "Rdd", k1 - k2 * Rd0**2)

        i = 1
        l = dh.length

        dt = dh.get_val(1, "t") - dh.get_val(0, "t")
        Rdd_function = lambda Rd: k1 - k2 * Rd**2

        t0 = time()
        while i < l:
            Rdnm1 = dh.get_val(i - 1, "Rd")
            Rnm1 = dh.get_val(i - 1, "R")

            Rdd = Rdd_function(Rdnm1)
            Rd = euler(Rdnm1, dt, f_val=Rdd)
            R = euler(Rnm1, dt, f_val=Rdd)

            dh.set_val(i, "R", R)
            dh.set_val(i, "Rd", Rd)
            dh.set_val(i, "Rdd", Rdd)

            i += 1
        t1 = time() - t0

    print(f"\nCalculated following:")
    print(dh.data)
    print(f"\nTime taken: {t1} s.")
    answer = ip.get_input(
        question="Save data?",
        input_description=(
            "y: yes",
            "n: no",
        ),
        possible_inputs=("y", "n"),
    )
    if answer == "y":
        print(f"\nSaved to '{dh.save()}'.")

    answer = ip.get_input(
        question="Show graph?",
        input_description=(
            "y: yes",
            "n: no",
        ),
        possible_inputs=("y", "n"),
    )
    p1 = multiprocessing.Process(target=graph.three_axes, args=(dh.data,))
    p2 = multiprocessing.Process(target=visualizer.animate, args=(dh, samples / t, a))

    if answer == "y":
        p1.start()
    answer = ip.get_input(
        question="Show animation?",
        input_description=(
            "y: yes",
            "n: no",
        ),
        possible_inputs=("y", "n"),
    )
    if answer == "y":
        p2.start()


def model2(ip: InputParser):
    t = ip.get_type_input("Specify time t in seconds to run.", float)
    samples = ip.get_type_input("Specify number of samples to take in the time t", int)
    m1 = ip.get_type_input("Specify mass of the zipline clip / trolley", float)
    m2 = ip.get_type_input("Specify mass of the zipline rider", float)
    l = ip.get_type_input(
        "Specify the length of the string between the trolley and the rider", float
    )
    alp = ip.get_type_input(
        "Specify angle with x-axis between -pi and 0", float, interval=(-math.pi, 0)
    )
    R0 = ip.get_type_input("Specify start displacement R0", float)
    Rd0 = ip.get_type_input("Specify start velocity Rd0", float)
    th0 = ip.get_type_input("Specify start angle of the rider th0", float)
    thd0 = ip.get_type_input("Specify start angular velocity of the rider thd0", float)

    a = m1 + m2
    b = lambda th: -m2 * l * math.cos(alp + th)
    c = lambda thd, th: m2 * thd**2 * l * math.sin(alp + th) + g * math.sin(alp) * (
        m1 + m2
    )
    d = lambda th: -1 / l * math.cos(alp + th)
    e = lambda th: g / l * math.sin(th)

    Rdd_function = lambda th, thd: (b(th) * e(th) - c(thd, th)) / (a - b(th) * d(th))
    thdd_function = lambda th, thd: (a * e(th) - c(thd, th) * d(th)) / (
        a - b(th) * d(th)
    )

    dh = DataHolder(t, samples)
    dh.set_val(0, "R", R0)
    dh.set_val(0, "Rd", Rd0)
    dh.set_val(0, "Rdd", Rdd_function(th0, thd0))
    dh.set_val(0, "th", th0)
    dh.set_val(0, "thd", thd0)
    dh.set_val(0, "thdd", thdd_function(th0, thd0))

    i = 1
    l = dh.length

    dt = dh.get_val(1, "t") - dh.get_val(0, "t")
    t0 = time()

    while i < l:
        Rdnm1 = dh.get_val(i - 1, "Rd")
        Rnm1 = dh.get_val(i - 1, "R")
        thdnm1 = dh.get_val(i - 1, "thd")
        thnm1 = dh.get_val(i - 1, "th")

        thdd = thdd_function(thnm1, thdnm1)
        thd = euler(thdnm1, dt, f_val=thdd)
        th = euler(thnm1, dt, f_val=thdd)

        Rdd = Rdd_function(thnm1, thdnm1)
        Rd = euler(Rdnm1, dt, f_val=Rdd)
        R = euler(Rnm1, dt, f_val=Rdd)

        dh.set_val(i, "R", R)
        dh.set_val(i, "Rd", Rd)
        dh.set_val(i, "Rdd", Rdd)

        dh.set_val(i, "th", th)
        dh.set_val(i, "thd", thd)
        dh.set_val(i, "thdd", thdd)

        i += 1
    t1 = time() - t0

    print(f"\nCalculated following:")
    print(dh.data)
    print(f"\nTime taken: {t1} s.")
    answer = ip.get_input(
        question="Save data?",
        input_description=(
            "y: yes",
            "n: no",
        ),
        possible_inputs=("y", "n"),
    )
    if answer == "y":
        print(f"\nSaved to '{dh.save()}'.")

    answer = ip.get_input(
        question="Show graph?",
        input_description=(
            "y: yes",
            "n: no",
        ),
        possible_inputs=("y", "n"),
    )
    p1 = multiprocessing.Process(target=graph.six_axes, args=(dh.data,))
    p2 = multiprocessing.Process(
        target=visualizer.animate, args=(dh, samples / t, alp, l)
    )

    if answer == "y":
        p1.start()
    answer = ip.get_input(
        question="Show animation?",
        input_description=(
            "y: yes",
            "n: no",
        ),
        possible_inputs=("y", "n"),
    )
    if answer == "y":
        p2.start()


if __name__ == "__main__":
    # https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Multiprocessing
    multiprocessing.freeze_support()
    main()
