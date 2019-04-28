import re

class LogSystems(object):
    '''
    Класс, который решает логические уравнения
    или системы логических уравнений
    '''
    def __init__(self, file):
        self.solutions = 0 # количество решений уравнения (системы)
        self.function = "" # логическая функция
        self.vars = [] # переменные в функции
        self.parse_file(file)


    def parse_file(self, file):
        '''
        Метод парсинга системы уравнений,
        заданной в файле
        '''
        fun = '1'
        with open(file) as file_handler:
            # fun = file_handler.read() # считываем данные из файла
            for line in file_handler:
                fun += " and(" + line + ")"

        vars = re.findall(r'[A-Za-z]+[0-9]+', fun) # получаем переменные функции
        [self.vars.append(x) for x in vars if x not in self.vars] # избавляемся от повторов

        fun = fun.replace(' ', '') # удаление лишних пробелов
        # заменяем логические операторы
        fun = fun.replace('!', " not ") # Отрицание
        fun = fun.replace('+', " or ")  # Дизъюнкция
        fun = fun.replace('*', " and ") # Конъюнкция
        fun = fun.replace('=', " == ") # Эквивалентность
        fun = fun.replace('-', " <= ") # Импликация

        for var in reversed(self.vars):
            fun = fun.replace(var, "set["+str(self.vars.index(var))+"]")

        self.function = fun


    def generate_set(self, number):
        '''
        Метод создания набора переменных,
        основанного на двоичном представлении
        номера набора
        '''
        set = []
        for i in range(len(self.vars)):
            set.append(number % 2)
            number //= 2
        return set[::-1]


    def solve(self):
        '''
        Метод перебора всех возможных значений
        переменных в функции. Находит количество
        решений системы вместе с самими решениями
        '''
        sets = 2**len(self.vars) # количество всех наборов переменных
        for number in range(sets):
            set = self.generate_set(number)
            if(eval(self.function)):
                self.solutions += 1
                print(set)
        print(self.solutions)
