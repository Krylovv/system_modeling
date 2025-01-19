import pandas as pd
from sort import DfSort
from model import Model

if __name__ == "__main__":
    file_path = 'generated_data.csv'
    df = pd.read_csv(file_path, sep=',')

    # Блок генерации первоначальной модели
    model = Model(df)
    model.print_coefficients()
    model.print_stats()

    # Блок отбора значимых факторов
    print('\nБлок отбора значимых факторов\n')
    sort_object = DfSort(df)
    a = ''

    # Цикл оценки и отбора
    while a != 'n':
        # Выбор метрики
        metric = str(input('Выберите метрику оценки факторов\n1: Статистическая значимость - коэффициент Стьюдента\n2: Коэффициент корреляции Пирсона\n3: Удалить фактор\n4: Пропустить\n'))
        if metric == '1':
            sort_object.compare_t_result()
        elif metric == '2':
            print(sort_object.get_correlation_coefficient())
        elif metric == '3':
            sort_object.remove_factor(sort_object.factor_set_selector())
        elif metric == '4':
            break
        else:
            print('Неверный формат')
            pass
        a = input('Повторить цикл отбора факторов? Y/n ')

    # result_df = sort_object.get_df()
    resulting_factors = sort_object.get_columns()
    print(f'Итоговые факторы: {resulting_factors}\n')
    choice = str(input('Хотите переобучить модель с выбранными факторами? Y/n '))
    if choice != 'n':
        model = Model(df, resulting_factors)
        model.print_coefficients()
        model.print_stats()
    model.print_evaluation()

    evaluation_coefficients = []
    i = 0
    for i in range(len(resulting_factors)):
        i += 1
        evaluation_coefficients.append(input(f'Введите фактор {i}: '))
    print(model.get_prediction(evaluation_coefficients))
    print('\n\n\n')
    print(model.print_special_values())

    # TODO выбор ввода из файла, вывод в файл