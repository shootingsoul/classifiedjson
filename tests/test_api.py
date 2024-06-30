# SPDX-FileCopyrightText: Coypright © 2024 Shooting Soul Ventures, LLC <jg@shootingsoul.com>
# SPDX-License-Identifier: MIT

from classifiedjson import dump, load


def test_file(tmp_path):
    file_name = tmp_path / "test.json"

    c = '{"abc": 123}'
    with open(file_name, 'w') as outfile:
        dump(c, outfile)

    with open(file_name, 'r') as file:
        d = load(file)

    assert c == d
