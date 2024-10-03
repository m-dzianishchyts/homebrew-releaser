<div align="center">

# Fork of Homebrew Releaser

Release scripts, binaries, and executables directly to Homebrew via GitHub Actions.

[![Build](https://github.com/Justintime50/homebrew-releaser/workflows/build/badge.svg)](https://github.com/Justintime50/homebrew-releaser/actions)
[![Coverage Status](https://coveralls.io/repos/github/Justintime50/homebrew-releaser/badge.svg?branch=main)](https://coveralls.io/github/Justintime50/homebrew-releaser?branch=main)
[![Version](https://img.shields.io/github/v/tag/justintime50/homebrew-releaser)](https://github.com/justintime50/homebrew-releaser/releases)
[![Licence](https://img.shields.io/github/license/Justintime50/homebrew-releaser)](LICENSE)

<img src="https://raw.githubusercontent.com/justintime50/assets/main/src/homebrew-releaser/showcase.png" alt="Showcase">

</div>

Homebrew Releaser allows you to release scripts, binaries, and executables directly to a personal Homebrew tap via a GitHub Action.

When you cut a new release when using this GitHub Action, it will clone your repo and clone your Homebrew tap on CI, build the new formula Ruby file, create a `checksum.txt` file and upload it to your release containing the checksum(s) of your scripts/binaries, and then push the new formula to your Homebrew Tap. If you do not specify a `target` to use, the workflow will use the autogenerated tar archive from GitHub when you created a release, otherwise you can tell Homebrew Releaser which OS and arch pairs you have binaries for. See the accompanying target details below for the URL patterns to follow.

## Usage

**Notes:**

- Shell scripts distributed via Homebrew Releaser **must be executable** and contain a proper shebang to work.
- Homebrew Releaser **will always use the latest release** of a GitHub project. Git release tags must follow semantic versioning for Homebrew to properly infer the installation instructions (eg: `v1.2.0` or `0.3.0`, etc).
- The Homebrew formula filename will match the github repo name.
- It is **highly** recommended to enable debug mode and skip the commit on the first run through to ensure you have configured your workflow correctly and that the generated formula looks the way you want.
- Homebrew Releaser is **not** compatible with monorepos.
- Every precaution will be made to ensure that major releases of this action remain compatible (every `0.x` release of this action rebuilds and packages the `v1` action as a convenience to users). If you value stability over "getting new features for free", it's highly recommended to pin a specific version or commit hash of this action when using it (eg: `v0.16.0`)

### GitHub Actions YAML

After you release a project on GitHub, Homebrew Releaser can publish that release to a personal Homebrew tap by updating the project description, version, tar archive url, license, checksum, installation and testing command, and any other required info so you don't have to. You can check the [Homebrew documentation on taps](https://docs.brew.sh/How-to-Create-and-Maintain-a-Tap) and the [formula cookbook](https://docs.brew.sh/Formula-Cookbook) for more details on setting up a Homebrew formula or tap.

```yml
# .github/workflows/release.yml
# Start Homebrew Releaser when a new GitHub release is created
on:
  release:
    types: [published]

jobs:
  homebrew-releaser:
    runs-on: ubuntu-latest
    name: homebrew-releaser
    steps:
      - name: Release my project to my Homebrew tap
        uses: m-dzianishchyts/homebrew-releaser@v1
        with:
          # The name of the homebrew tap to publish your formula to as it appears on GitHub.
          # Required - strings
          homebrew_owner: organisation
          homebrew_tap: homebrew-formulas

          # The name of the folder in your homebrew tap where formula will be committed to.
          # Default is shown - string
          formula_folder: formula

          # The Personal Access Token (saved as a repo secret) that has `repo` permissions for the repo running the action AND Homebrew tap you want to release to.
          # Required - string
          github_token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}

          # Git author info used to commit to the homebrew tap.
          # Defaults are shown - strings
          commit_owner: homebrew-releaser
          commit_email: homebrew-releaser@example.com

          # Custom dependencies in case other formulas are needed to build the current one.
          # Optional - multiline string
          depends_on: |
            "bash" => :build
            "gcc"

          # Custom install command for your formula.
          # Required - string
          install: 'bin.install "src/my-script.sh" => "my-script"'

          # Custom test command for your formula so you can run `brew test`.
          # Optional - string
          test: 'assert_match("my script output", shell_output("my-script-command"))'

          # Allows you to set a custom download strategy. Note that you'll need
          # to implement the strategy and add it to your tap repository.
          # Example: https://docs.brew.sh/Formula-Cookbook#specifying-the-download-strategy-explicitly
          # Optional - string
          download_strategy: CurlDownloadStrategy

          # Allows you to add a custom require_relative at the top of the formula template.
          # Optional - string
          custom_require: custom_download_strategy

          # Allows you to add custom includes inside the formula class, before dependencies and install blocks.
          # Optional - string
          formula_includes: 'include Language::Python::Virtualenv'

          # Override the automatically detected version of a formula with an explicit value.
          # This option should only be used if Homebrew cannot automatically detect the version when generating
          # the Homebrew formula. Including this when not necessary could lead to uninstallable formula that may 
          # not pass `brew audit` due to mismatched or redundant version strings
          # Optional - string
          version: '1.2.0'
          
          # Adds default URL and checksum target.
          # Optional - string
          target: 'release.tar.gz'

          # Adds URL and checksum targets for different OS and architecture pairs.
          # Optional - boolean | string
          target_darwin_amd64: true
          target_darwin_arm64: false
          target_linux_amd64: true
          target_linux_arm64: false

          # Update your homebrew tap's README with a table of all projects in the tap.
          # This is done by pulling the information from all your formula.rb files - eg:
          #
          # | Project                                    | Description  | Install                  |
          # | ------------------------------------------ | ------------ | ------------------------ |
          # | [formula_1](https://github.com/user/repo1) | helpful text | `brew install formula_1` |
          # | [formula_2](https://github.com/user/repo2) | helpful text | `brew install formula_2` |
          # | [formula_3](https://github.com/user/repo3) | helpful text | `brew install formula_3` |
          #
          # Place the following in your README or wrap your project's table in these comment tags:
          # <!-- project_table_start -->
          # TABLE HERE
          # <!-- project_table_end -->
          #
          # Finally, mark `update_readme_table` as `true` in your GitHub Action config and we'll do the work of building a custom table for you.
          # Default is `false` - boolean
          update_readme_table: true

          # Skips committing the generated formula to a homebrew tap (useful for local testing).
          # Default is shown - boolean
          skip_commit: false

          # Logs debugging info to console.
          # Default is shown - boolean
          debug: false
```

## Development

```bash
# Get a comprehensive list of development tools
just --list
```

### Run Manually via Docker

Homebrew Releaser does not clean up artifacts after completing since the temporary Docker image on GitHub Actions will be discarded anyway.

**Note:** All environment variables from above must be prepended with `INPUT_` for the local Docker image (eg: `INPUT_SKIP_COMMIT=true`).

```bash
docker compose up -d --build
```
