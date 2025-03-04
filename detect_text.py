import cv2
import numpy as np
import matplotlib.pyplot as plt

# Path to pre-trained EAST model
EAST_MODEL_PATH = "models/frozen_east_text_detection.pb"

# Function to detect text regions in an image
def detect_text(image_path):
    image = cv2.imread(image_path)
    orig = image.copy()
    (H, W) = image.shape[:2]

    # Resize dimensions for EAST model
    newW, newH = 320, 320
    rW, rH = W / float(newW), H / float(newH)

    # Resize image
    image = cv2.resize(image, (newW, newH))
    blob = cv2.dnn.blobFromImage(image, 1.0, (newW, newH), (123.68, 116.78, 103.94), swapRB=True, crop=False)

    # Load pre-trained EAST model
    net = cv2.dnn.readNet(EAST_MODEL_PATH)
    net.setInput(blob)
    (scores, geometry) = net.forward(["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"])

    # Decode predictions
    def decode_predictions(scores, geometry):
        rects, confidences = [], []
        for y in range(scores.shape[2]):
            for x in range(scores.shape[3]):
                if scores[0, 0, y, x] < 0.5:
                    continue

                offsetX, offsetY = x * 4.0, y * 4.0
                angle = geometry[0, 4, y, x]
                cosA, sinA = np.cos(angle), np.sin(angle)
                h, w = geometry[0, 0, y, x], geometry[0, 1, y, x]

                endX, endY = int(offsetX + (cosA * w) + (sinA * h)), int(offsetY - (sinA * w) + (cosA * h))
                startX, startY = int(endX - w), int(endY - h)

                rects.append((startX, startY, endX, endY))
                confidences.append(scores[0, 0, y, x])

        return rects, confidences

    rects, confidences = decode_predictions(scores, geometry)
    indices = cv2.dnn.NMSBoxes(rects, confidences, 0.5, 0.4)

    # Draw bounding boxes
    for i in indices.flatten():
        startX, startY, endX, endY = rects[i]
        startX, startY, endX, endY = int(startX * rW), int(startY * rH), int(endX * rW), int(endY * rH)
        cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(orig, cv2.COLOR_BGR2RGB))
    plt.title("Detected Text Regions")
    plt.show()

# Test on a sample business card
detect_text("uploads/sample_card.jpg")