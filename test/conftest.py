import pytest
import unittest.mock as mock
import nhq_iseg
import serial

from patch_serial import patch_serial, PatchSerial

@pytest.fixture
def nhq_mock():
    "Test the mockup"
    with mock.patch('serial.Serial') as mock_serial:
        p = PatchSerial()
        mock_serial.return_value.write = p.write
        mock_serial.return_value.readline = p.readline
        com = serial.Serial('/dev/tty0')
        yield com


@pytest.fixture
def nhq_com():
    """Test nhq communication"""
    with mock.patch('nhq_iseg.communication.serial.Serial') as mock_serial:
        p = PatchSerial()
        mock_serial.return_value.write = p.write
        mock_serial.return_value.readline = p.readline

        nhq = nhq_iseg.NHQComm('/dev/tty0')
        yield nhq


@pytest.fixture()
def nhq_controller(request):
    """Test nhq controller"""
    with mock.patch('nhq_iseg.communication.serial.Serial') as mock_serial:
        # patch_serial(mock_serial)
        p = PatchSerial()
        mock_serial.return_value.write = p.write
        mock_serial.return_value.readline = p.readline

        nhq = nhq_iseg.NHQPowerSupply('/dev/tty0', request.param)
        yield nhq
