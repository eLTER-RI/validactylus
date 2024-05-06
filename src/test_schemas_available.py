import pytest




from os import chdir, getcwd

chdir("c:/Users/offenthaler//fremd//fremd//CI//validactylus//src//")





schema_base_url = ("https://raw.githubusercontent.com/eLTER-RI/"
                   "elter-ci-schemas/main/schemas/")


from validactylus import *

rs = get_remote_schemas(schema_base_url, "data_mapping", "shared")


register_schemas(rs["schema_topic"], rs["schema_shared"])

rs["schema_topic"]
