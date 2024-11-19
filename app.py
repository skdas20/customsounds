from flask import Flask, request, jsonify
from fer import FER
import random
import os
import cv2

app = Flask(__name__)

detector = FER()  # Initialize the FER emotion detector

# Function to estimate age based on face bounding box
def estimate_age(face_box):
    (x, y, w, h) = face_box
    face_area = w * h
    if face_area > 60000:
        return random.randint(45, 70)  # Older adult
    elif face_area > 40000:
        return random.randint(30, 45)  # Middle-aged adult
    elif face_area > 20000:
        return random.randint(18, 30)  # Young adult
    else:
        return random.randint(12, 18)  # Teenager

# Function to categorize generation based on age
def categorize_generation(age):
    if age <= 24:
        return "Gen Z"
    elif age <= 40:
        return "Millennial"
    elif age <= 56:
        return "Gen X"
    else:
        return "Boomer"

# Function to suggest songs based on emotion and generation
def suggest_song(emotion, generation):
    song_database = {
        "Gen Z": {
            "happy": ("Blinding Lights - The Weeknd", "https://www.youtube.com/watch?v=4NRXx6U8ABQ"),
            "sad": ("Someone You Loved - Lewis Capaldi", "https://www.youtube.com/watch?v=bCuhuePlP8o"),
            "angry": ("bad guy - Billie Eilish", "https://www.youtube.com/watch?v=DyDfgMOUjCI"),
            "neutral": ("Levitating - Dua Lipa", "https://www.youtube.com/watch?v=TUVcZfQe-Kw"),
        },
        "Millennial": {
            "happy": ("Uptown Funk - Mark Ronson ft. Bruno Mars", "https://www.youtube.com/watch?v=OPf0YbXqDm0"),
            "sad": ("Fix You - Coldplay", "https://www.youtube.com/watch?v=k4V3Mo61fJM"),
            "angry": ("Rolling in the Deep - Adele", "https://www.youtube.com/watch?v=rYEDA3JcQqw"),
            "neutral": ("Happy - Pharrell Williams", "https://www.youtube.com/watch?v=ZbZSe6N_BXs"),
        },
        "Gen X": {
            "happy": ("Don't Stop Believin' - Journey", "https://www.youtube.com/watch?v=1k8craCGpgs"),
            "sad": ("Tears in Heaven - Eric Clapton", "https://www.youtube.com/watch?v=JxPj3GAYYZ0"),
            "angry": ("Smells Like Teen Spirit - Nirvana", "https://www.youtube.com/watch?v=hTWKbfoikeg"),
            "neutral": ("Take On Me - a-ha", "https://www.youtube.com/watch?v=djV11Xbc914"),
        },
        "Boomer": {
            "happy": ("Here Comes The Sun - The Beatles", "https://www.youtube.com/watch?v=KQetemT1sWc"),
            "sad": ("Yesterday - The Beatles", "https://www.youtube.com/watch?v=jo505ZyaCbA"),
            "angry": ("Born to Be Wild - Steppenwolf", "https://www.youtube.com/watch?v=egMWlD3fLJ8"),
            "neutral": ("Hotel California - Eagles", "https://www.youtube.com/watch?v=EqPtz5qN7HM"),
        },
    }

    # Select song based on emotion and generation
    generation_songs = song_database.get(generation, {})
    return generation_songs.get(emotion.lower(), ("Unknown Song", ""))

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)  # Ensure the directory exists
    filepath = os.path.join(upload_dir, file.filename)
    file.save(filepath)

    # Read the uploaded image using OpenCV
    image = cv2.imread(filepath)

    # Detect emotions using FER
    emotions = detector.detect_emotions(image)
    if not emotions:
        os.remove(filepath)
        return jsonify({"error": "No face detected"}), 400

    # Analyze the first face detected
    emotion_data = emotions[0]
    face_box = emotion_data["box"]
    dominant_emotion = max(emotion_data["emotions"], key=emotion_data["emotions"].get)

    # Estimate age and determine generation
    age = estimate_age(face_box)
    generation = categorize_generation(age)

    # Suggest a song
    song_title, song_link = suggest_song(dominant_emotion, generation)

    # Clean up the uploaded file
    os.remove(filepath)

    # Return the analysis results
    return jsonify({
        "age": age,
        "generation": generation,
        "emotion": dominant_emotion,
        "suggested_song": {
            "title": song_title,
            "link": song_link
        },
        "face_box": face_box  # Include face box details for debugging
    })
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
