def model_to_dict(model_instance, exclude_fields=None, include_fields=None):
    if not model_instance:
        return None

    default_exclude = ["_sa_instance_state", "password"]
    if exclude_fields:
        default_exclude.extend(exclude_fields)

    data = {}
    for column in model_instance.__table__.columns:
        key = column.name
        if key in default_exclude:
            continue
        if include_fields and key not in include_fields:
            continue
        value = getattr(model_instance, key)
        if hasattr(value, "isoformat"):
            data[key] = value.isoformat()
        else:
            data[key] = value

    return data
