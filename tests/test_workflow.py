import unittest
import sys
import os
import tempfile
import shutil

from applicake2.apps.examples.cp import CpApp
from applicake2.apps.examples.echowrapped import EchoWrapped
from applicake2.apps.flow.branch import Branch
from applicake2.apps.flow.collate import Collate
from applicake2.apps.flow.merge import Merge
from applicake2.apps.flow.split import Split
from applicake2.apps.flow.jobid import Jobid


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tdir = tempfile.mkdtemp(dir=".")
        os.chdir(cls.tdir)
        with open("input.ini", "w") as f:
            f.write("""
COMMENT = comm,ent
LOG_STORAGE = memory
LOG_LEVEL = DEBUG
FILE = test.txt""")
        open("test.txt", "w").write("""TESTTEXT""")

    def test1_jobid(self):
        sys.argv = ['--INPUT', 'input.ini', '--OUTPUT', 'jobid.ini']
        Jobid.main()
        assert os.path.exists('jobid.ini')
        assert 'JOB_ID' in open('jobid.ini').read()

    def test2_branch(self):
        sys.argv = ['--INPUT', 'jobid.ini', '--BRANCH', 'forcp.ini','--BRANCH', 'forecho.ini',]
        Branch.main()

        assert os.path.exists('forcp.ini')
        assert os.path.exists('forecho.ini')

    def test3_cp(self):
        sys.argv = ['--INPUT', 'forcp.ini', '--OUTPUT', 'cp.ini']
        CpApp.main()
        assert os.path.exists('cp.ini')
        assert 'COPY' in open('cp.ini').read()

    def test4_split(self):
        sys.argv = ['--INPUT', 'forecho.ini', '--SPLIT', 'split.ini', '--SPLIT_KEY', 'COMMENT']
        Split.main()

        assert os.path.exists('split.ini_0')
        assert 'comm' in open('split.ini_0').read()
        assert not 'ent' in open('split.ini_0').read()

        assert os.path.exists('split.ini_1')
        assert not 'comm' in open('split.ini_1').read()
        assert 'ent' in open('split.ini_1').read()


    def test5_echo(self):
        sys.argv = ['--INPUT', 'split.ini_0', '--OUTPUT', 'echo.ini_0']
        EchoWrapped.main()

        assert os.path.exists('echo.ini_0')

        sys.argv = ['--INPUT', 'split.ini_1', '--OUTPUT', 'echo.ini_1']
        EchoWrapped.main()

        os.path.exists('echo.ini_1')

    def test6_merge(self):
        sys.argv = ['--MERGE', 'echo.ini', '--MERGED', 'merged.ini']
        Merge.main()
        assert os.path.exists('merged.ini_0')

    def test7_collate(self):
        sys.argv = ['--COLLATE', 'cp.ini', '--COLLATE', 'merged.ini_0','--OUTPUT','collate.ini']
        Collate.main()
        assert os.path.exists('collate.ini')

        print open('collate.ini').read()
        assert 'comm, ent' in open('collate.ini').read()
        assert 'COPY' in open('collate.ini').read()

    @classmethod
    def tearDownClass(cls):
        os.chdir("..")
        shutil.rmtree(cls.tdir)