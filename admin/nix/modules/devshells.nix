{
  perSystem =
    {
      pkgs,
      lib,
      devArgs,
      self',
      ...
    }:
    {
      devShells = {
        # This devShell uses uv2nix to construct a virtual environment purely
        # from Nix, using the same dependency specification as the application.
        #
        # The notable difference is that we also apply another overlay here
        # enabling editable mode (https://setuptools.pypa.io/en/latest/userguide/development_mode.html).
        #
        # This means that any changes done to your local files do not require a rebuild.
        #
        # Note: Editable package support is still unstable and subject to change.
        default =
          let
            # Create an overlay enabling editable mode for all local dependencies.
            editableOverlay = devArgs.workspace.mkEditablePyprojectOverlay {
              root = "$REPO_ROOT";
            };

            # Override previous set with our overrideable overlay.
            editablePythonSet = devArgs.pythonSet.overrideScope (
              lib.composeManyExtensions [
                editableOverlay
              ]
            );

            # Build virtual environment, with local packages being editable.
            #
            # Enable all optional dependencies for development.
            virtualenv = editablePythonSet.mkVirtualEnv "scripts-dev-env" devArgs.workspace.deps.all;
          in
          pkgs.mkShell {
            buildInputs = [
              pkgs.uv
              self'.packages.sync-issues
              virtualenv
            ];

            env = {
              # Don't create venv using uv
              UV_NO_SYNC = "1";

              # Force uv to use Python interpreter from venv
              UV_PYTHON = "${virtualenv}/bin/python";

              # Prevent uv from downloading managed Python's
              UV_PYTHON_DOWNLOADS = "never";
            };

            shellHook = ''
              # Undo dependency propagation by nixpkgs.
              unset PYTHONPATH

              # Get repository root using git. This is expanded at runtime by the editable `.pth` machinery.
              export REPO_ROOT=$(git rev-parse --show-toplevel)
            '';
          };
      };
    };
}
