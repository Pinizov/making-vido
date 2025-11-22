"""
Prompt Utilities Module

Provides utilities for building and optimizing prompts for AI filmmaking.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class CameraAngle:
    """Camera angle configuration."""
    name: str
    description: str
    prompt_keywords: List[str]


@dataclass
class LightingSetup:
    """Lighting configuration."""
    name: str
    description: str
    temperature: str
    prompt_keywords: List[str]


class PromptBuilder:
    """
    Builds optimized prompts for cinematic AI scene generation.
    Implements best practices from the AI Filmmaking Guide.
    """

    # Pre-defined camera angles
    CAMERA_ANGLES = {
        "establishing": CameraAngle(
            "Establishing Shot",
            "Wide shot showing full scene and environment",
            ["wide shot", "establishing shot", "full scene visible", "medium-wide"]
        ),
        "ots": CameraAngle(
            "Over-the-Shoulder",
            "Camera positioned behind one character looking at another",
            ["over-the-shoulder shot", "camera behind", "looking at", "partial occlusion"]
        ),
        "closeup": CameraAngle(
            "Close-up",
            "Tight shot focused on face or specific detail",
            ["close-up", "fills frame", "tight shot", "detailed view"]
        ),
        "extreme_closeup": CameraAngle(
            "Extreme Close-up",
            "Very tight shot on specific feature",
            ["extreme close-up", "fills entire frame", "intimate detail"]
        ),
        "medium": CameraAngle(
            "Medium Shot",
            "Character from waist up",
            ["medium shot", "waist up", "mid-shot"]
        ),
        "two_shot": CameraAngle(
            "Two Shot",
            "Both characters in frame",
            ["two-shot", "both characters", "facing each other"]
        )
    }

    # Pre-defined lighting setups
    LIGHTING_SETUPS = {
        "cinematic": LightingSetup(
            "Cinematic",
            "Professional three-point lighting",
            "warm",
            ["cinematic lighting", "professional", "three-point lighting", "soft shadows"]
        ),
        "romantic": LightingSetup(
            "Romantic",
            "Warm, soft candlelit ambiance",
            "warm 3200K",
            ["romantic lighting", "candlelit", "warm atmosphere", "soft glow"]
        ),
        "dramatic": LightingSetup(
            "Dramatic",
            "High contrast with strong shadows",
            "neutral",
            ["dramatic lighting", "high contrast", "strong shadows", "moody"]
        ),
        "natural": LightingSetup(
            "Natural",
            "Natural daylight",
            "cool 5600K",
            ["natural lighting", "daylight", "soft natural light"]
        )
    }

    def __init__(self):
        """Initialize the Prompt Builder."""
        pass

    def build_scene_prompt(
        self,
        base_description: str,
        camera_angle: str = "establishing",
        lighting: str = "cinematic",
        characters: Optional[List[str]] = None,
        location: Optional[str] = None,
        additional_details: Optional[List[str]] = None,
        style: str = "professional film photography"
    ) -> str:
        """
        Build a comprehensive scene prompt.

        Args:
            base_description: Core description of what's happening
            camera_angle: Camera angle type (key from CAMERA_ANGLES)
            lighting: Lighting setup (key from LIGHTING_SETUPS)
            characters: List of character names
            location: Location description
            additional_details: Additional specific details
            style: Overall style description

        Returns:
            Optimized prompt string
        """
        prompt_parts = []

        # Add character information
        if characters:
            char_str = ", ".join(characters)
            prompt_parts.append(f"Characters: {char_str}")

        # Add base description
        prompt_parts.append(base_description)

        # Add location
        if location:
            prompt_parts.append(f"Location: {location}")

        # Add camera angle
        if camera_angle in self.CAMERA_ANGLES:
            angle = self.CAMERA_ANGLES[camera_angle]
            prompt_parts.extend(angle.prompt_keywords)

        # Add lighting setup
        if lighting in self.LIGHTING_SETUPS:
            light = self.LIGHTING_SETUPS[lighting]
            prompt_parts.extend(light.prompt_keywords)

        # Add additional details
        if additional_details:
            prompt_parts.extend(additional_details)

        # Add style
        prompt_parts.append(style)

        # Join all parts into a coherent prompt
        final_prompt = ". ".join(prompt_parts) + "."
        
        return final_prompt

    def build_motion_prompt(
        self,
        action: str,
        camera_movement: str = "static",
        pacing: str = "smooth",
        atmosphere: Optional[str] = None
    ) -> str:
        """
        Build a motion prompt for video generation.

        Args:
            action: Main action/movement description
            camera_movement: Camera movement type
            pacing: Pacing of the motion
            atmosphere: Optional atmosphere description

        Returns:
            Motion prompt string
        """
        prompt_parts = [action]

        if camera_movement != "static":
            prompt_parts.append(f"Camera {camera_movement}")

        prompt_parts.append(f"{pacing} motion")

        if atmosphere:
            prompt_parts.append(atmosphere)

        return ". ".join(prompt_parts) + "."

    def build_character_consistency_prompt(
        self,
        character_name: str,
        distinctive_features: List[str],
        maintain_appearance: bool = True
    ) -> str:
        """
        Build a prompt emphasizing character consistency.

        Args:
            character_name: Name of the character
            distinctive_features: List of distinctive features
            maintain_appearance: Whether to emphasize maintaining appearance

        Returns:
            Character consistency prompt
        """
        prompt_parts = [f"{character_name}"]

        if distinctive_features:
            features_str = ", ".join(distinctive_features)
            prompt_parts.append(f"with distinctive features: {features_str}")

        if maintain_appearance:
            prompt_parts.append("maintaining exact appearance from reference")

        return ". ".join(prompt_parts)

    def build_spatial_prompt(
        self,
        foreground: List[str],
        background: List[str],
        spatial_relationships: Dict[str, str]
    ) -> str:
        """
        Build a prompt with clear spatial relationships.

        Args:
            foreground: Elements in the foreground
            background: Elements in the background
            spatial_relationships: Dict of spatial relationships (e.g., {"bar": "left", "window": "right"})

        Returns:
            Spatial prompt string
        """
        prompt_parts = []

        if foreground:
            fg_str = ", ".join(foreground)
            prompt_parts.append(f"Foreground: {fg_str}")

        if background:
            bg_str = ", ".join(background)
            prompt_parts.append(f"Background: {bg_str}")

        for element, position in spatial_relationships.items():
            prompt_parts.append(f"{element} to the {position}")

        return ". ".join(prompt_parts)

    def optimize_prompt(
        self,
        prompt: str,
        max_length: int = 200,
        remove_redundancy: bool = True
    ) -> str:
        """
        Optimize a prompt for better results.

        Args:
            prompt: Original prompt
            max_length: Maximum prompt length
            remove_redundancy: Whether to remove redundant phrases

        Returns:
            Optimized prompt
        """
        # Basic optimization: remove extra spaces and redundancy
        optimized = " ".join(prompt.split())

        if remove_redundancy:
            # Remove duplicate words (simple approach)
            words = optimized.split()
            seen = set()
            filtered_words = []
            for word in words:
                word_lower = word.lower().strip(".,;:")
                if word_lower not in seen or word_lower in ["the", "a", "and", "or"]:
                    filtered_words.append(word)
                    seen.add(word_lower)
            optimized = " ".join(filtered_words)

        # Truncate if too long
        if len(optimized) > max_length:
            optimized = optimized[:max_length].rsplit(" ", 1)[0] + "..."

        return optimized

    def get_camera_angle_suggestions(self, scene_type: str) -> List[str]:
        """
        Get camera angle suggestions for a scene type.

        Args:
            scene_type: Type of scene (e.g., "dialogue", "action", "intimate")

        Returns:
            List of suggested camera angles
        """
        suggestions = {
            "dialogue": ["ots", "two_shot", "medium"],
            "action": ["establishing", "medium", "closeup"],
            "intimate": ["closeup", "extreme_closeup", "two_shot"],
            "establishing": ["establishing", "medium"],
            "dramatic": ["closeup", "extreme_closeup", "ots"]
        }

        return suggestions.get(scene_type, ["establishing", "medium"])
