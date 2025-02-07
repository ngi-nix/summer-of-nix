{
  perSystem =
    {
      devLib,
      self',
      ...
    }:
    let
      basedir = ../../scripts;
    in
    {
      # Make a script "greet.py" runnable as "nix run .#greet"
      apps = devLib.mkApps {
        inherit basedir;
        inherit (self') packages;
      };
    };
}
