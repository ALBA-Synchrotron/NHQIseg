import pytest
from nhq_iseg import Models, State


@pytest.mark.parametrize('nhq_controller', [Models.NHQ_102M, Models.NHQ_202M],
                         indirect=True)
def test_controller(nhq_controller):
    if nhq_controller.model == Models.NHQ_102M:
        nr_channels = 1
    elif nhq_controller.model == Models.NHQ_202M:
        nr_channels = 2
    assert nhq_controller.channels == nr_channels
    assert nhq_controller.max_voltage == 2000
    channel = nhq_controller[1]
    assert channel.voltage == 8
    assert channel.set_voltage == 4
    assert channel.current == 0.0
    assert channel.ramp_speed == 2
    assert channel.auto_start is False
    assert channel.state == State.ON
    assert channel.current_trip == 0
    assert channel.voltage_limit == 60
    assert channel.current_limit == 100
