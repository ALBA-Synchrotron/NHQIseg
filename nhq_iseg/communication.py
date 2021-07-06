import serial
import time
import logging

__all__ = ['NHQComm']


class NHQComm:
    CODING = 'ascii'
    MAX_LEN = 26

    def __init__(self, port, wait_time=0):
        log_name = '{}.NHQComm'.format(__name__)
        self.log = logging.getLogger(log_name)
        self._com = serial.serial_for_url(port)
        self._com.timeout = 0
        self._send('w')
        time.sleep(1)
        raw_value = self._read()
        if raw_value.count('\n') != 2:
            raise RuntimeError('break time must be between 1 and 80 ms')
        value = int(raw_value.split('\r\n')[1])
        if value == 0 or value > 30:
            raise RuntimeError('break time must be between 1 and 20 ms')
        self._wait_time = ((value * self.MAX_LEN) + 100 + wait_time) / 1000

    def _send(self, cmd):
        self.log.debug('Send cmd {}'.format(cmd))
        cmd = cmd + '\r\n'
        for i in cmd:
            self._com.write(i.encode(self.CODING))
            time.sleep(0.003)
        self.log.debug('Send raw: {}'.format(repr(cmd.encode(self.CODING))))

    def _read(self):
        ans = b''
        ans += self._com.readline()
        ans += self._com.readline()
        self.log.debug('Read raw: {}'.format(ans))
        return ans.decode(self.CODING)

    def send_cmd(self, cmd):
        if 'w=' in cmd.lower():
            raise RuntimeError('To change the break time use break_time cmd')
        self._send(cmd)
        time.sleep(self._wait_time)
        return self._read()


if __name__ == '__main__':
    import sys
    serial_port = sys.argv[1]

    nhq = NHQComm(serial_port)
    read_cmd_list = ['#', 'w', 'u1', 'u2', 'm1', 'm2', 'n1', 'n2', 'd1', 'd2',
                     'v1', 'v2', 'l1', 'l2', 's1', 's2', 't1', 't2', 'a1',
                     'a2']

    for command in read_cmd_list:
        answer = nhq.send_cmd(command)
        print('Cmd: {} Result: {}'.format(command, repr(answer)))

    write_cmd_list = ['d1=4', 'd1']

    for command in write_cmd_list:
        answer = nhq.send_cmd(command)
        print('Cmd: {} Result: {}'.format(command, repr(answer)))
