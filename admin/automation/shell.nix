{
  sources ? import ./npins,
  system ? builtins.currentSystem,
  pkgs ? import sources.nixpkgs { inherit system; },
}:
let
  src = ./.;
  python = pkgs.python3.withPackages (
    ps: with ps; [
      pandas
      pandas-stubs
      pydantic
      githubkit
    ]
  );
  export-project-data = pkgs.writeShellScriptBin "extract-project-data" ''
    ${pkgs.lib.getExe python} "${src}/sync/export-project-data.py" "$@"
  '';
  sync-projects = pkgs.writeShellScriptBin "sync-projects" ''
    ${pkgs.lib.getExe python} "${src}/sync/sync-projects.py" "$@"
  '';
in
pkgs.mkShellNoCC {
  packages = [
    export-project-data
    python
    sync-projects
  ];
}
