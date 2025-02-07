{ self, ... }:
{
  perSystem =
    {
      lib,
      devArgs,
      devLib,
      ...
    }:
    let
      basedir = ../../scripts;
      files = devLib.getPyFiles basedir;
    in
    {
      packages =
        # Map over files to:
        # - Rewrite script shebangs as shebangs pointing to the virtualenv
        # - Strip .py suffixes from attribute names and replace '_' with '-'
        lib.mapAttrs' (
          file_name: _:
          let
            name = devLib.scriptName file_name;
          in
          lib.nameValuePair name (
            devLib.mkPackage {
              inherit basedir file_name;
              buildInputs = [ devArgs.venv ];
              extraHook = ''
                cp -r ${self}/scripts/common $out
              '';
            }
          )
        ) files;
    };
}
