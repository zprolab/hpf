"""
 _____          _   _ ____  _____ 
|__  /         | | | |  _ \|  ___|
  / /   _____  | |_| | |_) | |_   
 / /_  |_____| |  _  |  __/|  _|  
/____|         |_| |_|_|   |_|       
                                  
@file    hpf.py
@info    Pure self-defined High Precision Float Platfrom
@auth    Chenyun Z.(hi-zcy)
@auth    hi-zcy.com
@create  Oct. 27 2024
@license MIT License

@WARN    Do NOT edit infomation above this!
@edit    Oct. 27 2024
@proj    Feb. 16 2025

"""


class HighPrecisionFloat:
    def __init__(self, value, precision=10):
        if isinstance(value, str):
            self.negative = value.startswith('-')
            if self.negative:
                value = value[1:]
            if '.' in value:
                self.int_part, self.frac_part = value.split('.')
            else:
                self.int_part, self.frac_part = value, '0'
        elif isinstance(value, (int, float)):
            self.negative = value < 0
            value = str(abs(value))
            if '.' in value:
                self.int_part, self.frac_part = value.split('.')
            else:
                self.int_part, self.frac_part = value, '0'
        else:
            raise ValueError(f"Unsupported value type: {type(value)}.")
        self.int_part = self.int_part.lstrip('0') or '0'
        self.frac_part = self.frac_part.rstrip('0') or '0'

        self.precision = precision

    def __str__(self):
        sign = '-' if self.negative else ''
        if int(self.frac_part):
            return f"{sign}{self.int_part}.{self.frac_part}"
        else:
            return f"{sign}{self.int_part}"

    def __repr__(self):
        return f"HighPrecisionFloat('{str(self)}')"

    def _align_parts(self, other):
        max_frac_len = max(len(self.frac_part), len(other.frac_part))
        self_frac = self.frac_part.ljust(max_frac_len, '0')
        other_frac = other.frac_part.ljust(max_frac_len, '0')
        return self.int_part, self_frac, other.int_part, other_frac

    def __add__(self, other):
        if not isinstance(other, HighPrecisionFloat):
            other = HighPrecisionFloat(other)
        if self.negative == other.negative:
            int_part, frac_part = self._add_abs(other)
            result = HighPrecisionFloat(f"{int_part}.{frac_part}")
            result.negative = self.negative
        else:
            if self._abs_greater(other):
                int_part, frac_part = self._sub_abs(other)
                result = HighPrecisionFloat(f"{int_part}.{frac_part}")
                result.negative = self.negative
            else:
                int_part, frac_part = other._sub_abs(self)
                result = HighPrecisionFloat(f"{int_part}.{frac_part}")
                result.negative = other.negative
        return result

    def __sub__(self, other):
        if not isinstance(other, HighPrecisionFloat):
            other = HighPrecisionFloat(other)
        other.negative = not other.negative
        result = self + other
        other.negative = not other.negative
        return result

    def __mul__(self, other):
        if not isinstance(other, HighPrecisionFloat):
            other = HighPrecisionFloat(other)
        int_part, frac_part = self._mul_abs(other)
        result = HighPrecisionFloat(f"{int_part}.{frac_part}")
        result.negative = self.negative != other.negative
        return result

    def __truediv__(self, other):
        if not isinstance(other, HighPrecisionFloat):
            other = HighPrecisionFloat(other)
        int_part, frac_part = self._div_abs(other)
        result = HighPrecisionFloat(f"{int_part}.{frac_part}")
        result.negative = self.negative != other.negative
        return result

    def __floordiv__(self, other):
        return HighPrecisionFloat(self.__truediv__(other).int_part)

    def __del__(self):
        del self.frac_part
        del self.int_part

        del self.precision

    def _add_abs(self, other):

        a_int, a_frac, b_int, b_frac = self._align_parts(other)
        carry = 0
        frac_sum = []

        for i in range(len(a_frac) - 1, -1, -1):
            sum_val = int(a_frac[i]) + int(b_frac[i]) + carry
            carry = sum_val // 10
            frac_sum.append(str(sum_val % 10))

        frac_sum.reverse()
        frac_sum = ''.join(frac_sum)

        int_sum = []

        a_int, b_int = a_int.zfill(max(len(a_int), len(b_int))), b_int.zfill(
            max(len(a_int), len(b_int))
        )

        for i in range(len(a_int) - 1, -1, -1):
            sum_val = int(a_int[i]) + int(b_int[i]) + carry
            carry = sum_val // 10
            int_sum.append(str(sum_val % 10))

        if carry:
            int_sum.append(str(carry))

        int_sum.reverse()
        int_sum = ''.join(int_sum)

        return int_sum, frac_sum

    def _sub_abs(self, other):
        a_int, a_frac, b_int, b_frac = self._align_parts(other)
        borrow = 0
        frac_diff = []

        for i in range(len(a_frac) - 1, -1, -1):
            diff = int(a_frac[i]) - int(b_frac[i]) - borrow
            if diff < 0:
                diff += 10
                borrow = 1
            else:
                borrow = 0
            frac_diff.append(str(diff))

        frac_diff.reverse()
        frac_diff = ''.join(frac_diff).rstrip('0') or '0'

        int_diff = []
        a_int, b_int = a_int.zfill(max(len(a_int), len(b_int))), b_int.zfill(
            max(len(a_int), len(b_int))
        )

        for i in range(len(a_int) - 1, -1, -1):
            diff = int(a_int[i]) - int(b_int[i]) - borrow
            if diff < 0:
                diff += 10
                borrow = 1
            else:
                borrow = 0
            int_diff.append(str(diff))

        int_diff.reverse()
        int_diff = ''.join(int_diff).lstrip('0') or '0'

        return int_diff, frac_diff

    def _mul_abs(self, other):

        a = self.int_part + self.frac_part
        b = other.int_part + other.frac_part

        self_frac_len = len(self.frac_part.strip('0'))
        other_frac_len = len(other.frac_part.strip('0'))
        total_frac_len = self_frac_len + other_frac_len

        a_len, b_len = len(self.frac_part), len(other.frac_part)
        result = [0] * (len(a) + len(b))

        for i in range(len(a) - 1, -1, -1):
            for j in range(len(b) - 1, -1, -1):
                result[i + j + 1] += int(a[i]) * int(b[j])
                result[i + j] += result[i + j + 1] // 10
                result[i + j + 1] %= 10

        result = ''.join(map(str, result)).lstrip('0') or '0'
        # print(result)
        int_part = result[: -a_len - b_len] or '0'
        frac_part = result[-a_len - b_len :] or '0'

        frac_part = frac_part.zfill(total_frac_len)

        return int_part, frac_part

    def _div_abs(self, other):

        preprocessing_flag = False
        pre_count = float(self.int_part + '.' + self.frac_part) / float(
            other.int_part + '.' + other.frac_part
        )

        precision = self.precision + len(str(pre_count))

        # Preprocessing:
        if self.int_part is None and self.frac_part is None:

            preprocessing_flag = True

            self.int_part = self.frac_part[0]
            self.frac_part = self.frac_part[1:]

            other.int_part = other.frac_part[0]
            other.frac_part = other.frac_part[1:]

        a = self.int_part + self.frac_part
        b = other.int_part + other.frac_part

        self_frac_len = len(self.frac_part.strip('0'))
        other_frac_len = len(other.frac_part.strip('0'))
        total_frac_len = self_frac_len + other_frac_len

        a_len, b_len = len(self.frac_part), len(other.frac_part)
        a = a.ljust(len(a) + precision, '0')

        result = []
        remainder = 0

        for digit in a:
            remainder = remainder * 10 + int(digit)
            result.append(str(remainder // int(b)))
            remainder %= int(b)

        result = ''.join(result).lstrip('0') or '0'

        # print(result)

        int_part = (
            result[: -precision - 1]
            if ((self.int_part is None) or (other.int_part is None))
            else result[:-precision]
        ) or '0'
        # print(int_part)

        frac_part = result[-precision:] or '0'

        if preprocessing_flag:

            self.frac_part = "".join([self.int_part, self.frac_part])
            self.int_part = None

            other.frac_part = "".join([other.int_part, other.frac_part])
            other.int_part = None

        return int_part, frac_part

    def _abs_greater(self, other):

        if len(self.int_part) != len(other.int_part):
            return len(self.int_part) > len(other.int_part)

        if self.int_part != other.int_part:
            return self.int_part > other.int_part

        return self.frac_part > other.frac_part

    def pos(self):
        pass

    def neg(self):
        self.negative = False if self.negative else True

    def __eq__(self, other):
        if not isinstance(other, HighPrecisionFloat):
            other = HighPrecisionFloat(other)
        return (self.int_part, self.frac_part) == (
            other.int_part,
            other.frac_part,
        ) and self.negative == other.negative

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if not isinstance(other, HighPrecisionFloat):
            other = HighPrecisionFloat(other)
        if self.negative != other.negative:
            return self.negative
        if self.negative:
            return not self.__gt__(other)
        return self._compare(other) < 0

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        if not isinstance(other, HighPrecisionFloat):
            other = HighPrecisionFloat(other)
        if self.negative != other.negative:
            return not self.negative
        if self.negative:
            return not self.__lt__(other)
        return self._compare(other) > 0

    def __ge__(self, other):
        return self > other or self == other

hpf = HighPrecisionFloat
HPF = HighPrecisionFloat
