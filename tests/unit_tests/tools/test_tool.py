##############################################################################
# (c) Crown copyright Met Office. All rights reserved.
# For further details please refer to the file COPYRIGHT
# which you should have received as part of this distribution
##############################################################################

'''Tests the tool class.
'''


import logging
from unittest import mock

import pytest

from fab.newtools import Categories, Tool, VendorTool


def test_tool_constructor():
    '''Test the constructor.'''
    tool = Tool("gnu", "gfortran", Categories.FORTRAN_COMPILER)
    assert str(tool) == "Tool - gnu: gfortran"
    assert tool.exec_name == "gfortran"
    assert tool.name == "gnu"
    assert tool.category == Categories.FORTRAN_COMPILER
    assert isinstance(tool.logger, logging.Logger)
    assert tool.is_compiler

    linker = Tool("gnu", "gfortran", Categories.LINKER)
    assert str(linker) == "Tool - gnu: gfortran"
    assert linker.exec_name == "gfortran"
    assert linker.name == "gnu"
    assert linker.category == Categories.LINKER
    assert isinstance(linker.logger, logging.Logger)
    assert not linker.is_compiler


def test_tool_is_available():
    '''Test that is_available works as expected.'''
    tool = Tool("gfortran", "gfortran", Categories.FORTRAN_COMPILER)
    with mock.patch.object(tool, "check_available", return_value=True):
        assert tool.is_available
    # Test the getter and setter
    tool.is_available = False
    assert not tool.is_available
    assert tool.is_compiler


class TestToolRun():
    '''Test the run method of Tool.'''

    def test_no_error_no_args(self,):
        '''Test usage of `run` without any errors when no additional
        command line argument is provided.'''
        tool = Tool("gnu", "gfortran", Categories.FORTRAN_COMPILER)
        mock_result = mock.Mock(returncode=0, return_value=123)
        mock_result.stdout.decode = mock.Mock(return_value="123")

        with mock.patch('fab.newtools.tool.subprocess.run',
                        return_value=mock_result):
            assert tool.run(capture_output=True) == "123"
            assert tool.run(capture_output=False) == ""

    def test_no_error_with_single_args(self):
        '''Test usage of `run` without any errors when a single
        command line argument is provided as string.'''
        tool = Tool("gnu", "gfortran", Categories.FORTRAN_COMPILER)
        mock_result = mock.Mock(returncode=0)
        with mock.patch('fab.newtools.tool.subprocess.run',
                        return_value=mock_result):
            tool.run("a")

    def test_no_error_with_multiple_args(self):
        '''Test usage of `run` without any errors when more than
        one command line argument is provided as a list.'''
        tool = Tool("gnu", "gfortran", Categories.FORTRAN_COMPILER)
        mock_result = mock.Mock(returncode=0)
        with mock.patch('fab.newtools.tool.subprocess.run',
                        return_value=mock_result):
            tool.run(["a", "b"])

    def test_error(self):
        '''Tests the error handling of `run`. '''
        tool = Tool("gnu", "gfortran", Categories.FORTRAN_COMPILER)
        result = mock.Mock(returncode=1)
        mocked_error_message = 'mocked error message'
        result.stderr.decode = mock.Mock(return_value=mocked_error_message)
        with mock.patch('fab.newtools.tool.subprocess.run',
                        return_value=result):
            with pytest.raises(RuntimeError) as err:
                tool.run()
            assert mocked_error_message in str(err.value)
            assert "Command failed with return code 1" in str(err.value)


def test_vendor_tool():
    '''Test the constructor.'''
    tool = VendorTool("gnu", "gfortran", "gnu", Categories.FORTRAN_COMPILER)
    assert str(tool) == "VendorTool - gnu: gfortran"
    assert tool.exec_name == "gfortran"
    assert tool.name == "gnu"
    assert tool.vendor == "gnu"
    assert tool.category == Categories.FORTRAN_COMPILER
    assert isinstance(tool.logger, logging.Logger)