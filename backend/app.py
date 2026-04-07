from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from sklearn.cluster import KMeans

app = Flask(__name__)
CORS(app)

# ---------- Predefined Thread Colors (20 shades) ----------
threads_list = [
    {"name": "White", "r": 255, "g": 255, "b": 255},
    {"name": "Soft Pink", "r": 255, "g": 201, "b": 201},
    {"name": "Rose Pink", "r": 245, "g": 173, "b": 173},
    {"name": "Coral", "r": 241, "g": 135, "b": 135},
    {"name": "Crimson Red", "r": 210, "g": 16, "b": 53},
    {"name": "Burgundy", "r": 145, "g": 40, "b": 59},
    {"name": "Peach", "r": 254, "g": 215, "b": 204},
    {"name": "Orange", "r": 253, "g": 156, "b": 151},
    {"name": "Deep Orange", "r": 233, "g": 106, "b": 103},
    {"name": "Scarlet", "r": 224, "g": 72, "b": 72},
    {"name": "Red", "r": 191, "g": 45, "b": 45},
    {"name": "Yellow", "r": 255, "g": 255, "b": 100},
    {"name": "Light Green", "r": 152, "g": 251, "b": 152},
    {"name": "Green", "r": 34, "g": 139, "b": 34},
    {"name": "Dark Green", "r": 0, "g": 100, "b": 0},
    {"name": "Sky Blue", "r": 135, "g": 206, "b": 235},
    {"name": "Blue", "r": 0, "g": 0, "b": 255},
    {"name": "Navy Blue", "r": 0, "g": 0, "b": 128},
    {"name": "Purple", "r": 128, "g": 0, "b": 128},
    {"name": "Black", "r": 0, "g": 0, "b": 0},
]


# ---------- Find Dominant Color in Fabric ----------
def get_dominant_color(image, k=3):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((-1, 3))
    image = np.float32(image)

    kmeans = KMeans(n_clusters=k, random_state=0)
    labels = kmeans.fit_predict(image)
    counts = np.bincount(labels)
    dominant = kmeans.cluster_centers_[np.argmax(counts)]
    return dominant


# ---------- Find Closest Thread Color ----------
def match_closest_thread(color_rgb):
    thread_colors = np.array([[t["r"], t["g"], t["b"]] for t in threads_list])
    distances = np.linalg.norm(thread_colors - color_rgb, axis=1)
    closest_index = np.argmin(distances)
    return threads_list[closest_index]


# ---------- API Endpoint ----------
@app.route("/match-color", methods=["POST"])
def match_color():
    try:
        file = request.files["image"]
        img_bytes = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({"error": "Invalid image"}), 400

        dominant_color = get_dominant_color(image)
        closest_thread = match_closest_thread(dominant_color)

        return jsonify({
            "name": closest_thread["name"],
            "r": int(closest_thread["r"]),
            "g": int(closest_thread["g"]),
            "b": int(closest_thread["b"]),
            "dominant": {
                "r": int(dominant_color[0]),
                "g": int(dominant_color[1]),
                "b": int(dominant_color[2])
            }
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Failed to process image"}), 500


if __name__ == "__main__":
    app.run(debug=True)
