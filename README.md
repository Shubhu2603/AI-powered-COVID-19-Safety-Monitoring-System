# AI-Powered COVID-19 Safety Monitoring System

An advanced computer vision application integrating deep learning models for real-time face mask detection and social distancing monitoring, wrapped in a responsive PyQt5 GUI.


## System Overview

### 1. User Authentication
Secure login system with SQLite database integration.
<p align="center"><br><img src="./Login Page.png" height="auto" width="auto"><br><br></p>


### 2. Intuitive Dashboard
User-friendly interface for easy navigation between different monitoring features.
<p align="center"><br><img src="./Landing Page.png" height="auto" width="auto"><br><br></p>


### 3. Face Mask Detection
Real-time face mask detection using deep learning models and OpenCV.
<p align="center"><br><img src="./Face Mask Test.png" height="auto" width="auto"><br><br></p>


### 4. Social Distancing Monitoring
Advanced social distancing violation detection with YOLO object detection.
<p align="center"><br><img src="./Social Dist Test.png" height="auto" width="auto"><br><br></p>

## Key Features

- Real-time video processing with OpenCV
- Deep learning-based face mask detection using TensorFlow/Keras
- YOLO-based object detection for social distancing analysis
- Multi-threaded video capture and processing
- SQLite database integration for user management
- SMTP integration for automated alert systems
- Responsive GUI design with PyQt5

### Core Technologies
- Python 3.x
- PyQt5
- OpenCV
- TensorFlow / Keras
- YOLO (You Only Look Once)
- SQLite
- CUDA (for GPU acceleration)

### Libraries & Frameworks
- NumPy for numerical operations
- imutils for video stream handling
- SciPy for spatial distance calculations

### Software Engineering Practices
- Multi-threading for performance optimization
- OOP principles in GUI and backend logic
- Event-driven programming with PyQt5
- Database design and management
- API integration (SMTP for email notifications)

### Computer Vision & AI
- Real-time video stream processing
- Object detection and tracking
- Transfer learning (MobileNetV2 for mask detection)
- Custom model training and deployment

### User Interface Design
- Responsive layout management
- Custom styling and theming
- Dynamic UI updates based on detection results

## System Requirements

- Python 3.7+
- NVIDIA GPU with CUDA support (for optimal performance)
- Webcam or IP camera for video input

