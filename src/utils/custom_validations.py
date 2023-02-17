from .error_handling import ErrorHandling

class custom_validations:
    def __init__(self, payload):
        self.payload = payload
        self.validation = True
        
    def validations(self):
        # for folder, location string should end with a '/'
        self.get_payload_folder_value('reference')
        self.get_payload_folder_value('lab')
        self.get_payload_folder_value('results')
            
        
        
        return self.validation

    def get_payload_folder_value(self, file_type): 
        reference_folder =  self.payload.get(file_type).get('folder', False) 
        reference_folder = reference_folder if file_type != 'results' else True
        
        if reference_folder: 
            self.folder_location_string(self.payload.get(file_type).get('location'))
        
        
    def folder_location_string(self, location):
        if not location[0].endswith('/'):
            self.raise_pipeline_config_error("Folder location should end with a slash (/)")
            self.validation = False
            
    def raise_pipeline_config_error(self, message):
        error_obj = ErrorHandling('PAYLOAD_CONFIG', 'NOTICE')
        error_obj.print_error(message)
