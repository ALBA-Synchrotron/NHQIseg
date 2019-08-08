import pytest


def test_nhq_mock(nhq_mock):
    nhq_mock.write(b'w')
    nhq_mock.write(b'\r\n')
    ans = nhq_mock.readline()
    ans += nhq_mock.readline()
    assert ans == b'w\r\n003\r\n'


def test_nhq_read_com(nhq_com):
    ans = nhq_com.send_cmd('w')
    assert ans == 'w\r\n003\r\n'
    with pytest.raises(RuntimeError):
        nhq_com.send_cmd('w=4')
    ans = nhq_com.send_cmd('U1')
    assert ans == 'u1\r\n+0008\r\n'
    ans = nhq_com.send_cmd('D1')
    assert ans == 'd1\r\n0004\r\n'
