#!/usr/bin/env bash

# ENVIRONMENTS: development (dev.) and production / deployment (prod.).
# - Ref.: 'https://andypickup.com/developing-in-python-with-dev-containers-part-1-setup-f1aeb89cbfed'.
# - Ref.: 'https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-r'.
# - Ref.: 'https://stackoverflow.com/questions/65909781/is-there-a-way-to-debug-the-postcreatecommand-in-vscode-devcontainers'.
pip install --requirement './rsrcs/requirements/requirements_production.txt' --requirement './rsrcs/requirements/requirements_development.txt' # To install requirements in development stage (DEFAULT).
# pip install --requirement './rsrcs/requirements/requirements_production.txt' # To install requirements in production stage.
