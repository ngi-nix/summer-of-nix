{
  description = "A very basic flake";


  inputs = {
      nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
      };

  outputs = { self, nixpkgs}: {

    packages.x86_64-linux.report = (
        let pkgs = import nixpkgs {system="x86_64-linux";};
            fonts = pkgs.makeFontsConf { fontDirectories = [ pkgs.dejavu_fonts ]; };
            styles = pkgs.fetchFromGitHub {
                owner = "citation-style-language";
                repo = "styles";
                rev = "cd7b72bbef45db2acb6a571a139dd9319f456ccf";
                sha256 = "sha256-ppa0wx00AbR19rA8apzdTOKTHHmSj0jQlWoFQ1oj6Us=";
            };
        in
          pkgs.stdenv.mkDerivation {
              name = "SoNReport";
              src = [
                  ./report.md
                  ./figures/repositories.png
                  ./figures/issues.png
                  ./figures/channels.png
                  ./contributions.md
                  ];
              buildInputs = with pkgs; [
                pandoc
                texlive.combined.scheme-small
                haskellPackages.pandoc-crossref
                ];
              phases = ["unpackPhase" "buildPhase"];
              unpackPhase = ''
              for srcFile in $src; do
                cp $srcFile $(stripHash $srcFile)
              done
              '';
              buildPhase = ''
              export FONTCONFIG_FILE=${fonts}
              mkdir -p $out
              sed -i -e '/{{contributions}}/{r contributions.md' -e 'd}' report.md
              pandoc report.md --filter pandoc-crossref --csl ${styles}/chicago-fullnote-bibliography.csl --citeproc --pdf-engine=xelatex -o $out/report.pdf
              '';
          }
        );

    defaultPackage.x86_64-linux = self.packages.x86_64-linux.report;

  };
}
