from unittest.mock import patch

import pytest

from brewtap.app import App


@patch('brewtap.app.SKIP_COMMIT', True)
@patch('brewtap.app.HOMEBREW_TAP', '123')
@patch('woodchips.get')
@patch('brewtap.git.Git.setup')
@patch('brewtap.git.Git.add')
@patch('brewtap.git.Git.commit')
@patch('brewtap.git.Git.push')
@patch('brewtap.utils.Utils.write_file')
@patch('brewtap.formula.Formula.generate_formula_data')
@patch('brewtap.checksum.Checksum.get_checksum', return_value=('123', 'mock-repo'))
@patch('brewtap.app.App.download_archive')
@patch('brewtap.utils.Utils.make_github_get_request')
@patch('brewtap.app.App.check_required_env_variables')
def test_run_github_action_skip_commit(
    mock_check_env_variables,
    mock_make_github_get_request,
    mock_download_archive,
    mock_get_checksum,
    mock_generate_formula,
    mock_write_file,
    mock_push_formula,
    mock_commit_formula,
    mock_add_formula,
    mock_setup_git,
    mock_logger,
):
    App.run_github_action()

    # TODO: Assert these `called_with` eventually
    mock_logger.assert_called()
    mock_check_env_variables.assert_called_once()
    assert mock_make_github_get_request.call_count == 2
    mock_download_archive.call_count == 2
    mock_get_checksum.call_count == 2
    mock_generate_formula.assert_called_once()
    mock_write_file.call_count == 2
    mock_setup_git.assert_called_once()
    mock_add_formula.assert_called_once()
    mock_commit_formula.assert_called_once()
    mock_push_formula.assert_not_called()


@patch('brewtap.app.HOMEBREW_TAP', '123')
@patch('brewtap.checksum.Checksum.upload_checksum_file')
@patch('woodchips.get')
@patch('brewtap.git.Git.setup')
@patch('brewtap.git.Git.add')
@patch('brewtap.git.Git.commit')
@patch('brewtap.git.Git.push')
@patch('brewtap.utils.Utils.write_file')
@patch('brewtap.formula.Formula.generate_formula_data')
@patch('brewtap.checksum.Checksum.get_checksum', return_value=('123', 'mock-repo'))
@patch('brewtap.app.App.download_archive')
@patch('brewtap.utils.Utils.make_github_get_request')
@patch('brewtap.app.App.check_required_env_variables')
def test_run_github_action(
    mock_check_env_variables,
    mock_make_github_get_request,
    mock_download_archive,
    mock_get_checksum,
    mock_generate_formula,
    mock_write_file,
    mock_push_formula,
    mock_commit_formula,
    mock_add_formula,
    mock_setup_git,
    mock_logger,
    mock_upload_checksum_file,
):
    App.run_github_action()

    # TODO: Assert these `called_with` eventually
    mock_logger.assert_called()
    mock_check_env_variables.assert_called_once()
    assert mock_make_github_get_request.call_count == 2
    mock_download_archive.call_count == 2
    mock_get_checksum.call_count == 2
    mock_generate_formula.assert_called_once()
    mock_write_file.call_count == 2
    mock_setup_git.assert_called_once()
    mock_add_formula.assert_called_once()
    mock_commit_formula.assert_called_once()
    mock_push_formula.assert_called_once()


@patch('brewtap.app.HOMEBREW_TAP', '123')
@patch('brewtap.app.UPDATE_README_TABLE', True)
@patch('brewtap.readme_updater.ReadmeUpdater.update_readme')
@patch('brewtap.checksum.Checksum.upload_checksum_file')
@patch('woodchips.get')
@patch('brewtap.git.Git.setup')
@patch('brewtap.git.Git.add')
@patch('brewtap.git.Git.commit')
@patch('brewtap.git.Git.push')
@patch('brewtap.utils.Utils.write_file')
@patch('brewtap.formula.Formula.generate_formula_data')
@patch('brewtap.checksum.Checksum.get_checksum', return_value=('123', 'mock-repo'))
@patch('brewtap.app.App.download_archive')
@patch('brewtap.utils.Utils.make_github_get_request')
@patch('brewtap.app.App.check_required_env_variables')
def test_run_github_action_update_readme(
    mock_check_env_variables,
    mock_make_github_get_request,
    mock_download_archive,
    mock_get_checksum,
    mock_generate_formula,
    mock_write_file,
    mock_push_formula,
    mock_commit_formula,
    mock_add_formula,
    mock_setup_git,
    mock_logger,
    mock_upload_checksum_file,
    mock_update_readme,
):
    App.run_github_action()

    # TODO: Assert these `called_with` eventually
    mock_logger.assert_called()
    mock_check_env_variables.assert_called_once()
    assert mock_make_github_get_request.call_count == 2
    mock_download_archive.call_count == 2
    mock_get_checksum.call_count == 2
    mock_generate_formula.assert_called_once()
    mock_write_file.call_count == 2
    mock_setup_git.assert_called_once()
    mock_add_formula.assert_called_once()
    mock_commit_formula.assert_called_once()
    mock_push_formula.assert_called_once()
    mock_update_readme.assert_called_once()


@patch('brewtap.app.HOMEBREW_TAP', '123')
@patch('brewtap.app.TARGET_DARWIN_AMD64', True)
@patch('brewtap.app.TARGET_DARWIN_ARM64', True)
@patch('brewtap.app.TARGET_LINUX_AMD64', True)
@patch('brewtap.app.TARGET_LINUX_ARM64', True)
@patch('brewtap.checksum.Checksum.upload_checksum_file')
@patch('woodchips.get')
@patch('brewtap.git.Git.setup')
@patch('brewtap.git.Git.add')
@patch('brewtap.git.Git.commit')
@patch('brewtap.git.Git.push')
@patch('brewtap.utils.Utils.write_file')
@patch('brewtap.formula.Formula.generate_formula_data')
@patch('brewtap.checksum.Checksum.get_checksum', return_value=('123', 'mock-repo'))
@patch('brewtap.app.App.download_archive')
@patch('brewtap.utils.Utils.make_github_get_request')
@patch('brewtap.app.App.check_required_env_variables')
def test_run_github_action_target_matrix(
    mock_check_env_variables,
    mock_make_github_get_request,
    mock_download_archive,
    mock_get_checksum,
    mock_generate_formula,
    mock_write_file,
    mock_push_formula,
    mock_commit_formula,
    mock_add_formula,
    mock_setup_git,
    mock_logger,
    mock_upload_checksum_file,
):
    """Tests that we append checksum URLs to the list when the user passes matrix targets."""
    App.run_github_action()

    # TODO: Assert these `called_with` eventually
    mock_logger.assert_called()
    mock_check_env_variables.assert_called_once()
    assert mock_make_github_get_request.call_count == 2
    mock_download_archive.call_count == 2
    mock_get_checksum.call_count == 2
    mock_generate_formula.assert_called_once()
    mock_write_file.call_count == 2
    mock_setup_git.assert_called_once()
    mock_add_formula.assert_called_once()
    mock_commit_formula.assert_called_once()
    mock_push_formula.assert_called_once()


@patch('woodchips.Logger')
def test_setup_logger(mock_logger):
    App.setup_logger()

    mock_logger.assert_called_once()


@patch('brewtap.app.GITHUB_TOKEN', '123')
@patch('brewtap.app.HOMEBREW_OWNER', 'm-dzianishchyts')
@patch('brewtap.app.HOMEBREW_TAP', 'homebrew-formulas')
@patch('brewtap.app.INSTALL', 'bin.install "src/my-script.sh" => "my-script"')
@patch('sys.exit')
def test_check_required_env_variables(mock_system_exit):
    App.check_required_env_variables()

    mock_system_exit.assert_not_called()


@patch('sys.exit')
def test_check_required_env_variables_missing_env_variable(mock_system_exit):
    with pytest.raises(SystemExit) as error:
        App.check_required_env_variables()
        mock_system_exit.assert_called_once()

    assert (
        str(error.value)
        == 'You must provide all necessary environment variables. Please reference the Brewtap documentation.'
    )


@patch('brewtap.utils.Utils.write_file')
@patch('brewtap.utils.Utils.make_github_get_request')
def test_download_public_archive(mock_make_github_get_request, mock_write_file):
    url = 'https://github.com/repos/m-dzianishchyts/brewtap/archive/refs/tags/v0.1.0.tar.gz'
    App.download_archive(url, True)

    mock_make_github_get_request.assert_called_once_with(url=url, stream=True)
    mock_write_file.assert_called_once()  # TODO: Assert `called_with` here instead


@patch('brewtap.utils.Utils.write_file')
@patch('brewtap.utils.Utils.make_github_get_request')
def test_download_private_archive(mock_make_github_get_request, mock_write_file):
    url = 'https://api.github.com/repos/m-dzianishchyts/brewtap/tarball/v0.1.0'
    App.download_archive(url, False)

    mock_make_github_get_request.assert_called_once_with(url=url, stream=False)
    mock_write_file.assert_called_once()  # TODO: Assert `called_with` here instead
