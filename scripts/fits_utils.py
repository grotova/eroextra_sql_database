import ast

def parse_numeric_field(x):
    """Parse numeric field to list of floats, handle None or empty."""
    if x is None:
        return []
    if isinstance(x, str):
        x = x.strip()
        if not x:
            return []
        try:
            val = ast.literal_eval(x)
        except Exception:
            try:
                return [float(x)]
            except Exception:
                return []
        if isinstance(val, (list, tuple)):
            return [float(v) for v in val]
        else:
            return [float(val)]
    else:
        return [float(x)]

def parse_instrument_field(x):
    """Parse instrument field string, splitting on commas, handle None or empty."""
    if x is None:
        return []
    if isinstance(x, str):
        x = x.strip()
        if not x:
            return []
        if x.startswith("(") and x.endswith(")"):
            x = x[1:-1]
        return [item.strip() for item in x.split(",")] if x else []
    else:
        return [str(x).strip()]

def safe_field_access(row, fieldname):
    try:
        value = row[fieldname]
        # Some FITS columns return masked values — check and convert masked to None
        if hasattr(value, 'mask'):
            if value.mask:
                return None
            else:
                # If it's a masked array with no mask, get data
                return value.data if hasattr(value, 'data') else value
        return value
    except (KeyError, IndexError, AttributeError):
        return None
