import os
import sys
import yaml
import requests
from collections import OrderedDict
from typing import Optional, Tuple
from importlib.util import spec_from_file_location, module_from_spec
from streamlit import sidebar


def load_yaml(filepath: str) -> dict:
    """
    Loads a YAML file.

    Can be used as stand-alone script by providing a command-line argument:
        python load_yaml.py --filepath /file/path/to/filename.yaml
        python load_yaml.py --filepath http://example.com/path/to/filename.yaml

    Args:
        filepath (str): The absolute path to the YAML file or a URL to the YAML file.

    Returns:
        dict: The contents of the YAML file as a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If there is an error while loading the YAML file.
    """
    if filepath.startswith('http://') or filepath.startswith('https://'):
        try:
            response = requests.get(filepath)
            response.raise_for_status()  # Raises a HTTPError if the response status is 4xx, 5xx
            yaml_data = yaml.safe_load(response.text)
        except (requests.RequestException, yaml.YAMLError) as e:
            raise Exception(f'Error loading YAML from `{filepath}`. \n {str(e)}')
        else:
            return yaml_data
    else:
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"No such file or directory: '{filepath}'")

        with open(filepath, 'r') as file_descriptor:
            try:
                yaml_data = yaml.safe_load(file_descriptor)
            except yaml.YAMLError as msg:
                raise yaml.YAMLError(f'File `{filepath}` loading error. \n {msg}')
            else:
                return yaml_data


def get_available_activities(activities_filepath: str) -> OrderedDict:
    """
    Retrieves available activities from a yaml file. These activities can be used to
    create a multi-page app using Streamlit. 

    Args:
        activities_filepath (str): The absolute path to the yaml file containing the activites (Pages).

    Returns:
        OrderedDict: An ordered dictionary of services if any are available. 
                     The dictionary is ordered based on the order of activities in the `yaml` file.
                     Each key-value pair corresponds to a service name and its associated information.
                     Returns None if the `yaml` file does not contain any activities.
    Raises:
        FileNotFoundError: If the `activities_filepath` does not exist.
    """
    if not os.path.isfile(activities_filepath):
        raise FileNotFoundError(f"No such file or directory: '{activities_filepath}'")

    available_services = load_yaml(filepath=os.path.abspath(activities_filepath))

    if available_services:
        services_dict = OrderedDict({service['name']: service for service in available_services})
        return services_dict

    return None



def _script_as_module(module_filepath: str, activities_dirpath: str) -> bool:
    """
    Loads a Python script as a module, registers it, and makes it available for the package path.
    This function is particularly useful for populating services in a Streamlit app.

    Args:
        module_filepath (str): The file path to the Python script that needs to be loaded as a module.
        activities_dirpath (str): The directory path where the activities(pages) resides.

    Returns:
        bool: True if the module was loaded successfully; otherwise, False.

    Raises:
        TypeError: If `module_filepath` or `activities_dirpath` are not strings.
        NotADirectoryError: If `activities_dirpath` is not a directory.
        FileNotFoundError: If `module_filepath` does not exist.
    """
    if not isinstance(activities_dirpath, str):
        raise TypeError(f"`activities_dirpath` must be a string, not {type(activities_dirpath).__name__}")
    if not isinstance(module_filepath, str):
        raise TypeError(f"`module_filepath` must be a string, not {type(module_filepath).__name__}")
    if not os.path.isdir(activities_dirpath):
        raise NotADirectoryError(f"No such directory: '{activities_dirpath}'")

    abs_module_filepath = os.path.join(activities_dirpath, module_filepath)

    if not os.path.isfile(abs_module_filepath):
        raise FileNotFoundError(f"No such file: '{abs_module_filepath}'")

    module_name = os.path.basename(abs_module_filepath).replace('.py', '')

    spec = spec_from_file_location(name=module_name, location=abs_module_filepath, submodule_search_locations=[activities_dirpath])

    if spec:
        try:
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
            sys.modules[module_name] = module
            return True
        except Exception as e:
            print(f"Failed to load module {module_name}: {e}")
            return False

    return False


def build_activities_menu(
    activities_dict: OrderedDict[str, dict], 
    label: str, 
    key: str, 
    activities_dirpath: str, 
    disabled: bool = False
) -> Tuple[Optional[str], OrderedDict[str, dict]]:
    """
    Builds an interactive activities menu using Streamlit's sidebar selectbox.

    Args:
        activities_dict (OrderedDict[str, dict]): An ordered dictionary of activities. Each key-value pair corresponds to a 
                                                  service name and its associated information.
        label (str): The label to display above the select box.
        key (str): A unique identifier for the select box widget.
        activities_dirpath (str): The directory path where the service resides.
        disabled (bool, optional): Whether the select box is disabled. Defaults to False.

    Returns:
        Tuple[Optional[str], OrderedDict[str, dict]]: The selected activity name and the dictionary of activities. 
                                                      If no activity is selected, the first item in the tuple is None.

    Raises:
        ValueError: If any activity in activities_dict does not have both `name` and `url`
    """
    # Validate that each activity has both 'name' and 'url'
    for task_dict in activities_dict.values():
        if 'name' not in task_dict or 'url' not in task_dict:
            raise ValueError("Each activity dict must have both 'name' and 'url'")

    activity_names = [(task_dict['name'], task_dict['url']) for task_dict in activities_dict.values()]

    selection_tuple = sidebar.selectbox(
        label=label,
        index=0,
        options=activity_names,
        format_func=lambda x: x[0],
        key=key,
        disabled=disabled
    )

    if selection_tuple is not None:
        selected_activity, module_filepath = selection_tuple
        _script_as_module(module_filepath=module_filepath, activities_dirpath=activities_dirpath)

    return (selected_activity if selection_tuple else None), activities_dict