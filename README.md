# Malaysia Electricity Bill Explorer

A public-data project exploring why Malaysian household electricity bills can rise sharply — through electricity usage, tariff thresholds, incentives, and hotter weather.

## Live App

👉 https://ganeisraaj-malaysia-electricity-bill-explorer.streamlit.app/

---

## Why I Built This

There has been a lot of discussion around rising electricity bills in Malaysia.

Instead of assuming the reason, I wanted to break the problem down into two questions:

1. **Why can a bill increase faster than electricity usage?**
2. **Do hotter months coincide with higher household electricity consumption?**

---

## Key Findings

### 1. The old 600 kWh threshold created a sharp bill jump

One of the most striking examples:

- **600 kWh:** ~RM215.98
- **601 kWh before the temporary government relief:** RM258.40

That is a difference of roughly **RM42** for only 1 extra kWh.

This does **not** mean 1 kWh costs RM42.

The jump happened because crossing the old 600 kWh threshold changed several billing components at once, including the Energy Efficiency Incentive and eligibility for certain exemptions.

---

### 2. Temporary government relief reduces bills between 601–800 kWh

Examples based on reported TNB figures:

| Usage | Before Relief | After Relief | Saving |
|---|---:|---:|---:|
| 601 kWh | RM258.40 | RM225.50 | RM32.90 |
| 650 kWh | RM280.20 | RM243.90 | RM36.30 |
| 700 kWh | RM316.75 | RM276.85 | RM39.90 |
| 750 kWh | RM347.85 | RM304.30 | RM43.55 |
| 800 kWh | RM375.85 | RM328.60 | RM47.25 |

The app calculator reproduces these protected-bill examples to within a few sen.

---

### 3. Hotter months were associated with higher household electricity use

I combined Malaysian domestic electricity consumption data with historical weather data from six Peninsular Malaysian cities:

- Kuala Lumpur
- George Town
- Ipoh
- Kuantan
- Kota Bharu
- Johor Bahru

Using monthly data from **January 2018 to June 2024**:

> **A 1°C warmer monthly mean temperature was associated with about 4.9% higher daily domestic electricity consumption.**

95% confidence interval:

**+3.0% to +6.9%**

This relationship remained positive across several robustness checks using:

- apparent temperature
- maximum temperature
- humidity controls
- year-on-year changes

This is an **observational association**, not a causal estimate.

---

## 🧮 What the App Does

The Streamlit app lets users:

- estimate their electricity bill for usage up to 800 kWh
- see how the bill is broken down
- understand the old 600 → 601 kWh threshold effect
- compare TNB-reported bills before and after the temporary relief
- explore historical electricity consumption
- compare temperature and household electricity use
- view the methodology and limitations

---

## Data Sources

### Electricity consumption

Official Malaysian monthly electricity consumption data.

Period used:

**January 2018 – June 2024**

Main series:

`local_domestic`

### Weather

Historical weather data from Open-Meteo.

Daily weather observations were aggregated into monthly averages across six Peninsular Malaysian cities.

### Tariff information

Tariff and bill components are based on official information from:

- Tenaga Nasional Berhad (TNB)
- Energy Commission Malaysia
- Ministry of Finance Malaysia
