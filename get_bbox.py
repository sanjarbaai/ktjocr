import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from PIL import Image
import json

# Define a list to store the bounding box coordinates
bounding_boxes = []


def onselect(eclick, erelease):
    """Callback function to capture the bounding box coordinates."""
    x1, y1 = int(eclick.xdata), int(eclick.ydata)
    x2, y2 = int(erelease.xdata), int(erelease.ydata)
    bounding_boxes.append((x1, y1, x2, y2))
    print(f"Bounding box: {(x1, y1, x2, y2)}")


def interactive_bbox_selection(image_path):
    """Function to display the image and interactively select bounding boxes."""
    image = Image.open(image_path)
    fig, ax = plt.subplots()
    ax.imshow(image)
    ax.set_title("Select the region of interest and close the window when done")

    toggle_selector.RS = RectangleSelector(
        ax, onselect, useblit=True,
        button=[1], minspanx=5, minspany=5, spancoords='pixels',
        interactive=True
    )

    plt.connect('key_press_event', toggle_selector)
    plt.show()

    # Return the collected bounding boxes
    return bounding_boxes


def toggle_selector(event):
    print('Key pressed.')
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        toggle_selector.RS.set_active(False)


def save_bounding_boxes(bounding_boxes, output_path):
    """Save the bounding boxes to a JSON file."""
    with open(output_path, 'w') as f:
        json.dump(bounding_boxes, f)
    print(f"Bounding boxes saved to {output_path}")


def main():
    img_path = "dataset/certificate_last.png"  # Change this to your image path
    # output_path = "bounding_boxes.json"  # Change this to your desired output path

    # Step 1: Interactively select bounding boxes
    bboxes = interactive_bbox_selection(img_path)

    # Step 2: Save the bounding boxes to a file
    # save_bounding_boxes(bboxes, output_path)

    print('')


if __name__ == '__main__':
    main()
