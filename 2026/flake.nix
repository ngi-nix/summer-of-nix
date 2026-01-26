{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    {
      self,
      nixpkgs,
    }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      fonts = pkgs.makeFontsConf {
        fontDirectories = [
          pkgs.dejavu_fonts
        ];
      };

      mkReport =
        report:
        pkgs.stdenv.mkDerivation {
          name = report;
          src = ./.;
          buildInputs = with pkgs; [
            pandoc
            texlive.combined.scheme-small
          ];
          phases = [
            "unpackPhase"
            "buildPhase"
          ];
          buildPhase = ''
            export FONTCONFIG_FILE=${fonts}
            mkdir -p $out
            pandoc $src/${report}.md \
                -f gfm \
                --pdf-engine=xelatex \
                -o $out/${report}.pdf
          '';
        };
    in
    {
      packages.${system} = {
        repository-report-2024-02-2026-01 = mkReport "repository-report-2024-02-2026-01";
      };
    };
}
