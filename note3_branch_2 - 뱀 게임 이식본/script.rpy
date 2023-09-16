# 이 파일에 게임 스크립트를 입력합니다.

# image 문을 사용해 이미지를 정의합니다.
# image eileen happy = "eileen_happy.png"

# 게임에서 사용할 캐릭터를 정의합니다.
define e = Character('송붕이', color="#c8ffc8")


# 여기에서부터 게임이 시작합니다.
label start:

    e "이 스크립트는 게임 구동 시 나타납니다."
    e "이 스크립트 이후 미니게임이 실행됩니다"

    call play_snake

    e "이 스크립트는 미니게임에서 성공적으로 빠져나오면 나타납니다"

    return
