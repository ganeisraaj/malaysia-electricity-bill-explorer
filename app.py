
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Malaysia Electricity Bill Shock", page_icon="⚡", layout="wide")
ROOT = Path(__file__).parent
hist = pd.read_csv(ROOT / "data" / "electricity_weather_monthly.csv", parse_dates=["month"])
validation = pd.read_csv(ROOT / "tariff_validation_against_tnb.csv")

EEI = [(200,25.00),(250,24.50),(300,22.50),(350,21.00),(400,17.00),(450,14.50),
       (500,12.00),(550,10.50),(600,9.00),(650,7.50),(700,5.50),(750,4.50),
       (800,4.00),(850,2.50),(900,1.00),(1000,0.50)]

def eei_rate(kwh):
    for upper, rate in EEI:
        if kwh <= upper:
            return rate
    return 0.0

def bill_protected(kwh):
    energy = kwh * 0.2703
    capacity = kwh * 0.0455
    network = kwh * 0.1285
    eei = kwh * eei_rate(kwh) / 100
    subtotal = energy + capacity + network - eei
    kwtbb = 0 if kwh <= 300 else 0.016 * subtotal
    total = subtotal + kwtbb
    return energy, capacity, network, eei, kwtbb, total

st.title("⚡ Why Is My TNB Bill So High?")
st.caption("A public-data analysis of Malaysia's household electricity bills, temperature and the Sep-Dec 2026 protection.")

c1, c2, c3 = st.columns(3)
c1.metric("Historical temperature association", "+4.9% use / +1°C")
c2.metric("800 kWh protected bill", "RM 328.60")
c3.metric("Official saving at 800 kWh", "RM 47.25")

st.warning("The historical electricity dataset ends in June 2024. This project does not claim that the September 2026 haze caused the recent bill complaints.")

tab1, tab2, tab3, tab4 = st.tabs(["Bill calculator", "The 600→601 kWh cliff", "Heat & electricity", "Methods & audit"])

with tab1:
    st.subheader("Sep-Dec 2026 protected household bill")
    kwh = st.slider("Monthly electricity use (kWh)", 50, 800, 600, 1)
    energy, capacity, network, eei, kwtbb, total = bill_protected(kwh)
    a,b,c = st.columns(3)
    a.metric("Estimated bill", f"RM {total:,.2f}")
    b.metric("EEI rebate", f"RM {eei:,.2f}")
    c.metric("Effective price", f"RM {total/kwh:.3f}/kWh")
    st.dataframe(pd.DataFrame({
        "Component":["Energy","Capacity","Network","Energy Efficiency Incentive","KWTBB","AFA","Retail","SST"],
        "RM":[energy,capacity,network,-eei,kwtbb,0,0,0]
    }), hide_index=True, use_container_width=True)
    st.caption("Calculator scope: General Domestic Tariff, <=800 kWh, Sep-Dec 2026 protection.")

with tab2:
    st.subheader("Why one extra kWh could previously trigger a much bigger bill change")
    left, right = st.columns(2)
    left.metric("600 kWh", "RM 215.98")
    right.metric("601 kWh before expansion", "RM 258.40", f"+RM 42.42")
    st.markdown("""
Before the temporary Sep-Dec 2026 expansion, the protected zone ended at 600 kWh.
Crossing the threshold changed **several rules at once** — not just the cost of the extra 1 kWh.
The Energy Efficiency Incentive also moves from the 551–600 band to the 601–650 band.

Under the temporary expansion, TNB's 601 kWh example falls to about **RM225.50**.
""")
    st.dataframe(validation[["kwh","before_protection_rm","after_protection_official_rm","saving_rm","saving_pct"]],
                 hide_index=True, use_container_width=True)

with tab3:
    st.subheader("Do hotter months coincide with higher household electricity use?")
    st.line_chart(hist.set_index("month")[["domestic_consumption_mkwh_per_day"]])
    st.scatter_chart(hist, x="temp_mean_c", y="domestic_consumption_mkwh_per_day")
    st.markdown("""
**Main historical estimate:** after accounting for a linear time trend, calendar-month effects and a broad COVID-period indicator,
a 1°C warmer monthly mean is associated with about **4.9% higher daily domestic electricity consumption**
(95% CI **3.0% to 6.9%**).

This is an observational association, not a causal estimate.
""")

with tab4:
    st.subheader("Audit")
    st.success("The calculator reproduces TNB's reported protected-bill examples at 601–800 kWh to within RM0.02.")
    st.dataframe(validation, hide_index=True, use_container_width=True)
    st.markdown("""
**Historical limitations**
- Electricity consumption covers Malaysia nationally; the uploaded weather proxy is based on six Peninsular cities.
- Domestic consumption includes public lighting.
- Electricity data ends June 2024.
- The model may still contain omitted-variable bias.
- Therefore the heat result is presented as association, not causation.

**Tariff scope**
- Energy: 27.03 sen/kWh for usage shown.
- Capacity: 4.55 sen/kWh.
- Network: 12.85 sen/kWh.
- EEI varies by total monthly usage band.
- KWTBB: 1.6% above 300 kWh.
- Sep-Dec 2026 <=800 kWh: AFA, retail and SST exempt.
""")
