import pytest
import unittest.mock as mock
import nhqiseg
import serialio

from patch_serial import PatchSerial


@pytest.fixture
def nhq_mock():
    "Test the mockup"
    with mock.patch('serialio.aio.posix.Serial') as mock_serial:
        p = PatchSerial()
        mock_serial.return_value.write = p.write
        mock_serial.return_value.readline = p.readline
        com = serialio.serial_for_url('serial://dev/tty0',concurrency='sync')
        yield com


@pytest.fixture
def nhq_com():
    """Test nhq communication"""
    with (mock.patch('nhqiseg.communication.serialio.aio.posix.Serial') as
          mock_serial):
        p = PatchSerial()
        mock_serial.return_value.write = p.write
        mock_serial.return_value.readline = p.readline

        nhq = nhqiseg.NHQComm('serial:/dev/tty0')
        yield nhq


@pytest.fixture()
def nhq_controller(request):
    """Test nhq controller"""
    with (mock.patch('nhqiseg.communication.serialio.aio.posix.Serial') as
          mock_serial):
        # patch_serial(mock_serial)
        p = PatchSerial()
        mock_serial.return_value.write = p.write
        mock_serial.return_value.readline = p.readline

        nhq = nhqiseg.NHQPowerSupply('serial:/dev/tty0', request.param)
        yield nhq
