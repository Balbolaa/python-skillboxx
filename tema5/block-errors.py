class BlockErrors:
    def __init__(self, err_types) -> None:
        # Store the types of errors you want to ignore
        self.err_types = err_types
    
    def __enter__(self):
        # This method is called when the 'with' block starts.
        # It doesn't need to do anything here, so it just passes.
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        # This method is called when an error occurs inside the 'with' block.

        # If the error type is NOT in the list of errors to ignore:
        # Check if exc_type isn't one of the errors in self.err_types and
        # that it's not a subclass of any of those types.
        if exc_type not in self.err_types and not any(issubclass(exc_type, i) for i in self.err_types):
            return False  # Returning False means the error will still be raised.
        
        # If the error IS in the list (or a subclass of one), ignore it:
        return True  # Returning True means the error is ignored.
