import streamlit as st
import pandas as pd
import altair as alt

# Title and description
st.title("Penicillin’s Edge Against Gram-Positive Pathogens")

st.markdown("""
This interactive chart visualizes how three antibiotics—**Penicillin**, **Streptomycin**, and **Neomycin**—
perform against 16 bacterial species, categorized by **Gram stain** (positive or negative).
Lower MIC values (log scale) reflect greater potency.
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

# Create DataFrame and melt for long-form
df = pd.DataFrame(data)
df_melted = df.melt(id_vars=["Bacteria", "Gram_Staining"],
                    value_vars=["Penicillin", "Streptomycin", "Neomycin"],
                    var_name="Antibiotic", value_name="MIC")

# Create highlight column for styling
df_melted["Highlight"] = df_melted["Antibiotic"].apply(lambda x: "Penicillin" if x == "Penicillin" else "Other")

# Main chart with shape + size to highlight Penicillin
points = alt.Chart(df_melted).mark_point(filled=True).encode(
    x=alt.X('MIC:Q', scale=alt.Scale(type='log'), title="MIC (μg/mL)"),
    y=alt.Y('Antibiotic:N', title="Antibiotic"),
    color=alt.Color('Gram_Staining:N', title="Gram stain", scale=alt.Scale(scheme='category10')),
    shape=alt.Shape('Highlight:N', scale=alt.Scale(domain=['Penicillin', 'Other'], range=['triangle', 'circle'])),
    size=alt.Size('Highlight:N', scale=alt.Scale(domain=['Penicillin', 'Other'], range=[150, 60])),
    tooltip=['Bacteria', 'Antibiotic', 'MIC', 'Gram_Staining']
)

# Annotation line
annotation = alt.Chart(pd.DataFrame({'x': [0.03]})).mark_rule(
    strokeDash=[4, 4], color='white'
).encode(x='x:Q')

# Annotation text
text = alt.Chart(pd.DataFrame({'x': [0.03], 'y': ['Penicillin']})).mark_text(
    text="Gram-positive MIC ≲ 0.03 µg/mL",
    align='left',
    dx=6,
    dy=-8,
    fontWeight='bold',
    color='white'
).encode(x='x:Q', y='y:N')

# Final composed chart
final_chart = (points + annotation + text).properties(
    title="Penicillin’s Edge Against Gram-Positive Pathogens",
    height=400,
    width=700
)

# Show in Streamlit
st.altair_chart(final_chart, use_container_width=True)

# Footer caption
st.caption("MIC is log-scaled—lower values indicate stronger potency. Penicillin stands out with high efficacy against Gram-positive bacteria.")
