{
  pkgs,
  sources,
  ...
}@args:
{
  packages = null;
  nixos = {
    modules = null;
    examples = {
      base = null;
    };
    tests = null;
  };
}
