{
  description = "A LLM backend development flake powered by unstructured and langchain";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = {nixpkgs, ...}: let
    system = "x86_64-linux";
    #       ↑ Swap it for your system if needed
    #       "aarch64-linux" / "x86_64-darwin" / "aarch64-darwin"
    pkgs = nixpkgs.legacyPackages.${system};
  in {
    devShells.${system}.default = pkgs.mkShell {
      packages = [
        (pkgs.python311.withPackages (python-pkgs: [
          python-pkgs.pip # VsCode starts
          python-pkgs.jupyter
          python-pkgs.notebook # VsCode ends
          python-pkgs.numpy
          python-pkgs.pandas
          python-pkgs.scipy
          python-pkgs.matplotlib
          python-pkgs.requests
          python-pkgs.langchain-community
          python-pkgs.langchain
          python-pkgs.langchain-text-splitters
          python-pkgs.unstructured
          python-pkgs.wrapt # unstructured[local-inference] starts
          python-pkgs.iso-639
          python-pkgs.emoji
          python-pkgs.pillow-heif
          python-pkgs.magic
          python-pkgs.poppler-qt5
          python-pkgs.pytesseract
          python-pkgs.langdetect # unstructured[local-inference] ends
          python-pkgs.openai
          python-pkgs.pydantic
          python-pkgs.python-dotenv
          python-pkgs.configargparse
          python-pkgs.streamlit
          python-pkgs.lark
          python-pkgs.sentence-transformers
          pkgs.unstructured-api
        ]))
      ];

      shellHook = ''
        venv="$(cd $(dirname $(which python)); cd ..; pwd)"
        ln -Tsf "$venv" .venv
      '';
    };
  };
}
