from enum import IntEnum, unique


# TODO: change to use auto method when support python 3.6
@unique
class Models(IntEnum):
    NHQ_102M = 1
    NHQ_202M = 2
    NHQ_103M = 3
    NHQ_203M = 4
    NHQ_104M = 5
    NHQ_204M = 6
    NHQ_105M = 7
    NHQ_205M = 8
    NHQ_106M = 9
    NHQ_206M = 10
    NHQ_124M = 11
    NHQ_224M = 12

    @staticmethod
    def from_str(model):
        model = model.upper()
        str2model = {
            'NHQ_102M': Models.NHQ_102M, 'NHQ_202M': Models.NHQ_202M,
            'NHQ_103M': Models.NHQ_103M, 'NHQ_203M': Models.NHQ_203M,
            'NHQ_104M': Models.NHQ_104M, 'NHQ_204M': Models.NHQ_204M,
            'NHQ_105M': Models.NHQ_105M, 'NHQ_205M': Models.NHQ_205M,
            'NHQ_106M': Models.NHQ_106M, 'NHQ_206M': Models.NHQ_206M,
            'NHQ_124M': Models.NHQ_124M, 'NHQ_224M': Models.NHQ_224M,

        }
        return str2model[model]


class Precision(IntEnum):
    High = 1
    Standard = 2

# TODO: change to use auto method when support python 3.6
@unique
class State(IntEnum):
    ON = 1
    OFF = 2
    MAN = 3
    ERR = 4
    INH = 5
    QUA = 6
    L2H = 7
    H2L = 8
    LAS = 9
    TRP = 10

    @staticmethod
    def means(state):
        msg = {
            State.ON: 'Output voltage according to set voltage',
            State.OFF: 'Channel front panel switch off',
            State.MAN: 'Channel is on, set to manual mode',
            State.ERR: 'Vmax or Imax is/ or was been exceeded',
            State.INH: 'Inhibit signal was been / is active',
            State.QUA: 'Quality of output voltage not given at present',
            State.L2H: 'Output voltage increasing',
            State.H2L: 'Output voltage falling',
            State.LAS: 'Look at Status (only after G-command)',
            State.TRP: 'Current trip was been active'
        }
        return msg[state]

    @staticmethod
    def from_str(state):
        state = state.upper()
        str2state = {'ON': State.ON, 'OFF': State.OFF, 'MAN': State.MAN,
                     'ERR': State.ERR, 'INH': State.INH, 'QUA': State.QUA,
                     'L2H': State.L2H, 'H2L': State.H2L, 'LAS': State.LAS,
                     'TRP': State.TRP}
        return str2state[state]


# TODO: Include the other models
# Models specifications: Maximum Voltage, Precision, Channels
class Specs:
    _specs = {
        Models.NHQ_102M: [2000, 6e-3, Precision.Standard, 1],
        Models.NHQ_202M: [2000, 6e-3, Precision.Standard, 2],
        Models.NHQ_103M: [3000, 4e-3, Precision.Standard, 1],
        Models.NHQ_203M: [3000, 4e-3, Precision.Standard, 2],
        Models.NHQ_104M: [4000, 3e-3, Precision.Standard, 1],
        Models.NHQ_204M: [4000, 3e-3, Precision.Standard, 2],
        Models.NHQ_105M: [5000, 2e-3, Precision.Standard, 1],
        Models.NHQ_205M: [5000, 2e-3, Precision.Standard, 2],
        Models.NHQ_106M: [6000, 1e-3, Precision.Standard, 1],
        Models.NHQ_206M: [6000, 1e-3, Precision.Standard, 2],
        Models.NHQ_124M: [4000, 3e-3, Precision.High, 1],
        Models.NHQ_224M: [4000, 3e-3, Precision.High, 2],
    }

    @staticmethod
    def max_voltage(model):
        return Specs._specs[model][0]

    @staticmethod
    def max_current(model):
        return Specs._specs[model][1]

    @staticmethod
    def is_high_precision(model):
        precision = Specs._specs[model][2]
        if precision == Precision.High:
            return True
        else:
            return False
    @staticmethod
    def channels(model):
        return Specs._specs[model][3]
