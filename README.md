# Don Tomate - pomodoro app


<img src="./don_tomate/don_tomate/Resources/don_tomate.PNG" width="100" height="100">


## Project setting
```Bash
conda create -n don_tomate python=3.11
```
```Bash
conda activate don_tomate
```
```Bash
pip install -r requirements.txt
```
#### optional for development
```Bash
pre-commit install
```

### Debugging
```Bash
 make run-macos
```

## Building
#### from navigate to app/
```Bash
pyinstaller --name "Don Tomate" --windowed --onedir main.py
```
#### make sure 'datas' contains the directories to the resources

```Bash
    datas=[
        ('don_tomate/Resources/play.png', 'don_tomate/Resources'),
        ('don_tomate/Resources/pause.png', 'don_tomate/Resources'),
        ('don_tomate/Resources/reset.png', 'don_tomate/Resources'),
        ('don_tomate/Resources/sound.png', 'don_tomate/Resources'),
        ('don_tomate/Resources/stop_sound.png', 'don_tomate/Resources'),
        ('don_tomate/Resources/settings.png', 'don_tomate/Resources'),
        ('don_tomate/Resources/next.png', 'don_tomate/Resources'),
        ('don_tomate/Resources/prev.png', 'don_tomate/Resources'),
        ('don_tomate/Resources/notification.wav', 'don_tomate/Resources'),
        ('don_tomate/Resources/don_tomate.png', 'don_tomate/Resources'),
    ],


    icon='don_tomate/Resources/don_tomate.png',

```
```Bash
pyinstaller Don\ Tomate.spec
```

```Bash
create-dmg 'dist/Don Tomate.app' --overwrite
```

### MAC
When macOS detects that an app has been downloaded or transferred from another system, it may quarantine the app, causing a "damaged" error. You can remove this attribute using the following command:
```Bash
xattr -cr /path/to/YourApp.app
```

### Project structure

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── docs               <- A default mkdocs project; see mkdocs.org for details
│
├── pyproject.toml     <- Project configuration file with package metadata for clustering_rpca
│                         and configuration for tools like black
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
├── tests
│   ├── contest.py     <-
│   └── don_tomate_testing.py <-
│
└── don_tomate         <- Source code for use in this project.
    │
    ├── __init__.py    <- Makes clustering_rpca a Python module
    │
    ├── main.py        <- Script with the app
    │
    └── visualization  <- Scripts to create exploratory and results oriented visualizations
        └── visualize.py
```
