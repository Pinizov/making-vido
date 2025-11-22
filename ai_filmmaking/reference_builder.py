"""
Reference Builder Module

Handles the compilation and management of character and environment references
for consistent scene generation.
"""

from typing import List, Optional, Tuple
from pathlib import Path
from PIL import Image
import json


class ReferenceBuilder:
    """
    Builds reference sheets by combining character, environment, and pose references
    into a single image that guides the AI generation process.
    """

    def __init__(self, output_dir: str = "/tmp/outputs"):
        """
        Initialize the Reference Builder.

        Args:
            output_dir: Directory to save compiled reference sheets
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def compile_reference_sheet(
        self,
        character_images: List[str],
        environment_image: Optional[str] = None,
        pose_reference: Optional[str] = None,
        output_name: str = "reference_sheet"
    ) -> str:
        """
        Compile multiple reference images into a single reference sheet.

        Args:
            character_images: List of paths to character reference images
            environment_image: Path to environment reference image
            pose_reference: Optional pose reference image
            output_name: Name for the output reference sheet

        Returns:
            Path to the compiled reference sheet
        """
        images_to_compile = []
        
        # Load character images
        for char_path in character_images:
            if Path(char_path).exists():
                try:
                    img = Image.open(char_path)
                    # Resize to standard size (512x512 for references)
                    img = img.resize((512, 512), Image.LANCZOS)
                    images_to_compile.append(("character", img))
                    print(f"Loaded character reference: {char_path}")
                except Exception as e:
                    print(f"Error loading character image {char_path}: {e}")

        # Load environment image
        if environment_image and Path(environment_image).exists():
            try:
                img = Image.open(environment_image)
                img = img.resize((512, 512), Image.LANCZOS)
                images_to_compile.append(("environment", img))
                print(f"Loaded environment reference: {environment_image}")
            except Exception as e:
                print(f"Error loading environment image: {e}")

        # Load pose reference
        if pose_reference and Path(pose_reference).exists():
            try:
                img = Image.open(pose_reference)
                img = img.resize((512, 512), Image.LANCZOS)
                images_to_compile.append(("pose", img))
                print(f"Loaded pose reference: {pose_reference}")
            except Exception as e:
                print(f"Error loading pose reference: {e}")

        if not images_to_compile:
            raise ValueError("No valid reference images provided")

        # Compile into a grid
        compiled_sheet = self._create_image_grid(images_to_compile)
        
        # Save the reference sheet
        output_path = self.output_dir / f"{output_name}.png"
        compiled_sheet.save(output_path, "PNG")
        
        print(f"Reference sheet compiled: {output_path}")
        return str(output_path)

    def _create_image_grid(
        self,
        images: List[Tuple[str, Image.Image]],
        grid_size: Optional[Tuple[int, int]] = None
    ) -> Image.Image:
        """
        Create a grid layout from multiple images.

        Args:
            images: List of tuples (label, image)
            grid_size: Optional grid size (cols, rows)

        Returns:
            Combined image grid
        """
        if not images:
            raise ValueError("No images provided for grid")

        num_images = len(images)
        
        # Calculate grid dimensions if not provided
        if grid_size is None:
            # Try to make a square-ish grid
            cols = int(num_images ** 0.5) + (1 if num_images ** 0.5 % 1 else 0)
            rows = (num_images + cols - 1) // cols
            grid_size = (cols, rows)
        
        cols, rows = grid_size
        img_width, img_height = 512, 512
        
        # Create blank canvas
        grid_width = cols * img_width
        grid_height = rows * img_height
        grid_image = Image.new('RGB', (grid_width, grid_height), color='white')
        
        # Place images in grid
        for idx, (label, img) in enumerate(images):
            col = idx % cols
            row = idx // cols
            x = col * img_width
            y = row * img_height
            grid_image.paste(img, (x, y))
        
        return grid_image

    def create_character_consistency_references(
        self,
        character_base: str,
        num_variations: int = 3
    ) -> List[str]:
        """
        Create multiple views/variations of a character for consistency.

        Args:
            character_base: Base character reference image
            num_variations: Number of variations to create

        Returns:
            List of paths to character variation references
        """
        # For now, this returns the base image multiple times
        # In a full implementation, this would generate different angles
        references = []
        
        if Path(character_base).exists():
            for i in range(num_variations):
                references.append(character_base)
        
        return references

    def save_reference_metadata(
        self,
        output_name: str,
        character_refs: List[str],
        environment_ref: Optional[str] = None,
        pose_ref: Optional[str] = None,
        additional_info: Optional[dict] = None
    ):
        """
        Save metadata about the reference compilation.

        Args:
            output_name: Name of the reference compilation
            character_refs: List of character reference paths
            environment_ref: Environment reference path
            pose_ref: Pose reference path
            additional_info: Any additional metadata
        """
        metadata = {
            "name": output_name,
            "character_references": character_refs,
            "environment_reference": environment_ref,
            "pose_reference": pose_ref,
            "additional_info": additional_info or {}
        }
        
        metadata_path = self.output_dir / f"{output_name}_metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Reference metadata saved: {metadata_path}")
