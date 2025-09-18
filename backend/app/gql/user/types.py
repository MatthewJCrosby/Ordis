from .. import schema
import magql


UserType = magql.Object("User", fields={
        "id": "String!",
        "email": "String!",
        "first_name": "String!",
        "last_name": "String!",

    }
)

schema.add_type(UserType)
