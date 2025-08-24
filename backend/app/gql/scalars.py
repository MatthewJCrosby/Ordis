from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import magql

"""
A custom scalar to map db Decimal types to custom magql Decimal type
to avoid mapping to a string type. 
"""

DecimalType = magql.Scalar("Decimal")

def _to_decimal(value) -> Decimal:
    if value is None:
        return None
    elif value is not None and isinstance(value, Decimal):
        return value
    try:
        res = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError(f"An error occured trying to convert {value} to a decimal ")
    return res


@DecimalType.parse_value
def parse_decimal(value):
    return _to_decimal(value)

@DecimalType.serialize
def serialize_decimal(value):
    if value is None:
        return None
    if not isinstance(value, Decimal):
        res = _to_decimal(value)
    return format(value, "f")

    
