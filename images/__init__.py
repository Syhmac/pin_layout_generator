from rich.console import Console
from rich.table import Table
import os

class IMAGES:
    image_paths = []
    border_colors = []
    background_colors = []
    max_images = 0
    ask_colors = True
    border_color = None
    console = None

    def __init__(self, max_images, console: Console, ask_for_colors = True, default_border_color = "#000000", default_background_color = "#ffffff"):
        self.max_images = max_images
        self.ask_colors = ask_for_colors
        self.border_color = default_border_color
        self.background_color = default_background_color
        self.console = console
        for i in range(self.max_images):
            self.image_paths.append(None)
            self.border_colors.append(None)
            self.background_colors.append(None)

    def set_image(self, index: int):
        if index >= self.max_images:
            raise IndexError
        self.console.print("[#ffffff]Enter the path for image [/#ffffff][#4FC3F7]" + str(index) + "[/#4FC3F7] [#ffffff]or[/#ffffff]")
        self.console.print("[#ffffff]Input the ID of already set image to copy its properties:[/#ffffff]")
        img_path = input("\t")
        # Check if the input is an integer (ID of already set image)
        try:
            im_id = int(img_path)
            self.image_paths[index] = self.image_paths[im_id]
            self.border_colors[index] = self.border_colors[im_id]
            return
        except ValueError or IndexError:
            # Treat input as path
            # Verify that image exists
            if not os.path.exists(img_path):
                self.console.print("[#ff0000]Image not found. Please enter a valid path.[/#ff0000]")
                return
            self.image_paths[index] = img_path
        if self.ask_colors:
            self.console.print("[#ffffff]Enter the border color for image [/#ffffff][#4FC3F7]" + str(index) + "[/#4FC3F7] (in hex format, e.g. #ff0000):")
            border_color = input("\t")
            self.border_colors[index] = border_color
            self.console.print("[#ffffff]Enter the background color for image [/#ffffff][#4FC3F7]" + str(index) + "[/#4FC3F7] (in hex format, e.g. #ff0000):")
            background_color = input("\t")
            self.background_colors[index] = background_color
        else:
            self.border_colors[index] = self.border_color
            self.background_colors[index] = self.background_color

    def get_table(self) -> list[list]:
        return [self.image_paths, self.border_colors, self.background_colors]

    def print_table(self) -> None:
        table = Table(title="Images")
        table.add_column("ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Image Path", style="white")
        table.add_column("Border Color", style="white")
        table.add_column("Background Color", style="white")
        for i in range(self.max_images):
            table.add_row(
                str(i),
                str(self.image_paths[i]),
                str(self.border_colors[i]),
                str(self.background_colors[i])
            )
        self.console.print(table)

    def verify_integrity(self) -> bool:
        """
        Checks if all entries are set. If not it will copy properties from the nearest previous entry. If the first entry is not set, it will raise an error.
        :return: False if no entries had to be fixed, True if at least one entry had to be fixed.
        """
        changes_made = False
        if self.image_paths[0] is None or self.border_colors[0] is None or self.background_colors[0] is None:
            raise Exception("First entry is not set. Please set the first entry before verifying integrity.")

        for i in range(1, self.max_images):
            if self.image_paths[i] is None:
                changes_made = True
                self.image_paths[i] = self.image_paths[i-1]
            if self.border_colors[i] is None:
                changes_made = True
                self.border_colors[i] = self.border_colors[i-1]
            if self.background_colors[i] is None:
                changes_made = True
                self.background_colors[i] = self.background_colors[i-1]

        return changes_made
