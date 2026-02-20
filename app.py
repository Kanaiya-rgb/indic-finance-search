import streamlit as st
import pandas as pd
import os

# 1. Page Configuration
st.set_page_config(page_title="Indic Finance Search Engine", layout="wide", page_icon="🏦")

# 2. Advanced CSS to fix the White Box and improve UI
st.markdown("""
    <style>
    /* Main background ko dark rakhne ke liye */
    .main { background-color: #0e1117; }
    
    /* Metric (White Box) ko fix karne ke liye CSS */
    [data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05); /* Transparent background */
        border: 1px solid #333;
        border-radius: 10px;
        padding: 15px;
    }
    
    /* Metric text labels ko white karne ke liye */
    [data-testid="stMetricLabel"] { color: #888 !important; }
    [data-testid="stMetricValue"] { color: #00d4ff !important; font-size: 32px !important; }
    
    .highlight-text { color: #00d4ff; font-weight: bold; font-size: 20px; }
    .stExpander { border: 1px solid #333 !important; border-radius: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Navigation + Filters
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/money-bag.png", width=60)
    st.title("Navigation")
    language = st.selectbox("🌐 Select Language", ("English", "Hindi"))
    st.divider()
    
    # NEW: Category Filters (like subject_domain)
    st.subheader("🔍 Filters")
    
    st.caption("Developed for AI Indian Summit 2026")

# --- Section 4: Data Loading (Corrected) ---
file_map = {"English": "BhashaBench_English.csv", "Hindi": "BhashaBench_Hindi.csv"}

if language in file_map:
    filename = file_map[language]
else:
    filename = "BhashaBench_English.csv" # Default backup

@st.cache_data
def load_data(file):
    if os.path.exists(file):
        return pd.read_csv(file)
    return None

df = load_data(filename)

# 5. Main UI Header
st.title("🏦 Indic Finance Query Parser")

if df is not None:
    st.write(f"Search and analyze over **{len(df):,}** financial records in {language}.")

    # Search Bar (Main)
    query = st.text_input("", placeholder="🔍 Search for keywords like 'loan', 'upi', 'tax'...", label_visibility="collapsed")
    
    # NEW: Sidebar Category Filter
    if 'subject_domain' in df.columns:
        domains = sorted(df['subject_domain'].dropna().unique())
        selected_domains = st.sidebar.multiselect(
            "📂 Select Categories (Domains)",
            options=domains,
            default=domains[:5] if len(domains) > 5 else domains,  # Pre-select top 5
            help="Filter by subject domains like 'Problem Solving', 'Banking Services'"
        )
    else:
        selected_domains = []
        st.sidebar.warning("No 'subject_domain' column found in dataset.")

    # Combined Filtering
    filtered_df = df.copy()
    if query:
        mask_search = filtered_df['question'].str.contains(query, case=False, na=False)
        filtered_df = filtered_df[mask_search]
    
    if selected_domains:
        mask_domain = filtered_df['subject_domain'].isin(selected_domains)
        filtered_df = filtered_df[mask_domain]

    if not filtered_df.empty:
        # --- FIXED UI SECTION (No More White Box) ---
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric(label="Results Found", value=f"{len(filtered_df):,}")
        with col2:
            domain_text = f" in domains {', '.join(selected_domains[:3])}..." if selected_domains else ""
            st.markdown(f"<br><p>Search results for <span class='highlight-text'>'{query}'</span>{domain_text}: Found <b>{len(filtered_df):,}</b> matches in {language} dataset.</p>", unsafe_allow_html=True)
        
        st.divider()

        # 6. Result List (Updated to use filtered_df)
        for _, row in filtered_df.head(30).iterrows():
            with st.container():
                domain_label = f"**Category:** {row.get('subject_domain', 'N/A')}" if 'subject_domain' in row else ""
                st.markdown(f"{domain_label} | **Question Excerpt:** {row['question'][:120]}...")
                
                with st.expander("📄 View Full Analysis & Options"):
                    st.write(f"**Full Question:** {row['question']}")
                    
                    # Options Grid
                    o1, o2 = st.columns(2)
                    with o1:
                        st.info(f"**A:** {row.get('option_a', 'N/A')}")
                        st.info(f"**B:** {row.get('option_b', 'N/A')}")
                    with o2:
                        st.info(f"**C:** {row.get('option_c', 'N/A')}")
                        st.info(f"**D:** {row.get('option_d', 'N/A')}")
                    
                    st.success(f"✔️ **Verified Answer:** {row.get('correct_answer', row.get('answer', 'N/A'))}")
                st.markdown("---")
    else:
        st.info("No results found. Try different keywords or clear filters.")
        
else:
    st.error(f"Dataset '{filename}' not found.")

# Footer
st.markdown("---")
st.markdown("*Powered by BhashaBench-Finance Dataset*")
