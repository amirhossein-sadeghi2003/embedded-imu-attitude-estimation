from pathlib import Path
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

INPUT_CSV = ROOT / "data" / "processed" / "high_rate_imu_demo_clean.csv"
RESULTS_DIR = ROOT / "results"
OUTPUT_GIF = RESULTS_DIR / "attitude_body_animation.gif"


def rotation_matrix(roll_deg, pitch_deg):
    roll = np.deg2rad(roll_deg)
    pitch = np.deg2rad(pitch_deg)

    rx = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, np.cos(roll), -np.sin(roll)],
            [0.0, np.sin(roll), np.cos(roll)],
        ]
    )

    ry = np.array(
        [
            [np.cos(pitch), 0.0, np.sin(pitch)],
            [0.0, 1.0, 0.0],
            [-np.sin(pitch), 0.0, np.cos(pitch)],
        ]
    )

    return ry @ rx


def make_body_vertices():
    length = 2.0
    width = 1.0
    height = 0.18

    x = length / 2
    y = width / 2
    z = height / 2

    return np.array(
        [
            [-x, -y, -z],
            [x, -y, -z],
            [x, y, -z],
            [-x, y, -z],
            [-x, -y, z],
            [x, -y, z],
            [x, y, z],
            [-x, y, z],
        ]
    )


def make_faces(vertices):
    return [
        [vertices[0], vertices[1], vertices[2], vertices[3]],
        [vertices[4], vertices[5], vertices[6], vertices[7]],
        [vertices[0], vertices[1], vertices[5], vertices[4]],
        [vertices[2], vertices[3], vertices[7], vertices[6]],
        [vertices[1], vertices[2], vertices[6], vertices[5]],
        [vertices[0], vertices[3], vertices[7], vertices[4]],
    ]


def rotate_points(points, roll_deg, pitch_deg):
    r = rotation_matrix(roll_deg, pitch_deg)
    return points @ r.T


def main():
    RESULTS_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(INPUT_CSV)

    if "time_s" not in df.columns:
        if "time_ms" in df.columns:
            df["time_s"] = (df["time_ms"] - df["time_ms"].iloc[0]) / 1000.0
        else:
            df["time_s"] = np.arange(len(df)) * 0.02

    frame_step = 8

    roll0 = df["filtered_roll_deg"].iloc[0]
    pitch0 = df["filtered_pitch_deg"].iloc[0]

    motion_score = np.sqrt(
        (df["filtered_roll_deg"] - roll0) ** 2
        + (df["filtered_pitch_deg"] - pitch0) ** 2
    )

    active_indexes = np.where(motion_score > 5.0)[0]

    if len(active_indexes) > 0:
        start_index = max(0, int(active_indexes[0]) - 50)
    else:
        start_index = 0

    frame_indexes = list(range(start_index, len(df), frame_step))

    base_vertices = make_body_vertices()

    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection="3d")

    fig.suptitle("IMU Attitude Estimation - Roll and Pitch Body Animation", fontsize=14)

    limit = 1.6
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_zlim(-limit, limit)

    ax.set_xlabel("Body x")
    ax.set_ylabel("Body y")
    ax.set_zlabel("Body z")

    ax.view_init(elev=25, azim=35)

    body = Poly3DCollection(
        make_faces(base_vertices),
        alpha=0.75,
        linewidths=1.0,
        edgecolor="black",
    )
    ax.add_collection3d(body)

    x_axis, = ax.plot([], [], [], linewidth=3, label="body x-axis")
    y_axis, = ax.plot([], [], [], linewidth=3, label="body y-axis")
    z_axis, = ax.plot([], [], [], linewidth=3, label="body z-axis")

    trace_roll, = ax.plot([], [], [], linewidth=1, alpha=0.5)

    text = ax.text2D(
        0.03,
        0.94,
        "",
        transform=ax.transAxes,
        fontsize=10,
        family="monospace",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.85),
    )

    ax.legend(loc="lower left")

    roll_history = []
    pitch_history = []
    time_history = []

    def update(frame_index):
        row = df.iloc[frame_index]

        roll = row["filtered_roll_deg"]
        pitch = row["filtered_pitch_deg"]
        t = row["time_s"]

        rotated_vertices = rotate_points(base_vertices, roll, pitch)
        body.set_verts(make_faces(rotated_vertices))

        axis_length = 1.3
        axes = np.array(
            [
                [0.0, 0.0, 0.0],
                [axis_length, 0.0, 0.0],
                [0.0, axis_length, 0.0],
                [0.0, 0.0, axis_length],
            ]
        )
        rotated_axes = rotate_points(axes, roll, pitch)

        origin = rotated_axes[0]
        x_tip = rotated_axes[1]
        y_tip = rotated_axes[2]
        z_tip = rotated_axes[3]

        x_axis.set_data([origin[0], x_tip[0]], [origin[1], x_tip[1]])
        x_axis.set_3d_properties([origin[2], x_tip[2]])

        y_axis.set_data([origin[0], y_tip[0]], [origin[1], y_tip[1]])
        y_axis.set_3d_properties([origin[2], y_tip[2]])

        z_axis.set_data([origin[0], z_tip[0]], [origin[1], z_tip[1]])
        z_axis.set_3d_properties([origin[2], z_tip[2]])

        roll_history.append(roll)
        pitch_history.append(pitch)
        time_history.append(t)

        text.set_text(
            f"time:  {t:5.2f} s\n"
            f"roll:  {roll:6.2f} deg\n"
            f"pitch: {pitch:6.2f} deg\n"
            f"source: complementary filter"
        )

        return body, x_axis, y_axis, z_axis, text

    animation = FuncAnimation(
        fig,
        update,
        frames=frame_indexes,
        interval=45,
        blit=False,
    )

    fig.tight_layout()
    animation.save(OUTPUT_GIF, writer=PillowWriter(fps=22))
    plt.close(fig)

    print("Saved:")
    print(OUTPUT_GIF)


if __name__ == "__main__":
    main()
