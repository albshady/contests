import collections

from . import _base


class Solver(_base.BaseSolver):
    _INPUT_FILENAME = 'diagnostic.txt'

    @staticmethod
    def _preprocess_line(line: str) -> list[int]:
        bits = [int(bit) for bit in line.strip()]
        return bits

    def solve1(self) -> int:
        bits_counter = collections.Counter()
        lines = 0

        for bits in self._input:
            lines += 1
            for position, bit in enumerate(bits):
                bits_counter[position] += bit

        most_common_bits = ''
        for value in bits_counter.values():
            most_common_bits += '1' if value >= lines // 2 else '0'

        least_common_bits = ''.join([str(abs(int(b) - 1)) for b in most_common_bits])

        return int(most_common_bits, 2) * int(least_common_bits, 2)

    def solve2(self) -> int:
        most = least = list(self._input)

        bit = 0
        while len(least) != 1:
            zeros, ones = self.get_zeros_ones(data=least, bit=bit)
            least = zeros if len(ones) >= len(zeros) else ones
            bit += 1

        for bit in range(len(least[0])):
            zeros, ones = self.get_zeros_ones(data=most, bit=bit)
            most = ones if len(ones) >= len(zeros) else zeros


        o2 = int(''.join([str(b) for b in most[0]]), 2)
        co2 = int(''.join([str(b) for b in least[0]]), 2)

        return o2 * co2

    @staticmethod
    def get_zeros_ones(
        data: list[list[int]], bit: int
    ) -> tuple[list[list[int]], list[list[int]]]:
        zeros = []
        ones = []

        for elem in data:
            if elem[bit] == 1:
                ones.append(elem)
            else:
                zeros.append(elem)

        return zeros, ones
