import random
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

population_size = 100

num_generations = 100

crossover_rate = 0.5

mutation_rate = 0.7

num_days = 3

num_hours = 5


class Teacher:
    def __init__(self, name, discipline):
        self.name = name
        self.discipline = discipline

#Метод повертає True, якщо передана дисципліна співпадає з дисципліною вчителя
    def teaches(self, discipline):
        return discipline == self.discipline

    def __str__(self):
        return self.name

#заняття
class Class:
    def __init__(self, discipline, teacher):
        self.discipline = discipline
        self.teacher = teacher

    def __str__(self):
        return f"{self.discipline} {self.teacher}"


#вказує, скільки разів кожна дисципліна повинна бути включена в розкладі.
disciplines_count = {
    0: 6,
    1: 4,
    2: 2,
    3: 1,
    4: 1,
    5: 2,
    6: 3,
    7: 1,
    8: 4,
    9: 2,
    10: 1,
    11: 1,
}

disciplines = [
    "Iнформаційні технології в менеджментi",
    "Вибрані розділи трудового права",
    "Коректність програм та логіки програмування",
    "Лаб. Коректність програм ",
    "Основи Data Mining",
    "Композиційна семантика SQL-подібних мов",
    "Методи специфікації програм",
    "Лаб. Методи специфікації програм",
    "Інтелектуальні системи",
    "Лаб. Інтелектуальні системи",
    "Розробка бізнес-аналітичних систем",
    "Лаб. Розробка бізнес-аналітичних систем",
]

teachers = [
    Teacher("0", 0),
    Teacher("1", 1),
    Teacher("2", 2),
    Teacher("2", 3),
    Teacher("3", 4),
    Teacher("4", 5),
    Teacher("5", 6),
    Teacher("5", 7),
    Teacher("6", 8),
    Teacher("7", 9),
    Teacher("8", 9),
    Teacher("9", 10),
    Teacher("9", 11),
]


def printSchedule(schedule):
    df = pd.DataFrame(data={
        'day': schedule.keys(),
        'lessons': schedule.values()
    })
    print(df)


#генерує випадковий розклад занять на певну кількість днів і годин.
# Для кожної години і дня випадковим чином вибирається дисципліна та вчитель, який її веде.
def generate_random_schedule():
    schedule = {}

    for day in range(num_days):
        for hour in range(num_hours):
            discipline_idx = random.randint(0, len(disciplines) - 1)
            discipline = disciplines[discipline_idx]

            eligible_teachers = list(
                filter(lambda x: x.teaches(discipline_idx), teachers)
            )
            teacher_idx = random.randint(0, len(eligible_teachers) - 1)
            teacher = eligible_teachers[teacher_idx]

            schedule[(day, hour)] = Class(discipline, teacher)

    return schedule

# Функція get_fitness(schedule) обчислює "привабливість" розкладу занять на основі критеріїв
# Основні критерії:
# 1) Оцінка збільшується, якщо в розкладі присутні більше різних дисциплін і вчителів.
# 2) Кількість разів, коли вчитель веде менше занять, ніж вказано у disciplines_count: оцінка збільшується.
# 3) Зменшення оцінки за наявність двох занять однієї дисципліни або одного вчителя підряд: 
# 4) Якщо в розкладі два заняття однієї дисципліни або одного вчителя призначені на один і той же час, то оцінка зменшується.
# 5) Зменшення оцінки за дисципліни, які ведуться більше, ніж вказано у disciplines_count
# 6) Збільшення оцінки, якщо деяка дисципліна ведеться лише одним вчителем

def get_fitness(schedule):
    fitness = 0
    #Створення списків schedule_disciplines і schedule_teachers
    # Вони представляють дисципліни і вчителів для кожного слоту розкладу відповідно. 
    # Це робиться шляхом ітерації по всіх можливих днях і годинах розкладу 
    # і отримання інформації про дисципліну і вчителя для кожного слоту. 
    schedule_disciplines = [
        schedule[(day, hour)].discipline
        for day in range(num_days)
        for hour in range(num_hours)
    ]
    schedule_teachers = [
        schedule[(day, hour)].teacher
        for day in range(num_days)
        for hour in range(num_hours)
    ]

    #Це сприяє тому, щоб розклад мав більше різноманітності
    fitness += len(set(schedule_disciplines)) + len(set(schedule_teachers))

    # add 1 if a discipline is taught less than 3 times in 2 days
    for _ in range(5):
        for discipline in disciplines:
            if schedule_disciplines.count(discipline) < 3:
                fitness += 1

    # add 1 if a teacher teaches less than 3 times in 2 days
    for _ in range(5):
        for teacher in teachers:
            if schedule_teachers.count(teacher) < 3:
                fitness += 1

    # subtract 1 if a there are 2 disciplines in a row
    for i in range(0, len(schedule_disciplines) - 1):
        if schedule_disciplines[i] == schedule_disciplines[i + 1]:
            fitness -= 1

    # subtract 1 if a there are 2 teachers in a row
    for i in range(0, len(schedule_teachers) - 1):
        if schedule_teachers[i] == schedule_teachers[i + 1]:
            fitness -= 1

    # subtract 1 for each discipline that is taught more than it should be
    for discipline in disciplines:
        if (
            schedule_disciplines.count(discipline)
            > disciplines_count[disciplines.index(discipline)]
        ):
            fitness -= 1

    # add 1 if a discipline is taught by a single teacher
    for discipline in disciplines:
        if schedule_disciplines.count(discipline) == 1:
            fitness += 1

    return fitness

# виконує кросовер між двома розкладами з певною ймовірністю (crossover_rate). 
def crossover(schedule1, schedule2, crossover_rate):
    new_schedule = {}

#Для кожного (day, hour) перевіряється, чи випадкове число 
# менше за crossover_rate. Це визначає ймовірність того, що дана година слоту буде успадкована
#  від schedule1 (якщо умова виконується) або schedule2 (якщо умова не виконується).
    for day, hour in schedule1:
        if random.random() < crossover_rate:
            new_schedule[(day, hour)] = schedule1[(day, hour)]
        else:
            new_schedule[(day, hour)] = schedule2[(day, hour)]
    return new_schedule

# випадковим чином міняє одне заняття в розкладі на інше з іншою дисципліною і вчителем. 
def mutation(schedule):
    day = random.randint(0, num_days - 1)
    hour = random.randint(0, num_hours - 1)

    discipline_idx = random.randint(0, len(disciplines) - 1)
    discipline = disciplines[discipline_idx]

    eligible_teachers = list(filter(lambda x: x.teaches(discipline_idx), teachers))
    teacher_idx = random.randint(0, len(eligible_teachers) - 1)
    teacher = eligible_teachers[teacher_idx]
    schedule[(day, hour)] = Class(discipline, teacher)



def genetic_algorithm():
    #Спочатку створюється початкова популяція розкладів, включаючи випадкові розклади
    population = [generate_random_schedule() for i in range(population_size)]

    for gen in range(num_generations):
        fitnesses = [get_fitness(schedule) for schedule in population]

        worst_schedule_idx = min (range(len(fitnesses)), key=lambda x: fitnesses[x])
        best_schedule_idx = max(range(len(fitnesses)), key=lambda x: fitnesses[x])
        best_schedule = population[best_schedule_idx]

        print("Generation:", gen, "Best fitness:", fitnesses[best_schedule_idx])
        print("Generation:", gen, "Worst fitness:", fitnesses[worst_schedule_idx])

        new_population = [best_schedule]

        while len(new_population) < population_size:
            parent1_idx = random.randint(0, len(population) - 1)
            parent2_idx = random.randint(0, len(population) - 1)
            parent1 = population[parent1_idx]
            parent2 = population[parent2_idx]
            # crossing
            child = crossover(parent1, parent2, crossover_rate)
            # mutation
            if random.random() < mutation_rate:
                mutation(child)
            # new child after crossover and mutation
            new_population.append(child)
        # update population
        population = new_population

    return best_schedule


crossover_schedule = crossover(generate_random_schedule(), generate_random_schedule(), crossover_rate)
printSchedule(crossover_schedule)

print()

mutation(crossover_schedule)
printSchedule(crossover_schedule)

print()

gen_algo = genetic_algorithm()
printSchedule(gen_algo)

print()
