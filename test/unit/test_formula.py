import inspect
import os
from unittest.mock import patch

from homebrew_releaser.formula import Formula


formula_path = 'test/formulas'

USERNAME = 'Justintime50'
VERSION = '0.1.0'
CHECKSUM = '0' * 64  # `brew audit` wants a 64 character number here, this would be true with real data
INSTALL = 'bin.install "src/secure-browser-kiosk.sh" => "secure-browser-kiosk"'
# Dependencies are purposefully out of order so we can test that they get ordered properly for `brew audit`
DEPENDS_ON = """
"gcc"
"bash" => :build
"""
TEST = 'assert_match("my script output", shell_output("my-script-command"))'
DESCRIPTION = 'Release scripts, binaries, and executables to GitHub'
LICENSE = {'spdx_id': 'MIT'}


def record_formula(formula_path: str, formula_name: str, formula_data: str):
    """Read from an existing formula file or create a new formula file if it's not present.

    Tests using this function will generate a formula into a file (similar to how
    `vcrpy` works for HTTP requests and responses: https://github.com/kevin1024/vcrpy) if it
    does not exist already.

    If formula generation changes, the tests will automatically save those changes to the auto-
    generated formula output in the `formulas` directory. These can then be compared to the expected
    output from before to determine if a change was correct or not.
    """
    full_formula_filename = os.path.join(formula_path, formula_name)

    if os.path.isfile(full_formula_filename):
        with open(full_formula_filename, 'r') as formula_file:
            assert formula_data == formula_file.read()
    else:
        os.makedirs(formula_path, exist_ok=True)
        with open(full_formula_filename, 'w') as formula_file:
            formula_file.write(formula_data)


def test_generate_formula():
    """Tests that we generate the formula content correctly when all parameters are passed
    (except a matrix so that we can test the auto-generate URL/checksum from GitHub).

    NOTE: See docstring in `record_formula` for more details on how recording formulas works.
    """
    formula_filename = f'{inspect.stack()[0][3]}.rb'
    mock_repo_name = formula_filename.replace('_', '-').replace('.rb', '')
    mock_tar_url = f'https://github.com/{USERNAME}/{mock_repo_name}/archive/refs/tags/v0.1.0.tar.gz'

    repository = {
        # We use a badly written description string here on purpose to test our formatting code, this includes:
        # - starting with an article
        # - punctuation
        # - trailing whitespace
        # - extra capitilization
        'description': 'A tool to release... scripts, binaries, and executables to GitHub. ',
        'license': LICENSE,
    }

    formula = Formula.generate_formula_data(
        owner=USERNAME,
        repo_name=mock_repo_name,
        repository=repository,
        checksums=[{
            f'{mock_repo_name}.tar.gz': {
                'checksum': CHECKSUM,
                'url': f'https://github.com/justintime50/{mock_repo_name}/releases/download/{VERSION}/{mock_repo_name}-{VERSION}.tar.gz',  # noqa
            },
        }],
        install=INSTALL,
        tar_url=mock_tar_url,
        depends_on=DEPENDS_ON,
        test=TEST,
    )

    record_formula(formula_path, formula_filename, formula)

    # The following assertions are explicitly listed as the "gold standard" for generic formula generation
    assert '''# typed: true
# frozen_string_literal: true

# This file was generated by Homebrew Releaser. DO NOT EDIT.''' in formula
    assert '''desc "Tool to release scripts, binaries, and executables to github"
  homepage "https://github.com/Justintime50/test-generate-formula"
  url "https://github.com/Justintime50/test-generate-formula/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"
  license "MIT"''' in formula
    assert '''depends_on "bash" => :build
  depends_on "gcc"''' in formula
    assert '''def install
    bin.install "src/secure-browser-kiosk.sh" => "secure-browser-kiosk"
  end''' in formula
    assert '''test do
    assert_match("my script output", shell_output("my-script-command"))
  end'''


def test_generate_formula_no_article_description():
    """Tests that we generate the formula content correctly (when there is no article
    that starts the description field).

    NOTE: See docstring in `record_formula` for more details on how recording formulas works.
    """
    formula_filename = f'{inspect.stack()[0][3]}.rb'
    mock_repo_name = formula_filename.replace('_', '-').replace('.rb', '')
    mock_tar_url = f'https://github.com/{USERNAME}/{mock_repo_name}/archive/refs/tags/v0.1.0.tar.gz'

    repository = {
        # Here we don't start the description off with an article
        'description': DESCRIPTION,
        'license': LICENSE,
    }

    formula = Formula.generate_formula_data(
        owner=USERNAME,
        repo_name=mock_repo_name,
        repository=repository,
        checksums=[{
            f'{mock_repo_name}.tar.gz': {
                'checksum': CHECKSUM,
                'url': f'https://github.com/justintime50/{mock_repo_name}/releases/download/{VERSION}/{mock_repo_name}-{VERSION}.tar.gz',  # noqa
            },
        }],
        install=INSTALL,
        tar_url=mock_tar_url,
        depends_on=None,
        test=None,
    )

    record_formula(formula_path, formula_filename, formula)

    assert 'desc "Release scripts, binaries, and executables to github"' in formula


def test_generate_formula_formula_name_starts_description():
    """Tests that we generate the formula content correctly (when the name of the formula
    starts the description field) - it should get stripped out per `brew audit`.

    NOTE: See docstring in `record_formula` for more details on how recording formulas works.
    """
    formula_filename = f'{inspect.stack()[0][3]}.rb'
    mock_repo_name = formula_filename.replace('_', '-').replace('.rb', '')
    mock_tar_url = f'https://github.com/{USERNAME}/{mock_repo_name}/archive/refs/tags/v0.1.0.tar.gz'

    repository = {
        # Here we don't start the description off with an article
        'description': 'TestGenerateFormulaFormulaNameStartsDescription is a tool',
        'license': LICENSE,
    }

    formula = Formula.generate_formula_data(
        owner=USERNAME,
        repo_name=mock_repo_name,
        repository=repository,
        checksums=[{
            f'{mock_repo_name}.tar.gz': {
                'checksum': CHECKSUM,
                'url': f'https://github.com/justintime50/{mock_repo_name}/releases/download/{VERSION}/{mock_repo_name}-{VERSION}.tar.gz',  # noqa
            },
        }],
        install=INSTALL,
        tar_url=mock_tar_url,
        depends_on=None,
        test=None,
    )

    record_formula(formula_path, formula_filename, formula)

    assert 'desc "Is a tool"' in formula


def test_generate_formula_no_depends_on():
    """Tests that we generate the formula content correctly (when no depends_on given).

    NOTE: See docstring in `record_formula` for more details on how recording formulas works.
    """
    formula_filename = f'{inspect.stack()[0][3]}.rb'
    mock_repo_name = formula_filename.replace('_', '-').replace('.rb', '')
    mock_tar_url = f'https://github.com/{USERNAME}/{mock_repo_name}/archive/refs/tags/v0.1.0.tar.gz'

    repository = {
        'description': DESCRIPTION,
        'license': LICENSE,
    }

    formula = Formula.generate_formula_data(
        owner=USERNAME,
        repo_name=mock_repo_name,
        repository=repository,
        checksums=[{
            f'{mock_repo_name}.tar.gz': {
                'checksum': CHECKSUM,
                'url': f'https://github.com/justintime50/{mock_repo_name}/releases/download/{VERSION}/{mock_repo_name}-{VERSION}.tar.gz',  # noqa
            },
        }],
        install=INSTALL,
        tar_url=mock_tar_url,
        depends_on=None,
        test=TEST,
    )

    record_formula(formula_path, formula_filename, formula)

    assert 'depends_on' not in formula


def test_generate_formula_no_test():
    """Tests that we generate the formula content correctly (when there is no test).

    NOTE: See docstring in `record_formula` for more details on how recording formulas works.
    """
    formula_filename = f'{inspect.stack()[0][3]}.rb'
    mock_repo_name = formula_filename.replace('_', '-').replace('.rb', '')
    mock_tar_url = f'https://github.com/{USERNAME}/{mock_repo_name}/archive/refs/tags/v0.1.0.tar.gz'

    repository = {
        'description': DESCRIPTION,
        'license': LICENSE,
    }

    formula = Formula.generate_formula_data(
        owner=USERNAME,
        repo_name=mock_repo_name,
        repository=repository,
        checksums=[{
            f'{mock_repo_name}.tar.gz': {
                'checksum': CHECKSUM,
                'url': f'https://github.com/justintime50/{mock_repo_name}/releases/download/{VERSION}/{mock_repo_name}-{VERSION}.tar.gz',  # noqa
            },
        }],
        install=INSTALL,
        tar_url=mock_tar_url,
        depends_on=DEPENDS_ON,
        test=None,
    )

    record_formula(formula_path, formula_filename, formula)

    assert 'test do' not in formula


@patch('homebrew_releaser.formula.TARGET_DARWIN_AMD64', True)
@patch('homebrew_releaser.formula.TARGET_DARWIN_ARM64', True)
@patch('homebrew_releaser.formula.TARGET_LINUX_AMD64', True)
@patch('homebrew_releaser.formula.TARGET_LINUX_ARM64', True)
def test_generate_formula_complete_matrix():
    """Tests that we generate the formula content correctly when we provide a complete OS matrix.

    NOTE: See docstring in `record_formula` for more details on how recording formulas works.
    """
    formula_filename = f'{inspect.stack()[0][3]}.rb'
    mock_repo_name = formula_filename.replace('_', '-').replace('.rb', '')
    mock_tar_url = f'https://github.com/{USERNAME}/{mock_repo_name}/archive/refs/tags/v0.1.0.tar.gz'

    repository = {
        'description': DESCRIPTION,
        'license': LICENSE,
    }

    formula = Formula.generate_formula_data(
        owner=USERNAME,
        repo_name=mock_repo_name,
        repository=repository,
        checksums=[
            {
                'test-generate-formula-complete-matrix.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-generate-formula-complete-matrix',  # noqa
                },
            },
            {
                'test-formula-0.1.0-darwin-amd64.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-darwin-amd64.tar.gz',  # noqa
                },
            },
            {
                'test-formula-0.1.0-darwin-arm64.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-darwin-arm64.tar.gz',  # noqa
                },
            },
            {
                'test-formula-0.1.0-linux-amd64.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-linux-amd64.tar.gz',  # noqa
                },
            },
            {
                'test-formula-0.1.0-linux-arm64.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-linux-arm64.tar.gz',  # noqa
                },
            },
        ],
        install=INSTALL,
        tar_url=mock_tar_url,
        depends_on=DEPENDS_ON,
        test=TEST,
    )

    record_formula(formula_path, formula_filename, formula)

    assert formula.count('url') == 5
    assert formula.count('sha256') == 5
    assert 'on_macos' in formula
    assert 'on_intel' in formula
    assert 'on_linux' in formula
    assert 'on_arm' in formula


@patch('homebrew_releaser.formula.TARGET_DARWIN_AMD64', True)
@patch('homebrew_releaser.formula.TARGET_DARWIN_ARM64', True)
def test_generate_formula_darwin_matrix():
    """Tests that we generate the formula content correctly when we provide a Darwin matrix.

    NOTE: See docstring in `record_formula` for more details on how recording formulas works.
    """
    formula_filename = f'{inspect.stack()[0][3]}.rb'
    mock_repo_name = formula_filename.replace('_', '-').replace('.rb', '')
    mock_tar_url = f'https://github.com/{USERNAME}/{mock_repo_name}/archive/refs/tags/v0.1.0.tar.gz'

    repository = {
        'description': 'Release scripts, binaries, and executables to GitHub',
        'license': LICENSE,
    }

    formula = Formula.generate_formula_data(
        owner=USERNAME,
        repo_name=mock_repo_name,
        repository=repository,
        checksums=[
            {
                'test-generate-formula-darwin-matrix.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-generate-formula-darwin-matrix.tar.gz',  # noqa
                },
            },
            {
                'test-formula-0.1.0-darwin-amd64.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-darwin-amd64.tar.gz',  # noqa
                },
            },
            {
                'test-formula-0.1.0-darwin-arm64.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-darwin-arm64.tar.gz',  # noqa
                },
            },
        ],
        install=INSTALL,
        tar_url=mock_tar_url,
        depends_on=None,
        test=None,
    )

    record_formula(formula_path, formula_filename, formula)

    assert 'on_macos' in formula
    assert 'on_intel' in formula
    assert 'on_linux' not in formula
    assert 'on_arm' in formula


@patch('homebrew_releaser.formula.TARGET_LINUX_AMD64', True)
@patch('homebrew_releaser.formula.TARGET_LINUX_ARM64', True)
def test_generate_formula_linux_matrix():
    """Tests that we generate the formula content correctly when we provide a Linux matrix.

    NOTE: See docstring in `record_formula` for more details on how recording formulas works.
    """
    formula_filename = f'{inspect.stack()[0][3]}.rb'
    mock_repo_name = formula_filename.replace('_', '-').replace('.rb', '')
    mock_tar_url = f'https://github.com/{USERNAME}/{mock_repo_name}/archive/refs/tags/v0.1.0.tar.gz'

    repository = {
        'description': 'Release scripts, binaries, and executables to GitHub',
        'license': LICENSE,
    }

    formula = Formula.generate_formula_data(
        owner=USERNAME,
        repo_name=mock_repo_name,
        repository=repository,
        checksums=[
            {
                'test-generate-formula-linux-matrix.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-generate-formula-linux-matrix.tar.gz',  # noqa
                },
            },
            {
                'test-formula-0.1.0-linux-amd64.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-linux-amd64.tar.gz',  # noqa
                },
            },
            {
                'test-formula-0.1.0-linux-arm64.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-linux-arm64.tar.gz',  # noqa
                },
            },
        ],
        install=INSTALL,
        tar_url=mock_tar_url,
        depends_on=None,
        test=None,
    )

    record_formula(formula_path, formula_filename, formula)

    assert 'on_macos' not in formula
    assert 'on_intel' in formula
    assert 'on_linux' in formula
    assert 'on_arm' in formula


@patch('homebrew_releaser.formula.TARGET_DARWIN_ARM64', True)
@patch('homebrew_releaser.formula.TARGET_LINUX_AMD64', True)
def test_one_of_each_matrix():
    """Tests that we generate the formula content correctly when we specify only one arch from each OS.
    This test helps ensure that we properly spaces the `on_` functions correctly when only one is present.

    NOTE: See docstring in `record_formula` for more details on how recording formulas works.
    """
    formula_filename = f'{inspect.stack()[0][3]}.rb'
    mock_repo_name = formula_filename.replace('_', '-').replace('.rb', '')
    mock_tar_url = f'https://github.com/{USERNAME}/{mock_repo_name}/archive/refs/tags/v0.1.0.tar.gz'

    repository = {
        'description': DESCRIPTION,
        'license': LICENSE,
    }

    formula = Formula.generate_formula_data(
        owner=USERNAME,
        repo_name=mock_repo_name,
        repository=repository,
        checksums=[
            {
                f'{mock_repo_name}.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': f'https://github.com/justintime50/{mock_repo_name}/releases/download/{VERSION}/{mock_repo_name}-{VERSION}.tar.gz',  # noqa
                },
            },
            {
                'test-formula-0.1.0-darwin-arm64.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-darwin-arm64.tar.gz',  # noqa
                },
            },
            {
                'test-formula-0.1.0-linux-amd64.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-linux-amd64.tar.gz',  # noqa
                },
            },
        ],
        install=INSTALL,
        tar_url=mock_tar_url,
        depends_on=None,
        test=None,
    )

    record_formula(formula_path, formula_filename, formula)

    assert 'on_macos' in formula
    assert 'on_intel' in formula
    assert 'on_linux' in formula
    assert 'on_arm' in formula


@patch.dict(os.environ, {'INPUT_TARGET_DARWIN_AMD64': 'false'})
@patch.dict(os.environ, {'INPUT_TARGET_DARWIN_ARM64': 'false'})
@patch.dict(os.environ, {'INPUT_TARGET_LINUX_AMD64': 'false'})
@patch.dict(os.environ, {'INPUT_TARGET_LINUX_ARM64': 'false'})
def test_generate_formula_string_false_configs():
    """Tests that we generate the formula content correctly when the user specifies `false` on
    boolean flags because GitHub Actions passes them in as strings...

    NOTE: See docstring in `record_formula` for more details on how recording formulas works.
    """
    formula_filename = f'{inspect.stack()[0][3]}.rb'
    mock_repo_name = formula_filename.replace('_', '-').replace('.rb', '')
    mock_tar_url = f'https://github.com/{USERNAME}/{mock_repo_name}/archive/refs/tags/v0.1.0.tar.gz'

    repository = {
        'description': DESCRIPTION,
        'license': LICENSE,
    }

    formula = Formula.generate_formula_data(
        owner=USERNAME,
        repo_name=mock_repo_name,
        repository=repository,
        checksums=[{
            f'{mock_repo_name}.tar.gz': {
                'checksum': CHECKSUM,
                'url': f'https://github.com/justintime50/{mock_repo_name}/releases/download/{VERSION}/{mock_repo_name}-{VERSION}.tar.gz',  # noqa
            },
        }],
        install=INSTALL,
        tar_url=mock_tar_url,
        depends_on=None,
        test=None,
    )

    record_formula(formula_path, formula_filename, formula)

    assert 'on_macos' not in formula
    assert 'on_intel' not in formula
    assert 'on_linux' not in formula
    assert 'on_arm' not in formula


def test_generate_formula_empty_fields():
    """Tests that we generate the formula content correctly when there are empty fields
    such as the `license` or the `description` - license should not be included, desc should
    be a placeholder.

    NOTE: See docstring in `record_formula` for more details on how recording formulas works.
    """
    formula_filename = f'{inspect.stack()[0][3]}.rb'
    mock_repo_name = formula_filename.replace('_', '-').replace('.rb', '')
    mock_tar_url = f'https://github.com/{USERNAME}/{mock_repo_name}/archive/refs/tags/v0.1.0.tar.gz'

    repository = {}  # purposefully empty to test missing fields

    formula = Formula.generate_formula_data(
        owner=USERNAME,
        repo_name=mock_repo_name,
        repository=repository,
        checksums=[{
            f'{mock_repo_name}.tar.gz': {
                'checksum': CHECKSUM,
                'url': f'https://github.com/justintime50/{mock_repo_name}/releases/download/{VERSION}/{mock_repo_name}-{VERSION}.tar.gz',  # noqa
            },
        }],
        install=INSTALL,
        tar_url=mock_tar_url,
        depends_on=None,
        test=None,
    )

    record_formula(formula_path, formula_filename, formula)

    assert 'desc "NA"' in formula
    assert 'license' not in formula


@patch('homebrew_releaser.formula.TARGET_DARWIN_AMD64', True)
@patch('homebrew_releaser.formula.TARGET_DARWIN_ARM64', True)
@patch('homebrew_releaser.formula.TARGET_LINUX_AMD64', True)
@patch('homebrew_releaser.formula.TARGET_LINUX_ARM64', True)
def test_generate_formula_download_strategy():
    """Tests that we generate the formula content correctly when there a custom download strategy specified.

    NOTE: See docstring in `record_formula` for more details on how recording formulas works.
    """
    formula_filename = f'{inspect.stack()[0][3]}.rb'
    mock_repo_name = formula_filename.replace('_', '-').replace('.rb', '')
    mock_tar_url = f'https://github.com/{USERNAME}/{mock_repo_name}/archive/refs/tags/v0.1.0.tar.gz'

    repository = {
        'description': DESCRIPTION,
        'license': LICENSE,
    }

    formula = Formula.generate_formula_data(
        owner=USERNAME,
        repo_name=mock_repo_name,
        repository=repository,
        checksums=[
            {
                f'{mock_repo_name}.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': f'https://github.com/justintime50/{mock_repo_name}/releases/download/{VERSION}/{mock_repo_name}-{VERSION}.tar.gz',  # noqa
                },
            },
            {
                'test-formula-0.1.0-darwin-amd64.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-darwin-amd64.tar.gz',  # noqa
                },
            },
            {
                'test-formula-0.1.0-darwin-arm64.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-darwin-arm64.tar.gz',  # noqa
                },
            },
            {
                'test-formula-0.1.0-linux-amd64.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-linux-amd64.tar.gz',  # noqa
                },
            },
            {
                'test-formula-0.1.0-linux-arm64.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-linux-arm64.tar.gz',  # noqa
                },
            },
        ],
        install=INSTALL,
        tar_url=mock_tar_url,
        depends_on=None,
        test=None,
        download_strategy='CustomDownloadStrategy',
        custom_require='../formula_imports/mock_download_strategy',
    )

    record_formula(formula_path, formula_filename, formula)

    assert formula.count(', using: CustomDownloadStrategy') == 5
    assert 'require_relative "../formula_imports/mock_download_strategy"' in formula


def test_generate_formula_override_version():
    """Tests that we generate the formula content correctly (when the version is overridden).

    NOTE: See docstring in `record_formula` for more details on how recording formulas works.
    """
    formula_filename = f'{inspect.stack()[0][3]}.rb'
    mock_repo_name = formula_filename.replace('_', '-').replace('.rb', '')
    mock_tar_url = f'https://github.com/{USERNAME}/{mock_repo_name}/archive/refs/tags/v0.1.0.tar.gz'

    repository = {
        'description': DESCRIPTION,
        'license': LICENSE,
    }

    formula = Formula.generate_formula_data(
        owner=USERNAME,
        repo_name=mock_repo_name,
        repository=repository,
        checksums=[{
            f'{mock_repo_name}.tar.gz': {
                'checksum': CHECKSUM,
                'url': f'https://github.com/justintime50/{mock_repo_name}/releases/download/{VERSION}/{mock_repo_name}-{VERSION}.tar.gz',  # noqa
            },
        }],
        install=INSTALL,
        tar_url=mock_tar_url,
        version='9.8.7',
    )

    record_formula(formula_path, formula_filename, formula)

    assert '9.8.7' in formula
