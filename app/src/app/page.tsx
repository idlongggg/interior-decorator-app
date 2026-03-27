'use client';

import React, { useState, useEffect } from 'react';
import { Box, Container, Grid, Button, Typography, Paper, TextField, Divider, CircularProgress, Skeleton } from '@mui/material';
import { AutoAwesome, PhotoCamera, AutoFixHigh } from '@mui/icons-material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import ImageUploader from '@/components/ImageUploader';
import StyleSelector from '@/components/StyleSelector';
import ObjectsChecklist from '@/components/ObjectsChecklist';
import ImageComparison from '@/components/ImageComparison';
import { Chair, CompareArrows } from '@mui/icons-material';

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

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [selectedStyle, setSelectedStyle] = useState<string>('Modern');
  const [selectedObjects, setSelectedObjects] = useState<string[]>([]);
  const [customPrompt, setCustomPrompt] = useState<string>('');
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [resultUrl, setResultUrl] = useState<string | null>(null);
  const [progress, setProgress] = useState<number>(0);
  const [totalSteps, setTotalSteps] = useState<number>(40);
  const [remainingTime, setRemainingTime] = useState<number | null>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

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
      setProgress(0);

      const formData = new FormData();
      formData.append('file', file);

      const uploadRes = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData,
      });
      
      if (!uploadRes.ok) throw new Error('Failed to upload image');
      const uploadData = await uploadRes.json();

      const generatePayload = {
        image_path: uploadData.image_path,
        style: selectedStyle,
        objects: selectedObjects,
        room_type: null, // Let backend detect room type
        custom_prompt: selectedStyle === 'Custom' ? customPrompt : null,
      };

      const genRes = await fetch(`${API_URL}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(generatePayload),
      });

      if (!genRes.ok) throw new Error('Failed to generate image');
      const { task_id } = await genRes.json();

      // Start polling for status
      const pollInterval = setInterval(async () => {
        try {
          const statusRes = await fetch(`${API_URL}/status/${task_id}`);
          if (!statusRes.ok) return;
          
          const statusData = await statusRes.json();
          setProgress(statusData.progress || 0);
          setTotalSteps(statusData.total_steps || 40);
          setRemainingTime(statusData.remaining_time);

          if (statusData.status === 'completed') {
            clearInterval(pollInterval);
            setIsGenerating(false);
            setResultUrl(`${API_URL}${statusData.result_url}`);
          } else if (statusData.status === 'failed') {
            clearInterval(pollInterval);
            setIsGenerating(false);
            alert(`Generation failed: ${statusData.error}`);
          }
        } catch (err) {
          console.error('Polling error:', err);
        }
      }, 1000);

      // Clean up interval if component unmounts
      return () => clearInterval(pollInterval);
    } catch (error) {
      console.error(error);
      setIsGenerating(false);
      alert('An error occurred during generation.');
    }
  };

  if (!mounted) return null;

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

                <Typography variant="h6" sx={{ mt: 4, mb: 1, display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Chair color="primary" /> 3. Add Furniture (Optional)
                </Typography>
                <ObjectsChecklist 
                  selectedObjects={selectedObjects} 
                  onObjectsChange={setSelectedObjects} 
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
                  startIcon={isGenerating ? <CircularProgress variant="determinate" value={Math.min(100, (progress / totalSteps) * 100)} size={20} color="inherit" /> : <AutoAwesome />}
                  onClick={handleGenerate}
                  disabled={!file || isGenerating || (selectedStyle === 'Custom' && !customPrompt)}
                  sx={{ mt: 4, py: 2, px: 6, fontSize: '1.1rem' }}
                  fullWidth
                >
                  {isGenerating 
                    ? `AI is decorating... ${Math.round((progress / totalSteps) * 100)}%` 
                    : 'Generate Design'}
                </Button>
              </Grid>
            </Grid>
          </Paper>

          {(previewUrl || resultUrl || isGenerating) && (
            <Box sx={{ mt: 8 }}>
              <Divider sx={{ mb: 6 }}>
                <Typography variant="overline" sx={{ px: 2, color: 'text.secondary', fontWeight: 700, letterSpacing: 2 }}>
                  Your Transformation
                </Typography>
              </Divider>

              {resultUrl ? (
                <Box>
                  <Typography variant="h5" sx={{ mb: 3, fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1.5 }}>
                    <CompareArrows color="primary" sx={{ fontSize: 32 }} />
                    Compare Results
                  </Typography>
                  <Box sx={{ maxWidth: '1000px', mx: 'auto' }}>
                    <ImageComparison beforeImage={previewUrl || ''} afterImage={resultUrl} />
                    <Box sx={{ mt: 2, textAlign: 'center' }}>
                      <Typography variant="body2" color="text.secondary">
                        Slide horizontally to compare original and generated designs
                      </Typography>
                    </Box>
                  </Box>
                </Box>
              ) : (
                <Grid container spacing={4}>
                  <Grid size={{ xs: 12, md: 6 }}>
                    <Paper sx={{ p: 2, height: '100%', display: 'flex', flexDirection: 'column', border: '1px solid rgba(0,0,0,0.05)' }}>
                      <Typography variant="subtitle1" sx={{ mb: 2, fontWeight: 700, color: 'text.primary' }}>
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
                    <Paper sx={{ p: 2, height: '100%', display: 'flex', flexDirection: 'column', border: '1px solid rgba(0,0,0,0.05)' }}>
                      <Typography variant="subtitle1" sx={{ mb: 2, fontWeight: 700, color: 'text.primary' }}>
                        AI Generated Result
                      </Typography>
                      <Box sx={{ 
                        flexGrow: 1, 
                        borderRadius: 2, 
                        overflow: 'hidden', 
                        bgcolor: isGenerating ? 'transparent' : '#000', 
                        minHeight: 400, 
                        position: 'relative' 
                      }}>
                        {isGenerating ? (
                          <Box sx={{ 
                            height: '100%', 
                            display: 'flex', 
                            flexDirection: 'column', 
                            alignItems: 'center', 
                            justifyContent: 'center', 
                            color: '#fff', 
                            px: 4,
                            position: 'relative',
                            zIndex: 1
                          }}>
                            {previewUrl && (
                                <Box sx={{
                                    position: 'absolute',
                                    top: 0,
                                    left: 0,
                                    right: 0,
                                    bottom: 0,
                                    backgroundImage: `url(${previewUrl})`,
                                    backgroundSize: 'cover',
                                    backgroundPosition: 'center',
                                    filter: 'blur(10px) brightness(0.6)',
                                    zIndex: -1,
                                }} />
                            )}
                            
                            <Paper sx={{ 
                              p: { xs: 3, sm: 4 }, 
                              borderRadius: 4, 
                              bgcolor: 'rgba(255, 255, 255, 0.1)', 
                              backdropFilter: 'blur(20px)',
                              border: '1px solid rgba(255, 255, 255, 0.2)',
                              width: '100%',
                              maxWidth: 360,
                              textAlign: 'center',
                              boxShadow: '0 20px 25px -5px rgb(0 0 0 / 0.1)'
                            }}>
                              <CircularProgress 
                                variant="determinate" 
                                value={Math.min(100, (progress / totalSteps) * 100)} 
                                sx={{ 
                                  mb: 3, 
                                  color: '#fff',
                                  '& .MuiCircularProgress-circle': {
                                    strokeLinecap: 'round',
                                  }
                                }} 
                                size={54}
                                thickness={4}
                              />
                              
                              <Typography variant="h6" sx={{ mb: 1, fontWeight: 700 }}>
                                AI Decorating...
                              </Typography>
                              
                              <Typography variant="body2" sx={{ opacity: 0.9, mb: 3, fontWeight: 500 }}>
                                {remainingTime !== null ? `Estimated: ${remainingTime}s remaining` : 'Analyzing room structure...'}
                              </Typography>
                              
                              <Box sx={{ width: '100%', mb: 1, height: 6, bgcolor: 'rgba(255,255,255,0.2)', borderRadius: 3, overflow: 'hidden' }}>
                                <Box sx={{ 
                                  height: '100%', 
                                  width: `${Math.min(100, (progress / totalSteps) * 100)}%`, 
                                  bgcolor: '#fff', 
                                  transition: 'width 0.8s cubic-bezier(0.4, 0, 0.2, 1)' 
                                }} />
                              </Box>
                              
                              <Typography variant="caption" sx={{ opacity: 0.7, fontWeight: 600 }}>
                                Step {progress} of {totalSteps}
                              </Typography>
                            </Paper>
                          </Box>
                        ) : (
                          <Box sx={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#666' }}>
                             {file ? 'Click Generate to see the result' : 'Upload an image first'}
                          </Box>
                        )}
                      </Box>
                    </Paper>
                  </Grid>
                </Grid>
              )}
            </Box>
          )}
        </Container>
      </Box>
    </ThemeProvider>
  );
}
