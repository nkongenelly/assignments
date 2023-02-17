import pytest
from src.utils.error_handling import ErrorHandling

def test_error_handling():
    error_type = 'PAYLOAD_CONFIG'
    error_category = 'NOTICE'
    error_message = 'schema should be StructType or string'
    error_obj = ErrorHandling(error_type, error_category)
    result = error_obj.print_error(error_message)
    
    assert result == f'{error_type} - {error_message}'
    
def test_error_handling_without_message():
    error_type = 'PAYLOAD_CONFIG'
    error_category = 'NOTICE'
    
    with pytest.raises(Exception):
        error_obj.print_error()
    
    