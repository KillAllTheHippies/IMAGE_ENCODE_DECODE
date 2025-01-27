from PyQt5.QtCore import QSettings

class ConfigHandler:
    def __init__(self):
        self.settings = QSettings("ImageSteganography", "Settings")
    
    @property
    def dark_mode(self):
        return self.settings.value("dark_mode", False, bool)

    @dark_mode.setter
    def dark_mode(self, value):
        self.settings.setValue("dark_mode", value)
        
    # Logging configuration
    @property
    def logging_enabled(self):
        return self.settings.value("logging/enabled", True, bool)
        
    @logging_enabled.setter
    def logging_enabled(self, value):
        self.settings.setValue("logging/enabled", value)
        
    @property
    def log_retention_days(self):
        return self.settings.value("logging/retention_days", 30, int)
        
    @log_retention_days.setter
    def log_retention_days(self, value):
        self.settings.setValue("logging/retention_days", value)
        
    @property
    def thumbnail_size(self):
        return self.settings.value("logging/thumbnail_size", (128, 128), tuple)
        
    @thumbnail_size.setter
    def thumbnail_size(self, value):
        self.settings.setValue("logging/thumbnail_size", value)
        
    @property
    def visible_log_columns(self):
        return self.settings.value("logging/visible_columns",
            ["timestamp", "prompt", "image_path", "encoding_types"], list)
            
    @visible_log_columns.setter
    def visible_log_columns(self, value):
        self.settings.setValue("logging/visible_columns", value)