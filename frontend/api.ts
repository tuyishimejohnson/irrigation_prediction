const API_URL = import.meta.env.PROD 
  ? "https://irrigation-prediction-api.onrender.com" 
  : "http://localhost:8000";

export default API_URL;