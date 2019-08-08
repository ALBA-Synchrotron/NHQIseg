import pytest
import unittest.mock as mock
import nhq_iseg
import serial

from patch_serial import patch_serial

@pytest.fixture
def nhq_mock():
    "Test the mockup"
    with mock.patch('serial.Serial') as mock_serial:
        patch_serial(mock_serial)
        com = serial.Serial('/dev/tty0')
        yield com


@pytest.fixture
def nhq_com():
    """Test nhq communication"""
    with mock.patch('nhq_iseg.communication.serial.Serial') as mock_serial:
        patch_serial(mock_serial)
        nhq = nhq_iseg.NHQComm('/dev/tty0')
        yield nhq


@pytest.fixture()
def nhq_controller(request):
    """Test nhq controller"""
    with mock.patch('nhq_iseg.communication.serial.Serial') as mock_serial:
        patch_serial(mock_serial)
        nhq = nhq_iseg.NHQPowerSupply('/dev/tty0', request.param)
        yield nhq
