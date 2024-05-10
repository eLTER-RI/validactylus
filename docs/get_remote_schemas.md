Module src.get_remote_schemas
=============================

Functions
---------

    
`get_remote_schemas(url_schema_topic, url_schema_shared)`
:   retrieve validation schemas (1. topic specific and 2. shared definitions)
    from host; raise error if not both schemas can be retrieved
    (i. e. if server status not 200 for either schema)