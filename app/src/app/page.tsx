'use client';

import React, { useState, useEffect } from 'react';
import { Box, Container, Grid, Button, Typography, Paper, TextField, Divider, CircularProgress, Skeleton } from '@mui/material';
import { AutoAwesome, PhotoCamera, AutoFixHigh } from '@mui/icons-material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import ImageUploader from '@/components/ImageUploader';
import StyleSelector from '@/components/StyleSelector';
import ImageComparison from '@/components/ImageComparison';
import { CompareArrows } from '@mui/icons-material';

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

const PRIMARY_API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const FALLBACK_API_URL = process.env.NEXT_PUBLIC_FALLBACK_API_URL || 'https://rcjv1lk7-3000.asse.devtunnels.ms';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [selectedStyle, setSelectedStyle] = useState<string>('Modern');
  const [customPrompt, setCustomPrompt] = useState<string>('');
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [resultUrl, setResultUrl] = useState<string | null>(null);
  const [progress, setProgress] = useState<number>(0);
  const [totalSteps, setTotalSteps] = useState<number>(100);
  const [statusMessage, setStatusMessage] = useState<string>('');
  const [activeApiUrl, setActiveApiUrl] = useState<string>(PRIMARY_API_URL);
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

      // Simple wrapper to try both Primary and Fallback
      const fetchWithFallback = async (endpoint: string, options: RequestInit) => {
        try {
          // If we already know a working URL, use it
          const primaryRes = await fetch(`${activeApiUrl}${endpoint}`, options);
          if (!primaryRes.ok && primaryRes.status >= 500) throw new Error('Primary server error');
          return { res: primaryRes, workingUrl: activeApiUrl };
        } catch (error) {
          // If primary fails or error occurs, try the alternative
          const alternativeUrl = activeApiUrl === PRIMARY_API_URL ? FALLBACK_API_URL : PRIMARY_API_URL;
          console.warn(`API (${activeApiUrl}) failed, attempting fallback to ${alternativeUrl}`);
          const altRes = await fetch(`${alternativeUrl}${endpoint}`, options);
          if (!altRes.ok) throw new Error(`Both API endpoints failed: ${altRes.statusText}`);
          setActiveApiUrl(alternativeUrl); // Update state for future calls
          return { res: altRes, workingUrl: alternativeUrl };
        }
      };

      const { res: uploadRes, workingUrl: usedUrl } = await fetchWithFallback('/upload', {
        method: 'POST',
        body: formData,
      });

      const uploadData = await uploadRes.json();

      const generatePayload = {
        image_path: uploadData.image_path,
        style: selectedStyle,
        objects: [],
        room_type: null,
        custom_prompt: selectedStyle === 'Custom' ? customPrompt : null,
      };

      const genRes = await fetch(`${usedUrl}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(generatePayload),
      });

      if (!genRes.ok) throw new Error('Failed to generate image');
      if (!genRes.body) throw new Error('No response body');

      const reader = genRes.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          const trimmedLine = line.trim();
          if (!trimmedLine || !trimmedLine.startsWith('data: ')) continue;

          try {
            const data = JSON.parse(trimmedLine.slice(6));

            if (data.progress !== undefined) {
              setProgress(data.progress);
            }
            if (data.total_steps !== undefined) {
              setTotalSteps(data.total_steps);
            }
            if (data.message) {
              setStatusMessage(data.message);
            }
            if (data.result_url) {
              setIsGenerating(false);
              setResultUrl(`${usedUrl}${data.result_url}`);
              return; // Generation complete
            }
            if (data.error) {
              throw new Error(data.error);
            }
          } catch (e) {
            console.error('Error parsing SSE data:', e);
          }
        }
      }
    } catch (error: any) {
      console.error(error);
      setIsGenerating(false);
      alert(`An error occurred: ${error.message}`);
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
                  <PhotoCamera color="primary" /> 1. Tải ảnh phòng lên
                </Typography>
                <ImageUploader
                  onImageSelected={handleImageSelected}
                  previewUrl={previewUrl}
                  onClear={handleClearImage}
                />
              </Grid>

              <Grid size={{ xs: 12, md: 7 }}>
                <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                  <AutoFixHigh color="primary" /> 2. Chọn phong cách
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
                  {isGenerating 
                    ? 'AI đang tạo ảnh...' 
                    : 'Bắt đầu trang trí'}
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
                        Ảnh gốc
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
                        Kết quả sau khi Decor
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
                                AI đang thiết kế...
                              </Typography>
                              
                              <Typography variant="body2" sx={{ opacity: 0.9, fontWeight: 500 }}>
                                {statusMessage || 'Đang phân tích cấu trúc phòng...'}
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
