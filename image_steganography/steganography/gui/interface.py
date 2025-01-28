from abc import ABC, abstractmethod

class IMainWindow(ABC):
    @abstractmethod
    def show(self) -> None:
        """Show the main window"""
        pass

    @abstractmethod
    def hide(self) -> None:
        """Hide the main window"""
        pass

    @abstractmethod
    def set_title(self, title: str) -> None:
        """Set the window title"""
        pass

    @abstractmethod
    def set_size(self, width: int, height: int) -> None:
        """Set the window size"""
        pass