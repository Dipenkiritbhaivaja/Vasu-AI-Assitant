"""
Windows known folders for VASU AI ASSISTANT.
"""

from __future__ import annotations

from pathlib import Path
import ctypes

from assistant.core.logger import LoggerManager


class WindowsKnownFolders:
    """
    Provides access to Windows known folders.
    """

    _FOLDER_IDS = {
        "Desktop": "{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}",
        "Documents": "{FDD39AD0-238F-46AF-ADB4-6C85480369C7}",
        "Downloads": "{374DE290-123F-4565-9164-39C4925E467B}",
        "Pictures": "{33E28130-4E1E-4676-835A-98395C3BC3BB}",
        "Videos": "{18989B1D-99B5-455B-841C-AB7C74E4DDFC}",
    }

    def __init__(self) -> None:
        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )

    def get(
        self,
        name: str,
    ) -> Path:
        """
        Return the path of a Windows known folder.
        """

        folder_id = self._FOLDER_IDS[name]

        path_ptr = ctypes.c_wchar_p()

        ctypes.windll.shell32.SHGetKnownFolderPath(
            ctypes.c_char_p(bytes(folder_id, "utf-8")),
            0,
            None,
            ctypes.byref(path_ptr),
        )

        return Path(path_ptr.value)