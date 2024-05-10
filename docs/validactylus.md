Module src.validactylus
=======================

Functions
---------

    
`get_remote_schemas(url_schema_topic, url_schema_shared)`
:   Retrieve validation schemas from a remote schema store (e. g. a dedicated
    GitHub repo).
    Will raise an error if not both schemas can be retrieved
    with a server status of 200.
    
    **Arguments:**
    
    `url_schema_topic` -- full URL of topic-specific schema
        (e. g. site description),
        
    `url_schema_shared`  -- full URL of shared schema (containing common 
                definitions shared by several topic-specific schemas)

    
`get_validator(schema_topic, registry)`
:   

    
`register_schemas(schema_topic, schema_shared, spec=<Specification name='draft2020-12'>)`
:   Registers schemas (JSON objects of schemas written in JSONSchema)                       
                       locally in a Registry object.
    
    This is necessary to allow references from one schema to another,
    e. g. a topic-specific schema for site description referring to 
    common definitions (like latitude or site code format) stored in a
    shared schema.
    
    **Arguments**:
    `schema_topic` -- JSON object of topic specific schema,
    `schema_shared` -- JSON object of schema with shared definitions

    
`validate_elter(file_path, validator)`
: