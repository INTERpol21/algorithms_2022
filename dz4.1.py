"""
Задание 1.
Приведен код, который позволяет сохранить в
массиве индексы четных элементов другого массива
Сделайте замеры времени выполнения кода с помощью модуля timeit
Попробуйте оптимизировать код, чтобы снизить время выполнения
Проведите повторные замеры
ОБЯЗАТЕЛЬНО! Добавьте аналитику: что вы сделали и какой это принесло эффект
"""
#from numba import njit, prange
from timeit import timeit


def func_1(nums):
    new_arr = []
    for i in range(len(nums)):
        if nums[i] % 2 == 0:
            new_arr.append(i)
    return new_arr



#@njit(parallel=True, cache=True) #пробовал. Не удалось......
#def func_2(nums):
    #new_arr = []
    #for i in range(len(nums)):
    #    if nums[i] % 2 == 0:
   #         new_arr.append(i)
    #return new_arr


def func_3(nums):
    return [x for x in nums if x % 2 == 0]


# Тестирование
print('  func_1\t  func_3\t На 10 000 запусках для списка из:')
for n in (10, 100, 1000):
    nums = list(range(1,n))
    res1 = timeit("func_1(nums)", globals=globals(), number=10_000)
    res3 = timeit("func_3(nums)", globals=globals(), number=10_000)
   # res2 = timeit("func_2(nums)", globals=globals(), number=10_000)
    print(f'{res1:>8.5f}\t', end='')
    print(f'{res3:>8.5f}\t - {n} элементнов func_2 быстрее func_1 на {(1-res3/res1)*100:.0f}%')
   # print(f'{res2:>8.5f}\t - {n} элементнов func_2 быстрее func_1 на {(1 - res2/res1) * 100:.0f}%')



"""
Задание 2.
Приведен код, который формирует из введенного числа
обратное по порядку входящих в него цифр.
Задача решена через рекурсию
Выполнена попытка оптимизировать решение мемоизацией
Сделаны замеры обеих реализаций.
Сделайте аналитику, нужна ли здесь мемоизация или нет и почему?!!!
П.С. задание не такое простое, как кажется
"""

from timeit import timeit
from random import randint


def recursive_reverse(number):
    if number == 0:
        return str(number % 10)  # здесь появляется лишний 0 в конце
    return f'{str(number % 10)}{recursive_reverse(number // 10)}'


num_100 = randint(10000, 1000000)
num_1000 = randint(1000000, 10000000)
num_10000 = randint(100000000, 10000000000000)

print('Не оптимизированная функция recursive_reverse')
print(
    timeit(
        "recursive_reverse(num_100)",
        setup='from __main__ import recursive_reverse, num_100',
        number=10000))
print(
    timeit(
        "recursive_reverse(num_1000)",
        setup='from __main__ import recursive_reverse, num_1000',
        number=10000))
print(
    timeit(
        "recursive_reverse(num_10000)",
        setup='from __main__ import recursive_reverse, num_10000',
        number=10000))


def memoize(f):
    cache = {}

    def decorate(*args):

        if args in cache:
            return cache[args]
        else:
            cache[args] = f(*args)
            return cache[args]
    return decorate


@memoize
def recursive(number):
    if number == 0:
        return ''
    return f'{str(number % 10)}{recursive(number // 10)}'


print('Оптимизированная функция recursive')
print(
    timeit(
        'recursive(num_100)',
        setup='from __main__ import recursive, num_100',
        number=10000))
print(
    timeit(
        'recursive(num_1000)',
        setup='from __main__ import recursive, num_1000',
        number=10000))
print(
    timeit(
        'recursive(num_10000)',
        setup='from __main__ import recursive, num_10000',
        number=10000))

##############################################################################
"""
Нет, в данном случае мемоизация не нужна
В данном случае рекурсия является последовательной и на каждом последущем шаге функция рекурсивно вызывает себя с аргументом,
отличным от предыдущих вызовов (как минимум они отличаются по количеству цифр в
составе числа-аргумента). Поэтому нет смысла кэшировать значения функции для
различных аргументов, программе все равно не доведется ими воспользоваться
при сворачивании рекурсии.
Пример: 12345
Последовательность вызовов рекурсии:
alt(12345) -> alt(1234) -> alt(123) -> alt(12) -> alt(1) -> alt(0)
Последовательность сворачивания рекурсии (она же последовательность
кешируемых значений):
alt(12345) <- alt(1234) <- alt(123) <- alt(12) <- alt(1) <- alt(0)
"""
##############################################################################



"""
Задание 3.
Приведен код, формирующий из введенного числа
обратное по порядку входящих в него
цифр и вывести на экран.
Сделайте профилировку каждого алгоритма через timeit
Обязательно предложите еще свой вариант решения!
Сделайте вывод, какая из четырех реализаций эффективнее и почему!
"""
from timeit import timeit
from random import randint

def revers_1(enter_num, revers_num=0):
    if enter_num == 0:
        return revers_num
    else:
        num = enter_num % 10
        revers_num = (revers_num + num / 10) * 10
        enter_num //= 10
        return revers_1(enter_num, revers_num)  # добавил return



def revers_2(enter_num, revers_num=0):
    while enter_num != 0:
        num = enter_num % 10
        revers_num = (revers_num + num / 10) * 10
        enter_num //= 10
    return revers_num


def revers_3(enter_num):
    enter_num = str(enter_num)
    revers_num = enter_num[::-1]
    return revers_num

def revers_4(enter_num):
    return ''.join(reversed(list(str(enter_num))))


num = randint(10_000_000, 1_000_000_000)

print(f'Исходное число: {num}')
print(f'Реализация 1: {int(revers_1(num)):>10} за {timeit("revers_1(num)", globals=globals(), number=10_000):.7f}')
print(f'Реализация 2: {int(revers_2(num)):>10} за {timeit("revers_2(num)", globals=globals(), number=10_000):.7f}')
print(f'Реализация 3: {revers_3(num):>10} за {timeit("revers_3(num)", globals=globals(), number=10_000):.7f}')
print(f'Реализация 4: {revers_4(num):>10} за {timeit("revers_4(num)", globals=globals(), number=10_000):.7f}')


"""
- Реализация 1: Рекурсия. Удобно, но самый медленный вариант. 
- Реализация 2: Цикл
- Реализация 3: является самой эффективной, т.к. использует исключительно
возможности срезов!!!
- Реализация 4: Использует возможности срезов для списков,
не для строк, но дополнительно производит преобразование строки в список и списка
в строку, на что уходит дополнительное время, поэтому эта реализация немного медленнее 3 варинта. 
"""
##############################################################################




"""
Задание 4.
Приведены два алгоритма. В них определяется число,
которое встречается в массиве чаще всего.
Сделайте профилировку каждого алгоритма через timeit
Обязательно напишите третью версию (здесь возможно даже решение одной строкой).
Сделайте замеры и опишите, получилось ли у вас ускорить задачу
"""

##############################################################################
"""
- Реализация 3: Копия 2 реализации, просто написаное в одну строку, отличия 1 и 2, где основное
время уходит на то, чтобы пробежать все элементы в списке 
- Реализация 4: аналог реализации 3, только перебор идет не по всем элементам
исходного списка, а лишь по уникальным. 
"""

from timeit import timeit
from random import randint


def func_1():
    m = 0
    num = 0
    for i in array:
        count = array.count(i)
        if count > m:
            m = count
            num = i
    return f'Чаще всего встречается число {num}, ' \
           f'оно появилось в массиве {m} раз(а)'


def func_2():
    new_array = []
    for el in array:
        count2 = array.count(el)
        new_array.append(count2)

    max_2 = max(new_array)
    elem = array[new_array.index(max_2)]
    return f'Чаще всего встречается число {elem}, ' \
           f'оно появилось в массиве {max_2} раз(а)'


def func_3():
    max_el = max([(x, array.count(x)) for x in array], key=lambda x: x[1])
    return f'Чаще всего встречается число {max_el[0]}, ' \
           f'оно появилось в массиве {max_el[1]} раз(а)'


def func_4():
    max_el = max([(x, array.count(x)) for x in set(array)], key=lambda x: x[1])             #Добавил set
    return f'Чаще всего встречается число {max_el[0]}, ' \
           f'оно появилось в массиве {max_el[1]} раз(а)'


array = [randint(1, 10) for i in range(1000)]


print(f'{func_1()} -> {timeit("func_1()", globals=globals(), number=1000):.7f}')
print(f'{func_2()} -> {timeit("func_2()", globals=globals(), number=1000):.7f}')
print(f'{func_3()} -> {timeit("func_3()", globals=globals(), number=1000):.7f}')
print(f'{func_4()} -> {timeit("func_4()", globals=globals(), number=1000):.7f}')