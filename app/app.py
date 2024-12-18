import streamlit as st
from typing import List

# Новый расширенный список функциональных групп
FUNCTIONAL_GROUPS = [
    "NO2", "SO3H", "CN", "PO4", "F", "Cl", "Br", "I", "OH", "NH2", "COOH", "CH3", 
    "SH", "NH", "CO", "C=O", "CH2", "CF3", "SiH3", "C≡N", "C=C", "OCH3", "COOCH3"
]

# Функция для расчета совпадений
def compute_match(target: List[str], candidate: List[str]):
    return sum(1 for group in candidate if group in target)

# Настройка страницы
st.set_page_config(
    page_title="Лиганд Подборщик",
    page_icon="🔬",
    layout="wide"
)

# Основной заголовок
st.title("🧬 Система поиска совместимых лигандов")

# Описание процесса
st.write("""
Добро пожаловать в приложение, которое помогает находить оптимальные функциональные группы для подбора лигандов к молекуле. 
Используйте методику сопоставления функциональных групп для поиска наиболее совместимого лиганда.
""")

# Колонки для лучшего разделения интерфейса
col1, col2 = st.columns(2)

# Ввод функциональных групп для молекулы (замок)
with col1:
    st.header("Настройки молекулы")
    lock = st.multiselect("Функциональные группы молекулы (замок)", options=FUNCTIONAL_GROUPS, default=["OH", "NH2"])

# Ввод параметров для лигандов
with col2:
    st.header("Настройки лигандов")
    num_keys = st.slider("Сколько лигандов нужно сравнить?", min_value=1, max_value=5, value=3)
    group_size = st.slider("Сколько групп у каждого лиганда?", min_value=1, max_value=len(FUNCTIONAL_GROUPS), value=2)

# Ввод функциональных групп для каждого лиганда в динамически создаваемых полях
st.write(f"### Укажите функциональные группы для каждого из {num_keys} лигандов:")
key_groups = []
for i in range(num_keys):
    key_group = st.multiselect(f"Функциональные группы для лиганда {i + 1}", FUNCTIONAL_GROUPS, key=f"key_group_{i}", max_selections=group_size)
    key_groups.append(key_group)

# Кнопка для расчета совпадений и вывод результата
if st.button("Рассчитать наиболее подходящий лиганд"):
    best_match = -1
    best_ligand = None

    # Рассчитываем лучший лиганд
    for i, key in enumerate(key_groups):
        score = compute_match(lock, key)
        if score > best_match:
            best_match = score
            best_ligand = key

    # Вывод результата
    if best_ligand:
        st.success(f"🔑 Наиболее подходящий лиганд: **{', '.join(best_ligand)}** с совпадением: **{best_match}**")
    else:
        st.warning("Не удалось найти подходящий лиганд.")

# Дополнительные детали для интерактивности
st.write("---")
st.write("### Полезная информация")
st.info("Вы можете использовать это приложение для подбора функциональных групп к разным типам молекул. Сравните различные лигандные наборы и выберите оптимальные варианты.")
