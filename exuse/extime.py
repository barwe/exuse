from datetime import datetime


def timestamp(fmt: str = None):
    """Timestamp for now.

    Args:
        fmt (str, optional): datetime format. Defaults to `'%Y%m%d_%H%M%S'`.

    Returns:
        str: formatted datetime.
    """
    if fmt is None:
        fmt = "%Y%m%d_%H%M%S"
    return datetime.now().strftime(fmt)
