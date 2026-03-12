### Mach 11th, 2026
### Created by: María José Ramírez, Natalia Lemus and Jimena Camey
### Hack-4-Sages

import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="BioSwitch-K2", layout="wide")

# Style CSS
st.markdown("""
<style>
.main-title {
    font-size:44px;
    font-weight:900;
    color:#003851;
}
.section-title {
    font-size:28px;
    font-weight:800;
    color:#22646e;
    margin-top:20px;
}
.subtitle {
    font-size:20px;
    font-weight:600;
    color:#3b89ac;
}
.regime-box {
    padding:14px;
    border-radius:6px;
    font-size:22px;
    font-weight:700;
    text-align:center;
    margin-top:10px;
    margin-bottom:10px;
}
.caption {
    font-size:14px;
    color:#555555;
}
</style>
""", unsafe_allow_html=True)

# Navigation Menu
page = st.sidebar.selectbox("Navigate", ["Home", "About", "Team"])

# Model
def run_simulation(UV, temperature, threshold, r, alpha):
    K = 1.0
    T_opt = 285
    B = 0.1
    G = 0.0
    steps = 200

    B_hist = []
    G_hist = []

    for _ in range(steps):
        stress = 0.001 * (temperature - T_opt) ** 2
        B = max(B + r * B * (1 - B / K) - stress, 0)

        lambda_eff = 0.05 + 0.3 * UV
        G = max(G + alpha * B - lambda_eff * G, 0)

        B_hist.append(B)
        G_hist.append(G)

    return B_hist, G_hist


# ---------------Home Page---------------------
if page == "Home":

    st.markdown('<div class="main-title">BioSwitch-K2</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Hidden Habitability Digital Twin Prototype</div>', unsafe_allow_html=True)

    st.markdown("""
BioSwitch-K2 explores detectability bias in exoplanet biosignature searches.  
The framework investigates how climate stability, biological productivity, stellar ultraviolet radiation, and instrumental sensitivity interact to shape atmospheric observability.
""")

    st.divider()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        UV = st.slider("UV", 0.0, 1.0, 0.5)
    with col2:
        temperature = st.slider("Temp (K)", 250, 320, 284)
    with col3:
        threshold = st.slider("Threshold", 0.0, 1.0, 0.3)
    with col4:
        r = st.slider("Growth r", 0.05, 0.5, 0.2)
    with col5:
        alpha = st.slider("Gas α", 0.01, 0.2, 0.05)

    B_hist, G_hist = run_simulation(UV, temperature, threshold, r, alpha)

    final_B = B_hist[-1]
    final_G = G_hist[-1]

    if final_B <= 0.01:
        st.markdown('<div class="regime-box" style="background:#F8D7DA;color:#721C24;">No Life Regime</div>', unsafe_allow_html=True)
    elif final_G > threshold:
        st.markdown('<div class="regime-box" style="background:#D4EDDA;color:#155724;">Detectable Life Regime</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="regime-box" style="background:#FFF3CD;color:#856404;">Hidden Life Regime</div>', unsafe_allow_html=True)

    st.markdown("""
**No Life:** Environmental stress prevents biomass stability.  
**Detectable Life:** Gas exceeds instrumental detection limits.  
**Hidden Life:** Biomass remains stable while UV-driven destruction suppresses gas below detection thresholds.
""")

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=B_hist, name="Biomass", line=dict(color="#2E7D32", width=3)))
    fig.add_trace(go.Scatter(y=G_hist, name="Gas", line=dict(color="#1565C0", width=3)))
    fig.add_hline(y=threshold, line_dash="dash", line_color="black")

    fig.update_layout(height=500, xaxis_title="Time", yaxis_title="Normalized Abundance")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="caption">Figure 1. Biomass and atmospheric gas evolution.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">UV Sensitivity Analysis</div>', unsafe_allow_html=True)

    uv_range = np.linspace(0, 1, 30)
    gas_final = []

    for uv_test in uv_range:
        B = 0.1
        G = 0.0
        for _ in range(200):
            B = max(B + r * B * (1 - B / 1.0), 0)
            lambda_eff = 0.05 + 0.3 * uv_test
            G = max(G + alpha * B - lambda_eff * G, 0)
        gas_final.append(G)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=uv_range, y=gas_final, line=dict(color="#1565C0", width=3)))
    fig2.add_hline(y=threshold, line_dash="dash", line_color="black")
    fig2.update_layout(height=400, xaxis_title="UV Radiation", yaxis_title="Final Gas")

    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('<div class="caption">Figure 2. Suppression of biosignature gas under increasing UV radiation.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Phase Space Dynamics</div>', unsafe_allow_html=True)

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=B_hist, y=G_hist, mode="lines", line=dict(color="#2E7D32", width=3)))
    fig3.update_layout(height=400, xaxis_title="Biomass", yaxis_title="Gas Concentration")

    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('<div class="caption">Figure 3. Stable attractor structure in biomass–gas space.</div>', unsafe_allow_html=True)


# ---------------About Page---------------------
elif page == "About":

    st.markdown('<div class="main-title">About BioSwitch-K2</div>', unsafe_allow_html=True)

    st.markdown("""
BioSwitch-K2 is a conceptual Digital Twin designed to investigate detectability bias in exoplanet life detection. Inspired by the debated temperate sub-Neptune K2-18b, this project isolates the essential interactions between biological productivity, stellar ultraviolet radiation, and instrumental detection thresholds.

Rather than reconstructing full atmospheric chemistry, the model provides a controlled and parametric framework to explore structured detectability regimes.
""")

    st.markdown('<div class="section-title">What the Model Demonstrates</div>', unsafe_allow_html=True)

    st.markdown("""
The system couples logistic biomass growth, biosignature gas production proportional to biological activity, UV-driven atmospheric destruction, and instrumental detection limits.

It reveals three structured regimes:

- **No Life Regime**
- **Detectable Life Regime**
- **Hidden Life Regime**

The Hidden Life regime represents a physically plausible false negative.
""")

    st.markdown('<div class="section-title">Scientific Relevance</div>', unsafe_allow_html=True)

    st.markdown("""
As atmospheric characterization improves, interpretation becomes critical. Non-detection of biosignatures cannot be directly equated with biological absence.

BioSwitch-K2 highlights the importance of considering stellar radiation environments and atmospheric destruction mechanisms when evaluating temperate exoplanets.
""")

    st.markdown('<div class="section-title">Planetary and Stellar Context</div>', unsafe_allow_html=True)

    colA, colB = st.columns([1,1])

    with colA:
        st.markdown("""
**K2-18b**
- Mass: 0.028 MJ  
- Radius: 0.211 RJ  
- Equilibrium Temperature: 284 K  
- Orbital Period: 32.94 days  

**Host Star K2-18**
- Spectral Type: M2.5 V  
- Stellar Mass: 0.36 M☉  
- Distance: 38.07 pc
""")

    with colB:
        st.image("images/k218b_visual.png", width=350)
        st.caption("Conceptual artistic rendering inspired by K2-18b.")

    st.markdown("""
K2-18b orbits an M-dwarf star capable of enhanced ultraviolet radiation. Elevated UV flux can shorten atmospheric molecular lifetimes, reducing steady-state biosignature accumulation.
""")

    video_file = open("https://youtu.be/llr8UnwtCes")
    video_bytes = video_file.read()
    st.video(video_bytes)

# ---------------Team Page---------------------
elif page == "Team":

    st.markdown('<div class="main-title">Our Team</div>', unsafe_allow_html=True)

    st.markdown("""
We are three undergraduate students from Guatemala pursuing degrees in:

- Chemical Industrial Engineering  
- Biochemistry & Microbiology  
- Data Science Engineering  

Astrobiology and space sciences are advancing worldwide, yet many regions in Latin America remain underrepresented in global research conversations.

Through BioSwitch-K2, we aim to contribute meaningfully to interdisciplinary life detection research while strengthening scientific participation from emerging regions.
""")

    st.markdown("""
Our broader mission is to inspire more young women in Guatemala and across Latin America to pursue careers in science, engineering, and space research. We believe rigorous scientific inquiry is not limited by geography, but driven by curiosity, collaboration, and access.
""")

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("images/member2.jpg", width=200)
        st.markdown("**Natalia Renée Lemus Cruz**")
        st.markdown("Chemical Industrial Engineering")
        st.markdown("[LinkedIn](https://www.linkedin.com/in/natalia-lemus-cruz-b363b8305/)")
        st.markdown("Email: lem22496@uvg.edu.gt")

    with col2:
        st.image("images/member1.jpg", width=200)
        st.markdown("**María José Ramírez Cifuentes**")
        st.markdown("Data Science Engineering")
        st.markdown("[LinkedIn](https://www.linkedin.com/in/mar%C3%ADajos%C3%A9ram%C3%ADrez/)")
        st.markdown("Email: ram221051@uvg.edu.gt")

    with col3:
        st.image("images/member4.jpg", width=200)
        st.markdown("**Jimena Alejandra Camey Vásquez**")
        st.markdown("Biochemistry & Microbiology")
        st.markdown("Email: cam24244@uvg.edu.gt")
