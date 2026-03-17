'use client';

import React, { useState } from 'react';
import { Box, Container, Grid, Button, Typography, Paper } from '@mui/material';
import { AutoAwesome } from '@mui/icons-material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import ImageUploader from '@/components/ImageUploader';
import StyleSelector from '@/components/StyleSelector';
import ResultDisplay from '@/components/ResultDisplay';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
  },
  typography: {
    fontFamily: 'Roboto, sans-serif',
  },
});

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [selectedStyle, setSelectedStyle] = useState<string>('Modern');
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [resultUrl, setResultUrl] = useState<string | null>(null);

  const handleImageSelected = (selectedFile: File) => {
    setFile(selectedFile);
    setPreviewUrl(URL.createObjectURL(selectedFile));
    setResultUrl(null);
  };

  const handleClearImage = () => {
    setFile(null);
    setPreviewUrl(null);
    setResultUrl(null);
  };

  const handleGenerate = async () => {
    if (!file) return;

    try {
      setIsGenerating(true);
      setResultUrl(null);

      const formData = new FormData();
      formData.append('file', file);

      const uploadRes = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });
      
      if (!uploadRes.ok) throw new Error('Failed to upload image');
      const uploadData = await uploadRes.json();

      const generatePayload = {
        image_path: uploadData.image_path,
        style: selectedStyle,
        room_type: 'Living Room',
      };

      const genRes = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(generatePayload),
      });

      if (!genRes.ok) throw new Error('Failed to generate image');
      const genData = await genRes.json();

      setResultUrl(`http://localhost:8000${genData.result_url}`);
    } catch (error) {
      console.error(error);
      alert('An error occurred during generation.');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box
        sx={{
          minHeight: '100vh',
          bgcolor: '#f5f5f5',
          py: 3,
          px: 2,
        }}
      >
        <Container maxWidth="lg">
          <Typography variant="h4" align="center" sx={{ mb: 3, fontWeight: 600 }}>
            Interior Decorator
          </Typography>

          <Grid container spacing={3}>
            <Grid size={{ xs: 12, md: 6 }}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" sx={{ mb: 2 }}>
                  Input
                </Typography>
                
                <Box sx={{ mb: 2 }}>
                  <ImageUploader 
                    onImageSelected={handleImageSelected} 
                    previewUrl={previewUrl} 
                    onClear={handleClearImage} 
                  />
                </Box>

                <StyleSelector 
                  selectedStyle={selectedStyle} 
                  onStyleSelect={setSelectedStyle} 
                />

                <Button
                  variant="contained"
                  size="large"
                  startIcon={<AutoAwesome />}
                  onClick={handleGenerate}
                  disabled={!file || isGenerating}
                  sx={{ mt: 3, py: 1.5 }}
                  fullWidth
                >
                  {isGenerating ? 'Generating...' : 'Generate'}
                </Button>
              </Paper>
            </Grid>

            <Grid size={{ xs: 12, md: 6 }}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" sx={{ mb: 2 }}>
                  Output
                </Typography>
                
                <Box>
                  <ResultDisplay 
                    originalImage={previewUrl} 
                    resultImage={resultUrl} 
                    isGenerating={isGenerating} 
                  />
                </Box>
              </Paper>
            </Grid>
          </Grid>
        </Container>
      </Box>
    </ThemeProvider>
  );
}
