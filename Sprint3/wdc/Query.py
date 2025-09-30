from typing import List

# Importing user-defined modules
from wdc.Connection import allCoverages
from wdc.Params import Params

# Specifying the supported return and query types for the queries
returnTypes = [
        "image/png",
        "image/jpeg",
        "text/csv"
]

queryTypes = [
    "most_basic_query",
    "selecting_single_value",
    "transform_3d_to_1d_subset",
    "transform_3d_to_2d_subset",
    "celsius_to_kelvin",
    "min",
    "max",
    "avg",
    "when_temp_more_than_15",
    "_apply_operation",
    " _apply_subset",
    "_apply_scale",
    "encode_format"
]

class Query:
    """
    A class used to handle query generation

    Attributes
    ----------
    coverage: str = None
        Coverage the user wishes to query. Defaults to None if no coverage
        was provided.

    query_type: str = None
        Type of query to perform. Defaults to None if not provided.

    return_val: str = "$c"
        Return value of the query. By default, it is set to the iterator 
        of the coverage, denoted by '$c'.

    params: List[Params] = None
        A list of parameters and their corresponding values to apply to 
        the query. By default, this list is set to None as if no parameters
        are passed, no parameters are assumed.

    return_type: str = None
        Specifies the type of result the user wants the query to return.
        Defaults to None, allowing the default return type of the query
        specified by Rasdaman to be used.

    Methods
    -------
    __init__(self, coverage: str = None, query_type: str = None, 
            return_val: str = "$c", params: List[Params] = None, 
            return_type: str = None)
        Initializes a Query object with the provided attributes.

    set_coverage(self, coverage: str)
        Sets the coverage attribute to the provided coverage.

    set_return_type(self, return_type: str)
        Sets the return_type attribute to the provided return type.

    set_params(self, params: List[Params])
        Sets the params attribute to the provided list of parameters.

    set_query_type(self, query_type: str)
        Sets the query_type attribute to the provided query type.

    print_query(self) -> str
        Generates and prints the query based on the provided attributes.
    
    __str__(self) -> str
        Returns a string representation of the query.
        
    get_wcps(self) -> str
        Returns the WCPS query string representation of the object.
    """

    def __init__(self, coverage: str = None, query_type: str = None, return_val: str = "$c", 
                 params: List[Params] = None, return_type: str = None):
        """
        Initializes a Query object with the provided attributes.

        Parameters:
        -----------
        coverage : str, optional
            The coverage the user wishes to query. Defaults to None.
        query_type : str, optional
            Type of query to perform. Defaults to None.
        return_val : str, optional
            Return value of the query. Defaults to '$c'.
        params : List[Params], optional
            A list of parameters and their corresponding values to apply to 
            the query. Defaults to None.
        return_type : str, optional
            Specifies the type of result the user wants the query to return.
            Defaults to None.
        """

        self.coverage = coverage if coverage in allCoverages else None
        self.query_type = query_type if query_type in queryTypes else None
        self.return_val = return_val
        self.params = params
        self.return_type = return_type if return_type in returnTypes else None


    def set_coverage(self, coverage: str):
        """
        Sets the coverage attribute to the provided coverage.

        Parameters:
        -----------
        coverage : str
            The coverage to set.
        """

        if coverage not in allCoverages:
            raise ValueError("Error. Please select a valid coverage")
        self.coverage = coverage


    def set_return_type(self, return_type: str):
        """
        Sets the return_type attribute to the provided return type.

        Parameters:
        -----------
        return_type : str
            The return type to set.
        """

        if return_type not in returnTypes:
            raise ValueError("Error. Please select a valid return type")
        self.return_type = return_type


    def set_params(self, params: List[Params]):
        """
        Sets the params attribute to the provided list of parameters.

        Parameters:
        -----------
        params : List[Params]
            List of parameters to set.
        """

        self.params = params


    def set_query_type(self, query_type: str):
        """
        Sets the query_type attribute to the provided query type.

        Parameters:
        -----------
        query_type : str
            The query type to set.
        """
        
        if query_type not in queryTypes:
            valid_query_types = '\n'.join(queryTypes)
            raise ValueError(f"Error: Please select a valid query type from the following options:\n{valid_query_types}")
        self.query_type = query_type


    def print_query(self) -> str:

        """
        Generates and prints the query based on the provided attributes.
        """
        query = str(self)
        print(query)


    def __str__(self) -> str:
        """
        Returns a string representation of the query.

        Returns:
        --------
        str
        A string representation of the query.
        """
        query = ""
        query_prefixes = ['diagram>>', 'image>>']
        if self.params is not None:
            params_string = ", ".join([param.get_all_params() for param in self.params])
        else:
            params_string = ""

        if self.query_type in (queryTypes[2], queryTypes[4]):
            query += query_prefixes[0]
            if self.return_type is None:
                self.return_type = "text/csv"

        elif self.query_type == queryTypes[3]:
            query += query_prefixes[1]
            if self.return_type is None:
                self.return_type = "image/png"

        if self.coverage is not None:
            query += "for " + self.return_val + " in ( " + self.coverage + " )"

        else:
            raise ValueError("Error. Invalid coverage was specified")

        return_text = "\n return "

        if self.query_type == "most_basic_query":
            return_text += "1"

        elif self.query_type == "selecting_single_value":
            return_text += self.return_val + f"[{params_string}]"

        elif self.query_type in ("transform_3d_to_1d_subset", "transform_3d_to_2d_subset"):
            return_text += f'encode(\n{self.return_val}[{params_string}]\n, "{self.return_type}")'

        elif self.query_type == "celsius_to_kelvin":
            return_text += f'encode(\n{self.return_val}[{params_string}]\n+273.15\n, "{self.return_type}")'

        elif self.query_type in ("min", "max", "avg"):
            return_text += f'\n{self.query_type}({self.return_val}[{params_string}])'

        elif self.query_type == "when_temp_more_than_15":
            return_text += f'count(\n{self.return_val}[{params_string}]\n> 15)'

        else:
            raise ValueError("Error. Unsupported query type")
    
        query += return_text
        return query

    def get_wcps(self) -> str:
        """
        Returns the WCPS query string representation of the object.

        Returns
        -------
        str
            The WCPS query string representation.
        """

        return str(self)

    def _apply_operation(self, op) -> str:
        op_type = op.op_type

        if op_type == 'apply_operation':
            query = self._apply_custom_operation(op)
        elif op_type == 'apply_subset':
            query = self._apply_subset(op.kwargs['slices'])
        elif op_type == 'apply_scale':
            query = self._apply_scale(op.kwargs['scales'])
        elif op_type == 'encode_format':
            query = self.encode_format(self.return_query)
        else:
            raise ValueError("Unsupported operation type")

        return query

    def _apply_subset(self, selection: dict = None) -> str:
        axis_labels = self._info.keys()

        subset_expr = []
        for axis, value in selection.items():
            if axis not in axis_labels:
                raise ValueError(f"Invalid axis name: {axis}, possible axes are: {axis_labels}")

            if isinstance(value, (int, float)):
                subset_expr.append(f"{axis}({value})")
            elif isinstance(value, str) or (isinstance(value, tuple) and all(isinstance(s, str) for s in value)):
                if isinstance(value, tuple):
                    lo, hi = value
                    value = f'"{lo}":"{hi}"'
                elif isinstance(value, str):
                    value = f'"{value}"'
                subset_expr.append(f'{axis}({value})')
            elif isinstance(value, tuple):
                lo, hi = value
                subset_expr.append(f"{axis}({lo}:{hi})")
            else:
                raise ValueError(f"Invalid selection type for axis {axis}: {type(value)}")

        subset_query = f"{self.covExpr}[{', '.join(subset_expr)}]"
        self.covExpr = subset_query
        return subset_query


    def _apply_scale(self, scales: dict = None) -> str:
        axis_labels = self._info.keys()

        scale_expr = []
        for axis, factor in scales.items():
            if axis not in axis_labels:
                raise ValueError(f"Invalid axis name: {axis}, possible axes are: {axis_labels}")

            if isinstance(factor, (str)):
                scale_expr.append(f"{axis}(\"{factor}\")")
            elif isinstance(factor, (tuple)):
                lo, hi = factor
                scale_expr.append(f"{axis}({lo}:{hi})")
            elif isinstance(factor, (int, float)):
                scale_expr.append(f"{axis}({factor})")
            else:
                raise ValueError(f"Invalid factor type for axis {axis}: {type(factor)}")

        scale_query = f"scale({self.covExpr}, {{ {', '.join(scale_expr)} }})"
        self.covExpr = scale_query
        return scale_query

    def encode_format(self, query: str) -> str:
        if self.encode is not None:
            return f"encode({query}, \"{self.encode}\")"
            
        return query

