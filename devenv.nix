{ pkgs, inputs,... }:

{
  # https://devenv.sh/packages/
  packages = with pkgs; [
    pre-commit
  ];

  languages.python = {
    enable = true;
    venv.enable = true;
    poetry.enable = true;
    poetry.activate.enable = true;
    poetry.install.enable = true;
    poetry.install.groups = ["dev"];
    poetry.install.installRootPackage = true;
  };

  dotenv.disableHint = true;

  # https://devenv.sh/scripts/
  # Activate the environment right away
  enterShell = ''
  source .venv/bin/activate
  '';

  # https://devenv.sh/pre-commit-hooks/
  pre-commit.hooks = {
  };
}