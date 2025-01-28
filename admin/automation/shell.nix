{
  sources ? import ./npins,
  system ? builtins.currentSystem,
  pkgs ? import sources.nixpkgs { inherit system; },
}:
let
  python = pkgs.python3.withPackages (
    ps: with ps; [
      pandas
      pandas-stubs
      pygithub # TODO: remove
      pydantic
      githubkit
    ]
  );
  # Commands
  export = pkgs.writeShellScriptBin "extract-project-data-from-nlnet" ''
    ${pkgs.lib.getExe python} ${./process.py}
  '';
  sync = pkgs.writeShellScriptBin "sync-projects" ''
    ${pkgs.lib.getExe python} ${./sync.py}
  '';
in
pkgs.mkShellNoCC {
  packages = [
    export
    python
    sync
  ];
}
