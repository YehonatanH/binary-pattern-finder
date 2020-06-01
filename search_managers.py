import binascii
from collections import defaultdict


class PatternManager(object):

    def __init__(self, patterns_list):
        self.prefix_state = defaultdict(list)
        self.current_state = defaultdict(list)
        self.matched_patterns = defaultdict(list)
        self.current_location = 0

        self._create_prefix_state(patterns_list)

    def _create_prefix_state(self, patterns_list):
        for pattern in patterns_list:
            prefix = pattern[0:2]
            if prefix != b'XX':
                prefix = binascii.unhexlify(prefix)
                prefix = int.from_bytes(prefix, byteorder='big')
            self.prefix_state[prefix].append((pattern, 0))

    def receive_byte(self, byte):
        next_state = defaultdict(list)
        self._advance_state(byte, self.prefix_state, next_state)
        self._advance_state(byte, self.current_state, next_state)

        self.current_location += 2
        self.current_state = next_state

    def _advance_state(self, byte, search_state, next_state):
        for pattern, location in search_state[byte] + search_state[b'XX']:
            if location == len(pattern) - 2:
                abs_location = self.current_location - (len(pattern) - 2)
                self.matched_patterns[pattern].append(abs_location)
            else:
                next_byte_in_pattern = pattern[location + 2:location + 4]
                if next_byte_in_pattern != b'XX':
                    next_byte_in_pattern = int(next_byte_in_pattern.decode())

                next_state[next_byte_in_pattern].append((pattern, location + 2))


class SequenceManager(object):

    def __init__(self, threshold):
        self.threshold = threshold
        self.previous_byte = None
        self.counter = 1
        self.location = 0
        self.repeating_bytes = defaultdict(list)

    def receive_byte(self, byte):
        if byte == self.previous_byte:
            self.counter += 1
        else:
            if self.counter >= self.threshold:
                self.repeating_bytes[self.previous_byte].append((self.location - self.counter, self.counter))

            self.counter = 1
            self.previous_byte = byte

        self.location += 1
