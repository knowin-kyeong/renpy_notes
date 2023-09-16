# 이 파일에 게임 스크립트를 입력합니다.
# image 문을 사용해 이미지를 정의합니다.
image in_pick_phase = im.FactorScale("큐 화면 사진.jpg", 1.6)
image defeat = im.FactorScale("패배 화면 사진.jpg", 2.3)
image lanephase = im.FactorScale("바텀 라인전 사진.jpg", 1.6)
image slain_picture = im.FactorScale("킬 사진.jpg", 1)
image shutdown = im.FactorScale("제압골드 방생 사진.jpeg", 5)
image gshs = im.FactorScale("경곽 로고.jpeg", 4)
image ujeong1 = im. FactorScale("경곽 시설 사진.jpeg", 4)
image promoted = im.FactorScale("골드사진.png", 3)
# 게임에서 사용할 캐릭터를 정의합니다.
define player_name = "플레이어 이름"     
define n = Character("지나가던 송붕이", color = "#0000FF")
define gshsteacher = Character("방송", color = "#00FF00")
define p = Character("player_name", dynamic = True, color = "#50FFFF")
define camsetting = Position(xalign = 0, yalign = 0)


# 여기에서부터 게임이 시작합니다.
#scene background at camsetting with dissolve 처럼 할 수도 있음
#scene/show(name) + at(pos.) + with(effect)
#scene은 새로 그림 쓰기, show는 추가로 표시하기
label start:
    scene background
    n "당신의 이름은?"
    $player_name = renpy.input("나는..")
    p "나는 [player_name]이다.\n"

    show ujeong1
    gshsteacher "[player_name] 학생은 지금 바로 사감실로 오시기 바랍니다\n"
    p "알빠노\n"
    p "오랜만에 롤이나 돌릴까"
    hide ujeong1

    scene in_pick_phase
    p "라인 꼬였는데 그냥 원딜이나 해야지\n"
    p "(시발.. 나 서포터인데 게임 지는거 아니냐..)\n"

    scene lanephase
    p "아 이거 킬각인데 들어갈까?"

    show slain_picture with dissolve
    p "이이잉 기모링\n"
    p "이걸 킬을 따네\n"
    p "아 내가 실버3에 있긴 아깝잖아 이제 골드로 승격해야지\n"
    hide slain_picture

    menu:
        p "포탑에 딸피 1000골드 이렐리아가 있는데 이걸 참아?\n"
        
        "마스터 승격전이니까 참는다":
            "상대 채팅창에서 내분이 일어난 듯하다\n"
            "상대의 서렌 투표로 인해 게임에 승리했다\n"
            call fake_ending
      
        "이건 절대 못참지 ㅋㅋ":
            "도구새끼가 포탑 어그로를 안끌어준다"
            show shutdown with dissolve
            p "아 뭐해 도구련아!!\n"
            p "이래서 서폿 욕하는거지 도구론이 괜히 있는 게 아닌데 하.."
            hide shutdown
            call bad_ending
        
        "탈주하기" if player_name == "경노인":
        # 이렇게 if [조건식]: 으로 선택지를 선택적으로 표시할 수 있음
            scene background
            "개발자" "그 이름은 허용하지 않았어"
            return

    scene background
    show gshs with dissolve
    "경곽에서는 절대로 행복해질 수 없습니다...\n"
    "경곽에 무한한 영광이 있기를."
    hide gshs
    return

label bad_ending:
    scene background
    show defeat with dissolve
    "그 후 [player_name](은/는) 제압골을 이렐리아한테 먹여 게임을 이길 수 없었습니다\n"
    p "나는 그냥 실버3이 딱이야\n"
    hide defeat
    return

label fake_ending:
    scene background
    show promoted 
    "골드에 승급한 기쁨에 뒤에 선생님이 있는 줄도 모르고 소리를 지른다"
    p "아 이거지 ㅋㅋ\n"
    hide promoted
    "이해룡" "핸드폰 이리 내" 
    "핸드폰을 지키려고 했지만..{w}\n"
    "결국 난 힘으로 핸드폰을 뺏겼다\n"
    "" with vpunch
    #이렇게 효과를 넣을 수 있음
    return
