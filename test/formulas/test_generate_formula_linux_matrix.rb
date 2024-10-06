# typed: true
# frozen_string_literal: true

# This file was generated by Brewtap. DO NOT EDIT.
class TestGenerateFormulaLinuxMatrix < Formula
  desc "Release scripts, binaries, and executables to github"
  homepage "https://github.com/m-dzianishchyts/test-generate-formula-linux-matrix"
  url "https://github.com/m-dzianishchyts/test-generate-formula-linux-matrix/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"
  license "MIT"

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
    ohai "Installed successfully."
  end
end
