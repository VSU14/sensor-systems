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


def generate_data(dim: int, num_points: int) -> np.ndarray:
    np.random.seed(42)
    
    coefficients = np.random.randint(low=1, high=15, size=(dim, 2))

    data = []

    x = np.arange(num_points)
    for coef in coefficients:
        f = example_func(*coef)
        
        data.append(f(x))

    data = np.array(data)
    data = data + 0.2 * np.random.randn(dim, num_points) + 1

    return data.T


def generate_plot(y: np.ndarray, sensor_id: int):
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(y)
    ax.set_title(f"Сенсор #{sensor_id}")
    
    ax.set_xlabel("Отсчеты")
    ax.set_ylabel("Показатель")

    return fig


def generate_scatter(x: np.ndarray, y: np.ndarray):
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.scatter(x, y)
    
    ax.set_xlabel("Y")
    ax.set_ylabel("X")

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
    st.pyplot(generate_plot(data[:, sensor_id], sensor_id))

if st.button(label="Применить метод главных компонент", use_container_width=True):
    transformed_data = apply_pca(data)

    x, y = transformed_data[:, 0], transformed_data[:, 1]

    st.pyplot(generate_scatter(x, y))