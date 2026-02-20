"""Integration: TCP/UDP (TKT-C05-02)."""
from simulator.adapters.transport.composite_transport import CompositeTransportAdapter
from simulator.domain.models.target_and_task import TargetRef

def test_tcp_udp() -> None:
    a = CompositeTransportAdapter()
    t = TargetRef(host="127.0.0.1", port=9999, timeout_ms=1000)
    assert a.execute(target=t, protocol="tcp", messages=[], timeout_ms=1000) is not None
    assert a.execute(target=t, protocol="udp", messages=[], timeout_ms=1000) is not None
