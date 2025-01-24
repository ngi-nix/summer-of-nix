let
  pkgs = import <nixpkgs> { };
in
pkgs.mkShell {
  packages = with pkgs; [
    jaq
    (python3.withPackages (
      ps: with ps; [
        pandas
        pandas-stubs
        pygithub
        python-dotenv
      ]
    ))
  ];
}
