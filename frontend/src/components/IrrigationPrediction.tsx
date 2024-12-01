import React, { useState } from "react";
import axios from "axios";
import {
  Box,
  Button,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Slider,
  Typography,
  Paper,
  CircularProgress,
  Alert,
} from "@mui/material";

// Types
interface PredictionInput {
  soil_type: string;
  seedling_stage: string;
  moi: number;
  temp: number;
  humidity: number;
}

interface PredictionResult {
  needs_irrigation: boolean;
  confidence: number;
  recommendation: string;
  input_parameters: PredictionInput;
}

const IrrigationPredictionForm: React.FC = () => {
  // State for form inputs
  const [formData, setFormData] = useState<PredictionInput>({
    soil_type: "",
    seedling_stage: "",
    moi: 45,
    temp: 28,
    humidity: 65,
  });

  // State for API response
  const [predictionResult, setPredictionResult] =
    useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Available options
  const soilTypes = [
    "Black Soil",
    "Alluvial Soil",
    "Sandy Soil",
    "Red Soil",
    "Clay Soil",
    "Loam Soil",
    "Chalky Soil",
  ];
  const seedlingStages = [
    "Vegetative Growth / Root or Tuber Development",
    "Flowering",
    "Germination",
    "Seedling Stage",
    "Pollination",
    "Fruit/Grain/Bulb Formation",
    "Harvest",
    "Maturation",
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(
        "http://localhost:8000/predict",
        formData
      );
      setPredictionResult(response.data);
    } catch (err) {
      setError("Failed to get prediction. Please try again.");
      console.error("Prediction error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 800, margin: "auto", padding: 3 }}>
      <Typography variant="h4" gutterBottom className="text-2xl">
        Irrigation Prediction System
      </Typography>

      {/* Form */}
      <Paper elevation={3} sx={{ padding: 3, marginBottom: 3 }}>
        <form onSubmit={handleSubmit}>
          <FormControl fullWidth sx={{ marginBottom: 2 }}>
            <InputLabel>Soil Type</InputLabel>
            <Select
              value={formData.soil_type}
              label="Soil Type"
              onChange={(e) =>
                setFormData({ ...formData, soil_type: e.target.value })
              }
              required
            >
              {soilTypes.map((type) => (
                <MenuItem key={type} value={type}>
                  {type}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl fullWidth sx={{ marginBottom: 2 }}>
            <InputLabel>Seedling Stage</InputLabel>
            <Select
              value={formData.seedling_stage}
              label="Seedling Stage"
              onChange={(e) =>
                setFormData({ ...formData, seedling_stage: e.target.value })
              }
              required
            >
              {seedlingStages.map((stage) => (
                <MenuItem key={stage} value={stage}>
                  {stage}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <Box sx={{ marginBottom: 2 }}>
            <Typography gutterBottom>Moisture Index</Typography>
            <Slider
              value={formData.moi}
              onChange={(_, value) =>
                setFormData({ ...formData, moi: value as number })
              }
              min={0}
              max={100}
              valueLabelDisplay="auto"
            />
          </Box>

          <Box sx={{ marginBottom: 2 }}>
            <Typography gutterBottom>Temperature (°C)</Typography>
            <Slider
              value={formData.temp}
              onChange={(_, value) =>
                setFormData({ ...formData, temp: value as number })
              }
              min={0}
              max={50}
              valueLabelDisplay="auto"
            />
          </Box>

          <Box sx={{ marginBottom: 2 }}>
            <Typography gutterBottom>Humidity (%)</Typography>
            <Slider
              value={formData.humidity}
              onChange={(_, value) =>
                setFormData({ ...formData, humidity: value as number })
              }
              min={0}
              max={100}
              valueLabelDisplay="auto"
            />
          </Box>

          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : "Predict"}
          </Button>
        </form>
      </Paper>

      {/* Error Message */}
      {error && (
        <Alert severity="error" sx={{ marginBottom: 2 }}>
          {error}
        </Alert>
      )}

      {/* Results Display */}
      {predictionResult && (
        <Paper elevation={3} sx={{ padding: 3 }}>
          <Typography variant="h5" gutterBottom>
            Prediction Results
          </Typography>

          <Box sx={{ display: "flex", alignItems: "center", marginBottom: 2 }}>
            <CircularProgress
              variant="determinate"
              value={predictionResult.confidence * 100}
              size={80}
              sx={{ marginRight: 2 }}
            />
            <Box>
              <Typography
                variant="h6"
                color={predictionResult.needs_irrigation ? "error" : "success"}
              >
                {predictionResult.needs_irrigation
                  ? "Irrigation Needed"
                  : "No Irrigation Needed"}
              </Typography>
              <Typography>
                Confidence: {(predictionResult.confidence * 100).toFixed(1)}%
              </Typography>
            </Box>
          </Box>

          <Typography variant="h6" gutterBottom>
            Recommendation:
          </Typography>
          <Typography>{predictionResult.recommendation}</Typography>

          <Typography variant="h6" gutterBottom>
            Input Parameters:
          </Typography>
          <Box sx={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 2 }}>
            {Object.entries(predictionResult.input_parameters).map(
              ([key, value]) => (
                <Typography key={key}>
                  {key.replace(/_/g, " ").toUpperCase()}: {value}
                </Typography>
              )
            )}
          </Box>
        </Paper>
      )}
    </Box>
  );
};

export default IrrigationPredictionForm;
