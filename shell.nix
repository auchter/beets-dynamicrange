{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    dr14_tmeter
    python3
  ];

  propagatedBuildInputs = [
    pkgs.beets
  ];
}
