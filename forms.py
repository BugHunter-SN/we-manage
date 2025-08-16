from fastapi import Form
from pydantic import BaseModel
from typing import Type, get_type_hints, get_origin, get_args
import inspect

def as_form(cls: Type[BaseModel]):
    """
    Adds an as_form class method to a Pydantic model that can be used with FastAPI Form data.
    """
    new_params = []
    
    # Get type hints for the model
    type_hints = get_type_hints(cls)
    
    for field_name, field_info in cls.__fields__.items():
        field_type = type_hints[field_name]
        
        # Handle Optional types
        if get_origin(field_type) is type(None) or (hasattr(field_type, '__args__') and type(None) in field_type.__args__):
            # This is an Optional field
            if hasattr(field_type, '__args__'):
                # Get the non-None type from Union[SomeType, None]
                actual_type = next(arg for arg in field_type.__args__ if arg is not type(None))
            else:
                actual_type = field_type
            
            default_value = field_info.default if field_info.default is not Ellipsis else None
            param = inspect.Parameter(
                field_name,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                default=Form(default_value),
                annotation=actual_type
            )
        else:
            # Required field
            param = inspect.Parameter(
                field_name,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                default=Form(...),
                annotation=field_type
            )
        
        new_params.append(param)
    
    def _as_form(**kwargs):
        return cls(**kwargs)
    
    # Create new signature
    sig = inspect.Signature(new_params)
    _as_form.__signature__ = sig
    
    # Add the method to the class
    cls.as_form = classmethod(_as_form)
    return cls

# Alternative simpler approach if the above is too complex
def make_form_body(model_class):
    """
    Simple function to create form body from Pydantic model
    """
    def as_form(**data):
        return model_class(**data)
    return as_form