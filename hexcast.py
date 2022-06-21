import os
import sys
import math
import random
import configparser
import more_itertools


# def one(size=8):
#     """
#     This is the most naive attempt. It simply concatenates 8 (by default) random hex digits
#     It satisfies constraints 1 and 4 but may output the so-called hexspeak strings mentioned above.
#     :param size:
#     :return:
#     """
#     hex_str = ''.join([hex(random.randint(0, 15)) for d in range(size)]).replace('0x', '')
#     return hex_str
#
#
# Set of canned prines for numbber of a given digit length. Utility set

PRIMES = {2: 7, 3: 127, 4: 2039, 5: 28031, 6: 280037, 7: 6000047, 8: 94217771, 10: 1647483757}


def is_int(v):
    try:
        nv = int(v)
        return True
    except Exception as e:
        return False


class MinimumUniqueDigitsFilter(object):
    """
    Must be at least 4 distinct chars
    """
    def __init__(self, minimum=4) -> None:
        self.minimum = minimum

    def is_valid(self, candidate) -> bool:
        charset = [c for c in candidate]
        return len(set(charset)) >= self.minimum


class SequenceHexDigitsFilter(object):
    def __init__(self, minimum=3) -> None:
        self.minimum = minimum

    def _is_hex_sequence(self, candidate):
        hdl = [int(c, 16) for c in candidate]
        hdl_p1 = list(map(lambda v: v + 1, hdl))

        all_but_first = hdl[1:]
        all_but_last = hdl_p1[:-1]
        return all_but_last == all_but_first

    def is_valid(self, candidate) -> bool:
        """
        No set of 3 consecutive digits can repeat
        No set of any 2 digits can repeat more than twice
        No more than 3 chars in any sequence ever
        :param candidate:
        :return:
        """

        # check for consecutively repeated 3-sequences
        trips = [''.join(s) for s in more_itertools.windowed(candidate, 3)]
        has_multrip = any(['{}{}'.format(t, t) in candidate for t in trips])
        if has_multrip:
            return False

        # check for 3 consecutive 2-sequences
        pairs = [''.join(s) for s in more_itertools.windowed(candidate, 2)]
        has_tripairs = any(['{}{}{}'.format(p, p, p) in candidate for p in pairs])
        if has_tripairs:
            return False

        # make sure we have no 4-8 consecutive sequences
        for i in range(4, 8):
            snips = [''.join(s) for s in more_itertools.windowed(candidate, i)]
            has_seq = any([self._is_hex_sequence(s) for s in snips])
            if has_seq:
                return False
        return True


class HexSpeakFilter(object):
    HSFILE = 'hslist.txt'

    def __init__(self) -> None:
        try:
            with open(self.HSFILE, 'r') as f:
                self.snippets = {x.strip() for x in f}
        except OSError as e:
            print('Hex filtering failed: ' + str(e))

    def is_valid(self, candidate):
        for s in self.snippets:
            if s in candidate:
                return False
        return True


class HexValidator(object):
    MAX_TRIES = 1000

    def __init__(self) -> None:
        self.filters = [
            HexSpeakFilter(),
            SequenceHexDigitsFilter(),
            MinimumUniqueDigitsFilter()
        ]

    def is_valid(self, candidate):
        for f in self.filters:
            if not f.is_valid(candidate):
                return False
        return True


class HexInvalidException(Exception):
    pass


class HexConfig(object):
    """
    Configuration class for the Hexinator
    Persists various bits to a file t keep track of the state
    """
    CYCLE_SECTION = 'CYCLE'
    CONFIG_FILE = 'hfa.ini'
    DEFAULT_VALS = {
        'size': 4,
        'dimension': 2,
        'leap': 7,
        'index': 3,
        'nth': 0,
        'validate': 'false'
    }

    config = None

    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(self.CONFIG_FILE)

    def initialize(self, initial=None):
        self._init_config(initial)
        self.config = configparser.ConfigParser()
        self.config.read(self.CONFIG_FILE)
        return self

    def get_size(self):
        return self.config.getint(self.CYCLE_SECTION, 'size')

    def set_size(self, value):
        if not value:
            return
        self._set_value(self.CYCLE_SECTION, 'size', str(value))

    def get_dimension(self):
        return self.config.getint(self.CYCLE_SECTION, 'dimension')

    def set_dimension(self, value):
        if not value:
            return
        self._set_value(self.CYCLE_SECTION, 'dimension', str(value))

    def get_leap(self):
        return self.config.getint(self.CYCLE_SECTION, 'leap')

    def set_leap(self, value):
        if not value:
            return
        self._set_value(self.CYCLE_SECTION, 'leap', str(value))

    def get_index(self):
        return self.config.getint(self.CYCLE_SECTION, 'index')

    def set_index(self, value):
        if not is_int(value):
            return
        self._set_value(self.CYCLE_SECTION, 'index', str(value))

        # we must increment the nth val as well
        n = self.config.getint(self.CYCLE_SECTION, 'nth')
        self.config.set(self.CYCLE_SECTION, 'nth', str(n + 1))
        self._flush()

    def get_startindex(self):
        return self.config.getint(self.CYCLE_SECTION, 'start_index')

    def get_linear_size(self):
        s = self.get_size()
        d = self.get_dimension()
        return s ** d

    def get_validate(self):
        return self.config.getboolean(self.CYCLE_SECTION, 'validate')

    def _set_value(self, section, key, val):
        self.config.set(section, key, val)
        self._flush()

    def _stringify(self, config_items):
        return {k: str(v) for k, v in config_items.items()}

    def _flush(self):
        with open(self.CONFIG_FILE, 'w') as cf:
            self.config.write(cf)

    def _init_config(self, initial=None):
        config = configparser.ConfigParser()
        config[self.CYCLE_SECTION] = self._stringify(initial) if initial else self.DEFAULT_VALS

        cndx = config.get(self.CYCLE_SECTION, 'index')
        config.set(self.CYCLE_SECTION, 'start_index', cndx)
        config.set(self.CYCLE_SECTION, 'nth', '0')
        self.config = config
        self._flush()


class Hexinator(object):
    """
    Contains the logic to increment from one value to the next following the cycle pararameters
    """

    def __init__(self, hex_config: HexConfig = None) -> None:
        if not hex_config:
            hex_config = HexConfig().initialize()

        self.vector_size = hex_config.get_size()
        self.vector_dimension = hex_config.get_dimension()
        self.leap_distance = hex_config.get_leap()
        self.current_index = hex_config.get_index()
        self.tiers = [self.vector_size ** v for v in range(self.vector_dimension - 1, 0, -1)]#  + [1]
        self.linear_size = self.vector_size ** self.vector_dimension
        self.config = hex_config

    def get_next_hex_string(self):
        next_index = self._increment_index()
        next_vec = self._get_vector_from_index(next_index)
        next_hex = self._get_hexstr_from_vec(next_vec)
        return next_hex

    def get_next_valid_hex_string(self):
        hs = self.get_next_hex_string()
        if not self.config.get_validate():
            return hs
        validator = HexValidator()
        tries = 1
        while not validator.is_valid(hs) and tries < HexValidator.MAX_TRIES:
            hs = self.get_next_hex_string()

        if not validator.is_valid(hs):
            raise HexInvalidException()

        return hs

    def _increment_index(self):
        next_index = (self.current_index + self.leap_distance) % self.linear_size
        self.current_index = next_index
        self.config.set_index(self.current_index)
        return self.current_index

    def _get_vector_from_index(self, index):
        vec_dim = self.vector_dimension
        extracted = [0] * vec_dim
        tier_item = index
        for ci in range(vec_dim - 1):
            extracted[ci] = math.floor(tier_item / self.tiers[ci])
            tier_item = tier_item - extracted[ci] * self.tiers[ci]
        extracted[vec_dim - 1] = tier_item - extracted[vec_dim - 1] * self.tiers[vec_dim - 2]
        return extracted

    def _get_hexstr_from_vec(self, vector):
        hxs = ''.join([hex(v) for v in vector]).replace('0x', '').upper()
        return hxs

    def get_sequence(self):
        """
        Returns the sequence for the next 'random' nmber to be emitted
        :return:
        """
        print(self.tiers)
        lins = self.config.get_linear_size()
        nseq = []
        cseq = []
        # arbitrary but seems reasonable for this
        if lins < 1000:
            ld = self.config.get_leap()
            ci = self.config.get_startindex()
            cc = ''.join([str(d) for d in self._get_vector_from_index(ci)])
            seq = {cc: ci}
            nseq.append(ci)
            cseq.append(cc)
            for i in range(lins-1):
                ci = (ci + ld) % lins
                cc = ''.join([str(d) for d in self._get_vector_from_index(ci)])
                seq[cc] = ci
                nseq.append(ci)
                cseq.append(cc)
            return seq


def no_init():
    msg = ''
    msg += 'You must initialize the system before use:\n'
    msg += 'python hexcast init'
    print(msg)


def main():
    """
    python hexcast init
    python
    """
    pl = len(sys.argv)

    is_init = sys.argv[1] == 'init' if pl > 1 else None
    is_seq_req = sys.argv[1] == 'sequence' if pl > 1 else None
    vec_size = sys.argv[2] if pl > 2 else None
    vec_dim = sys.argv[3] if pl > 3 else None

    if is_init:
        initial_vals = {}
        if is_int(vec_size) and is_int(vec_dim):
            linear_size = int(vec_size) ** int(vec_dim)
            initial_vals['size'] = vec_size
            initial_vals['dimension'] = vec_dim
            initial_vals['index'] = random.randint(0, linear_size)
            initial_vals['leap'] = PRIMES.get(len(str(linear_size)), 7)
            initial_vals['validate'] = int(vec_dim) == 8

        HexConfig().initialize(initial_vals)
        return

    if is_seq_req:
        if not os.path.exists(HexConfig.CONFIG_FILE):
            no_init()
            return

        config = HexConfig()
        hexinator = Hexinator(config)
        seq = hexinator.get_sequence()
        print(seq)
        return

    if not os.path.exists(HexConfig.CONFIG_FILE):
        no_init()
        return

    config = HexConfig()
    hexinator = Hexinator(config)
    try:
        hs = hexinator.get_next_valid_hex_string()
        print(hs)
    except HexInvalidException as e:
        msg = 'After {} increments no valid Hexadecximal string was found.'.format(HexValidator.MAX_TRIES)
        print(msg)


def test_filters():
    """
    :return:
    """

    # unique digits test
    hex_filter = MinimumUniqueDigitsFilter()
    goods = ['12341234', 'ABABCCCDB']
    bads = ['11112222', '122333221']

    for g in goods:
        assert hex_filter.is_valid(g)
    for b in bads:
        assert (not hex_filter.is_valid(b))

    # consecutive digits test
    bads = ['12312312',    '11111111',    '12123456',    '12121256',    '12ABCD89']
    goods = ['123F2367', '1212F345', '12ABC789']
    hex_filter = SequenceHexDigitsFilter()

    for g in goods:
        assert hex_filter.is_valid(g)

    for b in bads:
        assert (not hex_filter.is_valid(b))


if __name__ == '__main__':
    main()
