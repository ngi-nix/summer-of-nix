{
  lib,
  writeShellScriptBin,
  runCommand,
  ...
}:
rec {
  # Get a list of regular Python files in a directory
  getPyFiles =
    basedir:
    lib.filterAttrs (name: type: type == "regular" && lib.hasSuffix ".py" name) (
      builtins.readDir basedir
    );

  scriptName =
    name:
    lib.pipe name [
      (lib.removeSuffix ".py")
      (lib.replaceStrings [ "_" ] [ "-" ])
    ];

  mkPackage =
    {
      basedir,
      file_name,
      buildInputs ? [ ],
      extraHook ? "",
      ...
    }:
    let
      script = basedir + "/${file_name}";
      name = scriptName file_name;

      # Patch script shebang
      program = runCommand name { inherit buildInputs; } ''
        mkdir -p $out

        cp ${script} $out/${name}
        ${extraHook}

        chmod +x $out/${name}
        patchShebangs $out/${name}
      '';
    in
    writeShellScriptBin name ''
      ${program}/${name} "$@"
    '';

  # Make a script "greet.py" runnable as "nix run .#greet"
  mkApps =
    { basedir, packages, ... }:
    let
      files = getPyFiles basedir;
    in
    lib.mapAttrs' (
      file_name: _:
      let
        name = scriptName file_name;
      in
      lib.nameValuePair name {
        type = "app";
        program = packages.${name};
      }
    ) files;
}
