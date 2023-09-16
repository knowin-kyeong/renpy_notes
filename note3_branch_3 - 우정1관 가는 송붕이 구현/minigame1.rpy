# 하단 문장을 script.rpy에 넣으면 프로그램이 돌아갑니다
# default: "minigame1_송붕이.png"이 image 폴더에 있고, 크기는 (25*82 pixel짜리)
"""label start:
    "3월 XX일 월요일, 오후 6시 50분"
    "송붕이는 1학년 5반의 전통 문화인 '야간 1차시에 기숙사가기'를 하려고 한다.\n
    사감선생님에게 걸리지 않고 기숙사 문이 잠기기 전에 들어가야 휴식을 즐길 수 있다."
    
    e "누가 3월달인데 벌써 공부하냐? 들어가서 롤토체스 다이아 승격전이나 해야지"
    
    "송붕이를 잘 조종해 제한시간 안에 무사히 우정1관 입구에 들어가자.\n
    마우스 포인터를 따라 송붕이가 이동한다\n
    단, 마우스 포인터와 송붕이가 너무 가까우면 송붕이가 돌발행동을 한다"
    call play_minigame1
    "무사히 기숙사에 들어간 송붕이는 노트북을 켰다."
    e "자 롤토체스 드가자~~" """



define minigame1_TimeLimits = 20
define minigame1_ExtendedTimeLimits = 30

init python:
    import math, random

    class Game1Diasplayable(renpy.Displayable):
        def __init__(self):
            renpy.Displayable.__init__(self)

            # 게임 내 스크린 사이즈
            self.screenXsize = 1920
            self.screenYsize = 1080

            # 게임 진행 시간 설정
            self.deltaTime = 0
            self.calculatedTime = None

            #주인공(character) 관련 변수들
            self.charaXsize = None
            self.charaYsize = None
            self.charaXpos = float(self.screenXsize/4)
            self.charaYpos = float(self.screenYsize/4)
            self.charaAbsoluteSpeed = 5

            # 도착 지점 관련 변수들(사진에 맞게 사이즈를 설정하세요)
            self.goalXsize = 50
            self.goalYsize = 100
            self.goalXpos = random.randint(0, (self.screenXsize - self.goalXsize)/2) + self.screenXsize/4
            self.goalYpos = random.randint(0, (self.screenYsize - self.goalYsize)/2) + self.screenYsize/4

            # 캐릭터와 목표 지점을 Displayable로 표현 (사진에 맞게 사이즈를 설정하세요)
            # 송붕이 사진의 픽셀 크기
            self.charaXsize = 25
            self.charaYsize = 82
            self.chara = Image("minigame1_송붕이.png", pos = (self.charaXpos, self.charaYpos), xsize=self.charaXsize, ysize=self.charaYsize)
            self.goal = Solid("#00FFC8", pos = (self.goalXpos, self.goalYpos), xsize=self.goalXsize, ysize=self.goalYsize)            

            # 위치를 갱신하도록 마우스 위치 백터와 위치 증분 저장
            self.charaXpos_increment = 0
            self.charaYpos_increment = 0
            self.mouse_X = None
            self.mouse_Y = None
            self.mouse_click = None

            # 게임 종료를 의미하는 변수들
            self.endedByReachingGoal = False
            self.endedByExtendedTimeLimit = False
            return

        # Draws the screen
        def render(self, width, height, st, at):

            # 렌더링할 때마다 게임이 실행된 시간을 갱신해준다
            if self.calculatedTime is None:
                self.calculatedTime = st
            self.deltaTime = st - self.calculatedTime

            # 새로운 프레임을 그려 저장하는 변수
            # blit로 다 합쳐서 return하면 다음 프레임이 출력됨
            newrender = renpy.Render(width, height)

            # 목표 지점을 새로운 프레임에 출력
            def drawGoal(goalXpos, goalYpos):

                # 주인공을 먼저 render 하고..
                goal = renpy.render(self.goal, width, height, st, at)
                
                # 위 변수에 추가로 그려줌
                newrender.blit(goal, (int(goalXpos), int(goalYpos)))

            drawGoal(self.goalXpos, self.goalYpos)

            # 주인공의 위치를 입력 받아 새로운 프레임에 출력
            def drawChara(charaXpos, charaYpos):

                # 주인공을 먼저 render 하고..
                chara = renpy.render(self.chara, width, height, st, at)
                
                # 위 변수에 추가로 그려줌
                newrender.blit(chara, (int(charaXpos), int(charaYpos)))

            drawChara(self.charaXpos, self.charaYpos)

            # 먼저 주인공 위치 갱신
            self.charaXpos += self.charaXpos_increment
            self.charaYpos += self.charaYpos_increment

            # 그 다음으로, 만약 화면을 벗어나면 위치 재조정
            def checkCollding():
                if self.charaXpos <= 0:
                    self.charaXpos = 0
                if self.charaYpos <= 0:
                    self.charaYpos = 0
                if self.charaXpos >= self.screenXsize:
                    self.charaXpos = self.screenXsize
                if self.charaYpos >= self.screenYsize:
                    self.charaYpos = self.screenYsize
            checkCollding()

            # 목표 지점 근처에 도달했는지 확인
            def is_reached():
                return (
                    self.charaXpos <= self.goalXpos + self.charaXsize and
                    self.charaXpos >= self.goalXpos - self.charaXsize and
                    self.charaYpos <= self.goalYpos + self.charaYsize and
                    self.charaYpos >= self.goalYpos - self.charaYsize
                )

            # 만약 목표 지점에 도달하면 게임 종료
            if is_reached():
                self.endedByReachingGoal = True
                renpy.timeout(0)
            
            # 추가된 제한 시간이 지나면 강제로 게임 종료
            if self.deltaTime >= minigame1_ExtendedTimeLimits:
                self.endedByExtendedTimeLimit = True
                renpy.timeout(0)

            # 디음 프레임과의 시간 간격 조절
            renpy.redraw(self, 0.05)

            # 최종적으로, 이 함수 안에서 그린 newrender 객체 return
            return newrender

        # 이벤트 설정
        def event(self, ev, x, y, st):
            import pygame

            # 마우스 위치를 받아 온다
            mouseX, mouseY = pygame.mouse.get_pos()

            # 속도 벡터(2-list)를 정의해 주고 단위벡터로 만들어 준다
            velocityVector = [mouseX - self.charaXpos, mouseY - self.charaYpos]
            velocityNorm =  math.sqrt((mouseX - self.charaXpos)**2 + (mouseY - self.charaYpos)**2)
            
            if velocityNorm == 0: #0으로 나누기 회피
                unitVelocityVector = [0, 0]
            elif velocityNorm <= self.charaAbsoluteSpeed: #캐릭터가 마우스와 너무 가까우면 이상 행동을 함
                unitVelocityVector = [0, 0]
            else:
                unitVelocityVector = [velocityVector[i]/velocityNorm for i in range(0, 2)]

            # 그 결과로 위치 증분을 저장
            self.charaXpos_increment = unitVelocityVector[0] * self.charaAbsoluteSpeed
            self.charaYpos_increment = unitVelocityVector[1] * self.charaAbsoluteSpeed

            # 스크린을 강제로 업데이트시킴
            renpy.restart_interaction()

            # 게임이 끝났다면, 그 이벤트를 return
            if self.endedByReachingGoal:
                return self.endedByReachingGoal
            elif self.endedByExtendedTimeLimit:
                return self.endedByExtendedTimeLimit
            # 아니면, 그 이벤트를 무시함
            else:
                raise renpy.IgnoreEvent()

    def display_s_score(st, at):
        return Text(_("소요 시간: ") + "%.3f" % game1.deltaTime, size=50, color="#40BFB7", outlines=[ (1, "#40BFB7", 0, 0) ]), None #font="gui/font/Gallagher.ttf"), .1

default game1 = Game1Diasplayable()

screen game1():
    #add "minigames/s_background.jpg"

    text _("사감쌤을 피해서 우정1관 입구에 들어가기"):
        xpos 30
        xanchor 0
        ypos 25
        yanchor 0
        size 40
        color "#FFC8C8"
        # outlines [ (4, "#FFC8C8", 0, 0) ]
        #font "gui/font/Gallagher.ttf"

    add DynamicDisplayable(display_s_score) xpos 30 ypos (1080 - 1000) xanchor 0

    add game1

label play_minigame1:

    # 게임 실행 중엔 quick_menu와 ui 숨기기
    window hide 
    $ quick_menu = False
    hide screen buttons_ui

    # 객체의 기본값 설정
    $ game1.screenXsize = 1920
    $ game1.screenYsize = 1080

    call screen game1

    # 게임이 끝났으므로 다시 quick_menu 공개
label result_minigame1:

    #제한 시간과 클리어 시간을 비교함
    if game1.deltaTime <= minigame1_TimeLimits:
        "축하합니다! 게임을 클리어하셨습니다! (소요 시간: [game1.deltaTime:.3] 초)\n
        클릭을 통해 다시 스토리로 돌아갑니다"
        $ quick_menu = True
        window auto
        return

    else:
        if game1.deltaTime <= minigame1_ExtendedTimeLimits:
            "게임 클리어에 실패하였습니다. 소요 시간: [game1.deltaTime:.3] 초, 제한 시간: [minigame1_TimeLimits] 초\n
            Tip: 도착 지점에 마우스를 잘 가져다 대면 클리어할 수 있습니다"
        else:
            "게임 클리어에 실패하였습니다. 소요 시간: [minigame1_ExtendedTimeLimits] 초 초과, 제한 시간: [minigame1_TimeLimits] 초\n
            Tip: 도착 지점에 마우스를 잘 가져다 대면 클리어할 수 있습니다"

            menu:
                "무엇을 하시겠습니까?"
                "미니게임을 재시도한다":
                    jump play_minigame1
                "시작으로 돌아간다":
                    $ quick_menu = True
                    window auto
                    jump start

    