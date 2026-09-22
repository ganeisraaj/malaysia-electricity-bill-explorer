# Tariff Audit

## Result
The protected-bill formula in this project reproduces TNB's reported Sep-Dec 2026 examples to within RM0.02.

| kWh | TNB protected bill | Our result | Absolute error |
|---:|---:|---:|---:|
| 601 | RM225.50 | RM225.50 | RM0.00 |
| 650 | RM243.90 | RM243.89 | RM0.01 |
| 700 | RM276.85 | RM276.87 | RM0.02 |
| 750 | RM304.30 | RM304.27 | RM0.03 |
| 800 | RM328.60 | RM328.62 | RM0.02 |

## Formula used up to 800 kWh
- Energy charge: 27.03 sen/kWh
- Capacity charge: 4.55 sen/kWh
- Network charge: 12.85 sen/kWh
- Energy Efficiency Incentive: one published rate determined by total monthly consumption band, applied across monthly kWh
- KWTBB: 1.6% above 300 kWh, applied after discounts
- Sep-Dec 2026 protection up to 800 kWh: AFA = 0, retail charge = 0, SST = 0

## Threshold insight
The estimated 600 kWh protected bill is **RM215.98**.
TNB's reported pre-expansion 601 kWh example is **RM258.40**.

That implies an illustrative jump of **RM42.42** when crossing from 600 to 601 kWh before the temporary threshold expansion. This does **not** mean one kWh itself costs RM42.42; several bill rules change at the threshold, including the EEI band and loss of the former <=600 kWh protections.

Under the Sep-Dec 2026 expansion, the same 601 kWh example is about **RM225.50**.

## Validation sources
- Ministry of Finance, 17 Sep 2026: protection expanded from 600 to 800 kWh, with AFA, retail and SST exemptions.
- TNB / Energy Commission RP4 tariff structure effective 1 Jul 2025.
- TNB KWTBB guidance: 1.6%, exempt for domestic use <=300 kWh.
- TNB media briefing examples reported on 18 Sep 2026: 601, 650, 700, 750 and 800 kWh before/after bills.
