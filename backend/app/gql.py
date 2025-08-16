import magql

schema = magql.Schema()

@schema.query.field("greet", "String!", args={"name": magql.Argument("String", default="Ordis")})
def resolve_greet(parent, info, **kwargs):
    name = kwargs.pop("name")
    return f"hello, {name}!"