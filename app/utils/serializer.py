def model_to_dict(model_instance, exclude_fields=None, include_fields=None):
    if not model_instance:
        return None
    
    default_exclude = ['_sa_instance_state', 'password']
    
    if exclude_fields:
        default_exclude.extend(exclude_fields)
    
    data = {}
    for key, value in model_instance.__dict__.items():
        if key.startswith('_'):
            continue
        
        if key in default_exclude:
            continue
        
        if include_fields and key not in include_fields:
            continue
        
        if hasattr(value, 'isoformat'):
            data[key] = value.isoformat()
        else:
            data[key] = value
    
    return data