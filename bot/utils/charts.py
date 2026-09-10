import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def make_devices_pie_chart(desktop: float, mobile: float, other: float) -> io.BytesIO:
    labels = ["Desktop", "Mobile", "Other"]
    values = [desktop, mobile, other]
    colors = ["#F6821F", "#404041", "#B4B4B4"]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(values, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90)

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight", dpi=150)
    plt.close(fig)
    buffer.seek(0)

    return buffer


def make_quality_bar_chart(
    download: float, upload: float,
    latency_idle: float, latency_loaded: float,
    jitter_idle: float, jitter_loaded: float,
    packet_loss: float,
) -> io.BytesIO:
    metrics = [
        ("Download (Mbps)", download),
        ("Upload (Mbps)", upload),
        ("Latency idle (ms)", latency_idle),
        ("Latency loaded (ms)", latency_loaded),
        ("Jitter idle (ms)", jitter_idle),
        ("Jitter loaded (ms)", jitter_loaded),
        ("Packet loss (%)", packet_loss),
    ]
    labels = [m[0] for m in metrics]
    values = [m[1] for m in metrics]

    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.barh(labels, values, color="#F6821F")
    ax.bar_label(bars, fmt="%.1f", padding=3)
    ax.invert_yaxis()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight", dpi=150)
    plt.close(fig)
    buffer.seek(0)

    return buffer