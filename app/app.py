import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Функция для обработки изображения и отображения точек
def process_image(image, lower_bound):
    # Преобразование изображения в HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    
    min_saturation = 0
    min_value = 0  

    ranges = [
        (lower_bound + k, 120, (0, 0, 0)) for k in range(0, 120 - lower_bound, 1)
    ][::-1]

    total_mask = np.zeros(hsv.shape[:2], dtype=np.uint8)    
    for min_hue, max_hue, color in ranges:
        lower = np.array([min_hue, min_saturation, min_value])
        upper = np.array([max_hue, 255, 255])

        # Создание маски для текущего диапазона оттенков
        mask = cv2.inRange(hsv, lower, upper)

        # Объединяем маски
        total_mask = cv2.bitwise_or(total_mask, mask)

        # Поиск контуров для текущей маски
        contours, _ = cv2.findContours(total_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Нарисуем центры найденных областей с соответствующим цветом
        for contour in contours:
            # Находим моменты контура для определения центра масс
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                # Нарисуем точку в центре области с цветом, соответствующим диапазону
                cv2.circle(image, (cX, cY), 5, color, -1)

    return image

def main():
    # Заголовок
    st.title("Детектор оттенков на тепловой карте")
    
    # Загружаем изображение
    uploaded_image = st.file_uploader("Загрузите изображение", type=["png", "jpg", "jpeg"])
    
    if uploaded_image is not None:
        file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
    
        # Decode the NumPy array into an OpenCV image
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        # Отображаем изображение
        st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Исходное изображение", use_container_width=True)

        # Вводим порог для яркости
        threshold = st.slider("Порог яркости (чем ниже, тем больше точек)", min_value=0, max_value=119, step=1)

        st.image(cv2.cvtColor(process_image(image, threshold), cv2.COLOR_BGR2RGB), caption="Выходное изображение", use_container_width=True)
        

# Запуск приложения
if __name__ == "__main__":
    main()
