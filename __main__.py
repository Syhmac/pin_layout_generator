# Imports
import os
import math as m
from config import CONFIG
from simple_logger import LOG
from images import IMAGES

log = LOG(level=0)

try:
    import numpy as np
except ImportError:
    # install scipy
    try:
        log.info("Installing Numpy")
        os.system("python -m pip install numpy --break-system-packages")
        import numpy as np
    except ModuleNotFoundError:
        log.critical(f"A critical error occurred while trying to install Numpy.")
        print("Please install numpy manually and try again.")
        print("python -m pip install numpy")
        input("Press Enter to exit...")
        exit(1)

try:
    from PIL import Image, ImageDraw
except ImportError:
    # install Pillow
    try:
        log.info("Installing Pillow")
        os.system("python -m pip install Pillow --break-system-packages")
        from PIL import Image, ImageDraw
    except ModuleNotFoundError:
        log.critical(f"A critical error occurred while trying to install Pillow.")
        print("Please install Pillow manually and try again.")
        print("python -m pip install Pillow")
        input("Press Enter to exit...")
        exit(1)

try:
    from rich.console import Console
except ImportError:
    # Install Rich
    try:
        log.info("Installing Rich")
        os.system("python -m pip install rich --break-system-packages")
        from rich.console import Console
    except ModuleNotFoundError:
        log.critical(f"A critical error occurred while trying to install Rich.")
        print("Please install Rich manually and try again.")
        print("python -m pip install rich")
        input("Press Enter to exit...")
        exit(1)

try:
    console = Console(color_system="truecolor")
except Exception as e:
    log.warn(f"An error occurred while initializing the console: {e}")
    console = Console(color_system="auto") # Sets color mode to auto if command prompt doesn't support truecolor

from rich.table import Table

log.debug("All imports successful")

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
    config = CONFIG(log)
    # Get target dpi
    console.print("[#ffffff]Enter the target dpi.[/#ffffff] [#aaaaaa]Leave blank to use the value from config.json[/#aaaaaa]")
    target_dpi = input("\t")
    if target_dpi == "":
        target_dpi = config.get_target_dpi()
    else:
        try:
            target_dpi = int(target_dpi)
        except ValueError:
            console.print("[bold #ff0000]Invalid input. Please enter a number.[/bold #ff0000]")
            input("Press Enter to exit...")
            log.save()
            exit(1)

    # Create blank image
    log.debug("Creating blank image")
    width, height = a4_size(target_dpi)
    bg = np.ones((height, width, 3), dtype=np.uint8) * 255
    im = Image.fromarray(bg)
    draw = ImageDraw.Draw(im)

    # Get pin outer diameter
    console.print("[#ffffff]Enter the pin outer diameter in millimeters. [/#ffffff][#aaaaaa]Leave blank to use the value from config.json[/#aaaaaa]")
    pin_outer_diameter = input("\t")
    if pin_outer_diameter == "":
        pin_outer_diameter = config.get_pin_outer_diameter()
    else:
        try:
            pin_outer_diameter = int(pin_outer_diameter)
        except ValueError:
            console.print("[bold #ff0000]Invalid input. Please enter a number.[/bold #ff0000]")
            input("Press Enter to exit...")
            log.save()
            exit(1)

    pin_outer_px = int(pin_outer_diameter * MM_TO_INCH * target_dpi)

    # Get pin inner diameter
    console.print("[#ffffff]Enter the pin inner diameter in millimeters. [/#ffffff][#aaaaaa]Leave blank to use the value from config.json[/#aaaaaa]")
    pin_inner_diameter = input("\t")
    if pin_inner_diameter == "":
        pin_inner_diameter = config.get_pin_inner_diameter()
    else:
        try:
            pin_inner_diameter = int(pin_inner_diameter)
        except ValueError:
            console.print("[bold #ff0000]Invalid input. Please enter a number.[/bold #ff0000]")
            input("Press Enter to continue...")
            exit(1)

    pin_inner_px = int(pin_inner_diameter * MM_TO_INCH * target_dpi)

    log.debug("File properties calculated.")

    console.print(f"[#ffffff]Page size: [/#ffffff][#4FC3F7]{width}x{height} pixels[/#4FC3F7]")
    console.print(f"[#ffffff]Pin outer diameter: [/#ffffff][#4FC3F7]{pin_outer_px} pixels[/#4FC3F7]")
    console.print(f"[#ffffff]Pin inner diameter: [/#ffffff][#4FC3F7]{pin_inner_px} pixels[/#4FC3F7]")
    im_count_max = count_pins(width, height, pin_outer_px)
    console.print(f"[#ffffff]Number of pins that can fit on the page: [/#ffffff][#4FB053]{im_count_max}[/#4FB053]")

    # Get images
    log.info("Getting images from the user")
    img = IMAGES(im_count_max, console, config.get_ask_for_colors(), config.get_border_color(), config.get_background_color())
    console.print("[#ffffff]You will be prompted to enter the path for images. If you leave any image set to None it will be filled with the details of the nearest previous image[/#ffffff]")
    console.print("[#ff0000]WARNING: IMAGE OF ID 0 NEEDS TO BE SET. YOU CAN'T LEAVE IT EMPTY!!![/#ff0000]")
    while True:
        img.print_table()
        console.print("[#ffffff]Enter the ID of the image you want to set (or press Enter to finish): [/#ffffff]")
        choice = input()
        if choice == "":
            break
        try:
            img.set_image(int(choice))
        except ValueError:
            console.print("[bold #ff0000]Invalid input. Please enter a number.[/bold #ff0000]")
        except IndexError:
            console.print(f"[bold #ff0000]Index out of range. Please enter a number between 0 and {im_count_max - 1}.[/bold #ff0000]")

    log.info("Verifying integrity of inputted data")
    if img.verify_integrity():
        console.print("[#F57C00]Some images were not set and has been filled automatically.[/#F57C00] [#ffffff]Here's the final table[/#ffffff]")
        img.print_table()

    images, colors, bg_colors = img.get_table()

    log.info("Creating the file")
    pins_height = get_pins_height(height, pin_outer_px)
    height_offset = (height - pins_height) // 2

    curr_img_index = 0
    for y in range(0, height - pin_outer_px, pin_outer_px):
        for x in range(0, width - pin_outer_px, pin_outer_px):
            # Set up image
            inner_img_original = Image.open(images[curr_img_index]).convert("RGBA")
            border_color = colors[curr_img_index]
            background_color = bg_colors[curr_img_index]
            curr_img_index += 1
            inner_img_original = make_circular(inner_img_original)
            inner_img = inner_img_original.resize((pin_inner_px, pin_inner_px), Image.Resampling.LANCZOS)
            # Draw background and outline
            try:
                draw.ellipse((x, y + height_offset, x + pin_outer_px, y + pin_outer_px + height_offset), fill=background_color)
                draw.ellipse((x, y + height_offset, x + pin_outer_px, y + pin_outer_px + height_offset), outline=border_color, width=2)
            except Exception as e:
                log.error(f"An error occurred while drawing border or background for image {curr_img_index}: {e}\nSkipping.")
            # Paste image
            inner_x = x + (pin_outer_px - pin_inner_px) // 2
            inner_y = y + (pin_outer_px - pin_inner_px) // 2 + height_offset
            im.paste(inner_img, (inner_x, inner_y), inner_img)

    log.info("Finished successfully")
    # Save image
    im.save("pins.jpg")
    log.save()

