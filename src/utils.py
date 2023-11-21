import psutil


def get_system_metrics() -> dict:
    cpu_usage = psutil.cpu_percent(interval=1)
    process = psutil.Process()
    memory_usage = process.memory_info().rss
    return {
        "cpu_usage_percent": cpu_usage,
        "memory_usage_bytes": memory_usage
    }
