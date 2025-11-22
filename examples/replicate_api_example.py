#!/usr/bin/env python3
"""
Example script for testing ComfyUI workflows with Replicate API
This script can be used to test your workflow before integrating with n8n

Requirements:
    pip install requests

Usage:
    export REPLICATE_API_TOKEN="your_token_here"
    python examples/replicate_api_example.py
"""

import os
import sys
import json
import time

try:
    import requests
except ImportError:
    print("Error: 'requests' library not found.")
    print("Install it with: pip install requests")
    sys.exit(1)

from typing import Optional, Dict, Any, List


class ReplicateComfyUI:
    """Helper class for interacting with ComfyUI model on Replicate"""
    
    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize the Replicate client
        
        Args:
            api_token: Your Replicate API token. If not provided, will read from REPLICATE_API_TOKEN env var
        """
        self.api_token = api_token or os.environ.get("REPLICATE_API_TOKEN")
        if not self.api_token:
            raise ValueError("REPLICATE_API_TOKEN not found. Set it as environment variable or pass to constructor")
        
        self.base_url = "https://api.replicate.com/v1"
        self.headers = {
            "Authorization": f"Token {self.api_token}",
            "Content-Type": "application/json"
        }
    
    def create_prediction(
        self,
        workflow_json: Dict[str, Any],
        input_file: Optional[str] = None,
        output_format: str = "webp",
        output_quality: int = 90,
        randomise_seeds: bool = True,
        return_temp_files: bool = False,
        version: str = "latest"
    ) -> Dict[str, Any]:
        """
        Create a prediction with the ComfyUI model
        
        Args:
            workflow_json: Your ComfyUI workflow as a dictionary
            input_file: Optional URL to input file (image, video, tar, or zip)
            output_format: Output image format (webp, jpg, png)
            output_quality: Output quality (1-100)
            randomise_seeds: Automatically randomize seeds
            return_temp_files: Return temporary files for debugging
            version: Model version ID or "latest"
        
        Returns:
            Prediction response from Replicate API
        """
        payload = {
            "version": version,
            "input": {
                "workflow_json": json.dumps(workflow_json),
                "output_format": output_format,
                "output_quality": output_quality,
                "randomise_seeds": randomise_seeds,
                "return_temp_files": return_temp_files
            }
        }
        
        if input_file:
            payload["input"]["input_file"] = input_file
        
        response = requests.post(
            f"{self.base_url}/predictions",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def get_prediction(self, prediction_id: str) -> Dict[str, Any]:
        """
        Get the status and results of a prediction
        
        Args:
            prediction_id: The ID of the prediction
        
        Returns:
            Prediction data from Replicate API
        """
        response = requests.get(
            f"{self.base_url}/predictions/{prediction_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def wait_for_prediction(
        self,
        prediction_id: str,
        poll_interval: int = 5,
        max_wait: int = 600
    ) -> Dict[str, Any]:
        """
        Wait for a prediction to complete
        
        Args:
            prediction_id: The ID of the prediction
            poll_interval: Seconds between status checks
            max_wait: Maximum seconds to wait
        
        Returns:
            Final prediction data
        
        Raises:
            TimeoutError: If prediction doesn't complete within max_wait
            RuntimeError: If prediction fails
        """
        start_time = time.time()
        
        while True:
            if time.time() - start_time > max_wait:
                raise TimeoutError(f"Prediction did not complete within {max_wait} seconds")
            
            prediction = self.get_prediction(prediction_id)
            status = prediction.get("status")
            
            print(f"Status: {status}", end="\r")
            
            if status == "succeeded":
                print("\nPrediction succeeded!")
                return prediction
            elif status == "failed":
                error = prediction.get("error", "Unknown error")
                raise RuntimeError(f"Prediction failed: {error}")
            elif status in ["starting", "processing"]:
                time.sleep(poll_interval)
            else:
                print(f"\nUnexpected status: {status}")
                time.sleep(poll_interval)
    
    def run_workflow(
        self,
        workflow_json: Dict[str, Any],
        wait: bool = True,
        **kwargs
    ) -> List[str]:
        """
        Run a workflow and optionally wait for results
        
        Args:
            workflow_json: Your ComfyUI workflow as a dictionary
            wait: Whether to wait for completion
            **kwargs: Additional arguments passed to create_prediction
        
        Returns:
            List of output file URLs
        """
        prediction = self.create_prediction(workflow_json, **kwargs)
        prediction_id = prediction["id"]
        
        print(f"Created prediction: {prediction_id}")
        print(f"View at: https://replicate.com/p/{prediction_id}")
        
        if wait:
            final_prediction = self.wait_for_prediction(prediction_id)
            return final_prediction.get("output", [])
        else:
            return []


def example_text_to_image():
    """Example: Simple text-to-image generation"""
    
    # Simple SDXL workflow
    workflow = {
        "3": {
            "inputs": {
                "seed": 42,
                "steps": 20,
                "cfg": 7,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1,
                "model": ["4", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0]
            },
            "class_type": "KSampler"
        },
        "4": {
            "inputs": {
                "ckpt_name": "sd_xl_base_1.0.safetensors"
            },
            "class_type": "CheckpointLoaderSimple"
        },
        "5": {
            "inputs": {
                "width": 1024,
                "height": 1024,
                "batch_size": 1
            },
            "class_type": "EmptyLatentImage"
        },
        "6": {
            "inputs": {
                "text": "a beautiful mountain landscape at sunset, highly detailed, 8k",
                "clip": ["4", 1]
            },
            "class_type": "CLIPTextEncode"
        },
        "7": {
            "inputs": {
                "text": "blurry, low quality, text, watermark",
                "clip": ["4", 1]
            },
            "class_type": "CLIPTextEncode"
        },
        "8": {
            "inputs": {
                "samples": ["3", 0],
                "vae": ["4", 2]
            },
            "class_type": "VAEDecode"
        },
        "9": {
            "inputs": {
                "filename_prefix": "ComfyUI",
                "images": ["8", 0]
            },
            "class_type": "SaveImage"
        }
    }
    
    client = ReplicateComfyUI()
    outputs = client.run_workflow(workflow, output_format="webp", output_quality=90)
    
    print("\nGenerated images:")
    for i, url in enumerate(outputs, 1):
        print(f"{i}. {url}")
    
    return outputs


def example_from_file():
    """Example: Load workflow from file"""
    
    # Load workflow from JSON file
    workflow_path = "workflow_api.json"
    
    if not os.path.exists(workflow_path):
        print(f"Error: {workflow_path} not found")
        print("Export your workflow from ComfyUI using 'Save (API format)'")
        return
    
    with open(workflow_path, 'r') as f:
        workflow = json.load(f)
    
    client = ReplicateComfyUI()
    outputs = client.run_workflow(workflow)
    
    print("\nGenerated outputs:")
    for url in outputs:
        print(url)
    
    return outputs


def example_batch_processing():
    """Example: Process multiple prompts"""
    
    prompts = [
        "a serene lake at dawn",
        "a bustling city street at night",
        "a cozy cabin in the woods"
    ]
    
    client = ReplicateComfyUI()
    all_outputs = []
    
    for prompt in prompts:
        print(f"\nProcessing: {prompt}")
        
        workflow = {
            "3": {
                "inputs": {
                    "seed": int(time.time()),  # Different seed each time
                    "steps": 25,
                    "cfg": 7,
                    "sampler_name": "dpmpp_2m",
                    "scheduler": "karras",
                    "denoise": 1,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["5", 0]
                },
                "class_type": "KSampler"
            },
            "4": {
                "inputs": {
                    "ckpt_name": "sd_xl_base_1.0.safetensors"
                },
                "class_type": "CheckpointLoaderSimple"
            },
            "5": {
                "inputs": {
                    "width": 1024,
                    "height": 1024,
                    "batch_size": 1
                },
                "class_type": "EmptyLatentImage"
            },
            "6": {
                "inputs": {
                    "text": prompt,
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "7": {
                "inputs": {
                    "text": "blurry, low quality",
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "8": {
                "inputs": {
                    "samples": ["3", 0],
                    "vae": ["4", 2]
                },
                "class_type": "VAEDecode"
            },
            "9": {
                "inputs": {
                    "filename_prefix": "batch",
                    "images": ["8", 0]
                },
                "class_type": "SaveImage"
            }
        }
        
        outputs = client.run_workflow(workflow, randomise_seeds=False)
        all_outputs.extend(outputs)
    
    print("\n\nAll generated images:")
    for i, url in enumerate(all_outputs, 1):
        print(f"{i}. {url}")
    
    return all_outputs


def main():
    """Main function with example selector"""
    
    examples = {
        "1": ("Simple text-to-image", example_text_to_image),
        "2": ("Load workflow from file", example_from_file),
        "3": ("Batch processing", example_batch_processing)
    }
    
    print("ComfyUI Replicate API Examples")
    print("=" * 50)
    print("\nAvailable examples:")
    for key, (name, _) in examples.items():
        print(f"{key}. {name}")
    
    choice = input("\nSelect an example (1-3) or press Enter for example 1: ").strip() or "1"
    
    if choice in examples:
        name, func = examples[choice]
        print(f"\nRunning: {name}")
        print("-" * 50)
        try:
            func()
        except Exception as e:
            print(f"\nError: {e}")
            sys.exit(1)
    else:
        print("Invalid choice")
        sys.exit(1)


if __name__ == "__main__":
    main()
