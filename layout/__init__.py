from simple_logger import LOG
import numpy as np
from PIL import Image, ImageDraw
from enum import Enum
from math import sqrt

class LayoutType(Enum):
    GRID = 1
    HONEYCOMB = 2

class LAYOUT_GENERATOR:
    pin_outer_diameter = 0
    pin_inner_diameter = 0
    dpi = 0
    log = None
    layout = LayoutType.GRID
    MM_TO_INCH = 1 / 25.4

    def __init__(self, pin_outer_diameter, pin_inner_diameter, dpi, layout_type = LayoutType.GRID, log=None):
        self.dpi = dpi
        self.pin_outer_diameter = self.mm_to_px(pin_outer_diameter)
        self.pin_inner_diameter = self.mm_to_px(pin_inner_diameter)
        self.height = 0
        self.width = 0
        self.layout = layout_type
        self.width, self.height = self.a4_size()
        if log is None:
            self.log = LOG(level=0)
        else:
            self.log = log

    def mm_to_px(self, mm):
        return int(mm * self.MM_TO_INCH * self.dpi)

    def a4_size(self) -> tuple[int, int]:
        """
        Calculate the width and height of an A4 page in pixels based on the dpi.
        :return: width, height
        """
        width = int(8.27 * self.dpi)
        height = int(11.69 * self.dpi)
        return width, height

    def count_max_pins(self) -> tuple[int, int, int]:
        """
        Calculate the maximum number of pins that can fit on the page.
        :return: rows, columns, number of pins
        """
        if self.layout == LayoutType.GRID:
            rows = self.height // self.pin_outer_diameter
            cols = self.width // self.pin_outer_diameter
            return rows, cols, rows * cols
        elif self.layout == LayoutType.HONEYCOMB:
            h = sqrt(pow(self.pin_outer_diameter, 2) - (pow(self.pin_outer_diameter, 2)/4))
            rows = int((self.width - self.pin_outer_diameter) // h) + 1
            cols = int((self.height - self.pin_outer_diameter) // h) + 1
            diff = rows // 2
            return rows, cols, rows * cols - diff
        else:
            return 0, 0, 0

    def pin_height(self) -> int:
        rows = self.height // self.pin_outer_diameter
        return rows * self.pin_outer_diameter

    def pin_width(self) -> int:
        if self.layout == LayoutType.GRID:
            cols = self.width // self.pin_outer_diameter
            return cols * self.pin_outer_diameter
        elif self.layout == LayoutType.HONEYCOMB:
            h = sqrt(pow(self.pin_outer_diameter, 2) - (pow(self.pin_outer_diameter, 2) / 4))
            cols = int((self.width - self.pin_outer_diameter) // h)
            return int(cols * h) + self.pin_outer_diameter
        else:
            return 0

    def draw(self, images, border_colors, bg_colors) -> None:
        self.log.info("Generating document background")
        bg = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255
        im = Image.fromarray(bg)
        draw = ImageDraw.Draw(im)
        self.log.info("Drawing pins on the document")
        if self.layout == LayoutType.GRID:
            self.__draw_grid(images, border_colors, bg_colors, draw, im)
        elif self.layout == LayoutType.HONEYCOMB:
            self.__draw_honeycomb(images, border_colors, bg_colors, draw, im)
        else:
            self.log.error("Couldn't draw layout, unknown layout type.")
            return
        self.log.info("Drawing finished")
        im.save("pins.jpg", dpi=(self.dpi, self.dpi))


    def __draw_grid(self, images, border_colors, bg_colors, draw, im):
        height_offset = (self.height - self.pin_height()) // 2
        curr_img_index = 0
        for y in range(0, self.height - self.pin_outer_diameter, self.pin_outer_diameter):
            for x in range(0, self.width - self.pin_outer_diameter, self.pin_outer_diameter):
                # Set up image
                inner_img_original = Image.open(images[curr_img_index]).convert("RGBA")
                border_color = border_colors[curr_img_index]
                background_color = bg_colors[curr_img_index]
                curr_img_index += 1
                inner_img_original = self.__make_circular(inner_img_original)
                inner_img = inner_img_original.resize((self.pin_inner_diameter, self.pin_inner_diameter), Image.Resampling.LANCZOS)
                # Draw background and outline
                try:
                    draw.ellipse((x, y + height_offset, x + self.pin_outer_diameter, y + self.pin_outer_diameter + height_offset),
                                 fill=background_color)
                except Exception as e:
                    self.log.error(
                        f"An error occurred while drawing background for image {curr_img_index}: {e}\nSkipping.")
                try:
                    draw.ellipse((x, y + height_offset, x + self.pin_outer_diameter, y + self.pin_outer_diameter + height_offset),
                                 outline=border_color, width=2)
                except Exception as e:
                    self.log.error(
                        f"An error occurred while drawing border for image {curr_img_index}: {e}\nSkipping.")
                # Paste image
                inner_x = x + (self.pin_outer_diameter - self.pin_inner_diameter) // 2
                inner_y = y + (self.pin_outer_diameter - self.pin_inner_diameter) // 2 + height_offset
                im.paste(inner_img, (inner_x, inner_y), inner_img)

    def __draw_honeycomb(self, images, border_colors, bg_colors, draw, im):
        c_max, r_max, _ = self.count_max_pins()
        h = int(sqrt(pow(self.pin_outer_diameter, 2) - (pow(self.pin_outer_diameter, 2) / 4)))
        height_offset = (self.height - self.pin_height()) // 2
        width_offset = (self.width - self.pin_width()) // 2
        curr_img_index = 0
        for r in range(r_max):
            for c in range(c_max):
                if r+1 == r_max and c % 2 == 1:
                    continue
                # Set up image
                inner_img_original = Image.open(images[curr_img_index]).convert("RGBA")
                border_color = border_colors[curr_img_index]
                background_color = bg_colors[curr_img_index]
                curr_img_index += 1
                inner_img_original = self.__make_circular(inner_img_original)
                inner_img = inner_img_original.resize((self.pin_inner_diameter, self.pin_inner_diameter), Image.Resampling.LANCZOS)
                if c % 2 == 1:
                    y = height_offset + self.pin_outer_diameter*r + self.pin_outer_diameter//2
                else:
                    y = height_offset + self.pin_outer_diameter*r
                x = width_offset + c * h
                draw.ellipse((x, y, x + self.pin_outer_diameter, y + self.pin_outer_diameter), fill=background_color)
                draw.ellipse((x, y, x + self.pin_outer_diameter, y + self.pin_outer_diameter), outline=border_color, width=2)
                inner_x = x + (self.pin_outer_diameter - self.pin_inner_diameter) // 2
                inner_y = y + (self.pin_outer_diameter - self.pin_inner_diameter) // 2
                im.paste(inner_img, (inner_x, inner_y), inner_img)



    def __make_circular(self, img: Image.Image) -> Image.Image:
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