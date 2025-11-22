"""
Video Pipeline Module

Handles image-to-video generation and motion interpolation between scenes.
"""

from typing import List, Dict, Optional, Any
from pathlib import Path
import json


class VideoPipeline:
    """
    Manages the conversion of scene images to video with motion interpolation.
    Implements IMG2VID workflow for cinematic motion generation.
    """

    def __init__(self, output_dir: str = "/tmp/outputs"):
        """
        Initialize the Video Pipeline.

        Args:
            output_dir: Directory to save video outputs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_motion_video(
        self,
        start_frame: str,
        end_frame: str,
        motion_prompt: str,
        output_name: str = "motion_video",
        num_frames: int = 81,
        fps: int = 24,
        video_model: str = "wan_2.2"
    ) -> Dict[str, Any]:
        """
        Generate motion video between two keyframes.

        Args:
            start_frame: Path to starting frame image
            end_frame: Path to ending frame image
            motion_prompt: Description of the desired motion
            output_name: Name for output video
            num_frames: Number of frames to generate (default: 81)
            fps: Frames per second (default: 24)
            video_model: Video generation model to use

        Returns:
            Dictionary with video generation results
        """
        print(f"Generating motion video: {output_name}")
        print(f"Start frame: {start_frame}")
        print(f"End frame: {end_frame}")
        print(f"Motion: {motion_prompt}")
        print(f"Frames: {num_frames} at {fps} FPS")

        workflow = self._build_video_workflow(
            start_frame=start_frame,
            end_frame=end_frame,
            motion_prompt=motion_prompt,
            num_frames=num_frames,
            fps=fps,
            video_model=video_model
        )

        # Save workflow configuration
        workflow_path = self.output_dir / f"{output_name}_workflow.json"
        with open(workflow_path, "w") as f:
            json.dump(workflow, f, indent=2)

        result = {
            "video_name": output_name,
            "workflow_path": str(workflow_path),
            "output_path": str(self.output_dir / f"{output_name}.mp4"),
            "duration": num_frames / fps,
            "frames": num_frames,
            "fps": fps,
            "status": "configured"
        }

        return result

    def generate_scene_sequence_video(
        self,
        scenes: List[str],
        motion_prompts: List[str],
        project_name: str,
        fps: int = 24
    ) -> List[Dict[str, Any]]:
        """
        Generate videos for a sequence of scenes with transitions.

        Args:
            scenes: List of scene image paths
            motion_prompts: List of motion descriptions (one per transition)
            project_name: Name of the project
            fps: Frames per second

        Returns:
            List of video generation results
        """
        results = []
        
        if len(scenes) < 2:
            print("Warning: Need at least 2 scenes for video generation")
            return results

        # Generate videos for each scene transition
        for idx in range(len(scenes) - 1):
            start_frame = scenes[idx]
            end_frame = scenes[idx + 1]
            motion_prompt = motion_prompts[idx] if idx < len(motion_prompts) else "smooth transition"
            
            video_name = f"{project_name}_transition_{idx+1:03d}"
            
            result = self.generate_motion_video(
                start_frame=start_frame,
                end_frame=end_frame,
                motion_prompt=motion_prompt,
                output_name=video_name,
                fps=fps
            )
            
            results.append(result)

        return results

    def _build_video_workflow(
        self,
        start_frame: str,
        end_frame: str,
        motion_prompt: str,
        num_frames: int,
        fps: int,
        video_model: str
    ) -> Dict[str, Any]:
        """
        Build ComfyUI workflow for video generation.

        Args:
            start_frame: Path to start frame
            end_frame: Path to end frame
            motion_prompt: Motion description
            num_frames: Number of frames to generate
            fps: Frames per second
            video_model: Video model name

        Returns:
            Workflow configuration dictionary
        """
        workflow = {
            "meta": {
                "description": "IMG2VID Motion Generation",
                "version": "1.0.0"
            },
            "config": {
                "start_frame": start_frame,
                "end_frame": end_frame,
                "motion_prompt": motion_prompt,
                "num_frames": num_frames,
                "fps": fps,
                "video_model": video_model,
                "resolution": {
                    "width": 1024,
                    "height": 576
                }
            },
            "nodes": {
                "load_start_frame": {
                    "class_type": "LoadImage",
                    "inputs": {
                        "image": start_frame
                    }
                },
                "load_end_frame": {
                    "class_type": "LoadImage",
                    "inputs": {
                        "image": end_frame
                    }
                },
                "load_video_model": {
                    "class_type": "VideoModelLoader",
                    "inputs": {
                        "model_name": video_model,
                        "precision": "fp16"
                    }
                },
                "encode_motion_prompt": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {
                        "text": motion_prompt
                    }
                },
                "video_generation": {
                    "class_type": "KSamplerVideo",
                    "inputs": {
                        "steps": 50,
                        "cfg": 1.0,
                        "sampler_name": "euler_ancestral",
                        "scheduler": "karras",
                        "denoise": 1.0,
                        "length": num_frames
                    }
                },
                "video_encode": {
                    "class_type": "VideoEncode",
                    "inputs": {
                        "codec": "h264",
                        "crf": 18,  # Quality: 18 = visually lossless
                        "preset": "medium",
                        "fps": fps
                    }
                }
            }
        }

        return workflow

    def create_slideshow(
        self,
        images: List[str],
        duration_per_image: float,
        output_name: str = "slideshow",
        fps: int = 24,
        transition_type: str = "fade"
    ) -> Dict[str, Any]:
        """
        Create a slideshow video from a sequence of images.

        Args:
            images: List of image paths
            duration_per_image: Duration for each image in seconds
            output_name: Name for output video
            fps: Frames per second
            transition_type: Type of transition between images

        Returns:
            Dictionary with slideshow generation results
        """
        print(f"Creating slideshow: {output_name}")
        print(f"Images: {len(images)}")
        print(f"Duration per image: {duration_per_image}s")

        workflow = {
            "meta": {
                "description": "Image Slideshow",
                "version": "1.0.0"
            },
            "config": {
                "images": images,
                "duration_per_image": duration_per_image,
                "fps": fps,
                "transition_type": transition_type,
                "total_duration": len(images) * duration_per_image
            }
        }

        workflow_path = self.output_dir / f"{output_name}_slideshow_workflow.json"
        with open(workflow_path, "w") as f:
            json.dump(workflow, f, indent=2)

        result = {
            "slideshow_name": output_name,
            "workflow_path": str(workflow_path),
            "output_path": str(self.output_dir / f"{output_name}.mp4"),
            "total_duration": len(images) * duration_per_image,
            "images_count": len(images),
            "status": "configured"
        }

        return result
