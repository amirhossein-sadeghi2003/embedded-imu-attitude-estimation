from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"

items = [
    (
        "Roll estimation comparison",
        RESULTS / "roll_estimation_comparison.png",
    ),
    (
        "Pitch estimation comparison",
        RESULTS / "pitch_estimation_comparison.png",
    ),
    (
        "High-rate roll estimation",
        RESULTS / "high_rate_roll_estimation_comparison.png",
    ),
    (
        "High-rate pitch estimation",
        RESULTS / "high_rate_pitch_estimation_comparison.png",
    ),
]

fig, axes = plt.subplots(2, 2, figsize=(13, 9))
fig.suptitle("Embedded IMU Attitude Estimation - Visual Overview", fontsize=16)

for ax, (title, path) in zip(axes.flat, items):
    image = mpimg.imread(path)
    ax.imshow(image)
    ax.set_title(title, fontsize=11)
    ax.axis("off")

fig.tight_layout()
fig.savefig(RESULTS / "attitude_estimation_visual_overview.png", dpi=160)
plt.close(fig)

print("Saved results/attitude_estimation_visual_overview.png")
