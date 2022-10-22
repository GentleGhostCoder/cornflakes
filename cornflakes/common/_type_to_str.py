from decimal import Decimal
import re


def type_to_str(f):
    """Function to convert python object to string -> fix scientific notation for float / Decimal."""
    string = str(f)
    if type(f) in [Decimal, float, int]:
        string = re.sub(r".*'(.+)'.*", "\\1", repr(f).lower())
        if re.match(r"^(-)?1e[+-][1-9]", string):  # detect scientific notation
            digits, exp = string.split("e")
            digits = digits.replace(".", "").replace("-", "")
            exp = int(exp)
            zero_padding = "0" * (abs(int(exp)) - 1)  # minus 1 for decimal point in the sci notation
            sign = "-" if f < 0 else ""
            if exp > 0:
                string = f"{sign}{digits}{zero_padding}.0"
            else:
                string = f"{sign}0.{zero_padding}{digits}"
    return string
