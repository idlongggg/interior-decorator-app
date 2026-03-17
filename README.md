# AI Interior Decorator

This application uses FastAPI for the backend and Streamlit for the frontend.
It leverages Stable Diffusion with ControlNet to reimagined rooms.

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Install dependencies
uv sync
```

## Running the Application

You can now use the following commands to start each component:

### 1. Start the API (Backend)
```bash
uv run api
```
The API will be available at `http://localhost:8000`.

### 2. Start the UI (Frontend)
```bash
uv run ui
```
The UI will open in your browser.

## Project Structure

- `api/`: FastAPI backend implementation.
- `app/`: Streamlit frontend implementation.
- `uploads/`: Temporary storage for uploaded images.
- `results/`: Storage for generated designs.
