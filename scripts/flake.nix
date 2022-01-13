
{
  # inspired by: https://serokell.io/blog/practical-nix-flakes#packaging-existing-applications
  description = "Plotting script for Summer of Nix";
  inputs.nixpkgs.url = "nixpkgs";
  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" ];
      forAllSystems = f: nixpkgs.lib.genAttrs supportedSystems (system: f system);
      nixpkgsFor = forAllSystems (system: import nixpkgs {
        inherit system;
        config = {allowBroken = true;};
        overlays = [ self.overlay ];
      });
    in
    {
      overlay = (final: prev: {
        plotter = final.haskellPackages.callCabal2nix "plotter" ./. {};
      });
      packages = forAllSystems (system: {
         plotter = nixpkgsFor.${system}.plotter;
      });
      defaultPackage = forAllSystems (system: self.packages.${system}.plotter);
      checks = self.packages;
      devShell = forAllSystems (system:
        let haskellPackages = nixpkgsFor.${system}.haskellPackages;
            nodePackages = nixpkgsFor.${system}.nodePackages;
        in haskellPackages.shellFor {
          packages = p: [self.packages.${system}.plotter];
          withHoogle = true;
          buildInputs = with haskellPackages; [
            haskell-language-server
            ghcid
            cabal-install
            nodePackages.vega-cli
            (nodePackages.vega-lite.override {
                postInstall = ''
                    cd node_modules
                    for dep in ${nodePackages.vega-cli}/lib/node_modules/vega-cli/node_modules/*; do
                      if [[ ! -d ''${dep##*/} ]]; then
                        ln -s "${nodePackages.vega-cli}/lib/node_modules/vega-cli/node_modules/''${dep##*/}"
                      fi
                    done
                  '';})
          ];
        # Change the prompt to show that you are in a devShell
        shellHook = "export PS1='\\e[1;34mdev > \\e[0m'";
        });
  };
}
