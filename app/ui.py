import streamlit as st
import time
import os
import sys
import streamlit.web.cli as stcli
from PIL import Image
from app.api_client import api_client

st.set_page_config(
    page_title="AI Interior Decorator",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for premium look
st.markdown(
    """
<style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff3333;
        box-shadow: 0 4px 8px rgba(255, 75, 75, 0.3);
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    h1 {
        color: #f0f2f6;
        font-family: 'Inter', sans-serif;
    }
    .stSelectbox label, .stTextInput label {
        color: #f0f2f6 !important;
        font-weight: 500;
    }
    .css-1offfwp e1fqz7960 {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 20px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Sidebar for options
st.sidebar.title("🎨 Design Options")
style = st.sidebar.selectbox(
    "Interior Style", ["Minimalist", "Scandi", "Indochine", "Modern", "Custom"]
)
room_type = st.sidebar.selectbox(
    "Room Type", ["Living Room", "Bedroom", "Kitchen", "Bathroom", "Office"]
)

custom_prompt = None
if style == "Custom":
    custom_prompt = st.sidebar.text_area(
        "Custom Prompt", placeholder="Describe your dream room..."
    )

st.sidebar.markdown("---")
st.sidebar.info("Upload a photo of your room and let AI do the magic! ✨")

st.sidebar.markdown("---")
st.sidebar.markdown(f"📚 [API Documentation (Swagger)]({api_client.get_docs_url()})")

# Main content
st.title("🏡 AI Interior Decorator")
st.markdown("### Transform your space in seconds with Artificial Intelligence")

col1, col2 = st.columns(2)

uploaded_file = st.file_uploader(
    "Choose a photo of your room...", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    with col1:
        st.image(uploaded_file, caption="Original Room", use_column_width="always")

    if st.button("✨ Generate AI Design"):
        with st.status("🚀 Processing your room...", expanded=True) as status_box:
            status_box.write("📤 Uploading image...")
            image_path = api_client.upload_image(uploaded_file)

            if image_path:
                status_box.write("🤖 Triggering AI generation...")
                task_id = api_client.trigger_generation(
                    image_path, style, room_type, custom_prompt
                )

                if task_id:
                    progress_bar = st.progress(0)
                    while True:
                        task_data = api_client.get_status(task_id)
                        if not task_data:
                            st.error("Failed to get task status.")
                            break

                        status_str = task_data["status"]
                        progress = task_data["progress"]
                        total_steps = task_data["total_steps"]

                        if total_steps > 0:
                            percent = min(100, int((progress / total_steps) * 100))
                            progress_bar.progress(percent)
                            status_box.write(
                                f"⌛ Progress: {percent}% (Step {progress}/{total_steps})"
                            )

                        if status_str == "completed":
                            status_box.write("✅ Generation complete!")
                            result_url = task_data["result_url"]
                            with col2:
                                st.image(
                                    api_client.get_result_url(result_url),
                                    caption="AI Reimagined",
                                    use_column_width="always",
                                )
                            status_box.update(
                                label="✨ Design Ready!",
                                state="complete",
                                expanded=False,
                            )
                            st.balloons()
                            break
                        elif status_str == "failed":
                            st.error(f"Generation failed: {task_data['error']}")
                            status_box.update(
                                label="❌ Generation Failed", state="error"
                            )
                            break

                        time.sleep(1)
                else:
                    st.error("Failed to start generation task.")
            else:
                st.error("Failed to upload image.")
else:
    st.info("Please upload an image to get started.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "FastAPI + Streamlit + Stable Diffusion ControlNet"
    "</div>",
    unsafe_allow_html=True,
)


def start():
    import os
    import sys
    import subprocess

    if os.environ.get("STREAMLIT_RUN_IN_SUBPROCESS") == "1":
        sys.exit(stcli.main())

    os.environ["STREAMLIT_RUN_IN_SUBPROCESS"] = "1"
    sys.exit(
        subprocess.run([sys.executable, "-m", "streamlit", "run", __file__]).returncode
    )
