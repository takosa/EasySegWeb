import os
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import io
import base64

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = False

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("image_selector"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "image_selector",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("image_selector", path=build_dir)

# This function was created using the following link.
# https://github.com/jrieke/streamlit-image-select/blob/aecb446f90f2cc55d8ed11a47da740a04acd8015/streamlit_image_select/__init__.py
# The URL of the license is below.
# https://github.com/jrieke/streamlit-image-select/blob/aecb446f90f2cc55d8ed11a47da740a04acd8015/LICENSE
@st.cache_data
def _encode_file(file):
    img = Image.open(file)
    img.thumbnail((256, 256))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    encoded = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/jpeg;base64, {encoded}"

# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def image_selector(input_files, key=None):
    """Create a new instance of "image_selector".

    Parameters
    ----------
    input_files: list
        List of input files. It should be able to open with PIL.Image.open.
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    list
        The indexes of selected image files. If no image is selected, return [].
        (This is the value passed to `Streamlit.setComponentValue` on the
        frontend.)

    """
    images = []
    for file in input_files:
        if hasattr(file, "name"):
            name = file.name
        elif isinstance(file, str):
            name = os.path.basename(file)
        else:
            raise ValueError("Invalid input_files.")
        images.append({"name": name, "src": _encode_file(file)})
            
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func(images=images, key=key, default=[])

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run image_selector/__init__.py`
if not _RELEASE:

    st.subheader("Component with constant args")

    # Create an instance of our component with a constant `name` arg, and
    # print its output value.
    input_files = ['images/1.jpg', 'images/2.jpg']
    selected = image_selector(input_files=input_files)
    st.markdown(f"You've selected {[input_files[i] for i in selected]}!")

    st.markdown("---")
    st.subheader("Component with variable args")

    # Create a second instance of our component whose `name` arg will vary
    # based on a text_input widget.
    #
    # We use the special "key" argument to assign a fixed identity to this
    # component instance. By default, when a component's arguments change,
    # it is considered a new instance and will be re-mounted on the frontend
    # and lose its current state. In this case, we want to vary the component's
    # "name" argument without having it get recreated.
    input_files = st.file_uploader("Choose files", type=["jpg", "png"], accept_multiple_files=True)
    selected = image_selector(input_files=input_files, key="foo")
    st.markdown(f"You've selected {[input_files[i].name for i in selected]}!")
