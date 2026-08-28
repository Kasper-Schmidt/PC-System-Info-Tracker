import matplotlib.pyplot as plt

from .database import get_all_measurements

def plot_cpu_usage():
    measurements = get_all_measurements()

    times = [measurement["measured_at"] for measurement in measurements]
    cpu_usage = [measurement["cpu_usage"] for measurement in measurements]

    plt.plot(times, cpu_usage)

    plt.title("CPU Usage")
    plt.xlabel("Time")
    plt.ylabel("CPU Usage (%)")

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()



def plot_memory_usage():
    measurements = get_all_measurements()

    times = [measurement["measured_at"] for measurement in measurements]
    cpu_usage = [measurement["memory_usage"] for measurement in measurements]

    plt.plot(times, cpu_usage)

    plt.title("Memory Usage")
    plt.xlabel("Time")
    plt.ylabel("Memory Usage (%)")

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()



def plot_disk_usage():
    measurements = get_all_measurements()

    times = [measurement["measured_at"] for measurement in measurements]
    cpu_usage = [measurement["disk_usage"] for measurement in measurements]

    plt.plot(times, cpu_usage)

    plt.title("Disk Usage")
    plt.xlabel("Time")
    plt.ylabel("Disk Usage (%)")

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()


def plot_all():
    measurements = get_all_measurements()

    times = [measurement["measured_at"] for measurement in measurements]
    cpu_usage = [measurement["cpu_usage"] for measurement in measurements]
    memory_usage = [measurement["memory_usage"] for measurement in measurements]
    disk_usage = [measurement["disk_usage"] for measurement in measurements]

    plt.plot(times, cpu_usage, label="CPU", marker="o", linestyle="")
    plt.plot(times, memory_usage, label="Memory", marker="x", linestyle="-")
    plt.plot(times, disk_usage, label="Disk")

    plt.title("System Usage")
    plt.xlabel("Time")
    plt.ylabel("Usage (%)")

    plt.ylim(0, 100)

    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    plt.show()



# plot_cpu_usage()
# plot_memory_usage()
# plot_disk_usage()
plot_all()

# "python -m app.plot" i terminal