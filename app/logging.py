import json
import logging

class JsonFormatter(logging.Formatter):
    def format (self, record):
        payload = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        if hasattr(record, "extra"):
            payload.update(record.extra)
            
        return json.dumps(payload)
    
def configure_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    
    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(logging.INFO)
    