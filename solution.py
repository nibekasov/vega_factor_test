import typing as tp
from dataclasses import dataclass

@dataclass
class NumbersStep:
    m: int
    n: int

    def next(self) -> int:
        return self.m ** 2 + self.n ** 2 + 1

@dataclass
class NumbersPath:
    a: int
    b: int
    steps: tp.Tuple[
        tp.List[NumbersStep],  # steps for a
        tp.List[NumbersStep]   # steps for b
    ]
    
    @staticmethod
    def sum(m: int, n: int) -> int:
        return m + n
    
    @staticmethod
    def sq_sum1(m: int, n: int) -> int:
        return m ** 2 + n ** 2 + 1

class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size + 1))
        self.m_n_steps = {}  # Хранение шагов объединения

    def find(self, x: int) -> int:
        # Поиск с сжатием пути
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int, m: int, n: int):
        xroot = self.find(x)
        yroot = self.find(y)
        if xroot != yroot:
            self.parent[xroot] = yroot
            self.m_n_steps[xroot] = (m, n)  # Сохраняем m и n для xroot

class Checker:
    def __init__(self, max_n: int) -> None:
        self.N = max_n
        self.uf = UnionFind(max_n)

    def run_check(self) -> None:
        for m in range(self.N + 1):
            for n in range(self.N + 1):
                sum_mn = m + n
                sq_sum1 = m ** 2 + n ** 2 + 1
                if 1 <= sum_mn <= self.N and 1 <= sq_sum1 <= self.N:
                    self.uf.union(sum_mn, sq_sum1, m, n)

        # Проверка, все ли числа от 1 до N в одном множестве
        root = self.uf.find(1)
        for i in range(1, self.N + 1):
            if self.uf.find(i) != root:
                raise ValueError(f"Число {i} находится в другом множестве. Гипотеза неверна.")
        print("Все числа от 1 до N могут быть покрашены в один цвет.")

    def get_path(self, a: int, b: int) -> NumbersPath:
        # Проверяем, связаны ли числа
        if self.uf.find(a) != self.uf.find(b):
            raise ValueError(f"Числа {a} и {b} не связаны между собой.")

        # Функция для получения шагов от числа до корня
        def get_steps(x: int) -> tp.List[NumbersStep]:
            steps = []
            while self.uf.parent[x] != x:
                m_n = self.uf.m_n_steps.get(x)
                if m_n:
                    steps.append(NumbersStep(*m_n))
                x = self.uf.parent[x]
            steps.reverse()
            return steps

        steps_a = get_steps(a)
        steps_b = get_steps(b)

        return NumbersPath(a, b, (steps_a, steps_b))

def test_23():
    a = 2
    b = 3
    checker = Checker(3)
    checker.run_check()

    correct_path = NumbersPath(
        a, b,
        (
            [NumbersStep(1, 1)],
            []
        )
    )

    path = checker.get_path(a, b)
    print(correct_path)
    print(path)
    assert path == correct_path
    print("test_23 passed")

def test_correct_path():
    N = 10
    checker = Checker(N)
    checker.run_check()

    for a in range(1, N + 1):
        for b in range(a + 1, N + 1):
            path = checker.get_path(a, b)
            assert path.a == a
            assert path.b == b

            cur_a, cur_b = a, b
            for numbers_step in path.steps[0]:  # check a
                assert numbers_step.m + numbers_step.n == cur_a
                cur_a = numbers_step.next()

            for numbers_step in path.steps[1]:  # check b
                assert numbers_step.m + numbers_step.n == cur_b
                cur_b = numbers_step.next()

            assert cur_a == cur_b
    print("test_correct_path passed")

test_23()
test_correct_path()
