<!-- Information about the project -->

## First configuration
### Prepare environment
pyenv install 3.11.11
pyenv virtualenv 3.11.11 administracion_amalia_env
pyenv activate administracion_amalia_env
pip install -r requirements.txt

### Install database tools
sudo apt update && sudo apt install -y libsqlite3-dev sqlite3

### Install PyQt tools
sudo apt update && sudo apt install libxcb-cursor0 libxkbcommon-x11-0 libxcb-xinerama0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0
echo $QT_QPA_PLATFORM_PLUGIN_PATH
QT_QPA_PLATFORM_PLUGIN_PATH=~/.pyenv/versions/3.11.11/envs/administracion_amalia_env/lib/python3.11/site-packages/PyQt6/Qt6/plugins 



## Launching the application
### Initiate App
python main.py

### Initiate Database
python database/database.py

### Run tests
pytest

