# Quick Reference: n8n + ComfyUI Integration

## 30-Second Setup

```bash
# 1. Get API token
Visit: https://replicate.com/account/api-tokens

# 2. Test with Python
export REPLICATE_API_TOKEN="your_token"
python examples/replicate_api_example.py

# 3. Import to n8n
Import: examples/n8n_workflows/simple_text_to_image.json
Add credentials: Replicate API Token
Activate workflow
```

## Essential API Call

```bash
curl -X POST https://api.replicate.com/v1/predictions \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "version": "latest",
    "input": {
      "workflow_json": "{\"3\":{\"inputs\":{...}}}",
      "output_format": "webp",
      "output_quality": 90
    }
  }'
```

## n8n HTTP Request Node Config

**Create Prediction:**
- Method: `POST`
- URL: `https://api.replicate.com/v1/predictions`
- Auth: Header Auth → `Authorization: Token YOUR_TOKEN`
- Body: JSON with workflow

**Check Status:**
- Method: `GET`  
- URL: `{{ $json.urls.get }}`
- Auth: Same as above
- Loop until `status === "succeeded"`

## Input Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `workflow_json` | string | *required* | Your workflow (API format) |
| `output_format` | string | `webp` | webp, jpg, png |
| `output_quality` | int | 90 | 1-100 |
| `randomise_seeds` | bool | true | Auto-randomize seeds |
| `input_file` | string | null | URL to input file |

## Common Workflows

### Text-to-Image
```javascript
{
  "6": {
    "inputs": {
      "text": "your prompt here",
      "clip": ["4", 1]
    },
    "class_type": "CLIPTextEncode"
  }
}
```

### Image-to-Image
```javascript
{
  "inputs": {
    "image": "https://example.com/input.jpg",
    "denoise": 0.7
  }
}
```

## Error Codes

- `401`: Invalid API token
- `422`: Invalid workflow JSON
- `500`: Internal server error
- Check: `$json.error` for details

## Cost Optimization

1. Use `output_format: "webp"` - smaller files
2. Set `return_temp_files: false` - less bandwidth
3. Cache workflow JSON - reduce payload size
4. Batch operations - reduce API calls
5. Use appropriate quality settings

## Docs & Examples

- 📘 Full Guide: [N8N_INTEGRATION.md](N8N_INTEGRATION.md)
- 📁 n8n Examples: [examples/n8n_workflows/](examples/n8n_workflows/)
- 🐍 Python Example: [examples/replicate_api_example.py](examples/replicate_api_example.py)
- 🌐 Model Page: https://replicate.com/comfyui/any-comfyui-workflow

## Quick Links

- [Get API Token](https://replicate.com/account/api-tokens)
- [Replicate Docs](https://replicate.com/docs)
- [n8n Docs](https://docs.n8n.io)
- [ComfyUI Guide](README.md)
