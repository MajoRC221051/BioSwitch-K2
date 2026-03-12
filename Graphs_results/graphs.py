import numpy as np
import matplotlib.pyplot as plt


# MODEL PARAMETERS


temperature = 284
T_opt = 285
r = 0.2
alpha = 0.05
K = 1.0
threshold = 0.3

B0 = 0.1
G0 = 0.0
steps = 300

# MODEL EQUATIONS


def update_biomass(B):
    stress = 0.001 * (temperature - T_opt) ** 2
    dB = r * B * (1 - B / K) - stress
    return max(B + dB, 0)

def update_gas(G, B, UV):
    lambda_eff = 0.05 + 0.3 * UV
    dG = alpha * B - lambda_eff * G
    return max(G + dG, 0)

# =============================
# SIMULATION FUNCTION
# =============================

def run_simulation(UV):
    B = B0
    G = G0
    B_hist = []
    G_hist = []
    
    for _ in range(steps):
        B = update_biomass(B)
        G = update_gas(G, B, UV)
        B_hist.append(B)
        G_hist.append(G)
        
    return B_hist, G_hist

# =============================
# FIGURE 1 – TIME EVOLUTION
# =============================

UV_example = 0.3
B_hist, G_hist = run_simulation(UV_example)

plt.figure()
plt.plot(B_hist)
plt.plot(G_hist)
plt.axhline(y=threshold, linestyle='--')
plt.xlabel("Time Steps")
plt.ylabel("Normalized Abundance")
plt.title("Biomass and Biosignature Gas Evolution")
plt.tight_layout()
plt.savefig("figure1_time_evolution.png", dpi=300)
plt.show()


# FIGURE 2 – UV SENSITIVITY


uv_range = np.linspace(0, 1, 60)
gas_final = []

for uv in uv_range:
    B_hist, G_hist = run_simulation(uv)
    gas_final.append(G_hist[-1])

plt.figure()
plt.plot(uv_range, gas_final)
plt.axhline(y=threshold, linestyle='--')
plt.xlabel("UV Radiation Level")
plt.ylabel("Final Gas Concentration")
plt.title("Gas Sensitivity to Stellar UV Radiation")
plt.tight_layout()
plt.savefig("figure2_uv_sensitivity.png", dpi=300)
plt.show()


# FIGURE 3 – PHASE SPACE


plt.figure()
plt.plot(B_hist, G_hist)
plt.xlabel("Biomass")
plt.ylabel("Gas Concentration")
plt.title("Phase Space Trajectory (Gas vs Biomass)")
plt.tight_layout()
plt.savefig("figure3_phase_space.png", dpi=300)
plt.show()
