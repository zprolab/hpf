from . import HighPrecisionFloat

# Example usage:
if __name__ == "__main__":
    print('Testing HPF')
    interger_additive = 100
    interger_adder = 200
    decimal_additive = 0.1
    decimal_adder = 0.2

    for first_numbers in (interger_additive, decimal_additive):

        for second_numbers in (interger_adder, decimal_adder):

            for first_sign in ('', '-'):
                for second_sign in ('', '-'):

                    first_number = HighPrecisionFloat(f"{first_sign}{first_numbers}")
                    second_number = HighPrecisionFloat(f"{second_sign}{second_numbers}")

                    print("First number: ", first_number)
                    print("second number: ", first_number)

                    print(
                        "Addition:",
                        first_number,
                        '+',
                        second_number,
                        '=',
                        str(first_number + second_number),
                    )
                    print(
                        "Subtraction:",
                        first_number,
                        '-',
                        second_number,
                        '=',
                        str(first_number - second_number),
                    )
                    print(
                        "Multiplication:",
                        first_number,
                        '*',
                        second_number,
                        '=',
                        str(first_number * second_number),
                    )
                    print(
                        "Division:",
                        first_number,
                        '/',
                        second_number,
                        '=',
                        str(first_number / second_number),
                    )
