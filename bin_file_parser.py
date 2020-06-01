import binascii
import os


class BinFileParser(object):
    def __init__(self, file_path):
        self.path = file_path
        self.location = 0

    def parse_pattern_file(self):
        res = []

        with open(self.path, 'r') as f:
            for line in f.read().splitlines():
                res.append(line.encode())

        return res

    def stream_bytes(self, buffer_size=16324):
        file_size = os.path.getsize(self.path)
        print(f"File Size: {file_size // 1024 ** 2} Mb")
        file_in_chunks = file_size // buffer_size
        curr_chunk = 0
        with open(self.path, 'rb') as f:
            buffer = f.read(buffer_size)
            while buffer:
                print(f"{curr_chunk}/{file_in_chunks}")
                for byte in buffer:
                    yield byte
                buffer = f.read(buffer_size)
                curr_chunk += 1
