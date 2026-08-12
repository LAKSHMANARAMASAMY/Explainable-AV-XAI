from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "data"
O = ROOT / "results"
F = O / "figures"
F.mkdir(parents=True, exist_ok=True)

perf = pd.read_csv(D / "reported_performance.csv")
exp = pd.read_csv(D / "reported_explainability.csv")
lat = pd.read_csv(D / "reported_latency.csv")

perf.to_csv(O / "table3_performance.csv", index=False)
exp.to_csv(O / "table4_explainability.csv", index=False)
lat.to_csv(O / "table5_latency.csv", index=False)

def manuscript_line(y, ylabel, avg_label, filename, ylim=None, threshold=None):
    plt.figure(figsize=(8, 5))
    plt.plot(perf["Scenario"], y, marker="o", linestyle="--", label=ylabel.replace(" (%)", "").replace(" (ms)", "").replace(" (0–1)", "") + " for each scenario category")
    avg = float(y.mean())
    plt.axhline(avg, linewidth=1, label=avg_label)
    if threshold is not None:
        plt.axhline(threshold, linestyle=":", linewidth=1, label=f"{threshold} ms threshold")
    for x, value in zip(perf["Scenario"], y):
        plt.annotate(f"{value:g}", (x, value), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=8)
    plt.ylabel(ylabel)
    plt.xlabel("Safety-Critical Driving Scenario Category")
    plt.xticks(rotation=0)
    if ylim:
        plt.ylim(*ylim)
    plt.legend()
    plt.tight_layout()
    plt.savefig(F / filename, dpi=200)
    plt.close()

manuscript_line(perf["Accuracy_pct"], "Predictive Accuracy (%)", "Average predictive accuracy", "figure3_predictive_accuracy.png", (82, 92))
manuscript_line(perf["Response_Time_ms"], "Response Time (ms)", "Average response time", "figure4_response_time.png", (80, 102))
manuscript_line(perf["Transparency_Score_0_1"], "Transparency Score (0–1)", "Average transparency score", "figure5_transparency_score.png", (0.80, 0.94))

# Figure 6: the supplied manuscript graph contains only four scenario categories.
# Mechanical Failure has a proposed TI=8.5 in Table 4, but no baseline TI was supplied.
# We do not invent a missing baseline value.
ti4 = pd.DataFrame({
    "Scenario": ["Sudden Obstacle", "Ethical Decision-Making", "Complex Traffic", "Adverse Weather"],
    "Baseline_TI": [6.2, 5.9, 6.5, 5.8],
    "Proposed_TI": [8.7, 8.4, 8.8, 8.2],
})
ti4.to_csv(O / "figure6_visible_values.csv", index=False)
plt.figure(figsize=(8, 5))
plt.plot(ti4["Scenario"], ti4["Baseline_TI"], marker="o", label="Baseline TI")
plt.plot(ti4["Scenario"], ti4["Proposed_TI"], marker="s", label="Proposed TI")
for x, y in zip(ti4["Scenario"], ti4["Baseline_TI"]):
    plt.annotate(f"{y:.1f}", (x,y), xytext=(0,-15), textcoords="offset points", ha="center", fontsize=8)
for x, y in zip(ti4["Scenario"], ti4["Proposed_TI"]):
    plt.annotate(f"{y:.1f}", (x,y), xytext=(0,8), textcoords="offset points", ha="center", fontsize=8)
plt.ylabel("Transparency Index (TI)")
plt.xlabel("Scenario Category")
plt.ylim(5.0, 9.5)
plt.legend()
plt.tight_layout()
plt.savefig(F / "figure6_transparency_improvement.png", dpi=200)
plt.close()

# Figure 7 values supplied in the manuscript graph/table.
dts = pd.DataFrame({
    "Scenario": exp["Scenario"],
    "Baseline_DTS": [0.62, 0.59, 0.65, 0.58, 0.56],
    "Proposed_DTS": exp["DTS"],
})
dts.to_csv(O / "figure7_visible_values.csv", index=False)
plt.figure(figsize=(8, 5))
plt.plot(dts["Scenario"], dts["Baseline_DTS"], marker="o", label="Baseline DTS")
plt.plot(dts["Scenario"], dts["Proposed_DTS"], marker="s", label="Proposed DTS")
for x, y in zip(dts["Scenario"], dts["Baseline_DTS"]):
    plt.annotate(f"{y:.2f}", (x,y), xytext=(0,8), textcoords="offset points", ha="center", fontsize=8)
for x, y in zip(dts["Scenario"], dts["Proposed_DTS"]):
    plt.annotate(f"{y:.2f}", (x,y), xytext=(0,8), textcoords="offset points", ha="center", fontsize=8)
plt.ylabel("Decision Traceability Score (DTS)")
plt.xlabel("Scenario Category")
plt.ylim(0, 1.0)
plt.legend()
plt.tight_layout()
plt.savefig(F / "figure7_dts.png", dpi=200)
plt.close()

# Figure 8 reconstructed from the ARM values explicitly reported in Table 4/text.
plt.figure(figsize=(8, 5))
bars = plt.bar(exp["Scenario"], exp["ARM_pct"])
for b, val in zip(bars, exp["ARM_pct"]):
    plt.text(b.get_x()+b.get_width()/2, b.get_height()+0.25, f"{val:.1f}", ha="center", fontsize=8)
plt.ylabel("Ambiguity Reduction Metric (ARM, %)")
plt.xlabel("Safety-Critical Driving Scenario Category")
plt.ylim(0, 35)
plt.tight_layout()
plt.savefig(F / "figure8_arm.png", dpi=200)
plt.close()

print("Created manuscript-value tables and figures in results/")
print(f"Average accuracy = {perf['Accuracy_pct'].mean():.2f}%")
print(f"Average response time = {perf['Response_Time_ms'].mean():.1f} ms")
print(f"Average transparency score = {perf['Transparency_Score_0_1'].mean():.3f}")
