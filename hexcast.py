"""

Problem Statement
1. Every time you run the program, it should emit one 8-digit hexadecimal code;
2. It should emit every possible code before repeating;
3. It should not print "odd-looking" codes such as 0xAAAAAAAA or 0x01234567 or any commonly used words, phrases, or hexspeak such as 0xDEADBEEF;
4. Codes should be emitted in apparently random order.


Solutions are below



naive solves string: 1, 4
add dictionary excludes and that solves for 2

3 requires more thinking
Simple solution: keep a list and check it as you go
There are 16^8 strings. THis is 2^32 or 4G possibilities. So, too many to store in a list or even in a DB.

We must traverse the list. Simple to do if we are just incrementing the values; an odometer.
How do we randomize.
A list of 8 scalars is a vector. One can walk a 2d plane on the diagonals adnd then extend this to n more items but this may not work.
What if we randomize the values at location n and just do a standard traversal
Ie., instead of [0...F] we have soething like [A, 3, 9, B...] and then just travese that. Well, it still doesn't work as you can detect a pattern.
Ok, so what if we randomize each of the axes of the plane (or the vector) and walk that.
Or. We can just use a hash funcdtion. Encryption algorithms hav them. We don't really care about this beiung encruyoted as it is a one time use thing
We can then just iterate through the numbers. Hash is gauranteed to always convert N to NX.
We need to be able to store current index & the seed in a config file. Security is as good as the device on which it is run

shake_128()











"""
import os
import sys
import hashlib
import math
import random
import configparser
import fast_password_validation
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
# def is_conformant(hex_str):
#     """
#     TBD
#     :param hex_str:
#     :return:
#     """
#     return True
#
#
# def two(tries_before_capitulation=100):
#     """
#     The second approach grapples with item 3) and just adds a filter of dictionary terms to the output of the first solution
#     Tries are hardcoded which ought to work in almost all cases but is not gauranteed
#     :param tries_before_capitulation:
#     :return:
#     """
#     cur_try = 0
#     while cur_try < tries_before_capitulation:
#         hv = one()
#         if is_conformant(hv):
#             return hv
#     return ''
#
#
# def three():
#     """
#     Constraint 2) is the heart of the problem. How do we emit all of the conformant items before repeating any.
#     A simple approach would be just so store the visited items in a list and check it after each successive run. The list could
#     be persisted in a file or even in a DB.
#
#     For small set of possibles this could work, though given the current random strategy it will take ever more tries to find an unused value as the list size increases.
#     It is useful first to recognize how many possibilities there are. We have 16^8 possible hex strings. This is 2^32 or ~ 4G items.
#     For a set of this size, even a DB would be untenable as a way to persist the visited list.
#
#     It seems we have to actually traverse the list itself and somehow keep our place in it.
#     It is easy enough to traverse the list of numbers just by looping: 0...FFFFFF hex or 0...4294967296 in decimal but this
#     violates constraint 4): these must appear random.
#
#     Looking at arrays, or really vectors, maight prove useful. For a simple array of two hex digits we might have something like this:
#
#     00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F
#     10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F
#     20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F
#     30 31 32 33 34 35 36 37 38 39 3A 3B 3C 3D 3E 3F
#     40 41 42 43 44 45 46 47 48 49 4A 4B 4C 4D 4E 4F
#     50 51 52 53 54 55 56 57 58 59 5A 5B 5C 5D 5E 5F
#     60 61 62 63 64 65 66 67 68 69 6A 6B 6C 6D 6E 6F
#     70 71 72 73 74 75 76 77 78 79 7A 7B 7C 7D 7E 7F
#     80 81 82 83 84 85 86 87 88 89 8A 8B 8C 8D 8E 8F
#     90 91 92 93 94 95 96 97 98 99 9A 9B 9C 9D 9E 9F
#     A0 A1 A2 A3 A4 A5 A6 A7 A8 A9 AA AB AC AD AE AF
#     B0 B1 B2 B3 B4 B5 B6 B7 B8 B9 BA BB BC BD BE BF
#     C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 CA CB CC CD CE CF
#     D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 DA DB DC DD DE DF
#     E0 E1 E2 E3 E4 E5 E6 E7 E8 E9 EA EB EC ED EE EF
#     F0 F1 F2 F3 F4 F5 F6 F7 F8 F9 FA FB FC FD FE FF
#
#     We can traverse this row by row, column by column, or even diagonal by diagonal, but a cursiry examination shows that a visible pattern emerges.
#     Similarly, were we to extend this to a 3rd dimension or, in our case, 8, then we would likely have the same problem.
#     We could simply beghin with randomized axes, in which case we would have a 2D matrix such as this:
#
#     BC BF B3 B1 B4 BE B9 B6 B0 B8 BD BB BA B7 B2 B5
#     FC FF F3 F1 F4 FE F9 F6 F0 F8 FD FB FA F7 F2 F5
#     8C 8F 83 81 84 8E 89 86 80 88 8D 8B 8A 87 82 85
#     3C 3F 33 31 34 3E 39 36 30 38 3D 3B 3A 37 32 35
#     5C 5F 53 51 54 5E 59 56 50 58 5D 5B 5A 57 52 55
#     AC AF A3 A1 A4 AE A9 A6 A0 A8 AD AB AA A7 A2 A5
#     6C 6F 63 61 64 6E 69 66 60 68 6D 6B 6A 67 62 65
#     1C 1F 13 11 14 1E 19 16 10 18 1D 1B 1A 17 12 15
#     9C 9F 93 91 94 9E 99 96 90 98 9D 9B 9A 97 92 95
#     2C 2F 23 21 24 2E 29 26 20 28 2D 2B 2A 27 22 25
#     0C 0F 03 01 04 0E 09 06 00 08 0D 0B 0A 07 02 05
#     DC DF D3 D1 D4 DE D9 D6 D0 D8 DD DB DA D7 D2 D5
#     7C 7F 73 71 74 7E 79 76 70 78 7D 7B 7A 77 72 75
#     CC CF C3 C1 C4 CE C9 C6 C0 C8 CD CB CA C7 C2 C5
#     EC EF E3 E1 E4 EE E9 E6 E0 E8 ED EB EA E7 E2 E5
#     4C 4F 43 41 44 4E 49 46 40 48 4D 4B 4A 47 42 45
#
#     This is likely to still reveal a visible pattern in 2D but it might be harder to discern with higher dimensions.
#
#     00 01 02 03 04 05 06
#     10 11 12 13 14 15 16
#     20 21 22 23 24 25 26
#     30 31 32 33 34 35 36
#     40 41 42 43 44 45 46
#     50 51 52 53 54 55 56
#     60 61 62 63 64 65 66
#
#     0 00
#     1 10 01
#     2 20 11 02
#     3 30 21 12 03
#     4 40 31 22 13 04
#     5 50 41 32 23 14 05
#
#     6 60 51 42 33 24 15 06
#
#     7 61 52 43 34 25 16
#     8 62 53 44 35 26
#     9 63 54 45 36
#    10 64 55 46
#    11 65 56
#    12 66
#
#     0, 1, 2, 3, 4, 5, 6, 7...15         0 ... 256
#
#     0..15 1
#     0..15 2
#     ...
#     0..15 8
#
#
#
#     00000000
#     10000000
#     01000000
#     00100000
#     00010000
#     00001000
#     00000100
#     00000010
#     00000001
#
#     ffffffff
#
#     16^8 values
#     each vec is 8 coordinates
#     0000000
#
#
#
#     7777777
#
#
#
#
#     16 x 16 x 16 x 16 x 16 x 16 x 16 x 16
#
#
#
#
#
#
#     7    61 52 43 34 25 26
#     8
#     9
#
#
#     """
#     pass
#
#
# def four(hash_input, size=8):
#     """
#     This strategy goes back to the original proposition. We need a structure or process that has a 1-1 mapping
#     between a number in our set of 4G and a random 8 digit hex string. Since we are only concerned about the hex string
#     as output we only need a one way mapping. This is essentially a hash function.
#     The easiest such functiona to hand are encryption libraries, in particular, since this is python, those in the hashlib module
#
#     We can iterate through a set of numbers 1...n and get a distinct and repeatable value, hashed(i) for each one.
#
#     But the hash returned is much longer than 8 hex digits and taking pieces of the string
#
#     :param size:
#     :return:
#     """
#     m = hashlib.shake_128()
#     m.update(hash_input)
#     hx = m.hexdigest(4)
#     return hx
#
#
#
# def six():
#     xelms = ['{}'.format(hex(i)).replace('0x', '').upper() for i in range(16)]
#     yelms = ['{}'.format(hex(i)).replace('0x', '').upper() for i in range(16)]
#     zelms = ['{}'.format(hex(i)).replace('0x', '').upper() for i in range(16)]
#
#     random.shuffle(xelms)
#     random.shuffle(yelms)
#     random.shuffle(zelms)
#
#     cnt = 1
#     for x in xelms:
#         for y in yelms:
#             for z in zelms:
#                 if cnt < 50:
#                     print('{}{}{}'.format(x, y, z))
#                     cnt += 1
#                 else:
#                     return
#
#
# def array_out():
#
#     xelms = ['{}'.format(hex(i)).replace('0x', '').upper() for i in range(16)]
#     yelms = ['{}'.format(hex(i)).replace('0x', '').upper() for i in range(16)]
#     zelms = ['{}'.format(hex(i)).replace('0x', '').upper() for i in range(16)]
#
#     random.shuffle(xelms)
#     random.shuffle(yelms)
#
#     # print(xelms)
#     # print(yelms)
#     # return
#
#     for i in xelms:
#         curline = []
#         for j in yelms:
#             curline.append('{}{}'.format(i, j))
#         print(' '.join(curline))
#
# def do_test_one(iter=4):
#     """
#
#     :param iter: number of times to iterate the test
#     :return:
#     """
#     for i in range(iter):
#         print(one())
#
#
# def do_test_four():
#     hxl = []
#     for i in range(100000):
#         hx = four(bytes(str(i), 'utf-8'))
#         hxl.append(hx)
#     hxl = list(set(hxl))
#     print(len(hxl))
#
#
# bitty = [0, 1, 4, 8, 3, 6, 12, 5, 10, 9, 7, 11, 13, 15, 16]
#
# # 3 I found this recipe for rotating a list:
#
#
# import collections
#
#
#
# def saturday():
#     a = random.randint(0, 15)
#     b = random.randint(0, 15)
#     c = random.randint(0, 15)
#
#     alist = collections.deque(range(16))
#     alist.rotate(a)
#
#     blist = collections.deque(range(16))
#     blist.rotate(b)
#
#     clist = collections.deque(range(16))
#     clist.rotate(c)
#
#
#     # 1, 3, 5, 7, 11, 13, 15
#     mva = 3
#     mvb = 5
#
#     acurdx = a
#     bcurdx = b
#     ml = [(a, b)]
#     # print(a, b)
#     for i in range(16*16 - 1)[:25]:
#         acurdx = (acurdx + mva) % 16
#         bcurdx = (bcurdx + mvb) % 16
#         ml.append((acurdx, bcurdx))
#         # print(acurdx)
#         print(acurdx, bcurdx)
#
#     # print(len(set(ml)))
#     print(sorted(ml))
#
#     # xy -->   a0, a7
#
#
# def sat2():
#     # [0000,0000,0000,0000, 0001, 0010, 0100, 1000]
#
#     """
#     # all permutations of 4, 5, 6, 7, 8
#
#     00 01 02
#     10 11 12
#     20 21 22
#
#     3 x 3
#
#     00 01 02
#     10 11 12
#     20 21 22
#
#     00 01 02 10 11 12 20 21 22
#      0  1  2  3  4  5  6  7  8
#
#     2 x 2 x 2
#     000 010
#     100 110
#
#     001 011
#     101 111
#
#     000 001
#     010 011
#     -------
#     100 101
#     110 111
#
#     xyz xyz xyz
#     000 001 010 011 100 101 110 111
#       0   1   2   3   4   5   6  7
#
#     """
#
#     mat_size = 5
#     mat_dim = 4
#     offsets = [mat_size ** v for v in range(mat_dim - 1, 0, -1)] + [1]
#
#     for mi1 in range(mat_size):
#         for mi2 in range(mat_size):
#             for mi3 in range(mat_size):
#                 for mi4 in range(mat_size):
#                     ndx = sum(map(lambda v, m: v*m, offsets, [mi1, mi2, mi3, mi4]))
#                     extracted = [0] * mat_dim
#                     tm = ndx
#                     for ci in range(mat_dim-1):
#                         extracted[ci] = math.floor(tm / offsets[ci])
#                         tm = tm - extracted[ci] * offsets[ci]
#                     extracted[mat_dim-1] = tm - extracted[mat_dim-1] * offsets[mat_dim-2]
#                     #
#                     # ci1 = math.floor(ndx / offsets[0])
#                     # tm = ndx - ci1 * offsets[0]
#                     # ci2 = math.floor(tm / offsets[1])
#                     # tm = tm - ci2 * offsets[1]
#                     # ci3 = math.floor(tm / offsets[2])
#                     # ci4 = tm - ci3 * offsets[2]
#
#                     # match =
#                     print(mi1, mi2, mi3, mi4, '|', ndx, '|', *extracted)
#
#     return
#
#
# def dotProd(v1, v2):
#     dpv = sum(map(lambda x, y: x * y, v1, v2))
#     return dpv
#
#
# def get_vec_from_ndx_offets(ndx, mat_dim, offsets):
#     extracted = [0] * mat_dim
#     tm = ndx
#     for ci in range(mat_dim - 1):
#         extracted[ci] = math.floor(tm / offsets[ci])
#         tm = tm - extracted[ci] * offsets[ci]
#     extracted[mat_dim - 1] = tm - extracted[mat_dim - 1] * offsets[mat_dim - 2]
#     return extracted
#
# # 256 x 4
# # 16 x 8
#
#
#
#
# def sat3():
#     mat_size = 16
#     mat_dim = 2
#
#     offsets = [mat_size ** v for v in range(mat_dim - 1, 0, -1)] + [1]
#     bcoords = [random.randint(0, mat_size-2) for i in range(mat_dim)]
#     bndx = dotProd(bcoords, offsets)
#
#     mat_list_size = mat_size ** mat_dim
#     leap_distance = 25013
#
#     cndx = bndx
#     # collector = [cndx]
#     collector = []
#     print('bcoords:', bcoords)
#     print('bndx:', cndx)
#     for i in range(mat_size ** mat_dim):
#         cur_vec = get_vec_from_ndx_offets(cndx, mat_dim, offsets)
#         hex_str = ''.join(map(lambda v: hex(v), cur_vec)).replace('0x', '').upper()
#         # if vec_str in collector:
#         #     print('duplicate:', vec_str)
#         print(hex_str)
#         collector.append(hex_str)
#         cndx = (cndx + leap_distance) % mat_list_size
#         # collector.append(cndx)
#
#     # print(sorted(collector))
#
#     # dupes = [v for v in collector if collector.count(v) > 1]
#     # print(dupes)
#
#     print(len(set(collector)))
#
#
#
# def sun1():
#     #          2    3      4     5       6         7         8
#     primes = [127, 2039, 28031, 280037, 6000047, 94217771, 1647483757]
#     vecs = 16
#     vecd = 4
#     # ld = 127
#     # ld = 349
#     # ld = 1973
#     # ld = 3547
#     ld = 28031
#     hexinator = Hexinator(vector_size=vecs, vector_dimension=vecd, leap_distance=ld)
#     vals = []
#     for i in range(vecs ** vecd):
#         hxs = hexinator.get_next_hex_string()
#         vals.append(hxs)
#         # print(hx
#
#     print(vals)
#     # print(sorted(vals))
#     print(len(set(vals)))


# def sun2():
#
#     ld = 7
#     # ld = 349
#     # ld = 1973
#     # ld = 3547
#
#     vecs = 4
#     vecd = 2
#     # ld = 28031
#
#     initial_vals = {'size': vecs, 'dimension': vecd, 'leap': ld, 'index': random.randint(0, vecs ** vecd)}
#     config = HexConfig(initial=initial_vals)
#     hexinator = Hexinator(config)
#
#     hs = hexinator.get_next_hex_string()
#     print(hs)

# Set of canned prines for numbber of a given digit length. Utilit set
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
        self.tiers = [self.vector_size ** v for v in range(self.vector_dimension - 1, 0, -1)] + [1]
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
        lins = self.config.get_linear_size()
        # arbitrary but seems reasonable for this
        if lins < 1000:
            ld = self.config.get_leap()
            ci = self.config.get_startindex()
            cc = ''.join([str(d) for d in self._get_vector_from_index(ci)])
            seq = {cc: ci}
            for i in range(lins-1):
                ci = (ci + ld) % lins
                cc = ''.join([str(d) for d in self._get_vector_from_index(ci)])
                seq[cc] = ci
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
