# default: "minigame1_송붕이.png"이 image 폴더에 있고, 크기는 (25*82 pixel짜리)
# default: "minigame1_사감쌤.png"이 image 폴더에 있고, 크기는 (25*82 pixel짜리)
define minigame1_TimeLimits = 20
define minigame1_ExtendedTimeLimits = 30

init python:
    import math

    class Game1Diasplayable(renpy.Displayable):
        def __init__(self):
            renpy.Displayable.__init__(self)

            ############################### 게임 내 스크린 사이즈 ###############################
            self.screenXsize = 1920
            self.screenYsize = 1080

            ############################### 게임 진행 시간 설정 ###############################
            self.deltaTime = 0
            self.calculatedTime = None
            
            ############################### 주인공(character) 관련 변수들 ###############################
            self.characterXsize = 25
            self.characterYsize = 82
            self.characterXpos = renpy.random.randint(0, int(self.screenXsize/5) - int(self.characterXsize/2)) + self.screenXsize/4
            self.characterYpos = renpy.random.randint(0, int(self.screenYsize/5) - int(self.characterYsize/2)) + self.screenYsize/4
            self.characterAbsoluteSpeed = 3
            self.characterXpos_increment = 0
            self.characterYpos_increment = 0

            # 맨 처음에는 마우스를 충분히 움직일 때까지 정지해 있도록 함
            self.characterMoved = False
            self.initialMouse = None

            ############################### 도착 지점 관련 변수들(사진에 맞게 사이즈를 설정하세요) ###############################
            self.goalXsize = 40
            self.goalYsize = 100
            self.goalXpos = renpy.random.randint(0, int(self.screenXsize/5) - int(self.goalXsize/2)) + self.screenXsize*3/4
            self.goalYpos = renpy.random.randint(0, int(self.screenYsize/5) - int(self.goalYsize/2)) + self.screenYsize*3/4

            ############################### 장애물(obstacle) 관련 변수들 ###############################
            self.obstaclePosition = []
            self.obstacleNumber = 10
            self.obstacleXsize = 25
            self.obstacleYsize = 82

            # 장애물과 다른 객체 "변과 변" 사이의 최소 거리 (0: 서로 변이 붙을 수 있음)
            self.obstacleXMargin = self.obstacleXsize * 3
            self.obstacleYMargin = self.obstacleYsize * 3
            
            # 장애물이 유효한 위치에 생성되도록 위치를 결정해 주는 함수
            def generateObstacles():
                while True:
                    xPos = renpy.random.randint(0, self.screenXsize - self.obstacleXsize)
                    yPos = renpy.random.randint(0, self.screenYsize - self.obstacleYsize)

                    # 초기 캐릭터와 위치가 겹치는지 확인
                    if abs(xPos - self.characterXpos) < self.obstacleXsize/2 + self.characterXsize/2 and abs(yPos - self.characterYpos) < self.obstacleYsize/2 + self.characterYsize/2:
                        continue
                    
                    # 초기 도착지점과 위치가 겹치는지 확인
                    elif abs(xPos - self.goalXpos) < self.obstacleXsize/2 + self.goalXsize/2 and abs(yPos - self.goalYpos) < self.obstacleYsize/2 + self.goalYsize/2:
                        continue
                    
                    # 다른 장애물과 위치가 겹치는지 확인
                    else:
                        isConflictOthers = False
                        for obstaclePosition in self.obstaclePosition:
                            otherXpos = obstaclePosition[0]
                            otherYpos = obstaclePosition[1]

                            if abs(xPos - otherXpos) < self.obstacleXsize  and abs(yPos - otherYpos) < self.obstacleYsize:
                                isConflictOthers = True
                                continue
                        
                        if isConflictOthers == True:
                            continue

                    # 조건을 만족하면 반복문을 빠져나옴
                    break

                # 조건을 만족하는 장애물 좌표 위치를 배열에 넣어 준다.
                self.obstaclePosition.append((xPos, yPos))
            
            # 함수를 사용한 장애물 생성
            for index in range(0, self.obstacleNumber):
                generateObstacles()
                    
            ############################### 캐릭터와 목표 지점, 장애물을 Displayable로 표현 (사진에 맞게 사이즈를 설정하세요) ###############################  
            self.character = Image("minigame1_송붕이.png", pos = (self.characterXpos - self.characterXsize/2, self.characterYpos - self.characterYsize/2), xsize=self.characterXsize, ysize=self.characterYsize)
            self.goal = Solid("#00FFC8", pos = (self.goalXpos - self.goalXsize/2, self.goalYpos - self.goalYsize/2), xsize=self.goalXsize, ysize=self.goalYsize)            

            # 각각의 장애물 Displayable로 담는 list
            self.obstacle = []
            for index in range(0, self.obstacleNumber):
                tempXpos, tempYpos = self.obstaclePosition[index]
                self.obstacle.append(Image("minigame1_사감쌤.png", pos = (tempXpos - self.obstacleXsize/2, tempYpos - self.obstacleYsize/2), xsize=self.obstacleXsize, ysize=self.obstacleYsize))
            
            ############################### 게임 종료를 의미하는 변수들 ###############################
            self.endedByReachingGoal = False
            self.endedByExtendedTimeLimit = False
            self.endedByObstacleColliding = False
            return

        ############################### 스크린 그리기 ###############################
        def render(self, width, height, st, at):

            #렌더링할 때마다 게임이 실행된 시간을 갱신해준다
            if self.calculatedTime is None:
                self.calculatedTime = st
            self.deltaTime = st - self.calculatedTime

            #####새로운 프레임을 그려 저장하기#####
            # 새 렌더링 객체를 선언하고, blit로 하나씩 추가해준다
            newrender = renpy.Render(width, height)

            # 목표 지점을 새로운 프레임에 출력하는 함수
            def drawGoal(goalXpos, goalYpos):

                # 목표 지점 사진을 먼저 render 하고..
                goal = renpy.render(self.goal, width, height, st, at)
                
                # 위 변수에 추가로 그려줌
                newrender.blit(goal, (int(goalXpos), int(goalYpos)))

            drawGoal(self.goalXpos, self.goalYpos)

            # 주인공의 위치를 입력 받아 새로운 프레임에 출력하는 함수
            def drawCharacter(characterXpos, characterYpos):

                # 주인공을 먼저 render 하고..
                character = renpy.render(self.character, width, height, st, at)
                
                # 위 변수에 추가로 그려줌
                newrender.blit(character, (int(characterXpos), int(characterYpos)))

            drawCharacter(self.characterXpos, self.characterYpos)

            # 장애물의 위치를 입력 받아 새로운 프레임에 출력하는 함수
            def drawObstacles(obstacleXpos, obstacleYpos, index):

                # (i번째) 장애물을 먼저 render 하고..
                obstacle = renpy.render(self.obstacle[index], width, height, st, at)
                
                # 위 변수에 추가로 그려줌
                newrender.blit(obstacle, (int(obstacleXpos), int(obstacleYpos)))

            for index in range(0, self.obstacleNumber):
                drawObstacles(self.obstaclePosition[index][0], self.obstaclePosition[index][1], index)

            # 디음 프레임과의 시간 간격 조절
            renpy.redraw(self, 0)

            # 최종적으로, 이 함수 안에서 그린 newrender 객체 return
            return newrender

        ############################### 이벤트 설정 ###############################
        def event(self, ev, x, y, st):
            import pygame

            ##### 위치 갱신 #####
            # 마우스 위치를 받아 온다
            mouseX, mouseY = renpy.get_mouse_pos()

            # 마우스가 게임 시작 이후 충분한 거리를 움직였는지 확인
            if self.characterMoved == False:
                if math.sqrt((self.initialMouse[0] - mouseX)**2 + (self.initialMouse[1] - mouseY)**2) > min(self.screenXsize/10, self.screenYsize/10):
                    self.characterMoved = True
                else:
                    pass
            
            else:
                # 속도 벡터(2-list)를 정의해 주고 단위벡터로 만들어 준다
                velocityVector = [mouseX - self.characterXpos, mouseY - self.characterYpos]
                velocityNorm =  math.sqrt((mouseX - self.characterXpos)**2 + (mouseY - self.characterYpos)**2)
            
                if velocityNorm == 0: #0으로 나누기 회피
                    unitVelocityVector = [0, 0]
                elif velocityNorm <= self.characterAbsoluteSpeed: #캐릭터가 마우스와 너무 가까우면 이상 행동을 함
                    unitVelocityVector = [0, 0]
                else:
                    unitVelocityVector = [velocityVector[i]/velocityNorm for i in range(0, 2)]

                # 그 결과로 위치 증분을 저장
                self.characterXpos_increment = unitVelocityVector[0] * self.characterAbsoluteSpeed
                self.characterYpos_increment = unitVelocityVector[1] * self.characterAbsoluteSpeed

                # 먼저 주인공 위치 갱신
                self.characterXpos += self.characterXpos_increment
                self.characterYpos += self.characterYpos_increment

            # 스크린을 강제로 업데이트시킴
            renpy.restart_interaction()

            ##### 여러 조건 확인 #####
            # 만약 화면을 벗어나면 위치 재조정
            def checkScreenCollding():
                if self.characterXpos <= self.characterXsize/2:
                    self.characterXpos = self.characterXsize/2

                if self.characterYpos <= self.characterYsize/2:
                    self.characterYpos = self.characterYsize/2

                if self.characterXpos >= self.screenXsize - self.characterXsize/2:
                    self.characterXpos = self.screenXsize - self.characterXsize/2

                if self.characterYpos >= self.screenYsize - self.characterYsize/2:
                    self.characterYpos = self.screenYsize - self.characterYsize/2
            checkScreenCollding()

            # 목표 지점 근처에 도달했는지 확인
            def is_reached():
                return (
                    abs(self.characterXpos - self.goalXpos) < (self.characterXsize/2 + self.goalXsize/2) and
                    abs(self.characterYpos - self.goalYpos) < (self.characterYsize/2 + self.goalYsize/2)
                )

            # 장애물과 충돌했는지 확인
            def is_collided():
                for index in range(0, self.obstacleNumber):
                    if (
                        abs(self.characterXpos - self.obstaclePosition[index][0]) < (self.characterXsize/2 + self.obstacleXsize/2) and
                        abs(self.characterYpos - self.obstaclePosition[index][1]) < (self.characterYsize/2 + self.obstacleYsize/2)
                    ):
                        return True
                return False
            

            # 만약 목표 지점에 도달하면 게임 종료
            if is_reached():
                self.endedByReachingGoal = True
                renpy.timeout(0)
            
            # 만약 장애물과 충돌하면 게임 종료
            if is_collided():
                self.endedByObstacleColliding = True
                renpy.timeout(0)

            # 추가된 제한 시간이 지나면 강제로 게임 종료
            if self.deltaTime >= minigame1_ExtendedTimeLimits:
                self.endedByExtendedTimeLimit = True
                renpy.timeout(0)

            # 게임이 끝났다면, 그 이벤트를 return
            if self.endedByReachingGoal:
                return self.endedByReachingGoal

            elif self.endedByExtendedTimeLimit:
                return self.endedByExtendedTimeLimit
            
            elif self.endedByObstacleColliding:
                return self.endedByObstacleColliding
            
            # 종료 조건에 해당하지 않으면, 그 이벤트를 무시함
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

    # 객체의 기본값 설정(재시작 시 초기화에 사용됨)
    $ game1 = Game1Diasplayable()
    $ game1.initialMouse = renpy.get_mouse_pos()

    call screen game1

    # 게임이 끝났으므로 다시 quick_menu 공개
label result_minigame1:

    #제한 시간과 클리어 시간을 비교함
    if game1.deltaTime <= minigame1_TimeLimits and game1.endedByObstacleColliding == False:
        "축하합니다! 게임을 클리어하셨습니다! (소요 시간: [game1.deltaTime:.3] 초)\n
        클릭을 통해 다시 스토리로 돌아갑니다"
        $ quick_menu = True
        window auto
        return

    else:
        if game1.endedByObstacleColliding == True:
            "게임 클리어에 실패하였습니다. 장애물과 충돌하였습니다\n
            Tip: 장애물과 가까워지면 마우스를 잘 조절해 보세요"
        elif game1.endedByObstacleColliding == False:
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