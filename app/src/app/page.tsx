'use client';

import React, { useState } from 'react';
import { Box, Container, Grid, Button, Typography, Paper, TextField, Divider, CircularProgress } from '@mui/material';
import { AutoAwesome, PhotoCamera, AutoFixHigh } from '@mui/icons-material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import ImageUploader from '@/components/ImageUploader';
import StyleSelector from '@/components/StyleSelector';

const theme = createTheme({
  palette: {
    primary: {
      main: '#2563eb',
    },
    background: {
      default: '#f8fafc',
    }
  },
  typography: {
    fontFamily: '"Outfit", "Roboto", sans-serif',
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
        }
      }
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          textTransform: 'none',
          fontWeight: 600,
        }
      }
    }
  }
});

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [selectedStyle, setSelectedStyle] = useState<string>('Modern');
  const [customPrompt, setCustomPrompt] = useState<string>('');
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
        custom_prompt: selectedStyle === 'Custom' ? customPrompt : null,
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
      <Box sx={{ minHeight: '100vh', bgcolor: 'background.default', py: 6 }}>
        <Container maxWidth="lg">
          <Box sx={{ mb: 6, textAlign: 'center' }}>
            <Typography variant="h3" sx={{ fontWeight: 800, color: '#1e293b', mb: 1 }}>
              AI Interior Decorator
            </Typography>
            <Typography variant="h6" color="text.secondary" sx={{ fontWeight: 400 }}>
              Transform your room in seconds using AI
            </Typography>
          </Box>

          <Paper sx={{ p: { xs: 2, sm: 3, md: 4 }, mb: 4, overflow: 'hidden' }}>
            <Grid container spacing={{ xs: 2, md: 4 }}>
              <Grid size={{ xs: 12, md: 5 }}>
                <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                  <PhotoCamera color="primary" /> 1. Upload Room
                </Typography>
                <ImageUploader 
                  onImageSelected={handleImageSelected} 
                  previewUrl={previewUrl} 
                  onClear={handleClearImage} 
                />
              </Grid>
              
              <Grid size={{ xs: 12, md: 7 }}>
                <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                  <AutoFixHigh color="primary" /> 2. Choose Style
                </Typography>
                
                <StyleSelector 
                  selectedStyle={selectedStyle} 
                  onStyleSelect={setSelectedStyle} 
                />

                {selectedStyle === 'Custom' && (
                  <Box sx={{ mt: 3 }}>
                    <TextField
                      fullWidth
                      label="Describe your custom style"
                      placeholder="e.g. Cyberpunk with neon lights, futuristic furniture, dark metal walls"
                      variant="outlined"
                      multiline
                      rows={2}
                      value={customPrompt}
                      onChange={(e) => setCustomPrompt(e.target.value)}
                    />
                  </Box>
                )}

                <Button
                  variant="contained"
                  size="large"
                  startIcon={isGenerating ? <CircularProgress size={20} color="inherit" /> : <AutoAwesome />}
                  onClick={handleGenerate}
                  disabled={!file || isGenerating || (selectedStyle === 'Custom' && !customPrompt)}
                  sx={{ mt: 4, py: 2, px: 6, fontSize: '1.1rem' }}
                  fullWidth
                >
                  {isGenerating ? 'AI is decorating...' : 'Generate Design'}
                </Button>
              </Grid>
            </Grid>
          </Paper>

          {(previewUrl || resultUrl || isGenerating) && (
            <>
              <Divider sx={{ my: 6 }} />
              <Grid container spacing={4}>
                <Grid size={{ xs: 12, md: 6 }}>
                  <Paper sx={{ p: 2, height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                      Original Room
                    </Typography>
                    <Box sx={{ flexGrow: 1, borderRadius: 2, overflow: 'hidden', bgcolor: '#000', minHeight: 400, position: 'relative' }}>
                      {previewUrl ? (
                        <img src={previewUrl} alt="Original" style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
                      ) : (
                        <Box sx={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#666' }}>
                          Upload an image to see preview
                        </Box>
                      )}
                    </Box>
                  </Paper>
                </Grid>

                <Grid size={{ xs: 12, md: 6 }}>
                  <Paper sx={{ p: 2, height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                      AI Generated Result
                    </Typography>
                    <Box sx={{ flexGrow: 1, borderRadius: 2, overflow: 'hidden', bgcolor: '#000', minHeight: 400, position: 'relative' }}>
                      {isGenerating ? (
                        <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', color: '#fff' }}>
                          <CircularProgress color="inherit" sx={{ mb: 2 }} />
                          <Typography>Decorating your room...</Typography>
                        </Box>
                      ) : resultUrl ? (
                        <img src={resultUrl} alt="Generated" style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
                      ) : (
                        <Box sx={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#666' }}>
                          Click Generate to see the result
                        </Box>
                      )}
                    </Box>
                  </Paper>
                </Grid>
              </Grid>
            </>
          )}
        </Container>
      </Box>
    </ThemeProvider>
  );
}
