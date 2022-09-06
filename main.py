import json
from copy import deepcopy


# сохраняет данные в json
def safe_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=2)


# считывает данные из json
def load_data():
    with open('data.json') as f:
        data = json.load(f)
    return data


# показывает какой процент в портфеле занимает валюта
def show_percent(name, percent, weight = 50):
    full = '▮'
    empty = '-'
    bars = round(percent * weight) # кол-во заполненых ячеек
    progress = full * bars + empty * (weight - bars)
    print(f'{name:7} - {round(percent * 100)}% |{progress}|')


# принимает 2 списка: высота столбцов, подписи к столбцам и рисует график
def plot_stat(data, signs, hight = 7): # ф-ия создания вертикального графика
    for i in range(hight):
        if i % 3 == 0:
            current = max(data) - ((max(data) - min(data)) / hight) * (i)
            line = f'{str(round(current, 2)):10}'
        else:
            line = ' '*10

        for num in data:
            if max(data) - ((max(data) - min(data)) / hight) * (i + 1) < num:
                line += '▮   '
            else:
                line += '    '

        print(line)

    print(f'{str(round(min(data), 2)):10}' + '▮   ' * len(data))
    print(' '*10 + '▮   ' * len(data))
    line = ' '*10
    for sign in signs:
        line += f'{sign:4}'
    print(line)


# переводит все валюты в доллары и строит график для каждой недели
def show_convert(data):
    weeks = list(sorted(data.keys()))
    converted = []
    for week in weeks:
        currencies = data[week]
        total = 0
        for curr in currencies:
            total += curr['cost'] * curr['amount']
        converted.append(round(total, 2))
    plot_stat(converted, weeks)


# подсчитывает долю вылюты в портфеле(в долларах) и отображает в прогрессбарах
def show_stat(data, week_num):
    total = 0
    for curr in data[week_num]:
        total += curr['cost'] * curr['amount']
    stats = []
    for curr in data[week_num]:
        stats.append((curr['cost'] * curr['amount'] / total, curr['name']))
    stats = reversed(sorted(stats))
    for s, name in stats:
        show_percent(name, s)


# вывод сообщений с режимами и запрашивает ввод
def select_mode():
    print()
    print('-'*30)
    print(' Select operating mode:')
    print(' 1. Add new week:')
    print(' 2. Copy new week:')
    print(' 3. Add currency information:')
    print(' 4. Change currency information:')
    print(' 5. Show statistics:')
    print(' 6. Show currency distribution:')
    print(' 7. Exit the program:')
    print('-' * 30)
    print()
    return int(input())


# обработка режимов и вывод функций
def loop():
    data = load_data()
    while True:
        mode = select_mode()

        if mode == 1:
            week = input(' Enter new week number: ')
            data[week] = []

        elif mode == 2:
            week = input(' Enter new week number: ')
            from_week = input(' Select the week number to copy: ')
            # ниже код копирования написан вручную.
            # source = []
            # for currency_dict in data[from_week]:
            #     source.append(currency_dict.copy())

            # копирование с помощью библиотеки copy
            data[week] = deepcopy(data[from_week])

        elif mode == 3:
            week = input(' Enter week number: ')
            name = input(' Enter name currency: ')
            cost = float(input(' Enter cost of currency: '))
            amount = float(input(' Enter amount of currency: '))
            data[week].append({
                'name': name,
                'cost': cost,
                'amount': amount,
            })

        elif mode == 4:
            week = input(' Enter week number: ')
            name = input(' Enter name currency: ')
            num = None
            for i, curr in enumerate(data[week]):
                if curr['name'] == name:
                    num = i
            if num == None:
                print(' No such currency')
            else:
                curr_cost = data[week][num]['cost']
                cost = input(f' Enter cost of currency ({curr_cost}): ')
                if cost:
                    data[week][num]['cost'] = float(cost)

                curr_amount = data[week][num]['amount']
                amount = input(f' Enter amount of currency ({curr_amount}): ')
                if amount:
                    data[week][num]['amount'] = float(amount)

        elif mode == 5:
            show_convert(data)

        elif mode == 6:
            week = input(' Enter week number: ')
            show_stat(data, week)

        elif mode == 7:
            break
        else:
            print(' Incorrect input ')

    # сохранение данных
    safe_data(data)

loop()








