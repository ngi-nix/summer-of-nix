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
      tqdm
      ijson
      pytest
    ]
  );
  export-project-data = pkgs.writeShellScriptBin "extract-project-data" ''
    ${pkgs.lib.getExe python} "${src}/scripts/export_project_data.py" "$@"
  '';
  sync-projects = pkgs.writeShellScriptBin "sync-projects" ''
    ${pkgs.lib.getExe python} "${src}/scripts/sync_projects.py" "$@"
  '';
in
pkgs.mkShellNoCC {
  packages = [
    export-project-data
    python
    sync-projects
  ];
  shellHook = ''
    ln -s "${sources.ngipkgs}/projects/deliverables.py" scripts/lib/models/deliverables.py
  '';
}
