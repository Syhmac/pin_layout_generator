# Imports
import os
import math as m

try:
    import numpy as np
except ImportError:
    # install scipy
    try:
        os.system("python -m pip install numpy")
        import numpy as np
    except Exception as e:
        print("Error installing numpy: ", e)
        print("Please install numpy manually and try again.")
        print("python -m pip install numpy")
        input("Press Enter to continue...")
        exit(1)

try:
    from PIL import Image, ImageDraw
except ImportError:
    # install Pillow
    try:
        os.system("python -m pip install Pillow")
        from PIL import Image, ImageDraw
    except Exception as e:
        print("Error installing Pillow: ", e)
        print("Please install Pillow manually and try again.")
        print("python -m pip install Pillow")
        input("Press Enter to continue...")
        exit(1)

# Constants
RATIO = 1/m.sqrt(2) #Height/Width  ## 960 / 680
OUTER_CIRCLE_RATIO = 1/3
INNER_CIRCLE_RATIO = 58/210
MM_TO_INCH = 1 / 25.4

def a4_size(dpi=150):
    """
    Calculate the width and height of an A4 page in pixels based on the given dpi.
    :param dpi:
    :return: width, height
    """
    width = int(8.27 * dpi)
    height = int(11.69 * dpi)
    return width, height

def get_pins_height(page_height: int, pin_outer_diameter: int):
    """
    Calculate the height of the pins on the page based on the page height and pin outer diameter.
    Counts how many rows of pins can fit on the page and returns the total height of the pins.
    :param page_height:
    :param pin_outer_diameter:
    :return: Height of the pins on the page
    """
    rows = page_height // pin_outer_diameter
    return rows * pin_outer_diameter

def count_pins(page_width: int, page_height: int, pin_outer_diameter: int):
    """
    Calculate the number of pins that can fit on the page based on the page width, page height and pin outer diameter.
    :param page_width:
    :param page_height:
    :param pin_outer_diameter:
    :return: Number of pins that can fit on the page
    """
    rows = page_height // pin_outer_diameter
    cols = page_width // pin_outer_diameter
    return rows * cols

def make_circular(img: Image.Image) -> Image.Image:
    """
    Make the given image circular by applying a circular mask.
    :param img: The input image to be made circular
    :return: The circular image
    """
    size = min(img.size)
    img = img.crop((
        (img.width - size) // 2,
        (img.height - size) // 2,
        (img.width + size) // 2,
        (img.height + size) // 2
    ))

    # Create mask
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + (size, size), fill=255)

    # Apply mask to the image
    img.putalpha(mask)
    return img

if __name__ == "__main__":
    # Get target dpi
    target_dpi = input("Enter the target dpi (150 by default): ")
    if target_dpi == "":
        target_dpi = 150
    else:
        try:
            target_dpi = int(target_dpi)
        except ValueError:
            print("Invalid input. Please enter a number.")
            input("Press Enter to continue...")
            exit(1)

    # Create blank image
    width, height = a4_size(target_dpi)
    bg = np.ones((height, width, 3), dtype=np.uint8) * 255
    im = Image.fromarray(bg)
    draw = ImageDraw.Draw(im)

    # Get pin outer diameter
    pin_outer_diameter = input("Enter the pin outer diameter as number (70 [mm] by default): ")
    if pin_outer_diameter == "":
        pin_outer_diameter = 70
    else:
        try:
            pin_outer_diameter = int(pin_outer_diameter)
        except ValueError:
            print("Invalid input. Please enter a number.")
            input("Press Enter to continue...")
            exit(1)

    pin_outer_px = int(pin_outer_diameter * MM_TO_INCH * target_dpi)

    # Get pin inner diameter
    pin_inner_diameter = input("Enter the pin inner diameter as number (58 [mm] by default): ")
    if pin_inner_diameter == "":
        pin_inner_diameter = 58
    else:
        try:
            pin_inner_diameter = int(pin_inner_diameter)
        except ValueError:
            print("Invalid input. Please enter a number.")
            input("Press Enter to continue...")
            exit(1)

    pin_inner_px = int(pin_inner_diameter * MM_TO_INCH * target_dpi)

    print(f"Page size: {width}x{height} pixels")
    print(f"Pin outer diameter: {pin_outer_px} pixels")
    print(f"Pin inner diameter: {pin_inner_px} pixels")
    im_count_max = count_pins(width, height, pin_outer_px)
    print(f"Number of pins that can fit on the page: {im_count_max}")

    # Get images
    images: list[str] = []
    im_count = 0
    while im_count < im_count_max:
        img_path = input(f"Enter the path for image {im_count+1} (or press Enter to finish): ")
        if img_path == "":
            break
        if not os.path.isfile(img_path):
            print("File does not exist. Please enter a valid path. and try again.")
            continue
        else:
            images.append(img_path)
            im_count += 1

    if len(images) == 0:
        print("No images provided. Exiting.")
        input("Press Enter to continue...")
        exit(1)

    # Draw outlines
    pins_height = get_pins_height(height, pin_outer_px)
    height_offset = (height - pins_height) // 2

    curr_img_index = 0
    for y in range(0, height - pin_outer_px, pin_outer_px):
        for x in range(0, width - pin_outer_px, pin_outer_px):
            # Set up image
            if curr_img_index > len(images) - 1: # Load last image if there are more pins than images
                inner_img_original = Image.open(images[-1]).convert("RGBA")
            else:
                inner_img_original = Image.open(images[curr_img_index]).convert("RGBA")
                curr_img_index += 1
            inner_img_original = make_circular(inner_img_original)
            inner_img = inner_img_original.resize((pin_inner_px, pin_inner_px), Image.Resampling.LANCZOS)
            # Draw outline
            draw.ellipse((x, y + height_offset, x + pin_outer_px, y + pin_outer_px + height_offset), outline="black", width=1)
            # Paste image
            inner_x = x + (pin_outer_px - pin_inner_px) // 2
            inner_y = y + (pin_outer_px - pin_inner_px) // 2 + height_offset
            im.paste(inner_img, (inner_x, inner_y), inner_img)

    # Save image
    im.save("pins.jpg")

