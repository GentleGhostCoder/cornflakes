from cornflakes.common import recursive_update
from cornflakes.decorator.click.helper import get_command_name
from cornflakes.types import Constants


def fill_option_groups(callback, name, *slot_options):
    """Automatically fill option groups for click callback."""
    if hasattr(callback, "name"):
        option_groups_obj = callback.config.OPTION_GROUPS

        command = get_command_name(callback)

        new_option = {
            command: [
                {
                    "name": name,
                    "options": slot_options,
                },
            ]
        }

        recursive_update(option_groups_obj, new_option, merge_lists=True)

        return callback

    new_option = {
        "name": name,
        "options": slot_options,
    }
    if hasattr(callback, Constants.config_option.OPTION_GROUPS):
        getattr(callback, Constants.config_option.OPTION_GROUPS).append(new_option)
        return callback

    setattr(callback, Constants.config_option.OPTION_GROUPS, [new_option])
    return callback
