# Case 1: Поиск суммы отрицательных элементов между min и max

## Описание программы

**Программа для поиска суммы отрицательных элементов между минимальным и максимальным элементами массива**

Данная программа решает классическую задачу обработки одномерных массивов и состоит из нескольких логических блоков.

## Логика работы программы

### 1. Инициализация и ввод данных
Программа начинает работу с запроса у пользователя размерности массива. Реализована защита от некорректного ввода - система проверяет, что введено целое число больше или равное 2, и в случае ошибки повторяет запрос.

### 2. Генерация массива
После получения корректной размерности программа автоматически создает массив со случайными целыми числами в диапазоне от -100 до 100. Это обеспечивает наличие как положительных, так и отрицательных элементов для демонстрации работы алгоритма.

### 3. Поиск экстремальных элементов
Основная функция `find_sum_between_min_max()` определяет минимальный и максимальный элементы массива, а также их позиции (индексы). Это ключевые опорные точки для дальнейших вычислений.

### 4. Определение области поиска
Программа вычисляет границы области между минимальным и максимальным элементами. Независимо от того, какой элемент находится левее, алгоритм корректно определяет начальную и конечную позиции для анализа.

### 5. Суммирование отрицательных элементов
В найденной области программа последовательно проверяет каждый элемент на отрицательность и суммирует все отрицательные значения.

### 6. Вывод результатов
Программа предоставляет подробную информацию:
- Исходный массив
- Значения и позиции минимума и максимума
- Элементы между ними
- Отдельно выделенные отрицательные элементы
- Итоговую сумму

## Особенности реализации

- **Обработка граничных случаев** - корректная работа с массивами менее 2 элементов
- **Интуитивно понятный интерфейс** - пошаговый вывод информации
- **Защита от ошибок ввода** - проверка корректности введенных данных
- **Подробная визуализация** - детальное отображение процесса вычислений

## Функции программы

### `generate_array(n)`
Генерирует массив размерности n со случайными числами от -10 до 10.

### `find_sum_between_min_max(arr)`
Основная функция, которая:
- Находит минимальный и максимальный элементы
- Определяет их индексы
- Вычисляет сумму отрицательных элементов между ними
- Возвращает результат и дополнительную информацию

## Пример работы

1. Программа запрашивает размерность массива (например, 7)
2. Генерируется массив: `[3, -2, 8, -5, 1, -3, 6]`
3. Находится min = -5 (индекс 3), max = 8 (индекс 2)
4. Анализируются элементы между индексами 2 и 3 (таких элементов нет)
5. Выводится результат: сумма = 0

---

**Файлы проекта:**
- `case1.py` - основная программа с реализацией алгоритма
- `README.md` - данное описание проекта