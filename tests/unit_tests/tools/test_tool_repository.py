##############################################################################
# (c) Crown copyright Met Office. All rights reserved.
# For further details please refer to the file COPYRIGHT
# which you should have received as part of this distribution
##############################################################################

'''This module tests the ToolRepository.
'''

import pytest


from fab.tools import Category, Gcc, Gfortran, Ifort, Linker, ToolRepository


def test_tool_repository_get_singleton_new():
    '''Tests the singleton behaviour.'''
    ToolRepository._singleton = None
    tr1 = ToolRepository()
    tr2 = ToolRepository()
    assert tr1 == tr2
    ToolRepository._singleton = None
    tr3 = ToolRepository()
    assert tr1 is not tr3


def test_tool_repository_constructor():
    '''Tests the ToolRepository constructor.'''
    tr = ToolRepository()
    assert Category.C_COMPILER in tr
    assert Category.FORTRAN_COMPILER in tr


def test_tool_repository_get_tool():
    '''Tests get_tool.'''
    tr = ToolRepository()
    gfortran = tr.get_tool(Category.FORTRAN_COMPILER, "gfortran")
    assert isinstance(gfortran, Gfortran)

    ifort = tr.get_tool(Category.FORTRAN_COMPILER, "ifort")
    assert isinstance(ifort, Ifort)


def test_tool_repository_get_tool_error():
    '''Tests error handling during tet_tool.'''
    tr = ToolRepository()
    with pytest.raises(KeyError) as err:
        tr.get_tool("unknown-category", "something")
    assert "Unknown category 'unknown-category'" in str(err.value)

    with pytest.raises(KeyError) as err:
        tr.get_tool(Category.C_COMPILER, "something")
    assert ("Unknown tool 'something' in category 'C_COMPILER'"
            in str(err.value))


def test_tool_repository_get_default():
    '''Tests get_default.'''
    tr = ToolRepository()
    gfortran = tr.get_default(Category.FORTRAN_COMPILER)
    assert isinstance(gfortran, Gfortran)

    gcc_linker = tr.get_default(Category.LINKER)
    assert isinstance(gcc_linker, Linker)
    assert gcc_linker.name == "linker-gcc"

    gcc = tr.get_default(Category.C_COMPILER)
    assert isinstance(gcc, Gcc)


def test_tool_repository_get_default_error():
    '''Tests error handling in get_default.'''
    tr = ToolRepository()
    with pytest.raises(RuntimeError) as err:
        tr.get_default("unknown-category")
    assert "Invalid category type 'str'." in str(err.value)


def test_tool_repository_default_compiler_suite():
    '''Tests the setting of default suite for compiler and linker.'''
    tr = ToolRepository()
    tr.set_default_compiler_suite("gnu")
    for cat in [Category.C_COMPILER, Category.FORTRAN_COMPILER,
                Category.LINKER]:
        def_tool = tr.get_default(cat)
        assert def_tool.suite == "gnu"

    tr.set_default_compiler_suite("intel-classic")
    for cat in [Category.C_COMPILER, Category.FORTRAN_COMPILER,
                Category.LINKER]:
        def_tool = tr.get_default(cat)
        assert def_tool.suite == "intel-classic"
    with pytest.raises(RuntimeError) as err:
        tr.set_default_compiler_suite("does-not-exist")
    assert ("Cannot find 'FORTRAN_COMPILER' in the suite 'does-not-exist'"
            in str(err.value))
