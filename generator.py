"""
Арифметические примеры разделяют

По операциям (operation):
- Сложение (addition)
    - С переходом через десяток (over_ten)
    - Без перехода через десяток (under_ten)
- Вычитание (subtraction)
    - С переходом через десяток (over_ten)
    - Без перехода через десяток (under_ten)
- Умножение (multiplication)
- Деление (division)

#По характеристике действия (action_spec):

По характеристике результата (result_spec):
- Целочисленные (integer)
- Дробные (rational)

использовать шаблон вывода?

"""
import operator
import random

class Problem:
    """ Пример, включает в себя
    a - первый операнд
    b - второй операнд
    op - операция
    c - результат

    Чтобы шаблон правильно работал, нужно найти максимальную длину
    каждого операнда и результата после создания всех примеров.
    """
    op_map = { "+": operator.add,
               "-": operator.sub,
               "*": operator.mul,}
    
    def __init__(self, a, op, b):
        self.a = a
        self.op = op
        self.b = b

    @staticmethod
    def width(x):
        return len(str(x))

    @property
    def a_width(self):
        return self.width(self.a)
    @property
    def b_width(self):
        return self.width(self.b)
    @property
    def c_width(self):
        return self.width(self.c)

    @property
    def c(self):
        return self.op_map[self.op](self.a, self.b)

    def format(self, template="{a} {op} {b} = {c}"):
        return template.format(a=self.a, op=self.op, b=self.b, c=self.c)

    def __str__(self):
        return self.format()

    def __eq__(self, other):
        if isinstance(other, Problem):
            if self.a == other.a and self.op == other.op and self.b == other.b:
                return True
        return False
    def __ne__(self, other):
        if not self == other:
            return True
        return False

class Addition(Problem):

    def __init__(self, a, b):
        super().__init__(a, "+", b)

    @staticmethod
    def random_swap(a, b):
        if random.randint(0, 1) == 1:
            return b, a
        return a, b

    @classmethod
    def simple(cls):
        a = random.randint(1,9);
        b = random.randint(1,10-a);
        a, b = cls.random_swap(a, b)
        return cls(a, b)

    @classmethod
    def simple_over_ten(cls):
        """
        a    b
        1 - 10-10
        2 - 9-10
        3 - 8-10
        ...
        9 - 2-10
        """
        a = random.randint(1,9)
        b = random.randint(11-a, 10)
        a, b = cls.random_swap(a, b)
        return cls(a, b)

    @classmethod
    def complicated(cls):
        a = random.randint(1,99)
        b = random.randint(1,10-a%10) 
        a, b = cls.random_swap(a, b)
        return cls(a, b)        

    @classmethod
    def complicated_over_ten(cls):
        a = random.randint(1,8)*10 + random.randint(1,9)
        b = random.randint(10 - a%10, 9) + random.randint(1, 10-a//10)*10 
        a, b = cls.random_swap(a, b)
        return cls(a, b)        

class Task(list):
    pass

def format_simple(task):
    return '\n'.join(map(str, task))

def format_text(task, with_answers=True):
    template = "{{a:>{0}}} {{op}} {{b:<{1}}} = "
    answers = "{{c:<{2}}}"
    
    def deduce_format(self):
        a_width = max([ x.a_width for x in self ])
        b_width = max([ x.b_width for x in self ])
        c_width = max([ x.c_width for x in self ])
        if with_answers:
            return ''.join((template,answers)).format(a_width, b_width, c_width)
        else:
            return template.format(a_width, b_width, c_width)

    if task:
        t = deduce_format(task)
        return '\n'.join(x.format(t) for x in task)
    return "No problems in task"    
