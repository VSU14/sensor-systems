import gradio as gr
import cv2
import numpy as np
from PIL import Image

def detect_points_on_heatmap(image, brightness_threshold):
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    min_saturation = 0
    min_value = 0

    # Create ranges for hue detection
    hue_ranges = [
        (brightness_threshold + offset, 120, (0, 0, 0)) 
        for offset in range(0, 120 - brightness_threshold, 1)
    ][::-1]

    combined_mask = np.zeros(hsv.shape[:2], dtype=np.uint8)

    for min_hue, max_hue, color in hue_ranges:
        lower_bound = np.array([min_hue, min_saturation, min_value])
        upper_bound = np.array([max_hue, 255, 255])

        # Create a mask for the current hue range
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        # Combine masks
        combined_mask = cv2.bitwise_or(combined_mask, mask)

        # Find contours for the current mask
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw centers of detected areas with corresponding colors
        for contour in contours:
            # Calculate the moments of the contour to find the center of mass
            moments = cv2.moments(contour)
            if moments["m00"] != 0:
                center_x = int(moments["m10"] / moments["m00"])
                center_y = int(moments["m01"] / moments["m00"])
                # Draw a circle at the center of the area
                cv2.circle(image, (center_x, center_y), 5, color, -1)

    return image

def process_image(image, brightness_threshold):
    # Convert Gradio Image object to numpy array
    # image_np = np.array(image)

    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Process the image
    processed_image_np = detect_points_on_heatmap(image_bgr, brightness_threshold)

    # Convert processed image back to PIL format
    # processed_image = Image.fromarray(cv2.cvtColor(processed_image_np, cv2.COLOR_BGR2RGB))
    return cv2.cvtColor(processed_image_np, cv2.COLOR_BGR2RGB)

def main():
    # Define the Gradio interface
    interface = gr.Interface(
        fn=process_image,
        inputs=[
            gr.Image(type="numpy", label="Upload Image"),
            gr.Slider(minimum=0, maximum=119, value=60, label="Brightness Threshold")
        ],
        outputs=gr.Image(type="numpy", label="Processed Image"),
        title="Heatmap Point Detector",
        description="Upload an image and adjust the brightness threshold to detect points on a heatmap."
    )

    interface.launch()

if __name__ == "__main__":
    main()
