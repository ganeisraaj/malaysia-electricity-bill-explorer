import streamlit as st
import pandas as pd
from pathlib import Path

# =========================================================
# PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="Why Did My TNB Bill Jump?",
    page_icon="⚡",
    layout="wide"
)

ROOT = Path(__file__).parent

hist = pd.read_csv(
    ROOT / "data" / "electricity_weather_monthly.csv",
    parse_dates=["month"]
)

validation = pd.read_csv(
    ROOT / "tariff_validation_against_tnb.csv"
)

# =========================================================
# TARIFF LOGIC
# =========================================================

EEI = [
    (200, 25.00),
    (250, 24.50),
    (300, 22.50),
    (350, 21.00),
    (400, 17.00),
    (450, 14.50),
    (500, 12.00),
    (550, 10.50),
    (600, 9.00),
    (650, 7.50),
    (700, 5.50),
    (750, 4.50),
    (800, 4.00),
    (850, 2.50),
    (900, 1.00),
    (1000, 0.50)
]


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

    if kwh <= 300:
        kwtbb = 0
    else:
        kwtbb = 0.016 * subtotal

    total = subtotal + kwtbb

    return {
        "energy": energy,
        "capacity": capacity,
        "network": network,
        "eei": eei,
        "kwtbb": kwtbb,
        "total": total
    }


# =========================================================
# HERO
# =========================================================

st.title("⚡ Why Did My TNB Bill Jump?")

st.markdown(
    """
Malaysians have been complaining about unusually high electricity bills.

So I looked at Malaysia's tariff structure and historical electricity data
to answer two simple questions:

**1. Why can your electricity bill rise much faster than your usage?**

**2. Do hotter months coincide with Malaysians using more electricity?**
"""
)

st.divider()

# =========================================================
# BILL CALCULATOR
# =========================================================

st.header("🧮 Check your electricity bill")

st.write(
    "Move the slider to estimate your household electricity bill "
    "under the September–December 2026 protection."
)

kwh = st.slider(
    "How much electricity did you use this month?",
    min_value=50,
    max_value=800,
    value=600,
    step=1
)

bill = bill_protected(kwh)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Estimated bill",
    f"RM {bill['total']:,.2f}"
)

col2.metric(
    "Electricity used",
    f"{kwh:,} kWh"
)

col3.metric(
    "Effective cost",
    f"RM {bill['total'] / kwh:.3f}/kWh"
)

if kwh <= 300:
    st.success(
        "Your usage is relatively low, so you receive one of the "
        "strongest Energy Efficiency Incentive rebates."
    )

elif kwh <= 600:
    st.info(
        "You are still within the lower-consumption range, but your "
        "Energy Efficiency Incentive becomes smaller as usage increases."
    )

else:
    st.warning(
        "You are above 600 kWh. Before the temporary 2026 protection "
        "expansion, crossing this level could trigger several billing "
        "changes at once."
    )

with st.expander("See how the bill is calculated"):

    breakdown = pd.DataFrame(
        {
            "Component": [
                "Energy charge",
                "Capacity charge",
                "Network charge",
                "Energy Efficiency Incentive",
                "KWTBB",
                "AFA",
                "Retail charge",
                "SST"
            ],
            "RM": [
                bill["energy"],
                bill["capacity"],
                bill["network"],
                -bill["eei"],
                bill["kwtbb"],
                0,
                0,
                0
            ]
        }
    )

    st.dataframe(
        breakdown.style.format(
            {
                "RM": "RM {:.2f}"
            }
        ),
        hide_index=True,
        use_container_width=True
    )

    st.caption(
        "Calculator scope: General Domestic Tariff, up to 800 kWh, "
        "September–December 2026 protection."
    )

st.divider()

# =========================================================
# 600 -> 601 STORY
# =========================================================

st.header("😳 Why did 600 → 601 kWh matter so much?")

left, middle, right = st.columns(3)

left.metric(
    "600 kWh",
    "RM 215.98"
)

middle.metric(
    "601 kWh before expansion",
    "RM 258.40",
    "+RM 42.42"
)

right.metric(
    "601 kWh with protection",
    "RM 225.50",
    "-RM 32.90"
)

st.markdown(
    """
### One extra kWh did **not** cost RM42.

Before the temporary protection expansion, the protected zone ended at
**600 kWh**.

Crossing into 601 kWh changed several parts of the bill at the same time.

That included:

- a smaller **Energy Efficiency Incentive**
- losing protections that previously applied at or below 600 kWh
- additional bill components becoming relevant

So the sharp increase was a **threshold effect**, not the price of one extra unit of electricity.
"""
)

st.info(
    "For September–December 2026, the protection threshold was temporarily "
    "expanded from 600 kWh to 800 kWh."
)

st.divider()

# =========================================================
# PROTECTION SAVINGS
# =========================================================

st.header("💰 How much does the temporary protection save?")

st.write(
    "TNB's reported examples show how bills change for households "
    "between 601 and 800 kWh."
)

display_validation = validation[
    [
        "kwh",
        "before_protection_rm",
        "after_protection_official_rm",
        "saving_rm",
        "saving_pct"
    ]
].copy()

display_validation.columns = [
    "Usage (kWh)",
    "Before protection (RM)",
    "After protection (RM)",
    "Saving (RM)",
    "Saving (%)"
]

st.dataframe(
    display_validation.style.format(
        {
            "Before protection (RM)": "RM {:.2f}",
            "After protection (RM)": "RM {:.2f}",
            "Saving (RM)": "RM {:.2f}",
            "Saving (%)": "{:.1f}%"
        }
    ),
    hide_index=True,
    use_container_width=True
)

st.caption(
    "These figures are based on TNB-reported billing examples used "
    "to validate the calculator."
)

st.divider()

# =========================================================
# HEAT SECTION
# =========================================================

st.header("🌡️ Do hotter months mean higher electricity use?")

st.markdown(
    """
I combined Malaysian household electricity consumption data with weather
data from six Peninsular Malaysian cities:

- Kuala Lumpur
- George Town
- Ipoh
- Kuantan
- Kota Bharu
- Johor Bahru

The historical dataset covers **January 2018 to June 2024**.
"""
)

st.success(
    """
Main finding:

A **1°C warmer monthly mean temperature** was associated with about

**4.9% higher daily domestic electricity consumption**
"""
)

st.markdown(
    """
The estimate accounts for:

- long-term time trends
- normal month-of-year seasonal patterns
- a broad COVID-period effect
"""
)

st.info(
    """
This is an association, not proof that temperature directly caused
the entire increase.

Other factors such as household growth, appliance ownership, income,
behaviour and economic activity can also affect electricity usage.
"""
)

# =========================================================
# CHARTS
# =========================================================

chart1, chart2 = st.columns(2)

with chart1:

    st.subheader("Household electricity use over time")

    chart_hist = (
        hist
        .set_index("month")[["domestic_consumption_mkwh_per_day"]]
        .rename(
            columns={
                "domestic_consumption_mkwh_per_day":
                "Daily domestic consumption"
            }
        )
    )

    st.line_chart(chart_hist)

with chart2:

    st.subheader("Temperature vs electricity use")

    st.scatter_chart(
        hist,
        x="temp_mean_c",
        y="domestic_consumption_mkwh_per_day"
    )

st.divider()

# =========================================================
# DETAIL TABS
# =========================================================

tab1, tab2, tab3 = st.tabs(
    [
        "💸 Why bills rise",
        "🌡️ Heat analysis",
        "🔍 How I calculated this"
    ]
)

# =========================================================
# TAB 1
# =========================================================

with tab1:

    st.subheader("Why can the bill rise faster than electricity usage?")

    st.markdown(
        """
The electricity bill is not based on just one simple flat rate.

Several components can change as monthly usage increases.

**Energy charge**

The basic cost of electricity consumed.

**Capacity charge**

A charge linked to maintaining enough electricity-generation capacity.

**Network charge**

Covers transmission and distribution infrastructure.

**Energy Efficiency Incentive (EEI)**

Lower-usage households receive a bigger rebate.
As usage rises, this rebate becomes smaller.

**KWTBB**

A renewable-energy fund contribution which applies above certain usage levels.

**AFA**

The Automatic Fuel Adjustment reflects changes in fuel and generation costs.

That means a household using 30% more electricity can sometimes experience
a bill increase of **more than 30%**.
"""
    )

    st.subheader("Example: 600 → 800 kWh")

    bill600 = bill_protected(600)["total"]
    bill800 = bill_protected(800)["total"]

    usage_change = ((800 / 600) - 1) * 100
    bill_change = ((bill800 / bill600) - 1) * 100

    a, b = st.columns(2)

    a.metric(
        "Electricity usage increase",
        f"{usage_change:.1f}%"
    )

    b.metric(
        "Estimated bill increase",
        f"{bill_change:.1f}%"
    )

    st.write(
        "The bill rises faster than usage partly because the "
        "Energy Efficiency Incentive becomes smaller at higher consumption levels."
    )

# =========================================================
# TAB 2
# =========================================================

with tab2:

    st.subheader("Historical statistical result")

    st.markdown(
        """
The main model estimates:

**+4.9% daily domestic electricity consumption per +1°C**

95% confidence interval:

**+3.0% to +6.9%**
"""
    )

    with st.expander("See the statistical methodology"):

        st.code(
            """
log(daily domestic electricity consumption)
~ mean temperature
+ linear time trend
+ calendar-month effects
+ COVID-period indicator
""",
            language="text"
        )

        st.markdown(
            """
HAC standard errors with 3 lags are used to reduce sensitivity to
serial correlation.

The temperature relationship was also checked using:

- apparent temperature
- maximum temperature
- humidity controls
- year-on-year changes

The relationship remained positive across these alternative specifications.
"""
        )

# =========================================================
# TAB 3
# =========================================================

with tab3:

    st.subheader("Tariff assumptions")

    tariff_table = pd.DataFrame(
        {
            "Component": [
                "Energy charge",
                "Capacity charge",
                "Network charge",
                "Retail charge",
                "KWTBB"
            ],
            "Rate / treatment": [
                "27.03 sen/kWh",
                "4.55 sen/kWh",
                "12.85 sen/kWh",
                "Exempt ≤800 kWh during Sep–Dec 2026 protection",
                "1.6% above 300 kWh"
            ]
        }
    )

    st.dataframe(
        tariff_table,
        hide_index=True,
        use_container_width=True
    )

    st.subheader("Calculator validation")

    st.success(
        "The bill calculator reproduces TNB's reported protected-bill "
        "examples between 601 and 800 kWh to within a few sen."
    )

    audit_table = validation[
        [
            "kwh",
            "after_protection_official_rm",
            "our_after_rm",
            "absolute_error_rm"
        ]
    ].copy()

    audit_table.columns = [
        "Usage (kWh)",
        "TNB example (RM)",
        "Calculator result (RM)",
        "Difference (RM)"
    ]

    st.dataframe(
        audit_table.style.format(
            {
                "TNB example (RM)": "RM {:.2f}",
                "Calculator result (RM)": "RM {:.2f}",
                "Difference (RM)": "RM {:.2f}"
            }
        ),
        hide_index=True,
        use_container_width=True
    )

    st.subheader("Historical data")

    st.markdown(
        """
**Electricity**

Malaysia's official monthly domestic electricity consumption series,
January 2018–June 2024.

**Weather**

Open-Meteo historical daily weather data averaged across six Peninsular
Malaysian cities.

The six-city weather measure is an approximation rather than a
population-weighted or electricity-demand-weighted national temperature index.
"""
    )

# =========================================================
# LIMITATIONS
# =========================================================

st.divider()

with st.expander("⚠️ Important limitations"):

    st.markdown(
        """
- The public electricity dataset ends in **June 2024**.
- Therefore this project does **not** directly test the September 2026 haze episode.
- The historical electricity series covers Malaysia nationally, while the weather proxy uses six Peninsular cities.
- Domestic electricity consumption includes public lighting.
- The temperature relationship is observational and should not be interpreted as causal.
- Factors other than temperature may affect electricity consumption.
"""
    )

# =========================================================
# CLOSING
# =========================================================

st.divider()

st.markdown(
    """
### So what does this mean?

Higher electricity bills are not necessarily caused by one thing.

They can reflect a combination of:

**more electricity usage + smaller efficiency incentives + tariff thresholds + other bill components.**

And historically, hotter months have tended to coincide with higher household electricity consumption.
"""
)

st.caption(
    "Built using publicly available Malaysian electricity data, "
    "Open-Meteo weather data and official tariff information."
)
