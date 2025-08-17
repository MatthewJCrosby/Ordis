from flask import current_app

"""
Sets default and max pagination sizes
"""
def normalize_pagination(limit: int | None, offset: int | None):

    config = current_app.config
    max_size = config.get("MAX_PAGE_SIZE")
    default =  config.get("DEFAULT_PAGE_SIZE")
    choices = config.get("PAGE_SIZE_CHOICES")

    if limit is None:
        limit = default
    else:
        limit = max(1, min(limit, max_size))
        """
        Enforce limits, so no one can ovveride the 500 max or use a non-predifined value. 
        """
        if limit not in choices:
            new_limt = default
            for choice in choices:
                if limit > choice:
                    new_limt = choice
            limit = new_limt
    offset = 0 if offset is None else max(0, offset)
    return limit, offset