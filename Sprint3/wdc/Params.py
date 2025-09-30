from typing import Union

class Params:
    """
    A class to define the parameters passed to the WCPS query.

    Attributes
    ----------
    param : str
        The parameter name.
    start_val : Union[str, int, float], optional
        The start value of the parameter. Defaults to None.
    end_val : Union[str, int, float], optional
        The end value of the parameter. Defaults to None.

    Methods
    -------
    __init__(self, param: str, start_val: Union[str, int, float] = None, 
             end_val: Union[str, int, float] = None)
        Initializes a Params object with the provided attributes.

    __str__(self) -> str
        Returns a string representation of the parameter.

    get_all_params(self)
        Returns a string representation of all parameters.
    """
    
    def __init__(self, param: str, start_val: Union[str, int, float] = None, 
                 end_val: Union[str, int, float] = None):
        """
        Initializes a Params object with the provided attributes.

        Parameters:
        -----------
        param : str
            The parameter name.
        start_val : Union[str, int, float], optional
            The start value of the parameter. Defaults to None.
        end_val : Union[str, int, float], optional
            The end value of the parameter. Defaults to None.

        Returns:
        --------
        None
        """
        self.param = param
        self.start_val = start_val
        self.end_val = end_val
        
    
    def __str__(self) -> str:
        """
        Returns a string representation of the parameter.

        Returns:
        --------
        str
            A string representation of the parameter.
        """
        param_str = self.param
        
        if self.end_val:
            if isinstance(self.start_val, str):
                param_str += f'("{self.start_val}":"{self.end_val}")'
            else:
                param_str += f'({self.start_val}:{self.end_val})'
        else:
            if isinstance(self.start_val, str):
                param_str += f'("{self.start_val}")'
            else:
                param_str += f'({self.start_val})'

        return param_str

    def get_all_params(self):
        """
        Returns a string representation of all parameters.

        Returns:
        --------
        str
            A string representation of all parameters.
        """
        return str(self)
