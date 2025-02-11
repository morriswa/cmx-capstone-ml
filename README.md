# CMX Capstone Machine Learning

## Contributors
- William Morris [morriswa] morris.william@ku.edu
- Kevin Rivers [Kabuto1357] kevin.rivers14832@ku.edu
- Makenna Loewenherz [makennabrynn] makennaloewenherz@gmail.com


## Project Setup Guide
- Install python 3.12 https://www.python.org/downloads/
- Open project root directory in terminal
- Install Project environment

      python3.12 -m venv .
- Activate Project environment
    - Mac/Linux

          source bin/activate
        - NOTE: to deactivate project environment

              deactivate
        - NOTE: to reset project environment 

              rm -rf bin include lib pyvenv.cfg
    - Windows Powershell

          .\Scripts\activate
        - NOTE: to deactivate project environment

              .\Scripts\deactivate.bat
        - NOTE: to reset project environment 

              rm -r include
              rm -r lib 
              rm -r scripts
              rm -r pyvenv.cfg
- Install project in development mode and dependencies with PIP 

      pip install -e .
