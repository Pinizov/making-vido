"""
AI Filmmaking Automation Module

This module provides tools and utilities for automated AI filmmaking using ComfyUI workflows.
It implements the system described in AI-Filmmaking-Implementation-Guide.md.
"""

__version__ = "1.0.0"
__author__ = "AI Filmmaking Team"

from .scene_generator import SceneGenerator
from .reference_builder import ReferenceBuilder
from .environment_manager import EnvironmentManager
from .video_pipeline import VideoPipeline
from .prompt_utils import PromptBuilder
from .quality_control import QualityChecker

__all__ = [
    "SceneGenerator",
    "ReferenceBuilder",
    "EnvironmentManager",
    "VideoPipeline",
    "PromptBuilder",
    "QualityChecker",
]
