def str_to_slice(s):
    try:
        parts = [int(x) if x else None for x in s.split(":")]
        return slice(*parts)
    except (ValueError, TypeError):
        raise ValueError("Invalid slice format")
