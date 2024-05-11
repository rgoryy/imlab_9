import tkinter as tk
from tkinter import *
import random
import matplotlib.pyplot as plt
import scipy.stats as stats

window = tk.Tk()

probabilities = [0.15, 0.25, 0.1, 0.2, 0.3]


def set_def_probs():
    probabilities.clear()
    probabilities.append(0.15)
    probabilities.append(0.25)
    probabilities.append(0.1)
    probabilities.append(0.2)
    probabilities.append(0.3)


labels = []
entries = []
for i in range(len(probabilities)):
    labels.append(Label(text="Prob." + str(i + 1) + ":"))
    labels[i].pack()
    entries.append(Entry())
    entries[i].insert(i, str(probabilities[i]))
    entries[i].pack()

label_trials = Label(text="Number of experiments:")
label_trials.pack()

num_trials_var = tk.StringVar(window)
num_trials_var.set("10")
num_trials_options = ["10", "100", "1000", "10000"]

num_of_experiments = OptionMenu(window, num_trials_var, *num_trials_options)

num_of_experiments.pack()


def calculate_empirical_statistics_and_chi_square():
    for i in range(len(probabilities)):
        probabilities[i] = float(entries[i].get())

    # print(probabilities)
    # print(round(sum(probabilities), 2))

    if round(sum(probabilities), 2) != 1:
        set_def_probs()  # todo: обновлять UI
        return

    print(probabilities)

    N = int(num_trials_var.get()) # количество попыток

    values = []

    for _ in range(N):
        rand_value = random.random()
        comp_value = 0
        number = 0
        for prob in probabilities:
            number += 1
            comp_value += prob
            if rand_value < comp_value:
                values.append(number)
                break

    avrg = sum((i + 1) * probabilities[i] for i in range(len(probabilities)))
    disper = sum(((i + 1) ** 2) * probabilities[i] - (avrg ** 2) * probabilities[i] for i, prob in enumerate(probabilities))

    emp_avrg = sum((i + 1) * (values.count(value) / N) for i, value in enumerate(values))

    emp_disper = sum(((i + 1) ** 2) * (values.count(value) / N) - (emp_avrg ** 2) for i, value in enumerate(values))

    chi_square = sum(((values[i] - N * prob) ** 2) / (N * prob) for i, prob in enumerate(values))

    print(avrg)
    print(disper)
    print(emp_avrg)
    print(emp_disper)
    print(chi_square)

    err_avrg = abs(emp_avrg - avrg) / avrg * 100
    err_disper = abs(emp_disper - disper) / disper * 100

    avg_label.config(text=f"Empirical Average: {emp_avrg:.2f} ({err_avrg:.1f}%)")
    dispersion_label.config(text=f"Empirical Dispersion: {emp_disper:.2f} ({err_disper:.1f}%)")
    chi_square_label.config(text=f"Chi-Square Statistic: {chi_square:.2f}")

    plt.clf()
    plt.hist(values, bins=range(1, 7), edgecolor='black')
    plt.xlabel('Values')
    plt.ylabel('Count')
    plt.title('Histogram of Values')
    plt.show()
    print(values)


button = tk.Button(window,
                   text="Build Histogram",
                   command=calculate_empirical_statistics_and_chi_square,
                   font=("Arial", 20))
button.pack()

avg_label = Label()
dispersion_label = Label()
chi_square_label = Label()

avg_label.pack()
dispersion_label.pack()
chi_square_label.pack()

window.mainloop()
