{
  self ? import ./. { },
}:
let
  inherit (self)
    lib
    pkgs
    packages
    workspace
    pythonSet
    ;

  editableOverlay = workspace.mkEditablePyprojectOverlay { root = "$REPO_ROOT"; };
  editablePythonSet = pythonSet.overrideScope (lib.composeManyExtensions [ editableOverlay ]);

  # Enable all optional dependencies for development
  venv = editablePythonSet.mkVirtualEnv "scripts-development-env" workspace.deps.all;

  scripts = lib.mapAttrsToList (name: value: value) packages;
  scriptsList = lib.pipe packages [
    (lib.mapAttrsToList (name: value: "- ${name}"))
    (lib.concatStringsSep "\n")
  ];
in
pkgs.mkShellNoCC {
  packages = [
    pkgs.uv
    venv
    scripts
  ];

  env = {
    # Don't create venv using uv
    UV_NO_SYNC = "1";

    # Force uv to use Python interpreter from venv
    UV_PYTHON = "${venv}/bin/python";

    # Prevent uv from downloading managed Python's
    UV_PYTHON_DOWNLOADS = "never";
  };

  shellHook = ''
    # Undo dependency propagation by nixpkgs.
    # See https://pyproject-nix.github.io/pyproject.nix/build.html
    unset PYTHONPATH

    # Get repository root using git. This is expanded at runtime by the editable `.pth` machinery.
    export REPO_ROOT=$(git rev-parse --show-toplevel)

    echo "
    Available scripts:
    ${scriptsList}
    "
  '';
}
