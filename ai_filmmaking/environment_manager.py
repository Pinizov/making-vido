"""
Environment Manager Module

Manages 360° environment generation and camera angle consistency
for cinematic scene generation.
"""

from typing import Dict, Optional, Tuple, List
from pathlib import Path
from PIL import Image
import json
import math


class EnvironmentManager:
    """
    Manages 360° panoramic environments and extracts camera-specific views
    for consistent background rendering across scenes.
    """

    def __init__(self, output_dir: str = "/tmp/outputs"):
        """
        Initialize the Environment Manager.

        Args:
            output_dir: Directory to save environment outputs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.character_positions = {}
        self.camera_angles = {}

    def register_character_position(
        self,
        character_name: str,
        angle_degrees: float,
        depth: float = 1.0
    ):
        """
        Register a character's position in the 360° space.

        Args:
            character_name: Name of the character
            angle_degrees: Angle in degrees (0-360)
            depth: Depth value (0=far, 1=close)
        """
        self.character_positions[character_name] = {
            "angle": angle_degrees % 360,
            "depth": depth
        }
        print(f"Registered character '{character_name}' at {angle_degrees}° with depth {depth}")

    def register_camera_angle(
        self,
        scene_id: str,
        angle: float,
        field_of_view: float = 60
    ):
        """
        Register a camera position and field of view for a scene.

        Args:
            scene_id: Scene identifier
            angle: Camera angle in degrees
            field_of_view: Field of view in degrees (typical: 60°)
        """
        visible_start = (angle - field_of_view / 2) % 360
        visible_end = (angle + field_of_view / 2) % 360
        
        self.camera_angles[scene_id] = {
            "angle": angle % 360,
            "fov": field_of_view,
            "visible_range": (visible_start, visible_end)
        }
        print(f"Registered camera for scene '{scene_id}' at {angle}° with FOV {field_of_view}°")

    def extract_camera_view(
        self,
        panorama_path: str,
        scene_id: str,
        output_name: Optional[str] = None
    ) -> str:
        """
        Extract a specific camera view from a 360° panorama.

        Args:
            panorama_path: Path to the 360° panorama image
            scene_id: Scene identifier with registered camera angle
            output_name: Optional custom output name

        Returns:
            Path to the extracted camera view
        """
        if scene_id not in self.camera_angles:
            raise ValueError(f"Camera angle not registered for scene: {scene_id}")

        camera = self.camera_angles[scene_id]
        
        try:
            panorama = Image.open(panorama_path)
            extracted_view = self._crop_panorama_view(panorama, camera)
            
            if output_name is None:
                output_name = f"{scene_id}_camera_view"
            
            output_path = self.output_dir / f"{output_name}.png"
            extracted_view.save(output_path, "PNG")
            
            print(f"Extracted camera view for {scene_id}: {output_path}")
            return str(output_path)
            
        except Exception as e:
            print(f"Error extracting camera view: {e}")
            raise

    def _crop_panorama_view(
        self,
        panorama: Image.Image,
        camera: Dict
    ) -> Image.Image:
        """
        Crop a view from the panorama based on camera settings.

        Args:
            panorama: PIL Image of the 360° panorama
            camera: Camera configuration dictionary

        Returns:
            Cropped PIL Image
        """
        width, height = panorama.size
        start_angle, end_angle = camera["visible_range"]
        
        # Convert angles to pixel positions
        start_px = int((start_angle / 360) * width)
        end_px = int((end_angle / 360) * width)
        
        # Handle wrapping (e.g., 350° to 10°)
        if end_px < start_px:
            # Split crop: left side + right side
            left_part = panorama.crop((start_px, 0, width, height))
            right_part = panorama.crop((0, 0, end_px, height))
            
            # Combine the two parts
            combined_width = left_part.width + right_part.width
            combined = Image.new('RGB', (combined_width, height))
            combined.paste(left_part, (0, 0))
            combined.paste(right_part, (left_part.width, 0))
            return combined
        else:
            # Simple crop
            return panorama.crop((start_px, 0, end_px, height))

    def get_visible_characters(self, scene_id: str) -> List[str]:
        """
        Get list of characters visible in a specific camera view.

        Args:
            scene_id: Scene identifier

        Returns:
            List of character names visible in this view
        """
        if scene_id not in self.camera_angles:
            return []

        camera = self.camera_angles[scene_id]
        start_angle, end_angle = camera["visible_range"]
        visible_chars = []

        for char_name, position in self.character_positions.items():
            char_angle = position["angle"]
            
            # Check if character is within camera view
            if start_angle <= end_angle:
                if start_angle <= char_angle <= end_angle:
                    visible_chars.append(char_name)
            else:
                # Handle wrapping case
                if char_angle >= start_angle or char_angle <= end_angle:
                    visible_chars.append(char_name)

        return visible_chars

    def generate_environment_workflow(
        self,
        base_image_path: str,
        output_name: str = "360_environment",
        padding_size: int = 100
    ) -> Dict:
        """
        Generate workflow configuration for 360° environment creation.

        Args:
            base_image_path: Path to base environment image
            output_name: Name for output environment
            padding_size: Padding size for expansion

        Returns:
            Workflow configuration dictionary
        """
        workflow = {
            "meta": {
                "description": "360° Environment Generation",
                "version": "1.0.0"
            },
            "config": {
                "base_image": base_image_path,
                "output_name": output_name,
                "padding_size": padding_size,
                "steps": 8,  # More steps for environment generation
                "cfg_scale": 1.0
            },
            "nodes": {
                "load_base_image": {
                    "class_type": "LoadImage",
                    "inputs": {
                        "image": base_image_path
                    }
                },
                "canvas_pad": {
                    "class_type": "ImagePad",
                    "inputs": {
                        "left": padding_size,
                        "right": padding_size,
                        "top": padding_size,
                        "bottom": padding_size
                    }
                },
                "load_360_lora": {
                    "class_type": "LoraLoader",
                    "inputs": {
                        "lora_name": "360_scene_layout.safetensors",
                        "strength_model": 1.0,
                        "strength_clip": 1.0
                    }
                },
                "generate_panorama": {
                    "class_type": "KSampler",
                    "inputs": {
                        "steps": 8,
                        "cfg": 1.0,
                        "sampler_name": "dpmpp_2m_sde_gpu",
                        "scheduler": "karras"
                    }
                }
            }
        }

        # Save workflow
        workflow_path = self.output_dir / f"{output_name}_workflow.json"
        with open(workflow_path, "w") as f:
            json.dump(workflow, f, indent=2)

        return workflow

    def save_environment_map(self, output_name: str):
        """
        Save the current environment mapping configuration.

        Args:
            output_name: Name for the environment map file
        """
        env_map = {
            "character_positions": self.character_positions,
            "camera_angles": self.camera_angles
        }

        map_path = self.output_dir / f"{output_name}_map.json"
        with open(map_path, "w") as f:
            json.dump(env_map, f, indent=2)

        print(f"Environment map saved: {map_path}")
