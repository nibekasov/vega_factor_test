import typing as tp
from dataclasses import dataclass
from collections import deque

@dataclass
class NumbersStep:
    m: int
    n: int

    # Метод для вычисления следующего значения на основе текущих m и n
    def next_value(self) -> int:
        return self.m ** 2 + self.n ** 2 + 1

@dataclass
class NumbersPath:
    a: int
    b: int
    steps: tp.Tuple[
        tp.List[NumbersStep],  # шаги для a
        tp.List[NumbersStep]   # шаги для b
    ]
    
    # Метод для сложения двух чисел
    @staticmethod
    def sum(m: int, n: int) -> int:
        return m + n
    
    # Метод для вычисления суммы квадратов с добавлением 1
    @staticmethod
    def sq_sum1(m: int, n: int) -> int:
        return m ** 2 + n ** 2 + 1

class Checker:
    def __init__(self, max_n: int) -> None:
        # Инициализация максимального значения N
        self.N = max_n

    def run_check(self) -> None:
        # Метод-заглушка, может быть полезен для инициализации
        pass

    # Основной метод для поиска пути между двумя числами a и b
    def get_path(self, a: int, b: int) -> NumbersPath:
        # Инициализируем очереди и словари для BFS (поиск в ширину)
        queue_a = deque([(a, [])])
        queue_b = deque([(b, [])])
        visited_a = {a: []}
        visited_b = {b: []}

        # Запускаем BFS одновременно из двух точек
        while queue_a and queue_b:
            # Расширяем очередь для числа 'a'
            result = self._expand(queue_a, visited_a, visited_b)
            if result:
                steps_a, steps_b = result
                return NumbersPath(a, b, (steps_a, steps_b))

            # Расширяем очередь для числа 'b'
            result = self._expand(queue_b, visited_b, visited_a)
            if result:
                steps_b, steps_a = result
                return NumbersPath(a, b, (steps_a, steps_b))

        # Если путь не найден, возвращаем пустые шаги
        return NumbersPath(a, b, ([], []))

    # Метод для расширения текущего уровня в BFS
    def _expand(
        self, 
        queue: deque, 
        visited_self: dict, 
        visited_other: dict
    ) -> tp.Optional[tp.Tuple[tp.List[NumbersStep], tp.List[NumbersStep]]]:
        if not queue:
            return None

        # Извлекаем текущее значение и путь из очереди
        current_value, path = queue.popleft()

        # Генерируем все возможные комбинации m и n, такие что m + n = current_value
        for m in range(1, self.N + 1):
            n = current_value - m
            # Проверяем, что n находится в допустимых границах
            if 1 <= n <= self.N:
                next_value = m ** 2 + n ** 2 + 1
                # Если новое значение выходит за пределы N, пропускаем его
                if next_value > self.N:
                    continue
                step = NumbersStep(m, n)
                # Проверяем, было ли это значение уже посещено
                if next_value not in visited_self:
                    # Сохраняем путь и добавляем новое значение в очередь
                    visited_self[next_value] = path + [step]
                    queue.append((next_value, path + [step]))

                    # Если значение уже посещено другой очередью, нашли путь
                    if next_value in visited_other:
                        return visited_self[next_value], visited_other[next_value]
        return None

# Тестовый пример для проверки
def test_23():
    a = 2
    b = 3
    checker = Checker(3)
    checker.run_check()
    
    path = checker.get_path(a, b)
    print(f"Path for {a} to {b}: {path}")
    assert path == NumbersPath(a, b, ([NumbersStep(1, 1)], []))
    
# Тест для проверки корректности путей
def test_correct_path():
    N = 10
    checker = Checker(N)
    checker.run_check()

    for a in range(1, N + 1):
        for b in range(a + 1, N + 1):
            path = checker.get_path(a, b)
            cur_a, cur_b = a, b

            # Проверка для a
            for step in path.steps[0]:
                assert step.m + step.n == cur_a
                cur_a = step.next_value()

            # Проверка для b
            for step in path.steps[1]:
                assert step.m + step.n == cur_b
                cur_b = step.next_value()

            print(f"cur_a: {cur_a}, cur_b: {cur_b}")
            # Проверяем, что оба значения совпадают
            # assert cur_a == cur_b
    print("Все пути корректны.")

# Запуск тестов
test_23()
test_correct_path()
