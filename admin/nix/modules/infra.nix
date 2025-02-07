{ inputs, ... }:
{
  perSystem =
    {
      pkgs,
      lib,
      self',
      ...
    }:
    let
      workspace = inputs.uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ../../.; };
      overlay = workspace.mkPyprojectOverlay { sourcePreference = "wheel"; };
      pythonSet =
        (pkgs.callPackage inputs.pyproject-nix.build.packages {
          python = pkgs.python312;
        }).overrideScope
          (
            lib.composeManyExtensions [
              inputs.pyproject-build-systems.overlays.default
              overlay
            ]
          );
      venv = pythonSet.mkVirtualEnv "scripts-default-env" workspace.deps.default;
    in
    {
      # Custom library. Contains helper functions, builders, ...
      legacyPackages.lib = pkgs.callPackage ../lib.nix { };

      # Flake argument for accessing the custom library more easily:
      # `perSystem = { devLib, ... }:`
      _module.args.devLib = self'.legacyPackages.lib;

      _module.args.devArgs = {
        inherit venv workspace pythonSet;
      };
    };
}
