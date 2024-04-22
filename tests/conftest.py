# ##############################################################################
#  (c) Crown copyright Met Office. All rights reserved.
#  For further details please refer to the file COPYRIGHT
#  which you should have received as part of this distribution
# ##############################################################################

'''This file is read by pytest and provides common fixtures.
'''

from unittest import mock

import pytest

from fab.newtools import Categories, Compiler, ToolBox


# This avoids pylint warnings about Redefining names from outer scope
@pytest.fixture(name="mock_c_compiler")
def fixture_mock_c_compiler():
    '''Provides a mock C-compiler.'''
    mock_compiler = Compiler("mock_c_compiler", "mock_exec",
                             Categories.C_COMPILER)
    mock_compiler.run = mock.Mock()
    mock_compiler._version = "1.2.3"
    return mock_compiler


@pytest.fixture(name="mock_fortran_compiler")
def fixture_mock_fortran_compiler():
    '''Provides a mock C-compiler.'''
    mock_compiler = Compiler("mock_fortran_compiler", "mock_exec",
                             Categories.FORTRAN_COMPILER)
    mock_compiler.run = mock.Mock()
    mock_compiler._version = "1.2.3"
    return mock_compiler


@pytest.fixture(name="tool_box")
def fixture_tool_box(mock_c_compiler, mock_fortran_compiler):
    '''Provides a tool box with a mock Fortran and a mock C compiler.'''
    tool_box = ToolBox()
    tool_box.add_tool(mock_c_compiler)
    tool_box.add_tool(mock_fortran_compiler)
    return tool_box