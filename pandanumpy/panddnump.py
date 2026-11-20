# ============================================================
# ПРАКТИЧЕСКАЯ РАБОТА: Анализ данных Titanic (Pandas + NumPy)
# ============================================================

import pandas as pd
import numpy as np

# Путь к файлу с данными (должен содержать столбец Survived)
FILE_PATH = r"c:\!Ика\введение_в_специальность\pandanumpy\train.csv"

# ============================================================
# ЧАСТЬ II. ЗАГРУЗКА И ПЕРВИЧНЫЙ АНАЛИЗ ДАННЫХ
# ============================================================
print("=" * 60)
print("ЧАСТЬ II. ЗАГРУЗКА И ПЕРВИЧНЫЙ АНАЛИЗ ДАННЫХ")
print("=" * 60)

# 6. Загрузка CSV в DataFrame
df = pd.read_csv(FILE_PATH)
print("\n[6] Данные загружены. Размер исходной таблицы:", df.shape)

# Проверка наличия обязательных столбцов
required_cols = ['Age', 'Sex', 'Pclass', 'Fare', 'Embarked', 'Cabin', 'Survived']
missing_required = [c for c in required_cols if c not in df.columns]
if missing_required:
    print("ВНИМАНИЕ! Отсутствуют столбцы:", missing_required)
    print("Задания о выживаемости выполняются только при наличии Survived.")
else:
    print("Все обязательные столбцы присутствуют.")

# 7. Первые n строк (n вводится пользователем)
try:
    n = int(input("\n[7] Введите количество первых строк для вывода (n): "))
except ValueError:
    n = 5
    print("Некорректный ввод, используется n = 5")
print(df.head(n))

# 8. Последние 5 строк
print("\n[8] Последние 5 строк:")
print(df.tail(5))

# 9. Общее количество строк и столбцов
print(f"\n[9] Строк: {df.shape[0]}, Столбцов: {df.shape[1]}")

# 10. Названия всех столбцов
print("\n[10] Названия столбцов:")
print(df.columns.tolist())

# 11. Типы данных каждого столбца
print("\n[11] Типы данных столбцов:")
print(df.dtypes)

# 12. Разделение признаков на числовые и категориальные по смыслу
numeric_features = ['Age', 'Fare', 'SibSp', 'Parch']
categorical_features = ['Survived', 'Pclass', 'Sex', 'Embarked', 'Cabin']
print("\n[12] Числовые признаки:", numeric_features)
print("     Категориальные признаки:", categorical_features)
print("     (PassengerId, Name, Ticket — идентификаторы, не анализируются)")

# 13. Среднее, медиана, минимум, максимум, ст. отклонение числовых признаков
print("\n[13] Описательные статистики числовых признаков:")
numeric_stats = df[numeric_features].agg(['mean', 'median', 'min', 'max', 'std'])
print(numeric_stats)

# 14. Количество пассажиров каждого класса (Pclass)
print("\n[14] Количество пассажиров по классам (Pclass):")
print(df['Pclass'].value_counts().sort_index())

# 15. Количество уникальных значений в Embarked
print(f"\n[15] Уникальных значений в Embarked: {df['Embarked'].nunique()}")
print("     Значения:", df['Embarked'].dropna().unique().tolist())

# Контрольный вопрос 1 (ответ в выводах)

# ============================================================
# ЧАСТЬ III. ОБРАБОТКА ПРОПУЩЕННЫХ ЗНАЧЕНИЙ
# ============================================================
print("\n" + "=" * 60)
print("ЧАСТЬ III. ОБРАБОТКА ПРОПУЩЕННЫХ ЗНАЧЕНИЙ")
print("=" * 60)

# 16. Количество пропусков в каждом столбце
missing_counts = df.isnull().sum()
print("\n[16] Количество пропусков в каждом столбце:")
print(missing_counts)

# 17. Процент пропусков относительно общего числа строк
missing_percent = (missing_counts / len(df) * 100).round(2)
print("\n[17] Процент пропусков (%):")
print(missing_percent)

# 18. Столбец с максимальным количеством пропусков
print(f"\n[18] Столбец с максимумом пропусков: {missing_counts.idxmax()} "
      f"({missing_counts.max()} шт., {missing_percent[missing_counts.idxmax()]}%)")

# 19. Статистики Age ДО заполнения
age_known_before = df['Age'].count()
age_stats_before = df['Age'].agg(['mean', 'median', 'min', 'max', 'std'])
print("\n[19] Статистики Age ДО заполнения:")
print(age_stats_before)
print("     Количество известных значений:", age_known_before)

# 20. Заполнение пропусков в Age медианой (по исходным известным возрастам)
age_median = df['Age'].median()
df['Age'] = df['Age'].fillna(age_median)
print(f"\n[20] Пропуски в Age заполнены медианой = {age_median:.2f}")

# 21. Статистики Age ПОСЛЕ заполнения
age_known_after = df['Age'].count()
age_stats_after = df['Age'].agg(['mean', 'median', 'min', 'max', 'std'])
print("\n[21] Статистики Age ПОСЛЕ заполнения:")
print(age_stats_after)
print("     Количество известных значений:", age_known_after)

# 22. Таблица сравнения «до / после»
comparison = pd.DataFrame({
    'Показатель': ['Среднее арифметическое', 'Медиана', 'Минимальный возраст',
                   'Максимальный возраст', 'Стандартное отклонение',
                   'Количество известных значений'],
    'До обработки': [
        round(age_stats_before['mean'], 4),
        round(age_stats_before['median'], 4),
        age_stats_before['min'],
        age_stats_before['max'],
        round(age_stats_before['std'], 4),
        age_known_before
    ],
    'После обработки': [
        round(age_stats_after['mean'], 4),
        round(age_stats_after['median'], 4),
        age_stats_after['min'],
        age_stats_after['max'],
        round(age_stats_after['std'], 4),
        age_known_after
    ]
})
print("\n[22] Сравнение Age «до / после»:")
print(comparison.to_string(index=False))

# 23. Удаление строк с отсутствующим Embarked
rows_before = len(df)
df = df.dropna(subset=['Embarked']).copy()
rows_after_embarked = len(df)
print(f"\n[23] Удалено строк с пропущенным Embarked: {rows_before - rows_after_embarked}")

# 24. Доля пропусков в Cabin; удаление столбца при > 50%
cabin_missing_ratio = df['Cabin'].isnull().mean()
print(f"\n[24] Доля пропусков в Cabin: {cabin_missing_ratio:.2%}")
if cabin_missing_ratio > 0.5:
    df = df.drop(columns=['Cabin'])
    print("     Доля > 50% — столбец Cabin удалён.")
else:
    print("     Доля <= 50% — столбец Cabin оставлен.")

# 25. Оставшиеся пропуски после обработки
print("\n[25] Оставшиеся пропуски после обработки:")
if df.isnull().sum().sum() == 0:
    print("Пропусков не осталось! Все данные заполнены.")
else:
    print(df.isnull().sum())

# Обработка пропуска в Fare (если он был)
if df['Fare'].isnull().any():
    fare_median = df['Fare'].median()
    df['Fare'] = df['Fare'].fillna(fare_median)
    print(f"Пропуск в Fare заполнен медианой = {fare_median:.2f}")

# 26. Размер до и после обработки
print(f"\n[26] Размер до обработки: {rows_before} строк, "
      f"{rows_before and len(df.columns) + (1 if 'Cabin' in df.columns else 0)} столбцов (ориентировочно)")
print(f"     Размер после обработки: {df.shape[0]} строк, {df.shape[1]} столбцов")

# ============================================================
# ЧАСТЬ IV. АНАЛИЗ ДАННЫХ С ПОМОЩЬЮ NUMPY
# ============================================================
print("\n" + "=" * 60)
print("ЧАСТЬ IV. АНАЛИЗ ДАННЫХ С ПОМОЩЬЮ NUMPY")
print("=" * 60)

# Преобразование столбцов в массивы NumPy
survived = df['Survived'].to_numpy()
sex = df['Sex'].to_numpy()
age = df['Age'].to_numpy()
fare = df['Fare'].to_numpy()
pclass = df['Pclass'].to_numpy()

male_mask = (sex == 'male')
female_mask = (sex == 'female')

# 31. Общий процент выживших
overall_survival = survived.mean() * 100
print(f"\n[31] Общий процент выживших: {overall_survival:.2f}%")

# 32. Процент выживших среди мужчин и женщин
male_survival = survived[male_mask].mean() * 100
female_survival = survived[female_mask].mean() * 100
print(f"\n[32] Выживаемость: мужчины = {male_survival:.2f}%, "
      f"женщины = {female_survival:.2f}%")

# 33. Средний возраст мужчин и женщин
male_age_mean = age[male_mask].mean()
female_age_mean = age[female_mask].mean()
print(f"\n[33] Средний возраст: мужчины = {male_age_mean:.2f}, "
      f"женщины = {female_age_mean:.2f}")

# 34. Средний возраст выживших и погибших отдельно для мужчин и женщин
print("\n[34] Средний возраст по полу и факту выживания:")
rows34 = []
for s_name, s_mask in [('male', male_mask), ('female', female_mask)]:
    for sv in [0, 1]:
        mask = s_mask & (survived == sv)
        val = age[mask].mean() if mask.any() else np.nan
        rows34.append({'Пол': s_name, 'Survived': sv,
                       'Средний возраст': round(val, 2) if not np.isnan(val) else None})
        print(f"     {s_name}, Survived={sv}: {val:.2f}" if not np.isnan(val) else
              f"     {s_name}, Survived={sv}: нет данных")
df34 = pd.DataFrame(rows34)

# 35. Мин., макс., средняя стоимость билета
print(f"\n[35] Стоимость билета: min = {fare.min():.2f}, "
      f"max = {fare.max():.2f}, mean = {fare.mean():.2f}")

# 36. Стандартное отклонение возраста
print(f"\n[36] Стандартное отклонение возраста: {age.std():.2f}")

# Сравнительная таблица по полу
print("\nСравнительная таблица по полу:")
summary_sex = pd.DataFrame({
    'Показатель': ['% выживших', 'Средний возраст',
                   'Ср. возраст выживших', 'Ср. возраст погибших'],
    'Мужчины': [
        round(male_survival, 2),
        round(male_age_mean, 2),
        round(age[male_mask & (survived == 1)].mean(), 2),
        round(age[male_mask & (survived == 0)].mean(), 2)
    ],
    'Женщины': [
        round(female_survival, 2),
        round(female_age_mean, 2),
        round(age[female_mask & (survived == 1)].mean(), 2),
        round(age[female_mask & (survived == 0)].mean(), 2)
    ]
})
print(summary_sex.to_string(index=False))

# ============================================================
# ЧАСТЬ V. ФИЛЬТРАЦИЯ ДАННЫХ
# ============================================================
print("\n" + "=" * 60)
print("ЧАСТЬ V. ФИЛЬТРАЦИЯ ДАННЫХ")
print("=" * 60)

# Задание 1: мужчины старше 30 лет, первый класс
f1 = df[(df['Sex'] == 'male') & (df['Age'] > 30) & (df['Pclass'] == 1)]
print(f"\n[Задание 1] Мужчины > 30 лет, 1 класс: {len(f1)} пассажиров")
print(f1.head(10))

# Задание 2: пассажиры моложе 18 ИЛИ выжившие женщины
f2 = df[(df['Age'] < 18) | ((df['Sex'] == 'female') & (df['Survived'] == 1))]
print(f"\n[Задание 2] Возраст < 18 ИЛИ выжившие женщины: {len(f2)} пассажиров")

# Задание 3: 3-й класс, стоимость билета выше средней по 3-му классу
avg_fare_3 = df.loc[df['Pclass'] == 3, 'Fare'].mean()
f3 = df[(df['Pclass'] == 3) & (df['Fare'] > avg_fare_3)]
print(f"\n[Задание 3] 3 класс, Fare > средней по 3 классу ({avg_fare_3:.2f}): "
      f"{len(f3)} пассажиров")

# Задание 4: возраст 20–40 включительно, порт S
f4 = df[(df['Age'] >= 20) & (df['Age'] <= 40) & (df['Embarked'] == 'S')]
print(f"\n[Задание 4] Возраст 20–40, порт S: {len(f4)} пассажиров")

# ============================================================
# ЧАСТЬ VI. ГРУППИРОВКА И АГРЕГИРОВАНИЕ
# ============================================================
print("\n" + "=" * 60)
print("ЧАСТЬ VI. ГРУППИРОВКА И АГРЕГИРОВАНИЕ")
print("=" * 60)

# 37. Группировка по Pclass и Sex
group1 = df.groupby(['Pclass', 'Sex']).agg(
    Количество=('PassengerId', 'count'),
    Средний_возраст=('Age', 'mean'),
    Доля_выживших_pct=('Survived', lambda x: x.mean() * 100),
    Средняя_стоимость=('Fare', 'mean')
).round(2)
print("\n[37] Группировка по Pclass и Sex:")
print(group1)

# 38. Группировка по Embarked
group2 = df.groupby('Embarked').agg(
    Количество=('PassengerId', 'count'),
    Процент_выживших=('Survived', lambda x: x.mean() * 100)
).round(2)
print("\n[38] Группировка по Embarked:")
print(group2)

# 39. Класс с наибольшей долей выживших
survival_by_class = (df.groupby('Pclass')['Survived'].mean() * 100).round(2)
print("\n[39] Доля выживших по классам (%):")
print(survival_by_class)
print(f"     Класс с наибольшей долей выживших: {survival_by_class.idxmax()} "
      f"({survival_by_class.max():.2f}%)")

# ============================================================
# ЧАСТЬ VII. СОХРАНЕНИЕ РЕЗУЛЬТАТОВ
# ============================================================
print("\n" + "=" * 60)
print("ЧАСТЬ VII. СОХРАНЕНИЕ РЕЗУЛЬТАТОВ")
print("=" * 60)

# 40. Сохранение обработанного DataFrame
df.to_csv('titanic_processed.csv', index=False)
print("\n[40] Обработанный DataFrame сохранён в titanic_processed.csv")

# 41. Сохранение результатов группировки по классу и полу
group1.to_csv('titanic_statistics.csv')
print("[41] Результаты группировки сохранены в titanic_statistics.csv")

# 42. Повторная загрузка и проверка
df_loaded = pd.read_csv('titanic_processed.csv')
print("\n[42] Проверка повторной загрузки titanic_processed.csv:")
print(df_loaded.head())
print("Размер загруженного файла:", df_loaded.shape)

# ============================================================
# ЧАСТЬ VIII. ВЫВОДЫ
# ============================================================
print("\n" + "=" * 60)
print("ЧАСТЬ VIII. ВЫВОДЫ")
print("=" * 60)

print("""
43. Наибольшее количество пропусков содержали столбцы Cabin (более 70%),
    затем Age (~20%) и Embarked (несколько строк).

44. После удаления строк с пропущенным Embarked и столбца Cabin размер данных
    по столбцам уменьшился (Cabin удалён), по строкам — незначительно.
    Заполнение Age медианой увеличило число известных значений до общего,
    но снизило стандартное отклонение и изменило среднее (приблизило к медиане).

45. Выживаемость женщин (~74%) значительно выше, чем мужчин (~19%).
    Это отражает приоритет спасения женщин и детей.

46. Наибольшая доля выживших — в 1-м классе (~63%), затем 2-й (~47%),
    наименьшая — в 3-м (~24%).

47. Наиболее полезными оказались: groupby + agg (агрегирование по группам),
    fillna/dropna (обработка пропусков), булевы маски (фильтрация),
    векторизованные операции NumPy для быстрых расчётов.
""")

# Ответы на контрольные вопросы
print("=" * 60)
print("ОТВЕТЫ НА КОНТРОЛЬНЫЕ ВОПРОСЫ")
print("=" * 60)
print("""
1. Pclass — категориальный признак, т.к. числа обозначают класс обслуживания,
   а не измеряемую величину. Арифметические операции над ним не имеют смысла.

27. Медиана устойчива к выбросам и асимметрии; возраст на «Титанике» скошен,
    поэтому медиана лучше отражает типичное значение, чем среднее.

28. Изменились: среднее, стандартное отклонение, количество известных значений.
    Не изменились: медиана, минимум, максимум.

29. Добавление константных значений (медианы) уменьшает разброс вокруг среднего,
    поэтому стандартное отклонение снижается.

30. Исходное распределение не сохраняется: появляется пик на значении медианы.
    Для сохранения распределения применяют стохастическое заполнение или модели.

(Часть IV) Женщины выживали значительно чаще мужчин; средний возраст женщин
    немного ниже; среди выживших мужчин средний возраст ниже, чем среди погибших.

(Часть V) «И» (&) требует одновременного выполнения всех условий (пересечение),
    «ИЛИ» (|) — хотя бы одного (объединение). В Pandas каждое условие
    заключается в скобки из-за приоритета операторов.

(Часть VI) Фильтрация отбирает подмножество строк, сохраняя структуру.
    Группировка разбивает данные на группы и вычисляет агрегаты по каждой,
    создавая новую таблицу с агрегированными значениями.
""")

print("=" * 60)
print("РАБОТА ЗАВЕРШЕНА")
print("=" * 60)