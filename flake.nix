{
  inputs = {
    nixpkgs.url = "nixpkgs";
  };
  outputs = {
    self,
    nixpkgs,
  }: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
    fonts = pkgs.makeFontsConf {fontDirectories = [pkgs.dejavu_fonts];};
  in {
    packages.${system}.default = (
      pkgs.stdenv.mkDerivation {
        name = "XelatexReport";
        src = ./.;
        buildInputs = with pkgs; [
          pandoc
          texlive.combined.scheme-small
        ];
        phases = ["unpackPhase" "buildPhase"];
        buildPhase = ''
          export FONTCONFIG_FILE=${fonts}
          mkdir -p $out
          pandoc $src/README.md \
              -f gfm \
              --template template.latex \
              --pdf-engine=xelatex \
              -M date="`date "+%B %e, %Y"`" \
              -o $out/README.pdf
        '';
      }
    );
  };
}
