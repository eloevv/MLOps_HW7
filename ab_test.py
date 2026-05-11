import numpy as np
from scipy import stats

np.random.seed(42)

ALPHA = 0.05
POWER = 0.80
BASELINE_ACCURACY = 0.967
MIN_DETECTABLE_EFFECT = 0.015
N_SAMPLES_PER_GROUP = 200
N_DAYS = 14

n_control = N_SAMPLES_PER_GROUP
n_treatment = N_SAMPLES_PER_GROUP

control_accuracy = np.random.normal(BASELINE_ACCURACY, 0.02, n_control).clip(0, 1)
treatment_accuracy = np.random.normal(BASELINE_ACCURACY + MIN_DETECTABLE_EFFECT, 0.02, n_treatment).clip(0, 1)

t_stat, p_value = stats.ttest_ind(control_accuracy, treatment_accuracy)

effect_size = (treatment_accuracy.mean() - control_accuracy.mean()) / np.std(np.concatenate([control_accuracy, treatment_accuracy]))

print("=" * 50)
print("A/B Test Plan: ML Model v1.0.0 vs v1.1.0")
print("=" * 50)
print(f"Alpha (significance level):   {ALPHA}")
print(f"Power:                         {POWER}")
print(f"Baseline accuracy:             {BASELINE_ACCURACY:.3f}")
print(f"Minimum detectable effect:     {MIN_DETECTABLE_EFFECT:.3f}")
print(f"Samples per group:             {N_SAMPLES_PER_GROUP}")
print(f"Test duration:                 {N_DAYS} days")
print()
print("Simulated Results:")
print(f"  Control mean:                {control_accuracy.mean():.4f}")
print(f"  Treatment mean:              {treatment_accuracy.mean():.4f}")
print(f"  t-statistic:                 {t_stat:.4f}")
print(f"  p-value:                     {p_value:.4f}")
print(f"  Cohen's d (effect size):     {effect_size:.4f}")
print()

if p_value < ALPHA:
    print("Decision: REJECT H0 — treatment model is significantly better.")
    print("Action:   Switch 100% traffic to green (v1.1.0).")
else:
    print("Decision: FAIL TO REJECT H0 — no significant difference detected.")
    print("Action:   Keep blue (v1.0.0) as primary. Continue monitoring.")
print()
print("Traffic split during experiment:")
print("  Control (blue, v1.0.0):   90%")
print("  Treatment (green, v1.1.0): 10%")
print()
print("Metrics monitored:")
print("  - Prediction accuracy on labeled holdout")
print("  - Latency p50 / p99")
print("  - Error rate (HTTP 4xx/5xx)")
