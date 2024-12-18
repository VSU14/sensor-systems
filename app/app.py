import streamlit as st
from typing import List

# Список функциональных групп для выбора
GROUPS = [
    "NO2", "SO3H", "CN", "PO4", "F", "Cl", "Br", "I", "OH", "NH2", "COOH", "CH3",
]

# Функция для расчета совпадения
def calculate_similarity(lock: List[str], key: List[str]):
    return sum(1 for group in key if group in lock)

# Настройка страницы
st.set_page_config(
    page_title="Подбор лигандов",
    page_icon="🔑",
)

# Описание приложения
st.markdown("""
## Подбор функциональных групп лигандов для молекул

### Как это работает?
Приложение помогает находить наиболее подходящие функциональные группы для лиганда, используя методику «ключ-замок». Система оценивает, сколько функциональных групп ключа совпадают с группами замка и находит лучший вариант.

### Шаги:
1. Выберите функциональные группы для молекулы (замка).
2. Укажите количество вариантов лигандов и их размер.
3. Подберите функциональные группы для каждого лиганда.
4. Нажмите кнопку, чтобы найти наилучшее совпадение.
""")

# Выбор функциональных групп для замка
st.sidebar.markdown("### Настройка замка (молекулы)")
lock = st.sidebar.multiselect("Выберите функциональные группы молекулы", options=GROUPS, default=[GROUPS[0], GROUPS[1]])

# Ввод количества ключей и размера группы
st.sidebar.markdown("### Настройка ключей (лигандов)")
num_keys = st.sidebar.slider("Количество лигандов", min_value=1, max_value=5, value=3)
group_size = st.sidebar.slider("Количество групп на лиганд", min_value=1, max_value=len(lock), value=len(lock))

# Основная часть приложения
st.markdown(f"### Подберите функциональные группы для **{num_keys}** лигандов:")
keys = []
for i in range(num_keys):
    key = st.multiselect(f"Лиганд {i + 1}", GROUPS, key=f"ligand_{i}", max_selections=group_size)
    keys.append(key)

# Кнопка для расчета совпадений
if st.button("Найти лучший лиганд"):
    best_match = -1
    best_key = None

    for i, key in enumerate(keys):
        match_score = calculate_similarity(lock, key)
        
        if match_score > best_match:
            best_match = match_score
            best_key = key

    # Результат: вывод самого подходящего лиганда
    if best_key:
        st.success(f"Самый подходящий лиганд: **{', '.join(best_key)}** с совпадением: **{best_match}**.")
    else:
        st.warning("Не удалось найти подходящий лиганд.")
