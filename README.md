# Streamlit Activities Menu
[Demo in the Streamlit community cloud](https://sidebar-selectbox-menu.streamlit.app/)

Builds an interactive activities menu to create a multi-page app using Streamlit's sidebar selectbox, as an alternative to the `pages` implementation. The available activities (pages) are read from a `yaml` file. These activities can be used to create a multi-page app using Streamlit.

It is recommended to add the `app_activities.yaml` at the same level as the main `streamlit_app.py`. Then, an `activities` folder is recommended to exist as a subdirectory where the `streamlit_app.py` is located.

The `app_activities.yaml` follows the following schema:

```yaml
# Services for multipage Streamlit app
-
  name: 'Home Page'
  description: 'Home page'
  url: "home.py"

-
  name: 'Data Overview'
  description: 'Overall data overview'
  url: "overview.py"

- 
  name: 'Data Processing'
  description: 'Processing page'
  url: "processing.py"

# Add as required
```

In the `streamlit_app.py`:

```python
import os
import streamlit as st
from streamlit_activities_menu import get_available_activities, build_activities_menu

# Load the available activities
ACTIVITIES_FILEPATH = st.secrets['PATHS']['ACTIVITIES_FILEPATH']
ACTIVITIES_DIRPATH = st.secrets['PATHS']['ACTIVITIES_DIRPATH']

# Load the `yaml` file with core activities    
core_activities = get_available_activities(
    activities_filepath=os.path.abspath(ACTIVITIES_FILEPATH)        
)

build_activities_menu(
    activities_dict=core_activities, 
    label='**Menu:**', 
    key='activitiesMenu', 
    activities_dirpath=os.path.abspath(ACTIVITIES_DIRPATH),
    disabled=False
    )
```

## Subfolders

The recommended structure of the files within the subdirectory is:

```shell
my_app
|-- streamlit_app.py
|-- app_activities.yaml
|-- activities
|   |-- home.py
|   |-- overview.py
|   |-- processing.py
```

---
## Mantainers

* José M. Beltrán-Abaunza, PhD | Lund University, Department of Physical Geography and Ecosystem Science 