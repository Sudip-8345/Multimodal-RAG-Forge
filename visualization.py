import os
import matplotlib.pyplot as plt
from PIL import Image

# Plot multiple images
def plot_images(images_path, max_images=5):
    images_shown = 0
    plt.figure(figsize=(16, 9))
    for img_path in images_path:
        if os.path.isfile(img_path):
            image = Image.open(img_path)
            plt.subplot(2, 3, images_shown + 1)
            plt.imshow(image)
            plt.xticks([])
            plt.yticks([])
            images_shown += 1
            if images_shown >= max_images:
                break
    plt.tight_layout()
    plt.show()

# Display single image
def display_single_image(image_path):
    if os.path.isfile(image_path):
        image = Image.open(image_path)
        plt.figure(figsize=(10, 8))
        plt.imshow(image)
        plt.axis('off')
        plt.show()
    else:
        print(f"Image not found: {image_path}")
