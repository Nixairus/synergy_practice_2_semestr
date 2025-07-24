import random

def find_sum_between_min_max(arr):
    """Cчитаем сумму отрицательных элементов между минимальным и максимальным элементами по их индексам"""
    if len(arr) < 2:
        return 0
    
    min_value = min(arr)
    max_value = max(arr)
    min_index = arr.index(min_value)
    max_index = arr.index(max_value)
    
    start = min(min_index, max_index)
    end = max(min_index, max_index)
    
    sum_negative = 0
    for i in range(start + 1, end):
        if arr[i] < 0:
            sum_negative += arr[i]
    
    return sum_negative, min_value, max_value, min_index, max_index

def generate_array(n):
    """Генерируем массив размерности n со случайными числами от -100 до 100"""
    return [random.randint(-100, 100) for _ in range(n)]

# Основная программа
if __name__ == "__main__":
    print("Программа для поиска суммы отрицательных элементов между min и max")
    print("=" * 60)
    
    # Запрос размерности массива
    while True:
        try:
            n = int(input("Введите размерность массива (N >= 2): "))
            if n >= 2:
                break
            else:
                print("Размерность должна быть не менее 2!")
        except ValueError:
            print("Пожалуйста, введите целое число!")
    
    # Генерация массива
    A = generate_array(n)
    
    # Вывод массива
    print(f"\nСгенерированный массив размерности {n}:")
    print("A =", A)
    
    # Поиск минимума и максимума
    result, min_val, max_val, min_idx, max_idx = find_sum_between_min_max(A)
    
    # Вывод подробной информации
    print("\nАнализ массива:")
    print("-" * 40)
    print(f"Минимальный элемент: {min_val} (индекс: {min_idx})")
    print(f"Максимальный элемент: {max_val} (индекс: {max_idx})")
    
    # Показываем элементы между min и max
    start = min(min_idx, max_idx)
    end = max(min_idx, max_idx)
    
    if end - start > 1:
        elements_between = A[start + 1:end]
        print(f"\nЭлементы между min и max (индексы {start+1}-{end-1}):")
        print("Элементы:", elements_between)
        
        negative_elements = [x for x in elements_between if x < 0]
        if negative_elements:
            print("Отрицательные элементы:", negative_elements)
            print(f"Сумма отрицательных элементов: {result}")
        else:
            print("Отрицательных элементов между min и max нет")
            print(f"Сумма отрицательных элементов: {result}")
    else:
        print("\nМежду минимальным и максимальным элементами нет других элементов")
        print(f"Сумма отрицательных элементов: {result}") 