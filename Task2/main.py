from mersenne_tempest import MT19937
from test import Test
import random

def main():
    rng = MT19937(0)
    data = []
    for i in range(10000):
        data.append(rng.temper())
    data = rng.normalize_values(data)
    print('Тестирование алгоритма Вихрь Мерсенна')
    test_unit = Test(data)
    test_unit.kolmogorov_smirnov_test()

    lib_data = []
    for i in range(10000):
        lib_data.append(random.random())
    print('\n\nТестирование библиотеки random')
    test_lib_unit = Test(lib_data)
    test_lib_unit.kolmogorov_smirnov_test()

    print('\n\nИмпортированный тест на C++ из видео')
    hypothesis = test_unit.cpp_test_port(10, 0.06)
    if hypothesis == 1:
        print('Импортированный тест подтверждает гипотезу о равномерности')
    else:
        print('Импортированный тест опровергает гипотезу о равномерности')

if __name__ == '__main__':
    main()

