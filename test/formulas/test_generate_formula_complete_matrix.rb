# typed: true
# frozen_string_literal: true

# This file was generated by Brewtap. DO NOT EDIT.
class TestGenerateFormulaCompleteMatrix < Formula
  desc "Release scripts, binaries, and executables to github"
  homepage "https://github.com/m-dzianishchyts/test-generate-formula-complete-matrix"
  url "https://github.com/m-dzianishchyts/test-generate-formula-complete-matrix/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"
  license "MIT"

  depends_on "bash" => :build
  depends_on "gcc"

  on_macos do
    on_intel do
      url "https://github.com/m-dzianishchyts/test-formula/releases/download/0.1.0/test-formula-0.1.0-darwin-amd64.tar.gz"
      sha256 "0000000000000000000000000000000000000000000000000000000000000000"
    end

    on_arm do
      url "https://github.com/m-dzianishchyts/test-formula/releases/download/0.1.0/test-formula-0.1.0-darwin-arm64.tar.gz"
      sha256 "0000000000000000000000000000000000000000000000000000000000000000"
    end
  end

  on_linux do
    on_intel do
      url "https://github.com/m-dzianishchyts/test-formula/releases/download/0.1.0/test-formula-0.1.0-linux-amd64.tar.gz"
      sha256 "0000000000000000000000000000000000000000000000000000000000000000"
    end

    on_arm do
      url "https://github.com/m-dzianishchyts/test-formula/releases/download/0.1.0/test-formula-0.1.0-linux-arm64.tar.gz"
      sha256 "0000000000000000000000000000000000000000000000000000000000000000"
    end
  end

  def install
    bin.install "src/secure-browser-kiosk.sh" => "secure-browser-kiosk"
  end

  test do
    assert_match("my script output", shell_output("my-script-command"))
  end
end
