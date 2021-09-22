SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 600
BACKGROUND_VELOCITY = -300

PLAYER_WIDTH = 130
PLAYER_HEIGHT = 60

LASER_WIDTH = SCREEN_WIDTH
LASER_HEIGHT = 50
LASER_COOLDOWN = 15
LASERRED_COOLDOWN = 0.3
LASERBLINK_COOLDOWN = 0.3
LASERREMAINTIME = 3

BUILDING_HEIGHT = 100
BUILDING_WIDTH = 600
BUILDING_RATIO = 0.47

POLICECAR_WIDTH = 160
POLICECAR_HEIGHT = 70
POLICECAR_VELOCITY = 200

WARN_WIDTH = 50
WARN_HEIGHT = 10

BULLET_WIDTH = 10
BULLET_HEIGHT = 10
SHOOT_COOLDOWN = 2  # second
# BULLET_SPEED = -BACKGROUND_VELOCITY
QUICKFIRE_SKILL_COOLDOWN = 10  # second
QUICKFIRE_COOLDOWN = 0.1  # second

OBSTACLE_WIDTH = 30
OBSTACLE_HEIGHT = 90
OBSTACLE_COOLDOWN = 2  # second

EXPLODE_HEIGHT = 180
EXPLODE_WIDTH = 100

MISSILE_HEIGHT = 40
MISSILE_WIDTH = 120
MISSILE_SPEED = -BACKGROUND_VELOCITY * 2

PLAYER_ACC = 20
FRICTION_HORI = PLAYER_ACC * 0.4
FRICTION_VERT = PLAYER_ACC * 0.6
PLAYER_MAX_HORI_SPEED = 2 * -BACKGROUND_VELOCITY

INIT_SOUND_VOLUME = INIT_MUSIC_VOLUME = 0.3

# debug
DISABLE_BUILDINGS = False
SHOW_FPS = False
