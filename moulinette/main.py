#!/usr/bin/env python
"""Run custom service on different instances.

:arguments:
--name of service package (defaults to 'solve')
name of service module (default set as Service class argument)
-instance aliases (defaults to everything)

:Examples:
view all instances with default viewer:
>>> ./main.py --view

solve instances of aliases (a, b, small) with solver named "greedy"
>>> python main.py greedy/ a b small

:Nota bene:
Non-letter characters in module name are ignored (autocomplete can add '/').
Package name is required before an alias list.
"""
import control
import tools


def main():
    """Import solver based on code name, run it on aliased instances."""
    try:
        options = control.parse()

        for alias in options.aliases:
            options.service(alias)

        options.service.close()
    finally:
        times = tools.Clock.report()
        message = "{key:<20} (x{value[0]:<5}): {value[1]:.3f} s"
        tools.report("Clock", times, message)


if __name__ == "__main__":
    main()
