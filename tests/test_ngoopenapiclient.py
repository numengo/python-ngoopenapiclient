#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ngoopenapiclient` package."""
from click.testing import CliRunner

from ngoopenapiclient.cli import main

# PROTECTED REGION ID(ngoopenapiclient.tests.test_ngoopenapiclient) ENABLED START

def test_ngoopenapiclient():
    from ngoopenapiclient import API
    base_url = 'https://petstore.swagger.io/v2'
    api = API(base_url)
    pet = api.pet.get_pet_by_id(1)
    print(repr(pet))

    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.output == 'Hello World!\n'
    assert result.exit_code == 0


if __name__ == '__main__':
    # to run test file standalone
    test_ngoopenapiclient()

# PROTECTED REGION END
