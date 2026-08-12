from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "data"
perf = pd.read_csv(D / "reported_performance.csv")
exp = pd.read_csv(D / "reported_explainability.csv")
lat = pd.read_csv(D / "reported_latency.csv")

calc_ms = lat["XAI_Latency_ms"] - lat["Baseline_Latency_ms"]
calc_pct = calc_ms / lat["Baseline_Latency_ms"] * 100

checks = pd.DataFrame({
    "Scenario": lat["Scenario"],
    "CO_ms_from_Table5": calc_ms,
    "CO_ms_Table4": exp["CO_ms"],
    "Overhead_pct_calculated": calc_pct.round(1),
    "Overhead_pct_Table5": lat["Overhead_pct"],
})
checks["CO_ms_match"] = checks["CO_ms_from_Table5"].eq(checks["CO_ms_Table4"])
checks["Overhead_pct_match"] = np.isclose(checks["Overhead_pct_calculated"], checks["Overhead_pct_Table5"], atol=0.1)
checks.to_csv(ROOT / "results" / "consistency_checks.csv", index=False)

print(checks.to_string(index=False))
print("\nAverages:")
print(f"Accuracy: {perf['Accuracy_pct'].mean():.2f}%")
print(f"Response time: {perf['Response_Time_ms'].mean():.1f} ms")
print(f"Transparency score: {perf['Transparency_Score_0_1'].mean():.3f}")
print(f"TI: {exp['TI_0_10'].mean():.2f}")
print(f"DTS: {exp['DTS'].mean():.3f}")
print(f"ARM: {exp['ARM_pct'].mean():.1f}%")
