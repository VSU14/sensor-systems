import streamlit as st

from typing import List


FUNCTIONAL_GROUPS = ["OH", "NH2", "COOH", "CH3", "SH", "NH", "CO"]


def evaluate_match(lock: List[str], key: List[str]):
    match_score = sum(1 for group in key if group in lock)
    
    return match_score


st.set_page_config(
    page_title="Главная",
    page_icon="👋",
)

st.markdown("""
### Поиск оптимальных совпадений «ключ-замок» по реперным группам

#### Описание
В данном приложении предлагается выполнить поиск наилучшего совпадения между молекулой (замком) и лигандами (ключами) на основе их функциональных групп. 

#### Задача
Модель «ключ-замок» иллюстрирует, как функциональные группы различных молекул взаимодействуют друг с другом. Задача — выбрать функциональные группы для ключей (лигандов) и найти тот, который лучше всего подходит к заданному замку (молекуле белка).

#### Ответ
Система оценивает совпадение по количеству общих функциональных групп и выводит наиболее подходящий ключ (лиганд).
""")

lock = st.multiselect(label="Выберите замок (белок)", options=FUNCTIONAL_GROUPS, default=[FUNCTIONAL_GROUPS[0], FUNCTIONAL_GROUPS[1]])

col1, col2 = st.columns(2, gap="medium")

with col1:
    num_keys = st.number_input(label="Выберите количество ключей", min_value=1, max_value=5)

with col2:    
    group_size = st.number_input(label="Выберите размер группы", min_value=1, max_value=len(lock), value=len(lock))


with st.container():
    st.markdown(f"Выберите по **{group_size}** функциональные группы для ключей (лигандов):")
    if num_keys != "":
        num_keys = int(num_keys)

        keys = []
        for i in range(num_keys):
            key = st.multiselect(f"Ключ **{i + 1}**", FUNCTIONAL_GROUPS, key=f"key_{i}", max_selections=group_size)
            keys.append(key)

    if st.button(label="Рассчитать совпадения", use_container_width=True):
        best_score = -1
        
        for i, key in enumerate(keys):
            score = evaluate_match(lock, key)
            
            if score > best_score:
                best_score = score
                best_key = key

        # Выводим лучший ключ
        st.markdown(f"Лучший ключ: **{', '.join(best_key)}** со степенью похожести: **{best_score}**")




