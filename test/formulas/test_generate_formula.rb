# typed: true
# frozen_string_literal: true

# This file was generated by Brewtap. DO NOT EDIT.
class TestGenerateFormula < Formula
  desc "Tool to release scripts, binaries, and executables to github"
  homepage "https://github.com/m-dzianishchyts/test-generate-formula"
  url "https://github.com/m-dzianishchyts/test-generate-formula/archive/refs/tags/v0.1.0.tar.gz"
  version "1.1.1"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"
  license "MIT"

  depends_on "bash" => :build
  depends_on "gcc"

  def install
    bin.install "src/secure-browser-kiosk.sh" => "secure-browser-kiosk"
    ohai "Installed successfully."
  end

  test do
    assert_match("my script output", shell_output("my-script-command"))
    puts "Test passed."
  end

  def caveats
    <<~EOS
      This package requires `something` to be installed.

      Make sure `something` is available in your PATH.
    EOS
  end
end
