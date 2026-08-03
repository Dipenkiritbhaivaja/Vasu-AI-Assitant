"""
System Information Service for VASU AI ASSISTANT.
"""

from __future__ import annotations

from assistant.core.logger import LoggerManager
import psutil
from assistant.system.models import CpuInfo

class SystemInfoService:
    """
    Provides read-only system information.
    """

    def __init__(
        self,
    ) -> None:

        self._logger = LoggerManager.get_logger(
            self.__class__.__name__
        )

    def cpu(
        self,
    ) -> CpuInfo:
        """
        Return CPU information.
        """

        self._logger.info(
            "Reading CPU information."
        )

        frequency = psutil.cpu_freq()

        return CpuInfo(
            usage=psutil.cpu_percent(
                interval=1,
            ),
            physical_cores=psutil.cpu_count(
                logical=False,
            ),
            logical_cores=psutil.cpu_count(),
            frequency=(
                frequency.current
                if frequency
                else 0.0
            ),
        )