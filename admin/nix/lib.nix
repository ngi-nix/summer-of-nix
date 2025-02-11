{
  lib,
  writeShellScriptBin,
  runCommand,
  ...
}:
rec {
  # Get a list of regular Python files in a directory
  getPyFiles =
    scriptsDir:
    lib.filterAttrs (name: type: type == "regular" && lib.hasSuffix ".py" name) (
      builtins.readDir scriptsDir
    );

  scriptName =
    name:
    lib.pipe name [
      (lib.removeSuffix ".py")
      (lib.replaceStrings [ "_" ] [ "-" ])
    ];

  mkPackage =
    {
      scriptsDir,
      file_name,
      buildInputs ? [ ],
      extraHook ? "",
      ...
    }:
    let
      script = scriptsDir + "/${file_name}";
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
}
