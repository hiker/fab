# ##############################################################################
#  (c) Crown copyright Met Office. All rights reserved.
#  For further details please refer to the file COPYRIGHT
#  which you should have received as part of this distribution
# ##############################################################################
import subprocess
from pathlib import Path

from fab.build_config import BuildConfig
from fab.constants import EXECUTABLES
from fab.steps.analyse import Analyse
from fab.steps.c_pragma_injector import CPragmaInjector
from fab.steps.compile_c import CompileC
from fab.steps.find_source_files import FindSourceFiles
from fab.steps.link import LinkExe
from fab.steps.preprocess import c_preprocessor

PROJECT_SOURCE = Path(__file__).parent / 'project-source'


def test_MinimalC(tmp_path):

    # build
    config = BuildConfig(
        fab_workspace=tmp_path,
        project_label='foo',
        source_root=PROJECT_SOURCE,
        multiprocessing=False,

        steps=[
            FindSourceFiles(),

            CPragmaInjector(),
            c_preprocessor(),
            Analyse(root_symbol='main'),
            CompileC(compiler='gcc', common_flags=['-c', '-std=c99']),

            LinkExe(linker='gcc'),
        ],
    )
    config.run()
    assert len(config._artefact_store[EXECUTABLES]) == 1

    # run
    command = [str(config._artefact_store[EXECUTABLES][0])]
    res = subprocess.run(command, capture_output=True)
    output = res.stdout.decode()
    assert output == 'Hello world!'
