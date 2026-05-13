import json
from simple_logger import LOG

class CONFIG:
    """
    Class reliable for loading and storing app configurations.
    """

    config = {
        "ask_for_colors": True, # Should the app ask user for border colors, or use default for every one
        "default_border_color": "#000000", # Default border color
        "default_background_color": "#ffffff", # Default color between border and image
        "target_dpi": 150,
        "pin_outer_diameter": 70,
        "pin_inner_diameter": 58,
    }
    log = None

    def __init__(self, logger: LOG = None):
        """
        Initialize the CONFIG class by loading the configuration file, or creating a new one.
        """
        if logger is not None:
            self.log = logger
        else:
            self.log = LOG()
        self.log.debug("Initializing CONFIG class")
        try:
            config_file = json.load(open("config.json", "r"))
            self.config["ask_for_colors"] = config_file["ask_for_colors"]
            self.config["default_border_color"] = config_file["default_border_color"]
            self.config["default_background_color"] = config_file["default_background_color"]
            self.config["target_dpi"] = config_file["target_dpi"]
        except FileNotFoundError:
            self.config["ask_for_colors"] = True
            self.config["default_border_color"] = "#000000"
            self.config["default_background_color"] = "#ffffff"
            self.config["target_dpi"] = 150
            self.__save()

    def __save(self) -> None:
        """
        Private method to save the CONFIG object to a JSON file.
        """
        json.dump(self.config, open("config.json", "w"), sort_keys=True, indent=4)

    # Getters
    def get_ask_for_colors(self) -> bool:
        try:
            return bool(self.config["ask_for_colors"])
        except Exception as e:
            self.log.error(f"Error while getting ask_for_border_colors: {e}\n\tDefaulting to False.")
            return False

    def get_border_color(self) -> str:
        try:
            return str(self.config["default_border_color"])
        except Exception as e:
            self.log.error(f"Error while getting border_color: {e}\n\tDefaulting to '#000000'")
            return "#000000"

    def get_background_color(self) -> str:
        try:
            return str(self.config["default_background_color"])
        except Exception as e:
            self.log.error(f"Error while getting background_color: {e}\n\tDefaulting to '#ffffff'")
            return "#ffffff"

    def get_target_dpi(self) -> int:
        try:
            return int(self.config["target_dpi"])
        except Exception as e:
            self.log.error(f"Error while getting target_dpi: {e}\n\tDefaulting to 150.")
            return 150

    def get_pin_outer_diameter(self) -> int:
        try:
            return int(self.config["pin_outer_diameter"])
        except Exception as e:
            self.log.error(f"Error while getting pin_outer_diameter: {e}\n\tDefaulting to 70.")
            return 70

    def get_pin_inner_diameter(self) -> int:
        try:
            return int(self.config["pin_inner_diameter"])
        except Exception as e:
            self.log.error(f"Error while getting pin_inner_diameter: {e}\n\tDefaulting to 58.")
            return 58

    # Setters
    def set_ask_for_colors(self, value: bool) -> None:
        self.config["ask_for_colors"] = value
        self.__save()

    def set_border_color(self, value: str) -> None:
        self.config["default_border_color"] = value
        self.__save()

    def set_background_color(self, value: str) -> None:
        self.config["default_background_color"] = value
        self.__save()

    def set_target_dpi(self, value: int) -> None:
        self.config["target_dpi"] = value
        self.__save()

    def set_pin_outer_diameter(self, value: int) -> None:
        self.config["pin_outer_diameter"] = value
        self.__save()

    def set_pin_inner_diameter(self, value: int) -> None:
        self.config["pin_inner_diameter"] = value
        self.__save()