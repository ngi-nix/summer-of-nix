let
  pkgs = import <nixpkgs> { };
  export = pkgs.writeShellScriptBin "extract-project-data-from-nlnet" ''
    ${pkgs.lib.getExe python} ${./process.py}
  '';
  python = pkgs.python3.withPackages (
    ps: with ps; [
      pandas
      pandas-stubs
      pygithub
      python-dotenv
    ]
  );
in
pkgs.mkShellNoCC {
  packages = with pkgs; [
    jaq
    python
    export
  ];
}
