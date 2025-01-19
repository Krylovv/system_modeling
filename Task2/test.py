import numpy as np
from scipy.stats import kstest
import matplotlib.pyplot as plt


class Test:
    def __init__(self, data):
        self.data = data

    def kolmogorov_smirnov_test(self, alpha=0.05):
        # Проверка на равномерность на интервале от 0 до 1
        D, p_value = kstest(self.data, 'uniform')

        if p_value > alpha:
            print(f'Выборка следует равномерному распределению (p-value={p_value: .4f})')
        else:
            print(f'Выборка не следует равномерному распределению (p-value={p_value: .4f})')

        # Построение гистограммы и кумулятивной функции распределения
        fig, ax = plt.subplots(figsize=(10, 6))

        n_bins = int(np.sqrt(len(self.data)))
        ax.hist(self.data, bins=n_bins, density=True, label='Гистограмма', color='skyblue', edgecolor='black')

        ax.set_xlabel('Значение')
        ax.set_ylabel('Плотность вероятности')
        ax.legend()

        plt.title(f'Тест Колмогорова-Смирнова (p-value={p_value:.4f})')
        plt.show()

    # Порт представленного в видео теста на язык Python ради интереса
    def cpp_test_port(self, m, alpha):
        RN_arr = self.data
        n = len(RN_arr)

        frec = np.zeros(m, dtype=int)
        abs_diff = np.zeros(m, dtype=float)

        obs_distrib = 0
        sub_seg_len = 1.0 / m
        H0Acc = 1

        if alpha >= 0.1:
            DaN = 1.22 / np.sqrt(n)
        elif alpha > 0.05:
            DaN = 1.36 / np.sqrt(n)
        else:
            DaN = 1.63 / np.sqrt(n)

        print(f"Specified alpha = {alpha:.2f}. The critical value is {DaN:.4f}. Numbers of net's segments: {m}\n")

        for i in range(n):
            SegN = min(int(RN_arr[i] * m), m - 1)
            frec[SegN] += 1

        print("The observed frequencies:")
        print(frec)

        for i in range(m):
            obs_distrib += float(frec[i]) / n
            print(
                f"Subsegment: {i}. Observed distribution: {obs_distrib:.6f}, theoretical distribution {sub_seg_len * (i + 1): .6f}, the difference: {abs(obs_distrib - sub_seg_len * (i + 1)): .6f}.")
            abs_diff[i] = abs(obs_distrib - sub_seg_len * (i + 1))

        CDaN = abs_diff[np.argmax(abs_diff)]
        print(f"Maximum of differences: {CDaN:.6f}, critical value: {DaN:.6f}.\n")

        if DaN <= abs_diff[np.argmax(abs_diff)]:
            H0Acc = 0
        return H0Acc