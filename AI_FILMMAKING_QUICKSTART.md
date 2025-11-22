# AI Filmmaking Automation - Quick Start Guide

## Overview

This AI Filmmaking Automation system enables you to create cinematic AI-generated videos with character consistency, environment control, and camera transitions. It implements the comprehensive workflow described in `AI-Filmmaking-Implementation-Guide.md`.

## Installation

### Prerequisites
- Python 3.10+
- ComfyUI installed and running
- GPU with 12GB+ VRAM (recommended)
- Required models (see Model Setup below)

### Model Setup

Download and install the following models:

1. **Qwen Image Edit** (Main Generation Engine)
   - Repository: `alibaba-pai/Qwen2-VL-ImageEdit`
   - Recommended: Q5 GGUF version
   - Place in: `ComfyUI/models/unet/`

2. **Image Lightning LoRA** (4-step acceleration)
   - Repository: `cybercortex/image-lightning`
   - File: `image-lightning-4-step.safetensors`
   - Place in: `ComfyUI/models/loras/`

3. **Next Scene LoRA** (Scene transitions)
   - Repository: `lovis93/next-scene-lora`
   - Place in: `ComfyUI/models/loras/`

4. **Video Generation Model** (Optional)
   - Wan 2.2 or LTX Video
   - Place in: `ComfyUI/models/video/`

## Quick Start

### 1. Run the Example Project

```python
from ai_filmmaking.orchestrator import FilmmakingOrchestrator

# Create a filmmaking project
orchestrator = FilmmakingOrchestrator(
    project_name="my_first_film",
    output_dir="/tmp/ai_filmmaking"
)

# Run the restaurant proposal example
results = orchestrator.create_restaurant_proposal_example()

# Save project configuration
orchestrator.save_project_configuration()
```

### 2. Using Individual Components

#### Scene Generation

```python
from ai_filmmaking.scene_generator import SceneGenerator

generator = SceneGenerator(output_dir="/tmp/outputs")

# Configure a scene
scene_config = {
    "name": "establishing_shot",
    "prompt": "Two characters at a restaurant. Cinematic lighting.",
    "seed": 42,
    "character_references": ["alice.jpg", "bob.jpg"],
    "environment_reference": "restaurant.jpg"
}

# Generate the scene
result = generator.generate_single_scene(scene_config)
print(f"Scene configuration saved: {result['workflow_path']}")
```

#### Prompt Building

```python
from ai_filmmaking.prompt_utils import PromptBuilder

builder = PromptBuilder()

# Build a comprehensive scene prompt
prompt = builder.build_scene_prompt(
    base_description="Two characters talking at a table",
    camera_angle="ots",  # Over-the-shoulder
    lighting="romantic",
    characters=["Alice", "Bob"],
    location="restaurant with candlelit tables"
)

print(prompt)
```

#### Reference Sheet Creation

```python
from ai_filmmaking.reference_builder import ReferenceBuilder

ref_builder = ReferenceBuilder(output_dir="/tmp/outputs")

# Compile multiple references into a single sheet
reference_sheet = ref_builder.compile_reference_sheet(
    character_images=["alice_ref.jpg", "bob_ref.jpg"],
    environment_image="restaurant_ref.jpg",
    output_name="scene_1_references"
)

print(f"Reference sheet created: {reference_sheet}")
```

#### Environment Management

```python
from ai_filmmaking.environment_manager import EnvironmentManager

env_manager = EnvironmentManager(output_dir="/tmp/outputs")

# Register character positions in 360° space
env_manager.register_character_position("Alice", angle=180, depth=0.6)
env_manager.register_character_position("Bob", angle=0, depth=0.8)

# Register camera angles for scenes
env_manager.register_camera_angle("scene_1", angle=0, field_of_view=90)
env_manager.register_camera_angle("scene_2", angle=350, field_of_view=90)

# Extract camera-specific views from 360° panorama
camera_view = env_manager.extract_camera_view(
    panorama_path="360_environment.png",
    scene_id="scene_1"
)
```

#### Video Generation

```python
from ai_filmmaking.video_pipeline import VideoPipeline

video_pipeline = VideoPipeline(output_dir="/tmp/outputs")

# Generate motion video between two scenes
video_result = video_pipeline.generate_motion_video(
    start_frame="scene_1.png",
    end_frame="scene_5.png",
    motion_prompt="Characters move together in romantic moment",
    output_name="romantic_transition",
    num_frames=81,
    fps=24
)

print(f"Video workflow created: {video_result['workflow_path']}")
```

#### Quality Control

```python
from ai_filmmaking.quality_control import QualityChecker

qa = QualityChecker(output_dir="/tmp/outputs")

# Assess scene quality
assessment = qa.assess_scene(
    scene_path="scene_1.png",
    scene_config=scene_config
)

print(f"Quality Score: {assessment['overall_score']}/100")
print(f"Level: {assessment['quality_level']}")

# Get improvement recommendations
recommendations = qa.get_improvement_recommendations("scene_1")
for rec in recommendations:
    print(f"  - {rec}")
```

## Workflow Templates

### Single Scene Template

Use the `workflows/ai_filmmaking_single_scene.json` template:

1. Load the workflow in ComfyUI
2. Configure character and environment references
3. Write your scene prompt
4. Adjust camera angle and lighting settings
5. Generate the scene

### Multi-Scene Workflow

Create a sequence of scenes with automatic reference chaining:

```python
scenes = [
    {
        "name": "001_establishing",
        "prompt": "Wide shot of restaurant",
        "seed": 42
    },
    {
        "name": "002_closeup",
        "prompt": "Close-up of character smiling",
        "seed": 43
    },
    # ... more scenes
]

results = generator.generate_scene_sequence(
    scenes=scenes,
    project_name="my_story"
)
```

## Project Structure

When you create a project, the following structure is created:

```
project_name/
├── preproduction/       # Scripts, storyboards
├── assets/
│   ├── characters/      # Character reference images
│   ├── locations/       # Environment references
│   └── poses/          # Pose references
├── workflows/          # ComfyUI workflow files
├── outputs/
│   ├── scenes/         # Generated scene images
│   ├── video/          # Generated videos
│   └── environment/    # 360° environment assets
└── logs/              # Quality reports, metadata
```

## Best Practices

### Prompt Engineering

1. **Be Specific**: Use detailed descriptions
   - ❌ "Two people talking"
   - ✅ "Alice and Bob sitting opposite at restaurant table, warm candlelight, over-the-shoulder shot"

2. **Use Cinematic Language**: Reference film terminology
   - Camera angles: "over-the-shoulder", "close-up", "establishing shot"
   - Lighting: "three-point lighting", "warm candlelight", "dramatic shadows"

3. **Maintain Consistency**: Reference character names and features
   - "Alice with angular earrings, maintaining exact appearance from reference"

### Character Consistency

1. Always use character reference images
2. Reference previous scenes for continuity
3. Emphasize distinctive features in prompts
4. Use consistent character names across scenes

### Environment Consistency

1. Create a 360° environment reference (optional but recommended)
2. Register character positions in the environment
3. Extract camera-specific views for each scene
4. Use environment references in all scene generations

### Video Generation

1. Start with scenes that are close in composition
2. Use specific motion prompts
3. Set appropriate frame count (81 frames ≈ 3.4s @ 24fps)
4. Review transitions and iterate if needed

## Troubleshooting

### Common Issues

**Issue**: Character doesn't look like reference
- Add character reference twice in input
- Emphasize distinctive features in prompt
- Adjust LoRA strength (try 0.7-0.9)
- Try different seed values

**Issue**: Wrong environment/background
- Add environment reference image
- Use 360° environment crop for camera angle
- Include spatial details in prompt ("bar on left, window on right")

**Issue**: Video motion looks unnatural
- Select closer keyframes (less interpolation needed)
- Write more specific motion prompts
- Increase generation steps (25→50)
- Reduce frame count for smoother results

## Advanced Features

### Custom Character LoRAs

Train custom character LoRAs for even better consistency:

```python
# This would require separate LoRA training workflow
# See AI-Filmmaking-Implementation-Guide.md Phase 15.1
```

### 360° Environment Generation

Generate seamless 360° environments:

```python
workflow = env_manager.generate_environment_workflow(
    base_image_path="restaurant_base.jpg",
    output_name="restaurant_360",
    padding_size=100
)
```

### Batch Processing

Process multiple projects:

```python
projects = ["project_1", "project_2", "project_3"]
for project_name in projects:
    orchestrator = FilmmakingOrchestrator(project_name)
    orchestrator.create_restaurant_proposal_example()
```

## Examples

See the `examples/` directory for:
- Complete restaurant proposal workflow
- Multi-location storytelling
- Time-lapse sequences
- Cinematic camera movements

## Support

For issues, questions, or contributions:
- Review the comprehensive guide: `AI-Filmmaking-Implementation-Guide.md`
- Check existing workflow templates in `workflows/`
- Examine example projects in `examples/`

## License

This project is released under the MIT License. See LICENSE file for details.
