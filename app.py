import streamlit as st
import pandas as pd
import altair as alt

# Title and introduction
st.title("Penicillin’s Edge Against Gram-Positive Pathogens")
st.markdown("""
This interactive chart visualizes how three antibiotics—**Penicillin**, **Streptomycin**, and **Neomycin**—
perform against 16 bacterial species, separated by **Gram staining** (positive or negative).
Lower MIC values (log scale) indicate higher potency.
""")

# Dataset
data = [
    {"Bacteria": "Aerobacter aerogenes", "Penicillin": 870, "Streptomycin": 1, "Neomycin": 1.6, "Gram_Staining": "negative"},
    {"Bacteria": "Bacillus anthracis", "Penicillin": 0.001, "Streptomycin": 0.01, "Neomycin": 0.007, "Gram_Staining": "positive"},
    {"Bacteria": "Brucella abortus", "Penicillin": 1, "Streptomycin": 2, "Neomycin": 0.02, "Gram_Staining": "negative"},
    {"Bacteria": "Diplococcus pneumoniae", "Penicillin": 0.005, "Streptomycin": 11, "Neomycin": 10, "Gram_Staining": "positive"},
    {"Bacteria": "Escherichia coli", "Penicillin": 100, "Streptomycin": 0.4, "Neomycin": 0.1, "Gram_Staining": "negative"},
    {"Bacteria": "Klebsiella pneumoniae", "Penicillin": 850, "Streptomycin": 1.2, "Neomycin": 1, "Gram_Staining": "negative"},
    {"Bacteria": "Mycobacterium tuberculosis", "Penicillin": 800, "Streptomycin": 5, "Neomycin": 2, "Gram_Staining": "negative"},
    {"Bacteria": "Proteus vulgaris", "Penicillin": 3, "Streptomycin": 0.1, "Neomycin": 0.1, "Gram_Staining": "negative"},
    {"Bacteria": "Pseudomonas aeruginosa", "Penicillin": 850, "Streptomycin": 2, "Neomycin": 0.4, "Gram_Staining": "negative"},
    {"Bacteria": "Salmonella (Eberthella) typhosa", "Penicillin": 1, "Streptomycin": 0.4, "Neomycin": 0.008, "Gram_Staining": "negative"},
    {"Bacteria": "Salmonella schottmuelleri", "Penicillin": 10, "Streptomycin": 0.8, "Neomycin": 0.09, "Gram_Staining": "negative"},
    {"Bacteria": "Staphylococcus albus", "Penicillin": 0.007, "Streptomycin": 0.1, "Neomycin": 0.001, "Gram_Staining": "positive"},
    {"Bacteria": "Staphylococcus aureus", "Penicillin": 0.03, "Streptomycin": 0.03, "Neomycin": 0.001, "Gram_Staining": "positive"},
    {"Bacteria": "Streptococcus fecalis", "Penicillin": 1, "Streptomycin": 1, "Neomycin": 0.1, "Gram_Staining": "positive"},
    {"Bacteria": "Streptococcus hemolyticus", "Penicillin": 0.001, "Streptomycin": 14, "Neomycin": 10, "Gram_Staining": "positive"},
    {"Bacteria": "Streptococcus viridans", "Penicillin": 0.005, "Streptomycin": 10, "Neomycin": 40, "Gram_Staining": "positive"}
]

df = pd.DataFrame(data)

# Reshape
df_melted = df.melt(id_vars=["Bacteria", "Gram_Staining"],
                    value_vars=["Penicillin", "Streptomycin", "Neomycin"],
                    var_name="Antibiotic", value_name="MIC")

# Chart
import numpy as np

# Add jitter column to prevent overlap
df_melted["Jittered Antibiotic"] = df_melted["Antibiotic"].map({
    "Penicillin": 0,
    "Streptomycin": 1,
    "Neomycin": 2
}) + np.random.uniform(-0.2, 0.2, size=len(df_melted))

# Chart with flipped axes and styling changes
points = alt.Chart(df_melted).mark_square(size=90).encode(
    x=alt.X('MIC:Q', scale=alt.Scale(type='log'), title="MIC (μg/mL)"),
    y=alt.Y('Jittered Antibiotic:Q', axis=None),
    color=alt.Color('Gram_Staining:N', title="Gram stain", scale=alt.Scale(scheme='category10')),
    tooltip=['Bacteria', 'Antibiotic', 'MIC', 'Gram_Staining']
)

# Manually map antibiotic labels to jittered y positions
label_data = pd.DataFrame({
    'label': ['Penicillin', 'Streptomycin', 'Neomycin'],
    'y': [0, 1, 2]
})
labels = alt.Chart(label_data).mark_text(dx=-80).encode(
    y='y:Q',
    text='label:N'
)

# Annotation rule
annotation = alt.Chart(pd.DataFrame({'x': [0.03]})).mark_rule(
    strokeDash=[6, 3], color='black'
).encode(x='x:Q')

# Annotation text
text = alt.Chart(pd.DataFrame({'x': [0.03], 'y': [2.5]})).mark_text(
    text="Gram-positive MIC ≲ 0.03 µg/mL",
    align='left',
    dx=5,
    fontWeight='bold'
).encode(x='x:Q', y='y:Q')

# Combine all layers
final_chart = (points + labels + annotation + text).properties(
    title="Penicillin’s Edge Against Gram-Positive Pathogens",
    height=400,
    width=650
)

st.altair_chart(final_chart, use_container_width=True)


st.caption("MIC is log-scaled—lower values indicate stronger potency. Penicillin shows a clear advantage against Gram-positive bacteria, requiring far smaller doses.")
