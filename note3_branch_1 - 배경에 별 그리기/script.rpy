# 이 파일에 게임 스크립트를 입력합니다.

# image 문을 사용해 이미지를 정의합니다.
# image eileen happy = "eileen_happy.png"

# 게임에서 사용할 캐릭터를 정의합니다.
define e = Character('송붕이', color="#c8ffc8")

# we need the displayable to be attached to a screen
screen star_screen:
    add StarDisplay()

# 여기에서부터 게임이 시작합니다.
label start:
    # now we need to add the display to the background of our game
    e "첫 화면"
    
    show screen star_screen
    "{w}"
    hide screen star_screen
    e "끝 화면"