COMMON_HTTP_METHODS: list[str] = ['head', 'options']
ALLOWED_HTTP_METHODS: list[str] = ['get', 'post', 'patch', 'delete', *COMMON_HTTP_METHODS]