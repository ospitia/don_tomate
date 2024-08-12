# Don Tomate - pomodoro app

<img src="./app/don_tomate/Resources/don_tomate.PNG" width="100" height="100">

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
        ('don_tomate/Resources/notification.wav', 'don_tomate/Resources'),
        ('don_tomate/Resources/don_tomate.png', 'don_tomate/Resources'),
    ],
    
        
    icon='don_tomate/Resources/don_tomate.png',

``` 
```Bash
pyinstaller Don\ Tomate.spec 
```
#### optional for development
```Bash
create-dmg 'dist/Don Tomate.app' --overwrite 
```
