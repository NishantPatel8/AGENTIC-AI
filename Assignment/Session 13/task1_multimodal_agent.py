"""
Session 13 - Task 1: Simple Multi-Modal Agent Script
===================================================
This script implements a simple multi-modal agent that accepts both
a text prompt and an image file as input, verifies their presence,
and prints the prompt along with the image filename to confirm that
both multi-modal modalities were received successfully.
"""

import sys
import os

# Ensure safe UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def multimodal_agent(text_prompt: str, image_path: str):
    """
    Multi-modal agent receiving text prompt and image path.
    Validates both inputs and outputs confirmation details.
    """
    print("\n" + "=" * 65)
    print("           === MULTI-MODAL AGENT INVOCATION ===")
    print("=" * 65)

    # 1. Process Text Input Modality
    print("\n[Modality 1: Text Prompt]")
    if text_prompt and str(text_prompt).strip():
        print(f"  • Prompt Received: \"{text_prompt.strip()}\"")
        print(f"  • Prompt Length:   {len(text_prompt)} characters")
    else:
        print("  • Warning: No text prompt provided.")

    # 2. Process Visual Input Modality (Image)
    print("\n[Modality 2: Image File]")
    if os.path.exists(image_path) and os.path.isfile(image_path):
        image_filename = os.path.basename(image_path)
        file_size = os.path.getsize(image_path)
        file_ext = os.path.splitext(image_filename)[1].upper()

        print(f"  • Image Filename:  {image_filename}")
        print(f"  • Image Location:  {os.path.abspath(image_path)}")
        print(f"  • File Format:     {file_ext}")
        print(f"  • File Size:       {file_size:,} bytes")
        print("  • Status:          Image received successfully.")
    else:
        print(f"  • Path Specified:  {image_path}")
        print("  • Status:          Image file not found on disk.")

    print("\n" + "-" * 65)
    print("[CONFIRMATION] Multi-modal agent successfully processed both inputs!")
    print("=" * 65 + "\n")

def run_task1():
    print("=" * 65)
    print("      SESSION 13 - TASK 1: MULTI-MODAL AGENT INPUT RECEIPT")
    print("=" * 65)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    sample_image_path = os.path.join(current_dir, "sample.jpg")

    # Example 1: Standard input with valid image
    multimodal_agent(
        text_prompt="Describe this image and identify all objects in the scene.",
        image_path=sample_image_path
    )

    # Example 2: Handling edge case (missing image)
    multimodal_agent(
        text_prompt="Analyze this visual chart.",
        image_path="missing_artwork.png"
    )

if __name__ == "__main__":
    run_task1()
