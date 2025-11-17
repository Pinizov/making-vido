# n8n Integration Guide for ComfyUI Workflows

This guide will help you integrate the ComfyUI Any Workflow model with n8n, allowing you to automate AI image/video generation workflows without manual intervention.

## Overview

The ComfyUI model on Replicate provides automated access to run any ComfyUI workflow through a simple API. This eliminates the need to manually interact with AI models and provides seamless integration for your n8n automation workflows.

**Model URL:** https://replicate.com/comfyui/any-comfyui-workflow

## Prerequisites

1. A Replicate account with an API token (get one at https://replicate.com/account/api-tokens)
2. An n8n instance (cloud or self-hosted)
3. Your ComfyUI workflow in API JSON format

## Getting Your ComfyUI Workflow API JSON

Before integrating with n8n, you need to export your workflow in API format:

1. Open ComfyUI and enable "Dev mode Options" in settings
2. Load your workflow
3. Click "Save (API format)" to export the API JSON
4. Save this JSON - you'll use it in your n8n workflow

## n8n Integration Methods

### Method 1: Using HTTP Request Node (Recommended)

This method uses n8n's built-in HTTP Request node to call the Replicate API directly.

#### Step-by-Step Setup:

1. **Add HTTP Request Node** to your n8n workflow

2. **Configure the node:**
   - **Method:** POST
   - **URL:** `https://api.replicate.com/v1/predictions`
   - **Authentication:** Header Auth
     - **Name:** `Authorization`
     - **Value:** `Token YOUR_REPLICATE_API_TOKEN`
   - **Send Headers:**
     - `Content-Type`: `application/json`

3. **Set the Request Body** (JSON):
   ```json
   {
     "version": "VERSION_ID_OF_MODEL",
     "input": {
       "workflow_json": "YOUR_WORKFLOW_JSON_AS_STRING",
       "return_temp_files": false,
       "output_format": "webp",
       "output_quality": 90
     }
   }
   ```

4. **Add a Wait Node** to poll for completion (set to 10-30 seconds)

5. **Add another HTTP Request Node** to check status:
   - **Method:** GET
   - **URL:** `{{ $json.urls.get }}`
   - **Authentication:** Same as above

6. **Add a Loop** until `status` is `succeeded` or `failed`

### Method 2: Using Replicate Community Node

If available, use the community-maintained Replicate node:

1. Install the Replicate node from n8n community nodes
2. Add the Replicate node to your workflow
3. Configure with your API token
4. Select the `comfyui/any-comfyui-workflow` model
5. Provide your workflow JSON as input

## Example Workflows

### Example 1: Text-to-Image Generation

Here's a simple n8n workflow that generates images based on a webhook trigger:

```json
{
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "generate-image",
        "responseMode": "responseNode",
        "options": {}
      },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://api.replicate.com/v1/predictions",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "Content-Type",
              "value": "application/json"
            }
          ]
        },
        "sendBody": true,
        "bodyParameters": {
          "parameters": []
        },
        "jsonParameters": true,
        "options": {}
      },
      "name": "Create Prediction",
      "type": "n8n-nodes-base.httpRequest",
      "position": [450, 300]
    },
    {
      "parameters": {
        "amount": 10
      },
      "name": "Wait",
      "type": "n8n-nodes-base.wait",
      "position": [650, 300]
    },
    {
      "parameters": {
        "method": "GET",
        "url": "={{ $json.urls.get }}",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "options": {}
      },
      "name": "Check Status",
      "type": "n8n-nodes-base.httpRequest",
      "position": [850, 300]
    }
  ]
}
```

### Example 2: Batch Image Processing

Process multiple images from a data source:

1. **Trigger Node**: Schedule or webhook
2. **Read Data**: Get list of images/prompts from database or API
3. **Loop Node**: Iterate through each item
4. **HTTP Request**: Call Replicate API for each item
5. **Wait & Poll**: Check for completion
6. **Store Results**: Save output URLs to database or send notifications

## Input Parameters

The ComfyUI model accepts the following parameters:

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `workflow_json` | String/URL | Your ComfyUI workflow in API JSON format or URL to JSON file | Required |
| `input_file` | File/URL | Input image, video, tar, or zip file | None |
| `return_temp_files` | Boolean | Return temporary files (for debugging) | false |
| `output_format` | String | Output format: webp, jpg, png | webp |
| `output_quality` | Integer | Output quality (1-100) | 90 |
| `randomise_seeds` | Boolean | Automatically randomize seeds | true |
| `force_reset_cache` | Boolean | Force reset ComfyUI cache | false |

## Output Handling

The model returns an array of file URLs. In your n8n workflow:

1. **Parse the output** array from the prediction result
2. **Download files** using HTTP Request nodes if needed
3. **Store URLs** in your database or send via email/webhook
4. **Process further** with image analysis, compression, etc.

## Error Handling

Add error handling to your n8n workflow:

1. **Check prediction status**: Look for `failed` or `error` status
2. **Add retry logic**: Use IF node to retry failed predictions
3. **Send notifications**: Alert when workflows fail
4. **Log errors**: Store error messages for debugging

Example error check:
```
{{ $json.status === 'failed' ? $json.error : null }}
```

## Cost Optimization Tips

1. **Use `output_format: "webp"`** for smaller file sizes
2. **Set `return_temp_files: false`** to avoid unnecessary file transfers
3. **Cache workflow JSON** instead of sending it repeatedly
4. **Use workflow JSON URLs** instead of embedding large JSON in requests
5. **Batch operations** where possible to reduce API calls

## Advanced: Using Input Files

To process images or other files in your n8n workflow:

1. **Upload file to temporary storage** (S3, Dropbox, etc.)
2. **Get public URL** for the file
3. **Modify workflow JSON** to reference the URL:
   ```json
   {
     "3": {
       "inputs": {
         "image": "https://example.com/input-image.jpg"
       }
     }
   }
   ```
4. **Send workflow JSON** with URL references to Replicate

Alternatively, use the `input_file` parameter with a single file URL.

## Example Python Script (For Testing)

Before setting up n8n, test your integration with this Python script:

```python
import replicate
import json

# Load your workflow JSON
with open('workflow_api.json', 'r') as f:
    workflow = json.load(f)

# Run the model
output = replicate.run(
    "comfyui/any-comfyui-workflow:latest",
    input={
        "workflow_json": json.dumps(workflow),
        "output_format": "webp",
        "output_quality": 90
    }
)

# Print output URLs
for url in output:
    print(f"Generated: {url}")
```

## Common Use Cases

### 1. **Automated Social Media Content**
- Trigger: Schedule (daily/weekly)
- Action: Generate branded images
- Output: Post to social media APIs

### 2. **E-commerce Product Variations**
- Trigger: New product added
- Action: Generate product images with different backgrounds
- Output: Upload to product catalog

### 3. **Dynamic Email Headers**
- Trigger: Email campaign scheduled
- Action: Generate personalized header images
- Output: Embed in email template

### 4. **Video Thumbnail Generation**
- Trigger: Video uploaded
- Action: Generate custom thumbnails
- Output: Set as video thumbnail

## Troubleshooting

### Issue: "Model version not found"
- **Solution**: Use `"version": "latest"` or get the specific version ID from Replicate model page

### Issue: "Workflow JSON too large"
- **Solution**: Upload JSON to a public URL and reference the URL instead

### Issue: "Prediction taking too long"
- **Solution**: Increase wait time between polls, or use webhook callbacks

### Issue: "Invalid workflow JSON"
- **Solution**: Validate JSON syntax and ensure it's the API format (not UI format)

## Resources

- [Replicate API Documentation](https://replicate.com/docs/reference/http)
- [n8n HTTP Request Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/)
- [ComfyUI Workflow Guide](https://github.com/replicate/cog-comfyui)
- [n8n Community Nodes](https://www.npmjs.com/search?q=n8n-nodes-)

## Support

For issues or questions:
- Replicate Model: https://replicate.com/comfyui/any-comfyui-workflow
- GitHub Issues: https://github.com/replicate/cog-comfyui/issues
- n8n Community: https://community.n8n.io/

## License

This integration guide is provided as-is. Please refer to the respective licenses of Replicate, n8n, and ComfyUI for usage terms.
