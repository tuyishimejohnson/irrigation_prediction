import { useState } from "react";
import axios from "axios";
import { Box, Typography, Paper, Button, CircularProgress, Alert } from '@mui/material';

interface TrainingResult {
  message: string;
  history: {
    accuracy: number;
    val_accuracy: number;
  }
}

interface RetrainProps {}
const Retrain: React.FC<RetrainProps> = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);
  const [trainingMetrics, setTrainingMetrics] = useState<TrainingResult | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
      setError(null);
      setResult(null);
      setTrainingMetrics(null);
    }
  };

  const handleRetrain = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);
    setResult(null);
    setTrainingMetrics(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post<TrainingResult>(
        'http://localhost:8000/retrain',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      setTrainingMetrics(response.data);
      setResult('Model retrained successfully!');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred during retraining');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 600, margin: '0 auto', padding: 3 }}>
      <Typography variant="h4" gutterBottom>
        Retrain Model
      </Typography>
      
      <Paper elevation={3} sx={{ padding: 3 }}>
        <Box sx={{ marginBottom: 3 }}>
          <input
            accept=".csv"
            style={{ display: 'none' }}
            id="csv-file"
            type="file"
            onChange={handleFileChange}
          />
          <label htmlFor="csv-file">
            <Button variant="contained" component="span">
              Choose CSV File
            </Button>
          </label>
          {file && (
            <Typography sx={{ marginTop: 1 }}>
              Selected file: {file.name}
            </Typography>
          )}
        </Box>

        <Button
          variant="contained"
          color="primary"
          onClick={handleRetrain}
          disabled={loading || !file}
          fullWidth
        >
          {loading ? <CircularProgress size={24} /> : "Retrain Model"}
        </Button>

        {error && (
          <Alert severity="error" sx={{ marginTop: 2 }}>
            {error}
          </Alert>
        )}

        {result && (
          <Alert severity="success" sx={{ marginTop: 2 }}>
            {result}
          </Alert>
        )}

        {trainingMetrics && (
          <Box sx={{ marginTop: 3 }}>
            <Typography variant="h6" gutterBottom>
              Training Results
            </Typography>
            <Paper sx={{ padding: 2 }}>
              <Typography>
                Training Accuracy: {(trainingMetrics.history.accuracy * 100).toFixed(2)}%
              </Typography>
              <Typography>
                Validation Accuracy: {(trainingMetrics.history.val_accuracy * 100).toFixed(2)}%
              </Typography>
            </Paper>
          </Box>
        )}
      </Paper>
    </Box>
  );
};

export default Retrain;

