"""
System Service for VASU AI ASSISTANT.
"""

from __future__ import annotations

import ctypes
import subprocess
from assistant.core.logger import LoggerManager

class SystemService:
    """
    Provides operating system actions.
    """

    def __init__(
        self,
    ) -> None:

        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )

    def _execute(
        self,
        *command: str,
    ) -> None:
        """
        Execute a system command.
        """

        subprocess.Popen(
            command,
        )

    def lock(
        self,
    ) -> None:
        """
        Lock the current Windows session.
        """

        self._logger.info(
            "Locking Windows session."
        )

        ctypes.windll.user32.LockWorkStation()

    def sleep(
        self,
    ) -> None:
        """
        Put the computer into sleep mode.
        """

        self._logger.info(
            "Putting computer to sleep."
        )

        self._execute(
            "rundll32.exe",
            "powrprof.dll,SetSuspendState",
            "Sleep",
        )

    def shutdown(
        self,
    ) -> None:
        """
        Shut down the computer.
        """

        self._logger.info(
            "Shutting down computer."
        )

        self._execute(
            "shutdown",
            "/s",
            "/t",
            "0",
        )

    def restart(
        self,
    ) -> None:
        """
        Restart the computer.
        """

        self._logger.info(
            "Restarting computer."
        )

        self._execute(
            "shutdown",
            "/r",
            "/t",
            "0",
        )