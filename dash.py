import os
import shutil
import streamlit as st

# === Set up folders ===
GRAPH_FOLDER = "graphs"
ASSETS_FOLDER = "assets"
IMAGE_FILES = [f for f in os.listdir(GRAPH_FOLDER) if f.endswith(".png")]
IMAGE_FILES.sort()

if not os.path.exists(ASSETS_FOLDER):
    os.makedirs(ASSETS_FOLDER)

for img in IMAGE_FILES:
    src = os.path.join(GRAPH_FOLDER, img)
    dst = os.path.join(ASSETS_FOLDER, img)
    if not os.path.exists(dst):
        shutil.copy(src, dst)

# === Categorize images by type and tab ===
def categorize_images():
    categorized = {
        "Type 1": {"time": [], "perplexity": [], "tables": []},
        "Type 2": {"time": [], "perplexity": [], "tables": []}
    }
    for img in IMAGE_FILES:
        label = img.lower()
        if "type1" in label:
            key = "Type 1"
        elif "type2" in label:
            key = "Type 2"
        else:
            continue  # skip untyped

        if "table" in label:
            categorized[key]["tables"].append(img)
        elif "perplexity" in label:
            categorized[key]["perplexity"].append(img)
        elif "time" in label and "table" not in label:
            categorized[key]["time"].append(img)

    return categorized

categorized_imgs = categorize_images()

# === Streamlit UI ===
st.set_page_config(page_title="FL Dashboard", layout="wide")
st.title("Federated Learning Evaluation Dashboard")

# Select result type
selected_type = st.selectbox("Select Result Type:", list(categorized_imgs.keys()))

# Select tab (simulated with radio buttons)
tab = st.radio("Select View:", ["🕒 Training Time", "📉 Perplexity", "📋 Tables"])
tab_key_map = {
    "🕒 Training Time": "time",
    "📉 Perplexity": "perplexity",
    "📋 Tables": "tables"
}
selected_tab_key = tab_key_map[tab]

# Show images in two columns
images = categorized_imgs.get(selected_type, {}).get(selected_tab_key, [])
if images:
    num_cols = 2
    cols = st.columns(num_cols)

    for idx, img in enumerate(images):
        with cols[idx % num_cols]:
            st.subheader(img.replace("_", " ").replace(".png", "").title())
            st.image(os.path.join(ASSETS_FOLDER, img), use_column_width=True)
else:
    st.info("No images available for the selected view.")

st.markdown("---")
st.caption("Graphs and tables loaded from /graphs folder")
