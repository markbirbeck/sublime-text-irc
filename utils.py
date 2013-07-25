import sublime

def get_setting(key, default=None):

    # Set up the default value:
    #
    ret = default

    # Get the current view:
    #
    view = sublime.active_window().active_view()

    # Assuming we got the current view ok, then we should be able to pick up
    # the key from the settings:
    #
    if view:
        ret = view.settings().get(key, default)

    return ret
