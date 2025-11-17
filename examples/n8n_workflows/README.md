# n8n Workflow Examples for ComfyUI on Replicate

This directory contains example n8n workflows that demonstrate how to automate ComfyUI workflows using the Replicate API.

## Available Examples

### 1. Simple Text-to-Image (`simple_text_to_image.json`)

A basic webhook-triggered workflow that generates images from text prompts.

**Features:**
- Webhook trigger for easy integration
- Automatic workflow JSON generation
- Status polling with retry logic
- Returns image URLs in response

**How to use:**
1. Import the workflow into n8n
2. Configure your Replicate API credentials
3. Activate the workflow
4. Send POST requests to the webhook URL with:
   ```json
   {
     "prompt": "your image description here"
   }
   ```

### 2. Batch Processing (`batch_processing.json`)

A scheduled workflow that processes multiple images from a database queue.

**Features:**
- Scheduled execution (runs daily at 9 AM)
- Reads pending items from PostgreSQL database
- Processes items one at a time
- Updates database with results
- Error handling and retry logic

**Requirements:**
- PostgreSQL database with this schema:
  ```sql
  CREATE TABLE image_queue (
    id SERIAL PRIMARY KEY,
    prompt TEXT NOT NULL,
    negative_prompt TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    output_url TEXT,
    error TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
  );
  ```

**How to use:**
1. Import the workflow into n8n
2. Configure PostgreSQL and Replicate credentials
3. Populate the database with prompts
4. Activate the workflow (runs automatically)

## Setup Instructions

### 1. Configure Replicate API Credentials

In n8n, create credentials for HTTP Header Auth:

- **Name:** `Replicate API Token`
- **Header Name:** `Authorization`
- **Header Value:** `Token YOUR_REPLICATE_API_TOKEN`

Get your token from: https://replicate.com/account/api-tokens

### 2. Import Workflows

1. Open n8n
2. Go to **Workflows** → **Import from File**
3. Select one of the JSON files from this directory
4. Review and configure credential references
5. Activate the workflow

### 3. Test the Workflow

For webhook-based workflows:
- Copy the webhook URL from the trigger node
- Send a test request using curl or Postman
- Check the execution log in n8n

For scheduled workflows:
- Click "Execute Workflow" to run manually
- Check the execution log for results
- Verify database updates

## Customization

### Modify the ComfyUI Workflow

Each example includes JavaScript code that generates the workflow JSON. To customize:

1. Open the "Prepare Workflow" code node
2. Modify the `workflowJson` object
3. Update node IDs and parameters as needed
4. Test with a manual execution

### Change Model Parameters

Common parameters to adjust:

```javascript
{
  "output_format": "webp",     // webp, jpg, png
  "output_quality": 90,         // 1-100
  "randomise_seeds": true,      // auto-randomize seeds
  "return_temp_files": false    // include temp files
}
```

### Add Your Own Workflow

To use your own ComfyUI workflow:

1. Export your workflow from ComfyUI (API format)
2. Paste the JSON into the code node
3. Update dynamic values (prompts, seeds, etc.)
4. Test the workflow

## Troubleshooting

### "Credentials not found"
- Make sure you've created the Replicate API credentials in n8n
- Check that the credential name matches the workflow configuration

### "Workflow JSON invalid"
- Validate your JSON using a JSON validator
- Ensure you're using the API format (not UI format)
- Check for proper escaping of quotes and special characters

### "Prediction timeout"
- Increase the wait time in the Wait node
- Some workflows take longer depending on complexity
- Consider using webhook callbacks for very long operations

### "Database connection failed"
- Verify PostgreSQL credentials
- Check that the database and table exist
- Ensure n8n can reach the database server

## Best Practices

1. **Error Handling:** Always include error checking and logging
2. **Rate Limiting:** Don't overwhelm the API with too many concurrent requests
3. **Monitoring:** Set up notifications for failed executions
4. **Testing:** Test with a small dataset before processing large batches
5. **Cost Control:** Monitor Replicate usage to avoid unexpected charges

## Advanced Examples

For more complex scenarios, check the [n8n Integration Guide](../../N8N_INTEGRATION.md):

- Using input files from cloud storage
- Implementing webhook callbacks
- Processing video files
- Multi-step workflows with different models
- Integrating with other APIs (social media, storage, etc.)

## Resources

- [n8n Documentation](https://docs.n8n.io/)
- [Replicate API Reference](https://replicate.com/docs/reference/http)
- [ComfyUI Workflow Guide](../../README.md)
- [n8n Community](https://community.n8n.io/)

## Support

For issues or questions:
- n8n-specific: [n8n Community Forum](https://community.n8n.io/)
- ComfyUI/Replicate: [GitHub Issues](https://github.com/replicate/cog-comfyui/issues)
