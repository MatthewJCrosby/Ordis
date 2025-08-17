from .. import schema
from flask import current_app

@schema.query.field("pageSizeOptions", "[Int!]!")
def resolve_page_size_options(_, info):
    return current_app.config.get("PAGE_SIZE_CHOICES")
