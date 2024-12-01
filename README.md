# irrigation_prediction

# Smart Irrigation Prediction System

A machine learning-powered web application that predicts irrigation needs for crops based on environmental conditions and plant growth stages.

## Features

- Real-time irrigation predictions based on:
  - Soil moisture levels
  - Temperature
  - Humidity
  - Soil type
  - Plant growth stage
- Confidence scores for predictions
- Detailed recommendations for irrigation timing
- Interactive web interface with sliders and dropdown menus
- Visual results display with confidence indicators

## Technologies

### Backend

- FastAPI (Python web framework)
- Scikit-learn (Machine learning)
- Joblib (Model serialization)
- NumPy (Numerical computations)

### Frontend

- React
- TypeScript
- Material-UI
- Axios (API calls)





## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/irrigation_prediction.git
   cd irrigation_prediction
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   - source venv/bin/activate  
   - On Windows: venv\Scripts\activate
   ```

3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the FastAPI server:
   ```bash
   uvicorn src.app:app --reload
   ```

