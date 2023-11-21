from src.utils import get_system_metrics


def test_get_system_metrics():
    metrics = get_system_metrics()
    assert isinstance(metrics, dict)
    assert 'cpu_usage_percent' in metrics
    assert 'memory_usage_bytes' in metrics
    assert isinstance(metrics['cpu_usage_percent'], float)
    assert isinstance(metrics['memory_usage_bytes'], int)
