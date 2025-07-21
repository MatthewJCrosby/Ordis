# helpers to reduce repeated code throughout resolvers logic
def get_all(model, session):
    return session.query(model).all()

def get_by_id(model, session, id):
    return session.query(model).get(id)

def create_model(model, session, **kwargs):
    obj = model(**kwargs)
    session.add(obj)
    session.commit()
    return obj

def update_model(model, session, id, updates: dict):
    obj = session.query(model).get(id)
    if not obj:
        return None
    for k, v in updates.items():
        setattr(obj, k, v)
    session.commit()
    return obj

def delete_model(model, session, id):
    obj = session.query(model).get(id)
    if not obj:
        return False
    session.delete(obj)
    session.commit()
    return True
