"""
AI Filmmaking Orchestrator

Main script for orchestrating the complete AI filmmaking workflow.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Any

from ai_filmmaking.scene_generator import SceneGenerator
from ai_filmmaking.reference_builder import ReferenceBuilder
from ai_filmmaking.environment_manager import EnvironmentManager
from ai_filmmaking.video_pipeline import VideoPipeline
from ai_filmmaking.prompt_utils import PromptBuilder
from ai_filmmaking.quality_control import QualityChecker


class FilmmakingOrchestrator:
    """
    Orchestrates the complete AI filmmaking workflow from pre-production to final video.
    """

    def __init__(self, project_name: str, output_dir: str = "/tmp/outputs"):
        """
        Initialize the Filmmaking Orchestrator.

        Args:
            project_name: Name of the filmmaking project
            output_dir: Base output directory
        """
        self.project_name = project_name
        self.output_dir = Path(output_dir)
        
        # Initialize all components
        self.scene_generator = SceneGenerator(output_dir=str(self.output_dir))
        self.reference_builder = ReferenceBuilder(output_dir=str(self.output_dir))
        self.environment_manager = EnvironmentManager(output_dir=str(self.output_dir))
        self.video_pipeline = VideoPipeline(output_dir=str(self.output_dir))
        self.prompt_builder = PromptBuilder()
        self.quality_checker = QualityChecker(output_dir=str(self.output_dir))
        
        # Create project structure
        self.project_dirs = self.scene_generator.create_project_structure(project_name)
        
        print(f"Initialized AI Filmmaking Orchestrator for project: {project_name}")

    def create_restaurant_proposal_example(self):
        """
        Create the restaurant proposal example from the implementation guide.
        This demonstrates the complete workflow.
        """
        print("\n" + "="*60)
        print("Creating Restaurant Proposal Example Project")
        print("="*60 + "\n")

        # Phase 1: Define character and environment references
        print("Phase 1: Setting up references...")
        
        character_refs = {
            "alice": str(self.project_dirs["characters"] / "alice_reference.jpg"),
            "bob": str(self.project_dirs["characters"] / "bob_reference.jpg")
        }
        
        environment_ref = str(self.project_dirs["locations"] / "restaurant_interior.jpg")
        
        print(f"  Character references: {len(character_refs)}")
        print(f"  Environment reference: set")

        # Phase 2: Setup environment manager with 360° mapping
        print("\nPhase 2: Setting up environment mapping...")
        
        # Register character positions in the 360° space
        self.environment_manager.register_character_position("Alice", angle=180, depth=0.6)
        self.environment_manager.register_character_position("Bob", angle=0, depth=0.8)
        
        # Register camera angles for each scene
        scenes_camera_angles = {
            "scene_1_establishing": (0, 90),     # Wide angle
            "scene_2_ots_bob": (350, 90),        # Behind Bob
            "scene_3_closeup_alice": (180, 40),  # Close on Alice
            "scene_4_hand_ring": (0, 40),        # Close on hand
            "scene_5_kiss": (90, 60)             # Side angle for kiss
        }
        
        for scene_id, (angle, fov) in scenes_camera_angles.items():
            self.environment_manager.register_camera_angle(scene_id, angle, fov)
        
        print(f"  Registered {len(scenes_camera_angles)} camera angles")

        # Phase 3: Define scene sequence
        print("\nPhase 3: Defining scene sequence...")
        
        scenes = self._create_restaurant_proposal_scenes(character_refs, environment_ref)
        print(f"  Created {len(scenes)} scene configurations")

        # Phase 4: Generate scenes
        print("\nPhase 4: Generating scene sequence...")
        
        scene_results = self.scene_generator.generate_scene_sequence(
            scenes=scenes,
            project_name=self.project_name
        )
        
        print(f"  Generated {len(scene_results)} scenes")
        for result in scene_results:
            print(f"    - {result['scene_name']}: {result['status']}")

        # Phase 5: Quality assessment
        print("\nPhase 5: Quality assessment...")
        
        for scene_result in scene_results:
            assessment = self.quality_checker.assess_scene(
                scene_path=scene_result["output_path"],
                scene_config=scene_result["config"]
            )
            print(f"    - {scene_result['scene_name']}: {assessment['overall_score']:.1f}/100 ({assessment['quality_level']})")

        # Generate quality report
        scene_names = [r["scene_name"] for r in scene_results]
        quality_report = self.quality_checker.generate_quality_report(
            project_name=self.project_name,
            scenes=scene_names
        )

        # Phase 6: Video generation
        print("\nPhase 6: Generating motion videos...")
        
        motion_prompts = [
            "Camera remains still as characters interact",
            "Slow camera movement focusing on Alice's face",
            "Subtle movement as hand presents ring",
            "Characters move together in intimate moment"
        ]
        
        scene_paths = [r["output_path"] for r in scene_results]
        video_results = self.video_pipeline.generate_scene_sequence_video(
            scenes=scene_paths,
            motion_prompts=motion_prompts,
            project_name=self.project_name
        )
        
        print(f"  Generated {len(video_results)} video transitions")
        for video in video_results:
            print(f"    - {video['video_name']}: {video['duration']:.2f}s")

        # Phase 7: Summary
        print("\n" + "="*60)
        print("Project Summary")
        print("="*60)
        print(f"Project: {self.project_name}")
        print(f"Scenes generated: {len(scene_results)}")
        print(f"Videos generated: {len(video_results)}")
        print(f"Average quality: {quality_report['summary'].get('average_score', 0):.1f}/100")
        print(f"Output directory: {self.project_dirs['project_root']}")
        print("="*60 + "\n")

        return {
            "scenes": scene_results,
            "videos": video_results,
            "quality_report": quality_report
        }

    def _create_restaurant_proposal_scenes(
        self,
        character_refs: Dict[str, str],
        environment_ref: str
    ) -> List[Dict[str, Any]]:
        """
        Create scene configurations for the restaurant proposal example.

        Args:
            character_refs: Dictionary of character reference paths
            environment_ref: Environment reference path

        Returns:
            List of scene configurations
        """
        scenes = []

        # Scene 1: Establishing Shot
        scene_1_prompt = self.prompt_builder.build_scene_prompt(
            base_description="Two characters, Alice and Bob, sitting at a restaurant table opposite each other",
            camera_angle="establishing",
            lighting="romantic",
            characters=["Alice", "Bob"],
            location="romantic restaurant with candlelit tables",
            additional_details=["warm atmosphere", "elegant interior"],
            style="professional cinema photography, shot on RED camera"
        )
        
        scenes.append({
            "name": "001_establishing",
            "prompt": scene_1_prompt,
            "seed": 42,
            "character_references": list(character_refs.values()),
            "environment_reference": environment_ref
        })

        # Scene 2: Over-the-Shoulder (Bob's perspective)
        scene_2_prompt = self.prompt_builder.build_scene_prompt(
            base_description="Camera positioned behind Bob, over-the-shoulder shot looking at Alice smiling",
            camera_angle="ots",
            lighting="romantic",
            characters=["Alice", "Bob"],
            location="same restaurant",
            additional_details=[
                "half of Alice's face visible",
                "Bob's back partially in frame",
                "bar visible in background left",
                "large window in background right"
            ],
            style="cinematic film photography"
        )
        
        scenes.append({
            "name": "002_ots_bob",
            "prompt": scene_2_prompt,
            "seed": 43,
            "character_references": [character_refs["alice"]],
            "environment_reference": environment_ref
        })

        # Scene 3: Close-up on Alice
        scene_3_prompt = self.prompt_builder.build_scene_prompt(
            base_description="Extreme close-up of Alice's face, fills entire frame",
            camera_angle="extreme_closeup",
            lighting="romantic",
            characters=["Alice"],
            additional_details=[
                "soft focus background",
                "angular earrings visible",
                "delicate features",
                "gentle smile",
                "shallow depth of field"
            ],
            style="professional portrait photography"
        )
        
        scenes.append({
            "name": "003_closeup_alice",
            "prompt": scene_3_prompt,
            "seed": 44,
            "character_references": [character_refs["alice"]],
            "environment_reference": None  # No environment needed for close-up
        })

        # Scene 4: Hand with ring
        scene_4_prompt = self.prompt_builder.build_scene_prompt(
            base_description="Close-up of Bob's hand presenting small red ring box",
            camera_angle="closeup",
            lighting="dramatic",
            characters=["Bob"],
            additional_details=[
                "ring box centered in frame",
                "hand with five fingers clearly visible",
                "dramatic spotlight on box",
                "blurred romantic background",
                "sharp focus on ring box"
            ],
            style="cinematic close-up photography"
        )
        
        scenes.append({
            "name": "004_hand_ring",
            "prompt": scene_4_prompt,
            "seed": 45,
            "character_references": [character_refs["bob"]],
            "environment_reference": environment_ref
        })

        # Scene 5: Kiss scene
        scene_5_prompt = self.prompt_builder.build_scene_prompt(
            base_description="Alice and Bob kissing, faces very close together",
            camera_angle="two_shot",
            lighting="romantic",
            characters=["Alice", "Bob"],
            location="same restaurant table",
            additional_details=[
                "intimate moment",
                "warm candlelight",
                "emotional atmosphere",
                "tender scene"
            ],
            style="romantic cinema photography"
        )
        
        scenes.append({
            "name": "005_kiss",
            "prompt": scene_5_prompt,
            "seed": 46,
            "character_references": list(character_refs.values()),
            "environment_reference": environment_ref
        })

        return scenes

    def save_project_configuration(self):
        """Save the complete project configuration to a file."""
        config = {
            "project_name": self.project_name,
            "output_directory": str(self.project_dirs["project_root"]),
            "character_positions": self.environment_manager.character_positions,
            "camera_angles": self.environment_manager.camera_angles
        }

        config_path = self.project_dirs["project_root"] / "project_config.json"
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        print(f"Project configuration saved: {config_path}")


def main():
    """Main execution function."""
    print("\n🎬 AI Filmmaking Automation System 🎬\n")
    
    # Create orchestrator
    orchestrator = FilmmakingOrchestrator(
        project_name="restaurant_proposal",
        output_dir="/tmp/ai_filmmaking_projects"
    )
    
    # Run the restaurant proposal example
    results = orchestrator.create_restaurant_proposal_example()
    
    # Save project configuration
    orchestrator.save_project_configuration()
    
    print("\n✅ AI Filmmaking workflow completed successfully!\n")
    print("Next steps:")
    print("  1. Review generated scene configurations")
    print("  2. Execute workflows in ComfyUI")
    print("  3. Review quality assessments")
    print("  4. Generate final videos")
    print("  5. Post-process and add audio\n")


if __name__ == "__main__":
    main()
