#!/usr/bin/env python3
"""
AI Filmmaking CLI Tool

Command-line interface for AI filmmaking automation.
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ai_filmmaking.orchestrator import FilmmakingOrchestrator
from ai_filmmaking.scene_generator import SceneGenerator
from ai_filmmaking.prompt_utils import PromptBuilder


def cmd_create_project(args):
    """Create a new filmmaking project."""
    print(f"Creating project: {args.name}")
    
    orchestrator = FilmmakingOrchestrator(
        project_name=args.name,
        output_dir=args.output_dir
    )
    
    print(f"✓ Project created at: {orchestrator.project_dirs['project_root']}")
    print("\nNext steps:")
    print("  1. Add character references to assets/characters/")
    print("  2. Add environment references to assets/locations/")
    print("  3. Run: filmmaking.py generate-scene --project {args.name}")


def cmd_generate_scene(args):
    """Generate a single scene."""
    print(f"Generating scene for project: {args.project}")
    
    generator = SceneGenerator(output_dir=args.output_dir)
    
    # Build prompt if components provided
    if args.camera or args.lighting:
        builder = PromptBuilder()
        prompt = builder.build_scene_prompt(
            base_description=args.prompt or "Two characters in a scene",
            camera_angle=args.camera or "establishing",
            lighting=args.lighting or "cinematic",
            characters=args.characters.split(",") if args.characters else None,
            location=args.location
        )
    else:
        prompt = args.prompt
    
    scene_config = {
        "name": args.name or "scene_001",
        "prompt": prompt,
        "seed": args.seed,
        "character_references": args.char_refs.split(",") if args.char_refs else [],
        "environment_reference": args.env_ref
    }
    
    result = generator.generate_single_scene(scene_config)
    print(f"✓ Scene workflow generated: {result['workflow_path']}")
    print(f"  Output will be saved to: {result['output_path']}")


def cmd_run_example(args):
    """Run the restaurant proposal example."""
    print("Running restaurant proposal example...")
    
    orchestrator = FilmmakingOrchestrator(
        project_name="restaurant_proposal",
        output_dir=args.output_dir
    )
    
    results = orchestrator.create_restaurant_proposal_example()
    
    print(f"\n✓ Example completed!")
    print(f"  Scenes generated: {len(results['scenes'])}")
    print(f"  Videos configured: {len(results['videos'])}")
    print(f"  Project location: {orchestrator.project_dirs['project_root']}")


def cmd_list_cameras(args):
    """List available camera angles."""
    builder = PromptBuilder()
    
    print("\nAvailable Camera Angles:")
    print("=" * 60)
    
    for key, camera in builder.CAMERA_ANGLES.items():
        print(f"\n{key.upper()}: {camera.name}")
        print(f"  Description: {camera.description}")
        print(f"  Keywords: {', '.join(camera.prompt_keywords[:3])}")


def cmd_list_lighting(args):
    """List available lighting setups."""
    builder = PromptBuilder()
    
    print("\nAvailable Lighting Setups:")
    print("=" * 60)
    
    for key, lighting in builder.LIGHTING_SETUPS.items():
        print(f"\n{key.upper()}: {lighting.name}")
        print(f"  Description: {lighting.description}")
        print(f"  Temperature: {lighting.temperature}")
        print(f"  Keywords: {', '.join(lighting.prompt_keywords[:3])}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AI Filmmaking Automation CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a new project
  python filmmaking.py create-project my_film

  # Generate a scene
  python filmmaking.py generate-scene --project my_film --name scene_001 \\
    --prompt "Two characters talking" --camera ots --lighting romantic

  # Run the restaurant example
  python filmmaking.py run-example

  # List camera angles
  python filmmaking.py list-cameras

For more information, see AI_FILMMAKING_QUICKSTART.md
        """
    )
    
    parser.add_argument(
        "--output-dir",
        default="/tmp/ai_filmmaking",
        help="Output directory for projects (default: /tmp/ai_filmmaking)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Create project command
    create_parser = subparsers.add_parser(
        "create-project",
        help="Create a new filmmaking project"
    )
    create_parser.add_argument("name", help="Project name")
    create_parser.set_defaults(func=cmd_create_project)
    
    # Generate scene command
    scene_parser = subparsers.add_parser(
        "generate-scene",
        help="Generate a single scene"
    )
    scene_parser.add_argument("--project", required=True, help="Project name")
    scene_parser.add_argument("--name", help="Scene name (default: scene_001)")
    scene_parser.add_argument("--prompt", help="Scene description")
    scene_parser.add_argument("--camera", help="Camera angle (e.g., ots, closeup)")
    scene_parser.add_argument("--lighting", help="Lighting setup (e.g., romantic, dramatic)")
    scene_parser.add_argument("--characters", help="Character names (comma-separated)")
    scene_parser.add_argument("--location", help="Location description")
    scene_parser.add_argument("--char-refs", help="Character reference paths (comma-separated)")
    scene_parser.add_argument("--env-ref", help="Environment reference path")
    scene_parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    scene_parser.set_defaults(func=cmd_generate_scene)
    
    # Run example command
    example_parser = subparsers.add_parser(
        "run-example",
        help="Run the restaurant proposal example"
    )
    example_parser.set_defaults(func=cmd_run_example)
    
    # List cameras command
    cameras_parser = subparsers.add_parser(
        "list-cameras",
        help="List available camera angles"
    )
    cameras_parser.set_defaults(func=cmd_list_cameras)
    
    # List lighting command
    lighting_parser = subparsers.add_parser(
        "list-lighting",
        help="List available lighting setups"
    )
    lighting_parser.set_defaults(func=cmd_list_lighting)
    
    # Parse and execute
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        args.func(args)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        if "--debug" in sys.argv:
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
