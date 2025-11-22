# Project Description

## Overview

**cog-comfyui** is a production-ready implementation that enables running ComfyUI workflows on Replicate's cloud infrastructure. This project bridges the powerful node-based AI workflow system of ComfyUI with Replicate's scalable API platform, making it easy to deploy and run complex AI image and video generation workflows in the cloud.

## What is This Project?

This repository provides a containerized ComfyUI environment that can be deployed on Replicate, allowing users to:
- Run any ComfyUI workflow via API
- Access hundreds of pre-loaded AI model weights
- Use custom nodes for extended functionality
- Deploy personal instances for faster, dedicated inference
- Integrate AI workflows into applications via Replicate's API

## Key Features

### 🎨 Extensive Model Support
- **500+ pre-configured model weights** including:
  - Stable Diffusion variants (SD1.5, SDXL, SD3)
  - Video generation models (Wan 2.2, HunyuanVideo, LTXVideo, FlashVSR)
  - Image editing models (Qwen Image Edit)
  - ControlNet models for guided generation
  - LoRA and custom fine-tuned models
- Supports loading models from URLs (HuggingFace, CivitAI)
- Custom weight training via Replicate's train tab

### 🔌 Rich Custom Node Ecosystem
- **50+ custom node packages** pre-installed including:
  - IPAdapter Plus (image prompting)
  - AnimateDiff Evolved (animation)
  - VideoHelperSuite (video processing)
  - ControlNet Auxiliary (preprocessing)
  - Segment Anything 2 (segmentation)
  - ReActor (face swapping)
  - SUPIR (upscaling)
  - And many more specialized nodes

### 🚀 Deployment Options

1. **Public API**: Use `comfyui/any-comfyui-workflow` on Replicate
2. **Private Deployment**: Create dedicated instances for better performance
3. **Custom Fork**: Full control over ComfyUI version and configuration
4. **Train Tab**: Add custom weights without forking

### 🛠️ Technical Stack

- **Runtime**: Python 3.12 with CUDA 12.1 support
- **Container**: Cog-based containerization
- **Framework**: ComfyUI (latest version)
- **Infrastructure**: Replicate platform
- **GPU Support**: Optimized for NVIDIA GPUs (A100, H100)

## Current State (as of November 2025)

### Recent Updates

#### Latest Features (Nov 3, 2025)
- **FlashVSR Support**: Added video super-resolution capabilities with Wan2.1 models
- **HunyuanImage 2.1**: New state-of-the-art image generation models with refiner support
- **Qwen Image & Qwen Image Edit**: Advanced instruction-based image generation and editing

#### Video Generation Models
- Wan 2.2 models (14B parameters, text-to-video and image-to-video)
- Multiple precision options (fp16, fp8_scaled) for different VRAM requirements
- Support for both high-noise and low-noise generation modes

#### Recent Node Updates
The project maintains regular updates to custom nodes:
- ComfyUI-WanVideoWrapper (latest video generation features)
- ComfyUI-LTXVideo (Lightricks video model)
- ComfyUI-HunyuanVideoWrapper (Hunyuan video generation)
- ComfyUI-segment-anything-2 (improved segmentation)
- And 20+ other node packages updated in the last quarter

### Architecture

```
cog-comfyui/
├── ComfyUI/                 # Core ComfyUI submodule
├── custom_nodes.json        # List of installed custom nodes
├── weights.json             # 500+ model weight definitions
├── predict.py               # Main prediction endpoint
├── train.py                 # Custom weight training
├── comfyui.py              # ComfyUI server management
├── weights_downloader.py    # Model weight management
└── examples/                # Example workflows
```

### API Workflow

1. **Input**: Users provide ComfyUI workflow JSON (API format)
2. **Processing**: 
   - Workflow parsed and validated
   - Required models downloaded automatically
   - Input files handled (direct upload, URLs, or zip archives)
   - ComfyUI executes the workflow
3. **Output**: Generated images/videos returned via Replicate API

### Performance Characteristics

- **Cold Start**: ~30-60 seconds (includes model loading)
- **Warm Predictions**: 5-30 seconds (depending on workflow complexity)
- **Model Caching**: Frequently used models stay in memory
- **Scalability**: Auto-scales based on demand

## Use Cases

### Image Generation
- Text-to-image with various styles
- Image-to-image transformations
- Inpainting and outpainting
- Upscaling and enhancement
- Style transfer

### Video Creation
- Text-to-video generation
- Image-to-video animation
- Video interpolation and upscaling
- Motion synthesis
- Character-consistent video generation

### Advanced Workflows
- Multi-stage generation pipelines
- ControlNet-guided generation
- Face swapping and manipulation
- Background removal and composition
- AI filmmaking automation

## Documentation

- **Main Guide**: [README.md](README.md) - Complete usage instructions
- **Model Training**: [MAKING_A_MODEL_GUIDE.md](MAKING_A_MODEL_GUIDE.md)
- **Supported Weights**: [supported_weights.md](supported_weights.md)
- **AI Filmmaking**: [AI-Filmmaking-Implementation-Guide.md](AI-Filmmaking-Implementation-Guide.md)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md) - Detailed update history

## Getting Started

### For Users
1. Visit https://replicate.com/comfyui/any-comfyui-workflow
2. Export your ComfyUI workflow in API format
3. Run via web interface or API

### For Developers
```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/replicate/cog-comfyui.git

# Install custom nodes
./scripts/install_custom_nodes.py

# Test locally (requires GPU)
cog predict -i workflow_json=@your_workflow.json
```

## Project Status

✅ **Production Ready**
- Stable API
- Regular updates
- Extensive model support
- Active maintenance

🔄 **Continuously Updated**
- Monthly model additions
- Weekly node updates
- ComfyUI version tracking
- Community-driven improvements

## License

MIT License - Free for commercial and personal use

## Links

- **Replicate Model**: https://replicate.com/comfyui/any-comfyui-workflow
- **Repository**: https://github.com/replicate/cog-comfyui
- **ComfyUI**: https://github.com/comfyanonymous/ComfyUI
- **Documentation**: https://replicate.com/docs

---

*This project is maintained by the Replicate team and community contributors. It represents the intersection of ComfyUI's powerful workflow system and Replicate's cloud infrastructure, making advanced AI capabilities accessible through a simple API.*
