{
  description = "Mathematics for AI: slides and manim clips";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { nixpkgs, ... }:
    let
      pkgs = nixpkgs.legacyPackages.x86_64-linux;
      # manim 0.22.0 in nixpkgs fails one of its own tests during the build.
      # The library itself works, so skip the test phase rather than pin an
      # older nixpkgs.
      manim = pkgs.manim.overridePythonAttrs (_: {
        doCheck = false;
        doInstallCheck = false;
      });
    in {
      packages.x86_64-linux.manim = manim;
      devShells.x86_64-linux.default = pkgs.mkShell {
        packages = [ manim pkgs.nodejs pkgs.ffmpeg pkgs.chromium ];
      };
    };
}
