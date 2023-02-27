import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet import preprocess_input
from tensorflow.keras.applications import ResNet101V2

# Load the pre-trained ResNet101 model
model = ResNet101V2(weights='imagenet')

# Get the feature maps for each layer
layer_outputs = [layer.output for layer in model.layers]
activation_model = Model(inputs=model.input, outputs=layer_outputs)

def visualize(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # Get the feature maps for the input image
    activations = activation_model.predict(x)

    # Visualize the feature maps for each layer
    layer_names = [
        "conv1_pad",
        "conv1_conv",
        "pool1_pad",
        "pool1_pool",
        "conv2_block1_1_conv",
        "conv2_block1_1_pad",
        "conv3_block1_1_conv",
        "conv3_block1_1_pad",
        "conv4_block1_1_conv",
        "conv4_block1_1_pad",
        "conv5_block1_1_conv",
        "conv5_block1_1_pad",
        ]

    images_per_row = 8
    for layer_name, layer_activation in zip(layer_names, activations):
        n_features = layer_activation.shape[-1]
        size = layer_activation.shape[1]
        n_cols = n_features // images_per_row
        display_grid = np.zeros((size * n_cols, images_per_row * size))
        for col in range(n_cols):
            for row in range(images_per_row):
                channel_image = layer_activation[0, :, :, col * images_per_row + row]
                channel_image -= channel_image.mean()
                channel_image /= channel_image.std()
                channel_image *= 64
                channel_image += 128
                channel_image = np.clip(channel_image, 0, 255).astype('uint8')
                display_grid[col * size : (col + 1) * size, row * size : (row + 1) * size] = channel_image
        plt.figure(figsize=(50, 50))
        plt.title(layer_name)
        plt.grid(False)
        plt.imshow(display_grid, aspect='auto', cmap='viridis')
        plt.savefig(f"output/{layer_name}.jpg", dpi=100, bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    visualize("bird.jpg")