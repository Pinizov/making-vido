"""
Test script for AI Filmmaking Automation

This script demonstrates the AI filmmaking capabilities.
"""

import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from ai_filmmaking.scene_generator import SceneGenerator
from ai_filmmaking.reference_builder import ReferenceBuilder
from ai_filmmaking.environment_manager import EnvironmentManager
from ai_filmmaking.video_pipeline import VideoPipeline
from ai_filmmaking.prompt_utils import PromptBuilder
from ai_filmmaking.quality_control import QualityChecker
from ai_filmmaking.orchestrator import FilmmakingOrchestrator


def test_scene_generator():
    """Test scene generator functionality."""
    print("\n" + "="*60)
    print("Testing Scene Generator")
    print("="*60)
    
    generator = SceneGenerator(output_dir="/tmp/test_ai_filmmaking")
    
    # Create project structure
    dirs = generator.create_project_structure("test_project")
    print(f"✓ Created project structure at: {dirs['project_root']}")
    
    # Test single scene generation
    scene_config = {
        "name": "test_scene_001",
        "prompt": "Two characters at a restaurant table, cinematic lighting",
        "seed": 42,
        "character_references": ["character_1.jpg", "character_2.jpg"],
        "environment_reference": "restaurant.jpg"
    }
    
    result = generator.generate_single_scene(scene_config)
    print(f"✓ Scene workflow generated: {result['workflow_path']}")
    print(f"  Scene name: {result['scene_name']}")
    print(f"  Output path: {result['output_path']}")


def test_prompt_builder():
    """Test prompt builder functionality."""
    print("\n" + "="*60)
    print("Testing Prompt Builder")
    print("="*60)
    
    builder = PromptBuilder()
    
    # Test scene prompt
    prompt = builder.build_scene_prompt(
        base_description="Two characters talking at a table",
        camera_angle="ots",
        lighting="romantic",
        characters=["Alice", "Bob"],
        location="romantic restaurant"
    )
    print(f"✓ Scene prompt generated:")
    print(f"  {prompt}")
    
    # Test motion prompt
    motion = builder.build_motion_prompt(
        action="Characters move closer together",
        camera_movement="slow dolly in",
        pacing="smooth"
    )
    print(f"✓ Motion prompt generated:")
    print(f"  {motion}")
    
    # Test camera angle suggestions
    suggestions = builder.get_camera_angle_suggestions("dialogue")
    print(f"✓ Camera suggestions for dialogue scene: {suggestions}")


def test_environment_manager():
    """Test environment manager functionality."""
    print("\n" + "="*60)
    print("Testing Environment Manager")
    print("="*60)
    
    env_manager = EnvironmentManager(output_dir="/tmp/test_ai_filmmaking")
    
    # Register character positions
    env_manager.register_character_position("Alice", angle=180, depth=0.6)
    env_manager.register_character_position("Bob", angle=0, depth=0.8)
    print("✓ Character positions registered")
    
    # Register camera angles
    env_manager.register_camera_angle("scene_1", angle=0, field_of_view=90)
    env_manager.register_camera_angle("scene_2", angle=180, field_of_view=60)
    print("✓ Camera angles registered")
    
    # Get visible characters
    visible = env_manager.get_visible_characters("scene_1")
    print(f"✓ Characters visible in scene_1: {visible}")
    
    # Save environment map
    env_manager.save_environment_map("test_environment")
    print("✓ Environment map saved")


def test_video_pipeline():
    """Test video pipeline functionality."""
    print("\n" + "="*60)
    print("Testing Video Pipeline")
    print("="*60)
    
    pipeline = VideoPipeline(output_dir="/tmp/test_ai_filmmaking")
    
    # Test motion video configuration
    video_result = pipeline.generate_motion_video(
        start_frame="scene_1.png",
        end_frame="scene_5.png",
        motion_prompt="Smooth transition with characters moving closer",
        output_name="test_motion",
        num_frames=81,
        fps=24
    )
    print(f"✓ Motion video workflow generated:")
    print(f"  Name: {video_result['video_name']}")
    print(f"  Duration: {video_result['duration']:.2f}s")
    print(f"  Workflow: {video_result['workflow_path']}")


def test_quality_checker():
    """Test quality checker functionality."""
    print("\n" + "="*60)
    print("Testing Quality Checker")
    print("="*60)
    
    qa = QualityChecker(output_dir="/tmp/test_ai_filmmaking")
    
    # Test quality checklist
    checklist = qa.create_quality_checklist()
    print(f"✓ Quality checklist created with {len(checklist)} categories:")
    for category, items in checklist.items():
        print(f"  {category}: {len(items)} checks")
    
    # Test scene assessment (simulated)
    scene_config = {
        "name": "test_scene",
        "prompt": "Test prompt",
        "seed": 42
    }
    
    assessment = qa.assess_scene(
        scene_path="test_scene.png",
        scene_config=scene_config
    )
    print(f"✓ Scene assessment completed:")
    print(f"  Overall score: {assessment['overall_score']:.1f}/100")
    print(f"  Quality level: {assessment['quality_level']}")


def test_orchestrator():
    """Test the complete orchestrator."""
    print("\n" + "="*60)
    print("Testing Filmmaking Orchestrator")
    print("="*60)
    
    orchestrator = FilmmakingOrchestrator(
        project_name="test_orchestrator",
        output_dir="/tmp/test_ai_filmmaking"
    )
    
    print("✓ Orchestrator initialized")
    print(f"  Project: {orchestrator.project_name}")
    print(f"  Output dir: {orchestrator.output_dir}")
    
    # Save configuration
    orchestrator.save_project_configuration()
    print("✓ Project configuration saved")


def run_all_tests():
    """Run all tests."""
    print("\n🎬 AI Filmmaking Automation - Test Suite 🎬\n")
    
    try:
        test_scene_generator()
        test_prompt_builder()
        test_environment_manager()
        test_video_pipeline()
        test_quality_checker()
        test_orchestrator()
        
        print("\n" + "="*60)
        print("✅ All tests completed successfully!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
