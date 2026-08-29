import logging
from flask import Flask, request, send_file
from ultralytics import YOLO
import io
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
model = YOLO("yolo26m.pt")

@app.route("/detect", methods=["POST"])
def detect_objects():
    try:
        # Check if file part exists
        if 'file' not in request.files:
            return "No file part", 400
        
        # Read image from request
        file = request.files['file']
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Run inference
        results = model(image)
        
        # Render annotated image
        annotated_frame = results[0].plot()
        
        # Convert to PIL and save to bytes
        annotated_image = Image.fromarray(annotated_frame)
        buf = io.BytesIO()
        annotated_image.save(buf, format="JPEG")
        buf.seek(0)
        
        logger.info("Successfully processed image detection request.")
        return send_file(buf, mimetype="image/jpeg")
    
    except Exception as e:
        logger.error(f"Error during inference: {e}")
        return "Internal Server Error", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
