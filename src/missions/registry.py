"""
MLOpsHub: Production Quest - Mission Registry & Router

This module maps mission IDs (m01 through m21) to their respective
concrete mission implementation instances.
"""

from typing import Dict
from src.missions.base_mission import BaseMission
from src.missions.m01_roleplay import Mission01
from src.missions.m02_data_quality import Mission02
from src.missions.m03_baseline_model import Mission03
from src.missions.m04_reproducibility import Mission04
from src.missions.m05_dvc import Mission05
from src.missions.m06_mlflow import Mission06
from src.missions.m07_model_registry import Mission07
from src.missions.m08_feature_store import Mission08
from src.missions.m09_testing import Mission09
from src.missions.m10_ci import Mission10
from src.missions.m11_cd_docker import Mission11
from src.missions.m12_deployment import Mission12
from src.missions.m13_monitoring import Mission13
from src.missions.m14_fairness import Mission14
from src.missions.m15_explainability import Mission15
from src.missions.m16_governance import Mission16
from src.missions.m17_first_change import Mission17
from src.missions.m18_incident import Mission18
from src.missions.m19_rca import Mission19
from src.missions.m20_remediation import Mission20
from src.missions.m21_leadership import Mission21


class MissionRegistry:
    """Registry maintaining initialized singletons for each mission."""

    _instances: Dict[str, BaseMission] = {}

    @classmethod
    def get_mission(cls, mission_id: str) -> BaseMission:
        """
        Retrieve mission instance by identifier.

        Args:
            mission_id: String id like 'm01', 'm02', etc.

        Returns:
            Instantiated BaseMission instance.
        """
        if not cls._instances:
            cls._instances = {
                "m01": Mission01(),
                "m02": Mission02(),
                "m03": Mission03(),
                "m04": Mission04(),
                "m05": Mission05(),
                "m06": Mission06(),
                "m07": Mission07(),
                "m08": Mission08(),
                "m09": Mission09(),
                "m10": Mission10(),
                "m11": Mission11(),
                "m12": Mission12(),
                "m13": Mission13(),
                "m14": Mission14(),
                "m15": Mission15(),
                "m16": Mission16(),
                "m17": Mission17(),
                "m18": Mission18(),
                "m19": Mission19(),
                "m20": Mission20(),
                "m21": Mission21(),
            }

        return cls._instances.get(mission_id, cls._instances["m01"])
