from search_managers import PatternManager, SequenceManager
from bin_file_parser import BinFileParser
from timer_decorator import timeit
from sys import argv
import binascii
import datetime


@timeit
def find_patt(threshold, patterns_file, bin_file):
    patterns = patterns_file.parse_pattern_file()
    pattern_manager = PatternManager(patterns)
    sequence_manager = SequenceManager(threshold)

    for b in bin_file.stream_bytes():
        pattern_manager.receive_byte(b)
        sequence_manager.receive_byte(b)

    sequence_manager.receive_byte(None)
    result_file = bin_file.path[:-4] + "RES.txt"

    with open(result_file, "w") as rf:
        rf.write("Matching Patterns:\n")
        for pat in pattern_manager.matched_patterns:
            rf.write(pat.decode("utf-8") + ":")
            rf.write(str(pattern_manager.matched_patterns[pat]))
            rf.write("\n")

        rf.write("Repeating Bytes:\n")
        for seq in sequence_manager.repeating_bytes:
            rf.write(hex(seq) + ":")
            rf.write(str(sequence_manager.repeating_bytes[seq]))
            rf.write("\n")


if __name__ == '__main__':
    main_file_path = argv[1]
    patterns_file_path = argv[2]
    threshold = int(argv[3])

    main_file = BinFileParser(main_file_path)
    patterns_file = BinFileParser(patterns_file_path)
    print("Loaded File")
    print(datetime.datetime.now())
    find_patt(threshold, patterns_file, main_file)
    print(datetime.datetime.now())
