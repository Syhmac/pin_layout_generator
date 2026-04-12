# Pin Layout Generator
This project creates a print-ready image containing a circular pins layout.

## Requirements
- Python 3.9 or higher

## Features
- Automatically installs python dependencies.
- Automatically calculates image size based on the DPI.
- Creates a print-ready A4 sized image.
- Verifies that the image exists before processing.
- Allows the user to input custom DPI and pin sizes.


## Usage
1. Clone the repository or download the `__main__.py` file.
2. Run the script using Python.
3. Follow the prompts to input the desired DPI and pin size.
4. Follow further prompts to load the images. If you want to create multiple pins of the same image, you can break the 
loop by leaving an empty entry. Last image will be used for the remaining pins.
5. Script will generate a `pins.jpg` file and exit.

### Example:
```
python __main__.py

Enter the target dpi (150 by default): 
Enter the pin outer diameter as number (70 [mm] by default): 
Enter the pin inner diameter as number (58 [mm] by default): 
Page size: 1240x1753 pixels
Pin outer diameter: 413 pixels
Pin inner diameter: 342 pixels
Number of pins that can fit on the page: 12
Enter the path for image 1 (or press Enter to finish): 1.jpg
Enter the path for image 2 (or press Enter to finish): 
```

This will result in:
![Example Output](examples/pins.jpg)