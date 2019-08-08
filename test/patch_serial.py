
ENCODING = 'ascii'


def patch_serial(mock_serial):

    buffer_out = []
    values = {'#': ['#', '486100;2.08;2000V;6mA\r\n'],
              'u1': ['u1\r\n', '+0008\r\n'],
              'm1': ['m1\r\n', '060\r\n'],
              'n1': ['n1\r\n', '100\r\n'],
              'd1': ['d1\r\n', '0004\r\n'],
              'v1': ['v1\r\n', '002\r\n'],
              'l1': ['l1\r\n', '0000\r\n'],
              's1': ['s1\r\n', 'S1=ON \r\n'],
              't1': ['t1\r\n', '005\r\n'],
              'a1': ['a1\r\n', '000\r\n'],
              'i1': ['i1\r\n', '0000-6\r\n']
              }

    def write(data):
        global buffer_out
        if data == b'\r\n':
            return 2
        cmd = data.decode(ENCODING)
        cmd = cmd.lower().strip()
        if cmd == 'w':
            # TODO: implement value change to generate errors
            buffer_out = ['w\r\n', '003\r\n']
        else:
            buffer_out = values[cmd]
        return len(data)

    def readline():
        global buffer_out
        try:
            result = buffer_out.pop(0)
        except IndexError:
            result = ''
        return result.encode(ENCODING)

    mock_serial.return_value.write = write
    mock_serial.return_value.readline = readline
