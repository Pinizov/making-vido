# AI Filmmaking Examples

This directory contains example projects demonstrating various AI filmmaking techniques.

## Restaurant Proposal Example

A complete 5-scene cinematic sequence showing a romantic proposal at a restaurant.

### Scenes
1. **Establishing Shot**: Wide view of restaurant with both characters
2. **Over-the-Shoulder**: Camera behind Bob looking at Alice
3. **Close-up**: Extreme close-up of Alice's face
4. **Hand with Ring**: Close-up of Bob presenting ring
5. **Kiss Scene**: Intimate moment between characters

### Running the Example

```python
from ai_filmmaking.orchestrator import FilmmakingOrchestrator

orchestrator = FilmmakingOrchestrator(
    project_name="restaurant_proposal",
    output_dir="/tmp/ai_filmmaking"
)

results = orchestrator.create_restaurant_proposal_example()
```

### Project Structure

The example creates the following structure:

```
restaurant_proposal/
├── preproduction/
├── assets/
│   ├── characters/        # Alice and Bob references
│   ├── locations/         # Restaurant interior
│   └── poses/            # Pose references
├── workflows/            # Generated ComfyUI workflows
├── outputs/
│   ├── scenes/          # 5 generated scene images
│   ├── video/           # Motion videos
│   └── environment/     # 360° environment
└── logs/                # Quality reports
```

### Character Setup

**Alice**:
- Distinctive features: Angular earrings, elegant dress
- Position: Across the table (180°)
- Depth: 0.6 (mid-distance)

**Bob**:
- Distinctive features: Tailored suit, patterned shirt
- Position: Front (0°)
- Depth: 0.8 (closer)

### Camera Angles

1. **Scene 1** - Establishing: 0° angle, 90° FOV
2. **Scene 2** - OTS Bob: 350° angle, 90° FOV
3. **Scene 3** - Close-up Alice: 180° angle, 40° FOV
4. **Scene 4** - Hand Ring: 0° angle, 40° FOV
5. **Scene 5** - Kiss: 90° angle, 60° FOV

### Prompts Used

**Scene 1 - Establishing**:
```
Characters: Alice, Bob. Two characters, Alice and Bob, sitting at a 
restaurant table opposite each other. Location: romantic restaurant 
with candlelit tables. warm atmosphere. elegant interior. Medium-wide 
shot, establishing shot, full scene visible. romantic lighting, candlelit, 
warm atmosphere, soft glow. professional cinema photography, shot on RED camera.
```

**Scene 2 - Over-the-Shoulder**:
```
Characters: Alice, Bob. Camera positioned behind Bob, over-the-shoulder 
shot looking at Alice smiling. Location: same restaurant. half of Alice's 
face visible. Bob's back partially in frame. bar visible in background left. 
large window in background right. Over-the-shoulder shot, camera behind, 
looking at, partial occlusion. romantic lighting, candlelit, warm atmosphere, 
soft glow. cinematic film photography.
```

**Scene 3 - Close-up on Alice**:
```
Characters: Alice. Extreme close-up of Alice's face, fills entire frame. 
soft focus background. angular earrings visible. delicate features. gentle 
smile. shallow depth of field. Extreme close-up, fills entire frame, intimate 
detail. romantic lighting, candlelit, warm atmosphere, soft glow. professional 
portrait photography.
```

**Scene 4 - Hand with Ring**:
```
Characters: Bob. Close-up of Bob's hand presenting small red ring box. 
ring box centered in frame. hand with five fingers clearly visible. dramatic 
spotlight on box. blurred romantic background. sharp focus on ring box. 
Close-up, fills frame, tight shot, detailed view. dramatic lighting, high 
contrast, strong shadows, moody. cinematic close-up photography.
```

**Scene 5 - Kiss**:
```
Characters: Alice, Bob. Alice and Bob kissing, faces very close together. 
Location: same restaurant table. intimate moment. warm candlelight. 
emotional atmosphere. tender scene. Two-shot, both characters, facing 
each other. romantic lighting, candlelit, warm atmosphere, soft glow. 
romantic cinema photography.
```

### Video Transitions

Motion prompts for video generation:

1. **Scene 1→2**: "Camera remains still as characters interact"
2. **Scene 2→3**: "Slow camera movement focusing on Alice's face"
3. **Scene 3→4**: "Subtle movement as hand presents ring"
4. **Scene 4→5**: "Characters move together in intimate moment"

### Quality Targets

- Character Consistency: 85-95%
- Environment Consistency: 80-90%
- Composition Quality: 85-95%
- Motion Smoothness: 80-90%

### Expected Duration

- Scene Generation: 15-20 minutes (5 scenes × 3-4 min each)
- 360° Environment: 5 minutes
- Video Generation: 5-8 minutes per transition
- Total: ~30-45 minutes

## Tips for Best Results

1. **Character References**:
   - Use high-quality headshots
   - Clear facial features
   - Consistent lighting in references

2. **Environment References**:
   - Wide-angle room shots work best
   - Clear geometry and depth
   - Good lighting that matches scene mood

3. **Prompt Engineering**:
   - Be specific about spatial relationships
   - Use cinematic terminology
   - Reference character names consistently

4. **Quality Control**:
   - Review each scene before proceeding
   - Iterate on prompts if needed
   - Check character consistency across scenes

## Advanced Techniques

### Custom 360° Environment

Create a seamless 360° environment for better consistency:

```python
workflow = orchestrator.environment_manager.generate_environment_workflow(
    base_image_path="restaurant_base.jpg",
    output_name="restaurant_360",
    padding_size=100
)
```

### Quality Assessment

Run quality checks on generated scenes:

```python
assessment = orchestrator.quality_checker.assess_scene(
    scene_path="001_establishing.png",
    scene_config=scene_config
)

recommendations = orchestrator.quality_checker.get_improvement_recommendations(
    "001_establishing"
)
```

### Batch Processing

Process multiple variations:

```python
seeds = [42, 43, 44, 45, 46]
for seed in seeds:
    scene_config["seed"] = seed
    result = generator.generate_single_scene(scene_config)
```

## Next Steps

1. Execute the workflows in ComfyUI
2. Review generated scenes
3. Apply quality recommendations
4. Generate videos
5. Post-process with audio/music

## Resources

- Complete Implementation Guide: `../AI-Filmmaking-Implementation-Guide.md`
- Quick Start Guide: `../AI_FILMMAKING_QUICKSTART.md`
- Workflow Template: `../workflows/ai_filmmaking_single_scene.json`
