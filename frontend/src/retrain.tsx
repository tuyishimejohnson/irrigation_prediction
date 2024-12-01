import { useState } from 'react';
import axios from 'axios';
import { Box, Typography, Paper, Button, CircularProgress, Alert } from '@mui/material';

const Retrain = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
      setError(null);
    }
  };

  const handleRetrain = async () => {
    if (!file) {
      setError("Please select a CSV file first");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/retrain', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setResult(response.data.message);
    } catch (err) {
      setError("Failed to retrain model. Please check your CSV file format and try again.");
      console.error("Retrain error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 600, margin: 'auto', padding: 3 }}>
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
      </Paper>
    </Box>
  );
};

export default Retrain;
