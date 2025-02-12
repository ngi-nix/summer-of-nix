{
  sources ? import ./npins,
  system ? builtins.currentSystem,
  pkgs ? import sources.nixpkgs { inherit system; },
}:
let
  devLib = pkgs.callPackage ./nix/lib.nix { };

  inherit (pkgs) lib;
  inherit (devLib) getPyFiles scriptName mkPackage;

  pyproject-nix = import sources.pyproject-nix { inherit lib; };
  uv2nix = import sources.uv2nix { inherit pyproject-nix lib; };
  pyproject-build-systems = import sources.pyproject-build-systems {
    inherit pyproject-nix uv2nix lib;
  };

  workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };
  overlay = workspace.mkPyprojectOverlay { sourcePreference = "wheel"; };
  python = pkgs.callPackage pyproject-nix.build.packages { python = pkgs.python312; };
  pythonSet = python.overrideScope (
    lib.composeManyExtensions [
      pyproject-build-systems
      overlay
    ]
  );
  venv = pythonSet.mkVirtualEnv "scripts-default-env" workspace.deps.default;

  scriptsDir = ./scripts;
  files = getPyFiles scriptsDir;
in
rec {
  inherit
    lib
    pkgs
    sources
    system
    workspace
    pythonSet
    ;

  packages =
    # Map over files to:
    # - Rewrite script shebangs as shebangs pointing to the virtualenv
    # - Strip .py suffixes from attribute names and replace '_' with '-'
    lib.mapAttrs' (
      file_name: _:
      lib.nameValuePair (scriptName file_name) (mkPackage {
        inherit scriptsDir file_name;
        buildInputs = [ venv ];
        extraHook = ''
          cp -r ${./.}/scripts/common $out
        '';
      })
    ) files;
}
