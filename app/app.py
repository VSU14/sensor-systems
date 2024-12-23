import random
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA


st.set_page_config(
    page_title="Главная",
    page_icon="👋",
)

left, right = st.columns(2)


def example_func(scale: int, loc: int) -> float:
    def tmp(x: np.ndarray) -> np.ndarray:
        return np.sin(x / scale + loc)

    return tmp


def another_example_func(scale: int, loc: int) -> float:
    def tmp(x: np.ndarray) -> np.ndarray:
        return np.log(x * scale + loc)

    return tmp


def generate_data(dim: int, num_points: int) -> np.ndarray:
    np.random.seed(42)
    
    coefficients = np.random.randint(low=1, high=15, size=(dim, 2))

    data = []

    x = np.arange(num_points)
    for coef in coefficients:
        if random.random() < 0.5:
            f = example_func(*coef)
        else:
            f = another_example_func(*coef)
        
        data.append(f(x))

    data = np.array(data)
    data = data + 0.2 * np.random.randn(dim, num_points) + 1

    return data.T


def generate_plot(y: np.ndarray, x: np.ndarray=None, title: str = None, xlabel: str = None, ylabel: str = None):
    fig, ax = plt.subplots(figsize=(12, 6))

    if x is not None:
        ax.plot(x, y)
    else:
        ax.plot(y)
    
    if title is not None:
        ax.set_title(title)
    
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    return fig


def apply_pca(data: np.ndarray) -> np.ndarray:
    pca = PCA(n_components=2)

    transformed_data = pca.fit_transform(data)

    return transformed_data


with left:
    dim = st.number_input(label="Число сенсоров", min_value=2, step=1, value=30)

with right:
    num_points = st.number_input(label="Число отсчетов", min_value=2, step=1, value=1_000)

if dim is not None and num_points is not None:
    data = generate_data(dim, num_points)

sensor_id = st.selectbox(label="Выберите сенсор", options=[] if dim is None else list(range(dim)))

if sensor_id is not None:
    st.pyplot(
        generate_plot(
            y=data[:, sensor_id],
            title=f"Сенсор #{sensor_id}",
            xlabel="Время",
            ylabel="Показатель"
        )
    )

if st.button(label="Применить метод главных компонент", use_container_width=True):
    transformed_data = apply_pca(data)

    x, y = transformed_data[:, 0], transformed_data[:, 1]

    st.pyplot(
        generate_plot(
            y=x,
            title="Первая компонента",
            xlabel="Время",
            ylabel="Показатель"
        )
    )

    st.pyplot(
        generate_plot(
            y=y,
            title="Вторая компонента",
            xlabel="Время",
            ylabel="Показатель"
        )
    )