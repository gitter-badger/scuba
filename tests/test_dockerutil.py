 # coding=utf-8
from __future__ import print_function

from nose.tools import *
from .utils import *
from unittest import TestCase
try:
    from unittest import mock
except ImportError:
    import mock

import subprocess

import scuba.dockerutil as uut

class TestDockerutil(TestCase):
    def test_get_image_command_success(self):
        '''get_image_command works'''
        assert_true(uut.get_image_command('debian:8.2'))

    def test_get_image_command_bad_image(self):
        '''get_image_command raises an exception for a bad image name'''
        assert_raises(uut.DockerError, uut.get_image_command, 'nosuchimageZZZZZZZZ')

    def test_get_image_no_docker(self):
        '''get_image_command raises an exception if docker is not installed'''

        real_Popen = subprocess.Popen
        def mocked_popen(popen_args, *args, **kw):
            assert_equal(popen_args[0], 'docker')
            popen_args[0] = 'dockerZZZZ'
            return real_Popen(popen_args, *args, **kw)

        with mock.patch('subprocess.Popen', side_effect=mocked_popen) as popen_mock:
            assert_raises(uut.DockerError, uut.get_image_command, 'n/a')



    def test_make_vol_opt_no_opts(self):
        assert_equal(
                uut.make_vol_opt('/hostdir', '/contdir'),
                '--volume=/hostdir:/contdir'
                )

    def test_make_vol_opt_one_opt(self):
        assert_equal(
                uut.make_vol_opt('/hostdir', '/contdir', 'ro'),
                '--volume=/hostdir:/contdir:ro'
                )

    def test_make_vol_opt_multi_opts(self):
        assert_equal(
                uut.make_vol_opt('/hostdir', '/contdir', ['ro', 'z']),
                '--volume=/hostdir:/contdir:ro,z'
                )