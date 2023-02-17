import pytest
from src.utils.payload_validation_schema import payload_config_schema
from jsonschema import validate, ValidationError
from data.test_payload import payload as payload

def test_validation_schema_good():
    result = validate(payload, payload_config_schema)
    
    assert result == None
    
def test_validation_schema_bad():
    payload['reference']['header'] = "False"
    with pytest.raises(Exception):
        validate(payload, payload_config_schema)
    
    