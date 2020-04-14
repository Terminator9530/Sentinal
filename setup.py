import cx_Freeze
executables=[cx_Freeze.Executable("sentinal.py")]
images=["back1.jpg","back2.jpg","back3.jpg","back4.jpg","back5.jpg","end.jpg","homeImg.jpg","bold_gold.png","enemyBlue1.png","enemyBlue2.png","enemyBlue3.png","enemyBlue4.png","enemyBlue5.png","meteor.png","meteor1.png","meteor2.png","meteor3.png","meteor4.png","icon.png","laser.png","regularExplosion00.png","regularExplosion01.png","regularExplosion02.png","regularExplosion03.png","regularExplosion04.png","regularExplosion05.png","regularExplosion06.png","regularExplosion07.png","regularExplosion08.png","rocket.png","shield_gold.png","shield_silver.png","shield_bronze.png","ship.png","sonicExplosion00.png","sonicExplosion01.png","sonicExplosion02.png","sonicExplosion03.png","sonicExplosion04.png","sonicExplosion05.png","sonicExplosion06.png","sonicExplosion07.png","sonicExplosion08.png","space-2.png","ufoBlue.png"]
sound=["explode.wav","Laser_Shoot.wav","tgfcoder-FrozenJam-SeamlessLoop.obb","high_score.txt"]
allFiles=[]
for i in images:
    allFiles.append("img/"+i)
print(allFiles)
cx_Freeze.setup(
    name="Sentinal",
    options={"built_exe":{"packages":["pygame"],"include_files":images+sound}},
    executables=executables
)