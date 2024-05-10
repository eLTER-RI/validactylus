import requests
import json

def get_remote_schemas(url_schema_topic,
                       url_schema_shared):
    '''
    retrieve validation schemas (1. topic specific and 2. shared definitions)
    from host; raise error if not both schemas can be retrieved
    (i. e. if server status not 200 for either schema)
    '''


    max_waiting = 5 ## s
    rs = {
        "schema_topic" : requests.get(url_schema_topic,
                                      timeout = max_waiting),
        "schema_shared" : requests.get(url_schema_shared,
                                       timeout =max_waiting)
    }
    
    if not all (v.status_code == 200 for k, v in rs.items()):
        raise ValueError("failed to retrieve" +\
                         f"\"{url_schema_topic}\" and/or " + \
                         f"\"{url_schema_shared}.json\""
                         )
            
            
    # decode server byte response to UTF-8 and return schema as JSON:        
    rs = {k: json.loads(v.content.decode("UTF-8")) for k, v in rs.items()}
        
    return rs