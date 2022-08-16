{
    inputs = {
        nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
        utils.url = "github:numtide/flake-utils";
    };

    outputs = {self, nixpkgs, utils}:
    let out = system:
    let pkgs = nixpkgs.legacyPackages."${system}";
    in {

        devShell = pkgs.mkShell {
            buildInputs = with pkgs; [
              self.defaultPackage."${system}"
            ];
        };

        defaultPackage = pkgs.python3Packages.buildPythonApplication rec {
          pname = "beets-dynamicrange";
          version = "unstable-2022-08-15";

          src = ./.;

          nativeBuildInputs = [ pkgs.beets ];
          propagatedBuildInputs = [ pkgs.dr14_tmeter ];

          postPatch = ''
            substituteInPlace beetsplug/dynamicrange.py \
              --replace dr14_tmeter ${pkgs.dr14_tmeter}/bin/dr14_tmeter
          '';

          doCheck = false;

          meta = with pkgs.lib; {
            homepage = "https://github.com/auchter/beets-dynamicrange";
            description = "Calculate and store dynamic range of music for beets";
            license = licenses.mit;
            maintainers = with maintainers; [ auchter ];
            platforms = platforms.linux;
          };
        };

        defaultApp = utils.lib.mkApp {
            drv = self.defaultPackage."${system}";
        };

    }; in with utils.lib; eachSystem defaultSystems out;

}
