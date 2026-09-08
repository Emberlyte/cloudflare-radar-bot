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