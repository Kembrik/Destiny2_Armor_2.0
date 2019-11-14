import time
import io

# сортировка брони
start_time = time.time()


def SearchArmor(line, selectClassAndArmors):  # поиск совпадения класса и типа брони
    if line[7] in selectClassAndArmors[0] and line[5] in selectClassAndArmors[1]:
        return 1
    return 0

def ChekTag(armor): # Проверка тега
    if armor[3] == "infuse":
        return 0
    return 1

def LineToList(line):  # преобразуем строку в список
    armor = line.rstrip("\n")
    armor = armor.split(",")
    armor = [x.rstrip("*") for x in armor]
    armor[3] = ""
    armor[34] = ""
    return armor


def CheckType(armor, arrayAllStats):  # проверка брони на новезну
    if not armor[9] in arrayAllStats[armor[7]][armor[5]].keys():
        armor[3] = "junk"
        return 0  # броня старого типа
    return 1


def CheckArmor(state, listTypeActivity):
    for typeActivity in listTypeActivity:
        for typeState in listTypeActivity[typeActivity]:
            if state[-3] != typeState[-3] and state[-1] == typeState[-1]:
                return 0
    return 1


def CheckMod(armor, state):  # проверка установлен ли мод на стат
    mod = state[-3] + " Mod"
    if mod in armor[26:32]:
        armor[state[0]] = str(int(armor[state[0]]) - 10)


def RecordState(
    newArmor, state, arrayAllArmors, listTypeActivity, typeActivity
):  # перезапись брони и стаиов
    if state[-1]:
        for armor in arrayAllArmors:
            if armor[2] == state[-1]:
                if CheckArmor(state, listTypeActivity):
                    armor[34] = ""
                    armor[3] = "junk"
                    break
                else:
                    tmp = armor[34].split(" - ")
                    if len(state) == 5:
                        tmp.remove(typeActivity + " Sum")
                    else:
                        tmp.remove(
                            typeActivity + " " + arrayAllArmors[0][int(state[0])]
                        )
                    armor[34] = " - ".join(tmp)
                    break

    state[-1] = newArmor[2]
    newArmor[3] = "favorite"

    if not newArmor[34]:
        newArmor[34] = typeActivity + " " + arrayAllArmors[0][int(state[0])]
    elif len(state) == 5:
        newArmor[34] = newArmor[34] + " - " + typeActivity + " Sum"
    else:
        newArmor[34] = (
            newArmor[34] + " - " + typeActivity + " " + arrayAllArmors[0][int(state[0])]
        )


def CheckMaxState(armor, state):  # проверка брони на максимум характеристики
    # CheckMod(armor, state)
    value = int(armor[state[0]])
    if len(state) == 5:
        value = int(armor[state[0]]) + int(armor[state[1]])
    if value > state[-2]:
        state[-2] = value
        return 1
    return 0


def AddArmorArray(armor, arrayAllArmors):  # добавление в массив брони
    arrayAllArmors.append(armor)
    # return arrayAllArmors


def SortingArmors(armor, arrayAllStats, arrayAllArmors):  # сортировка брани
    classArmor = armor[7]
    typeArmor = armor[5]
    elementArmor = armor[9]
    listTypeActivity = arrayAllStats[classArmor][typeArmor][elementArmor]

    for typeActivity in listTypeActivity:
        for state in listTypeActivity[typeActivity]:
            if CheckMaxState(armor, state):
                RecordState(
                    armor, state, arrayAllArmors, listTypeActivity, typeActivity
                )
            elif not armor[3]:
                armor[3] = "junk"


def ReadFile(
    arrayAllArmors, selectClassAndArmors, arrayAllStats
):  # создания списка всей имеющейся брони
    with open(r"E:\python\PRO\Destiny_2\destinyArmor_ru.csv", "r", encoding='utf-8') as file:
        AddArmorArray(file.readline().rstrip("\n").split(","), arrayAllArmors)
        for line in file:
            if line.find("Legendary") > -1 and line.find("infuse") == -1:
                armor = LineToList(line)
                if SearchArmor(armor, selectClassAndArmors):
                    if CheckType(armor, arrayAllStats):
                        SortingArmors(armor, arrayAllStats, arrayAllArmors)
                    AddArmorArray(armor, arrayAllArmors)
    return arrayAllArmors


def WriteFile(arrayAllArmors):  # перезапись файла брони
    with open(r"E:\python\PRO\Destiny_2\destinyArmor_ru.csv", "w", encoding='utf-8') as file:
        for armor in arrayAllArmors:
            armor = ",".join(armor)
            file.write(armor + "\n")


def SelectBox():  # выбор чего оптимизируем
    listClassArmors = ["Варлок", "Титан", "Охотник"]
    listTypeArmors = [
        "Шлем",
        "Рукавицы",
        "Нагрудник",
        "Броня для ног",
    ]
    selectClassArmors, selectTypeArmors = [], []

    textLabel = "Какие классы сортеруем? \n"
    for classArmors in listClassArmors:
        textLabel += classArmors + "	"
    textLabel += "\n123\n"
    values = "111"
    # values = input(textLabel)

    for i, value in enumerate(values):
        if int(value):
            selectClassArmors.append(listClassArmors[i])

    textLabel = "Какие типы брони сортеруем? \n"
    for typeArmors in listTypeArmors:
        textLabel += typeArmors + "	"
    textLabel += "\n1234\n"
    values = "1111"
    # values = "0010"
    # values = input(textLabel)

    for i, value in enumerate(values):
        if int(value):
            selectTypeArmors.append(listTypeArmors[i])

    return [selectClassArmors, selectTypeArmors]


def SelectStatsArmors():  # выбор нужных статов
    listClassArmors = ["Варлок", "Титан", "Охотник"]
    listTypeArmors = [
        "Шлем",
        "Рукавицы",
        "Нагрудник",
        "Броня для ног",
    ]
    listElementArmors = [
        "Энергетическая емкость (Пустота)",
        "Энергетическая емкость (Солнце)",
        "Энергетическая емкость (Молния)",
    ]
    listTypeActivity = ["PVP", "PVE"]

    arrayAllStats = dict.fromkeys(listClassArmors)
    for classArmor in arrayAllStats:
        arrayAllStats[classArmor] = dict.fromkeys(listTypeArmors)
        for typeArmor in arrayAllStats[classArmor]:
            arrayAllStats[classArmor][typeArmor] = dict.fromkeys(listElementArmors)
            for ElementArmor in arrayAllStats[classArmor][typeArmor]:
                arrayAllStats[classArmor][typeArmor][ElementArmor] = {
                    key: [] for key in listTypeActivity
                }
                if classArmor == "Варлок":
                    arrayAllStats[classArmor][typeArmor][ElementArmor]["PVP"] = (
                        [27, "Resilience", 0, 0],
                        [28, "Recovery", 0, 0],
                        [27, 28, "Sum", 0, 0],
                    )  # [номерСтата, значениеСтата, номер Предмета]
                    arrayAllStats[classArmor][typeArmor][ElementArmor]["PVE"] = (
                        [28, "Recovery", 0, 0],
                        [29, "Discipline", 0, 0],
                        [28, 29, "Sum", 0, 0],
                    )  # [номерСтата, значениеСтата, номер Предмета]
                if classArmor == "Титан":
                    arrayAllStats[classArmor][typeArmor][ElementArmor]["PVP"] = (
                        [27, "Resilience", 0, 0],
                        [28, "Recovery", 0, 0],
                        [27, 28, "Sum", 0, 0],
                    )  # [номерСтата, значениеСтата, номер Предмета]
                    arrayAllStats[classArmor][typeArmor][ElementArmor]["PVE"] = (
                        [28, "Recovery", 0, 0],
                        [31, "Strength", 0, 0],
                        [28, 31, "Sum", 0, 0],
                    )  # [номерСтата, значениеСтата, номер Предмета]
                if classArmor == "Охотник":
                    arrayAllStats[classArmor][typeArmor][ElementArmor]["PVP"] = (
                        [27, "Resilience", 0, 0],
                        [28, "Recovery", 0, 0],
                        [27, 28, "Sum", 0, 0],
                    )  # [номерСтата, значениеСтата, номер Предмета]
                    arrayAllStats[classArmor][typeArmor][ElementArmor]["PVE"] = (
                        [28, "Recovery", 0, 0],
                        [29, "Discipline", 0, 0],
                        [28, 29, "Sum", 0, 0],
                    )  # [номерСтата, значениеСтата, номер Предмета]

    return arrayAllStats


if __name__ == "__main__":

    selectClassAndArmors = SelectBox()
    arrayAllStats = SelectStatsArmors()

    arrayAllArmors = []
    ReadFile(arrayAllArmors, selectClassAndArmors, arrayAllStats)
    WriteFile(arrayAllArmors)

    print("-" * 30)
    print(", ".join(selectClassAndArmors[0]))
    print(", ".join(selectClassAndArmors[1]))
    print("-" * 30)
    print("the End")

    print("__name__ --- %0.3f seconds ---" % (time.time() - start_time))

