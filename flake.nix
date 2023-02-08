{
  description = "A report built with Pandoc, XeLaTex and a custom font";

  inputs = {
      nixpkgs.url = "nixpkgs";
      styles.url = github:citation-style-language/styles;
      styles.flake = false;
  };
  outputs = { self, nixpkgs, styles }: {

    packages.x86_64-linux.report = (
        let
            system = "x86_64-linux";
            pkgs = nixpkgs.legacyPackages.${system};
            fonts = pkgs.makeFontsConf { fontDirectories = [ pkgs.dejavu_fonts ]; };
        in
          pkgs.stdenv.mkDerivation {
              name = "XelatexReport";
              src = ./.;
              buildInputs = with pkgs; [
                  pandoc
                  haskellPackages.pandoc-crossref
                  texlive.combined.scheme-small
                  gnome.librsvg # for conversion from svg to pdf
                  graphviz
                  plantuml
                  nodePackages.vega-cli
                  # the following is waiting on https://github.com/NixOS/nixpkgs/pull/162434
                  (nodePackages.vega-lite.override {
                      postInstall = ''
                          cd node_modules
                          for dep in ${nodePackages.vega-cli}/lib/node_modules/vega-cli/node_modules/*; do
                            if [[ ! -d ''${dep##*/} ]]; then
                              ln -s "${nodePackages.vega-cli}/lib/node_modules/vega-cli/node_modules/''${dep##*/}"
                            fi
                          done
                        '';})
                  nodePackages.mermaid-cli
                  svgbob
                  ];
              phases = ["unpackPhase" "buildPhase"];
              buildPhase = ''
              export FONTCONFIG_FILE=${fonts}
              mkdir -p $out
              pandoc $src/README.md \
                  --filter pandoc-crossref \
                  -M date="`date "+%B %e, %Y"`" \
                  --csl ${styles}/chicago-fullnote-bibliography.csl \
                  --citeproc \
                  --pdf-engine=xelatex \
                  -o $out/README.pdf
              '';
          }
        );

    defaultPackage.x86_64-linux = self.packages.x86_64-linux.report;
  };
}
