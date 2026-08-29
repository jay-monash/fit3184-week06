import logging
import os
import time
from ultralytics import YOLO

# Configure logging
logging.basicConfig(filename="inference.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Define directories
input_dir = "image_source"
output_dir = "process_result"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

try:
    # Load the YOLO26 medium model

    model = YOLO("yolo26m.pt")

    # Iterate through images in the source directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            file_path = os.path.join(input_dir, filename)
            
            # Run inference and measure speed
            start_time = time.time()
            results = model(file_path)
            duration = time.time() - start_time

            # Log and save detection data with timing
            for result in results:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    label = model.names[class_id]
                    logger.info(f"File: {filename} | Detected: {label} (Confidence: {confidence:.2f}) | Speed: {duration:.4f}s")
                
                # Save result
                result.save(filename=os.path.join(output_dir, filename))
                print(f"Processed: {filename} in {duration:.4f}s")

except Exception as e:
    logger.error(f"Inference failed: {e}")
    print(f"An error occurred during inference: {e}")