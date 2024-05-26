from strawberry.types import Info


MAX_DEPTH = 5
MAX_BREADTH = 3

def get_fields_by_selected_field(
    selected_field, 
    current_depth: int = 0,
    ignore_depth: int = MAX_DEPTH,
) -> dict | None:
    
    if not hasattr(selected_field, 'selections'):
        return

    response = {}
    current_depth += 1

    for selected_field in selected_field.selections:
        if current_depth >= ignore_depth:
            return response

        if hasattr(selected_field, 'type_condition'):
            collection = get_fields_by_selected_field(
                selected_field=selected_field,
                current_depth=current_depth,
                ignore_depth=ignore_depth,
            )
            if isinstance(collection, dict):
                response.update(collection)
            continue

        if selected_field.selections:
            response[selected_field.name] = get_fields_by_selected_field(
                selected_field=selected_field,
                current_depth=current_depth,
                ignore_depth=ignore_depth,
            )
        else:
            response[selected_field.name] = 1
    
    return response


def get_selected_fields(
    info: Info, 
    ignore_depth: int = MAX_DEPTH,
) -> dict:
    if ignore_depth > MAX_DEPTH:
        raise PermissionError('query depth exceeded')
    
    response = {}

    for selected_field in info.selected_fields:
        collection = get_fields_by_selected_field(
            selected_field=selected_field, 
            ignore_depth=ignore_depth,
        )
        if isinstance(collection, dict):
            response.update(collection)
    
    return response
