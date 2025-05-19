def get_product_access_permissions(user) -> dict:
    perm_map = {
        'allowed_create': 'add',
        'allowed_update': 'change',
        'allowed_delete': 'delete',
    }

    return {
        key: user.has_perm(f"module_engine.can_{perm}_product")
        for key, perm in perm_map.items()
    }