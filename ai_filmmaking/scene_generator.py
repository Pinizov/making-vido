"""
Scene Generator Module

Handles the generation of individual scenes with character and environment consistency.
Implements the scene generation workflow from the AI Filmmaking Guide.
"""

import json
import os
from typing import List, Dict, Optional, Any
from pathlib import Path


class SceneGenerator:
    """
    Orchestrates the generation of cinematic scenes with character consistency
    and environment control.
    """

    def __init__(
        self,
        output_dir: str = "/tmp/outputs",
        input_dir: str = "/tmp/inputs",
        comfyui_server: Optional[str] = "127.0.0.1:8188"
    ):
        """
        Initialize the Scene Generator.

        Args:
            output_dir: Directory to save generated scenes
            input_dir: Directory containing input reference images
            comfyui_server: ComfyUI server address
        """
        self.output_dir = Path(output_dir)
        self.input_dir = Path(input_dir)
        self.comfyui_server = comfyui_server
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_single_scene(
        self,
        scene_config: Dict[str, Any],
        previous_scene: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a single scene based on configuration.

        Args:
            scene_config: Scene configuration including prompt, references, etc.
            previous_scene: Path to previous scene output for continuity

        Returns:
            Dictionary containing scene generation results
        """
        scene_name = scene_config.get("name", "scene")
        prompt = scene_config.get("prompt", "")
        seed = scene_config.get("seed", 42)
        character_refs = scene_config.get("character_references", [])
        environment_ref = scene_config.get("environment_reference", None)

        print(f"Generating scene: {scene_name}")
        print(f"Prompt: {prompt}")
        print(f"Seed: {seed}")
        print(f"Character references: {len(character_refs)}")

        # Build workflow configuration
        workflow = self._build_scene_workflow(
            prompt=prompt,
            seed=seed,
            character_refs=character_refs,
            environment_ref=environment_ref,
            previous_scene=previous_scene
        )

        # Store workflow configuration
        workflow_path = self.output_dir / f"{scene_name}_workflow.json"
        with open(workflow_path, "w") as f:
            json.dump(workflow, f, indent=2)

        result = {
            "scene_name": scene_name,
            "workflow_path": str(workflow_path),
            "output_path": str(self.output_dir / f"{scene_name}.png"),
            "status": "configured",
            "config": scene_config
        }

        return result

    def generate_scene_sequence(
        self,
        scenes: List[Dict[str, Any]],
        project_name: str
    ) -> List[Dict[str, Any]]:
        """
        Generate a sequence of scenes with automatic reference chaining.

        Args:
            scenes: List of scene configurations
            project_name: Name of the project/story

        Returns:
            List of scene generation results
        """
        results = []
        previous_scene = None

        print(f"Generating scene sequence for project: {project_name}")
        print(f"Total scenes: {len(scenes)}")

        for idx, scene_config in enumerate(scenes, 1):
            scene_config["name"] = scene_config.get("name", f"{project_name}_scene_{idx:03d}")
            
            result = self.generate_single_scene(
                scene_config=scene_config,
                previous_scene=previous_scene
            )
            
            results.append(result)
            previous_scene = result["output_path"]

        return results

    def _build_scene_workflow(
        self,
        prompt: str,
        seed: int,
        character_refs: List[str],
        environment_ref: Optional[str],
        previous_scene: Optional[str]
    ) -> Dict[str, Any]:
        """
        Build the ComfyUI workflow configuration for scene generation.

        Args:
            prompt: Scene description prompt
            seed: Random seed for reproducibility
            character_refs: List of character reference image paths
            environment_ref: Environment reference image path
            previous_scene: Previous scene output for continuity

        Returns:
            ComfyUI workflow configuration dictionary
        """
        # Base workflow structure
        workflow = {
            "meta": {
                "description": "AI Filmmaking Scene Generation",
                "version": "1.0.0"
            },
            "nodes": {},
            "config": {
                "prompt": prompt,
                "seed": seed,
                "steps": 4,  # Image Lightning LoRA optimized
                "cfg_scale": 1.0,  # Image Lightning LoRA setting
                "width": 1024,
                "height": 576,  # 16:9 cinematic aspect ratio
                "sampler": "dpmpp_2m_sde_gpu",
                "scheduler": "karras"
            },
            "references": {
                "characters": character_refs,
                "environment": environment_ref,
                "previous_scene": previous_scene
            }
        }

        # Add node definitions for the workflow
        # These would be expanded with actual ComfyUI node configurations
        workflow["nodes"]["load_checkpoint"] = {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": "qwen_image_edit.safetensors"
            }
        }

        workflow["nodes"]["load_lora_image_lightning"] = {
            "class_type": "LoraLoader",
            "inputs": {
                "lora_name": "image_lightning_4step.safetensors",
                "strength_model": 0.8,
                "strength_clip": 0.8
            }
        }

        workflow["nodes"]["load_lora_next_scene"] = {
            "class_type": "LoraLoader",
            "inputs": {
                "lora_name": "next_scene_lora.safetensors",
                "strength_model": 0.85,
                "strength_clip": 0.85
            }
        }

        workflow["nodes"]["clip_text_encode_positive"] = {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": prompt
            }
        }

        workflow["nodes"]["ksampler"] = {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed,
                "steps": 4,
                "cfg": 1.0,
                "sampler_name": "dpmpp_2m_sde_gpu",
                "scheduler": "karras",
                "denoise": 1.0
            }
        }

        return workflow

    def create_project_structure(self, project_name: str) -> Dict[str, Path]:
        """
        Create organized folder structure for a filmmaking project.

        Args:
            project_name: Name of the project

        Returns:
            Dictionary of project directories
        """
        base_path = self.output_dir / project_name
        
        dirs = {
            "project_root": base_path,
            "preproduction": base_path / "preproduction",
            "assets": base_path / "assets",
            "characters": base_path / "assets" / "characters",
            "locations": base_path / "assets" / "locations",
            "poses": base_path / "assets" / "poses",
            "workflows": base_path / "workflows",
            "outputs": base_path / "outputs",
            "scenes": base_path / "outputs" / "scenes",
            "video": base_path / "outputs" / "video",
            "environment": base_path / "outputs" / "environment",
            "logs": base_path / "logs"
        }

        for dir_path in dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)

        print(f"Created project structure for: {project_name}")
        return dirs
