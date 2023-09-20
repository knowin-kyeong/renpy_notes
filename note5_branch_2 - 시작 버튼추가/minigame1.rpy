# default: "minigame1_송붕이.png"이 image 폴더에 있고, 크기는 (25*82 pixel짜리)
# default: "minigame1_사감쌤.png"이 image 폴더에 있고, 크기는 (25*82 pixel짜리)
define minigame1_TimeLimits = 20
define minigame1_ExtendedTimeLimits = 30

init python:
    import math

    ############################### 장애물 객체 ###############################
    # 생성자로 위치(list), 크기(list), 속도(list)을 받는다
    # 아랫 객체에서 (generateObstacle()로) 위치를 정해 여기 생성자로 보내면,
    # 해당하는 장애물 객체를 생성
    class Obstacle(object):
        # 화면 사이즈는 모든 객체가 공유하므로, 인스턴스 변수가 아닌 클래스 변수로 설정
        screenSize = (1920, 1080)

        def __init__(self, pos, size, velocity, type, image, index):
            self.position = pos
            self.size= size
            self.velocity = list(velocity) # 반사 때문에 값이 바뀔 수 있으므로 list
            self.type = type
            self.image = image #"minigame1_사감쌤.png"
            self.index = index

        
        # 프레임이 지날 때마다 위치 갱신
        def getNewPosition(self):
            self.position[0] += self.velocity[0]
            self.position[1] += self.velocity[1]

            if self.type==0:
                pass
            elif self.type==1:
                self.reflect()

        # 장애물이 벽에 닿으면 반사
        def reflect(self):
            if self.position[0] - self.velocity[0] < self.size[0]/2:
                self.position[0] = self.size[0]/2
                self.velocity[0] *= -1

            if self.position[0] + self.velocity[0] > Obstacle.screenSize[0] - self.size[0]/2:
                self.position[0] = Obstacle.screenSize[0] - self.size[0]/2
                self.velocity[0] *= -1

            if self.position[1] - self.velocity[1] < self.size[1]/2 :
                self.position[1] = self.size[1]/2
                self.velocity[1] *= -1

            if self.position[1] + self.velocity[1] > Obstacle.screenSize[1] - self.size[1]/2:
                self.position[1] = Obstacle.screenSize[1] - self.size[1]/2
                self.velocity[1] *= -1

    ############################### Displayable 객체 ###############################


    class Game1Diasplayable(renpy.Displayable):
        def __init__(self, currentmap, lastlocation):
            renpy.Displayable.__init__(self)

            ############################### 게임 내 스크린 사이즈 ###############################
            self.screenSize = (1920, 1080)

            ############################### 게임 진행 시간 설정 ###############################
            self.deltaTime = 0
            self.calculatedTime = None
            
            ############################### 주인공(character) 관련 변수들(사진에 맞게 사이즈를 설정하세요) ###############################
            self.characterSize = (25, 82)
            self.characterPosition = lastlocation
            
            self.characterAbsoluteSpeed = 3
            self.characterPositionIncrement = [None, None]

            # 맨 처음에는 마우스 위치를 캐릭터 위치로 고정하고, 마우스를 충분히 움직일 때까지 정지해 있도록 함
            self.initializedCursorPosition = False
            self.initialEffectiveMovement = False

            ############################### 도착 지점 관련 변수들(사진에 맞게 사이즈를 설정하세요) ###############################
            self.goalSize = (None, None)
            self.goalPosition = [None, None]
            ############################### 장애물(obstacle) 관련 변수들(사진에 맞게 사이즈를 설정하세요) ###############################            
            self.currentmap = currentmap
            self.last = False
            self.obstacles = []

            def mapUpdate():
                if self.currentmap == 1:
                    self.goalSize= (40, 100)
                    self.goalPosition = [500, 500]
                    self.map = [[[700,300],[40,40],[0,0],0,"minigame1_사감쌤.png"],
                                [[400,500],[40,40],[0,0],0,"minigame1_사감쌤.png"]]

                elif self.currentmap == 2:
                    self.goalSize= (40, 100)
                    self.goalPosition = [100, 100]
                    self.map = [[[30,30],[40,40],[7,7],1,"minigame1_교장쌤.png"],
                                [[170,170],[40,40],[7,7],1,"minigame1_교장쌤.png"],
                                [[200,200],[40,40],[0,0],0,"minigame1_사감쌤.png"],
                                [[400,800],[40,40],[0,0],0,"minigame1_사감쌤.png"],
                                [[800,400],[40,40],[0,0],0,"minigame1_사감쌤.png"]]

                elif self.currentmap == 3:
                    self.goalSize= (40, 100)
                    self.goalPosition = [None, None]
                    self.goalPosition[0] = renpy.random.randint(0, int(self.screenSize[0]/5) - int(self.goalSize[0]/2)) + self.screenSize[0] * 3/4
                    self.goalPosition[1] = renpy.random.randint(0, int(self.screenSize[1]/5) - int(self.goalSize[1]/2)) + self.screenSize[1] * 3/4
                    self.obstacleNumber = 10
                    self.obstacleSize = (25,82)
                    self.map = []

                    def generatePosition(currentIndex):
                        
                        obstacleMargin = (self.obstacleSize[0] * 3, self.obstacleSize[1] * 3)
                        while True:
                            Position = [None, None]
                            Position[0] = renpy.random.randint(0, self.screenSize[0] - self.obstacleSize[0])
                            Position[1] = renpy.random.randint(0, self.screenSize[1] - self.obstacleSize[1])

                            # 초기 캐릭터와 위치가 겹치는지 확인
                            if (
                                abs(Position[0] - self.characterPosition[0]) < self.obstacleSize[0]/2 + self.characterSize[0]/2 + obstacleMargin[0] and 
                                abs(Position[1] - self.characterPosition[1]) < self.obstacleSize[1]/2 + self.characterSize[1]/2 + obstacleMargin[1]
                            ):
                                continue
                            
                            # 초기 도착지점과 위치가 겹치는지 확인
                            elif (
                                abs(Position[0] - self.goalPosition[0]) < self.obstacleSize[0]/2 + self.goalSize[0]/2 + obstacleMargin[0] and 
                                abs(Position[1] - self.goalPosition[1]) < self.obstacleSize[1]/2 + self.goalSize[1]/2 + obstacleMargin[1]
                            ):
                                continue
                            
                            # 다른 장애물이 존재한다면, 서로 위치가 겹치는지 확인
                            else:
                                isConflictOthers = False
                                for index in range(0, currentIndex):
                                    otherPos = self.map[index][0]

                                    if (
                                        abs(Position[0] - otherPos[0]) < self.obstacleSize[0] + obstacleMargin[0] and 
                                        abs(Position[1] - otherPos[1]) < self.obstacleSize[1] + obstacleMargin[1]
                                    ):
                                        isConflictOthers = True
                                        continue
                                
                                if isConflictOthers == True:
                                    continue

                            # 조건을 만족하면 그 위치 list를 return함
                            return Position
                    
                    # 함수를 사용한 장애물 생성
                    for index in range(0, self.obstacleNumber):
                        self.map.append([generatePosition(index),self.obstacleSize, (3,5), 1,"minigame1_교장쌤.png"])
                    
                    self.last = True
                
                index = 0
                for a in self.map:
                        self.obstacles.append(Obstacle(a[0],a[1],a[2],a[3],a[4],index))
                        index += 1
            
            if currentmap==0:
                self.goalPosition = lastlocation
                self.goalSize= (40, 100)
                self.goalImage = Solid("#4c00ff", pos = (self.goalPosition[0] - self.goalSize[0]/2, self.goalPosition[1] - self.goalSize[1]/2), xsize=self.goalSize[0], ysize=self.goalSize[1])            

            else:
                mapUpdate()
                self.characterImage = Image("minigame1_송붕이.png", pos = (self.characterPosition[0] - self.characterSize[0]/2, self.characterPosition[1] - self.characterSize[1]/2), xsize=self.characterSize[0], ysize=self.characterSize[1])
                self.goalImage = Solid("#00FFC8", pos = (self.goalPosition[0] - self.goalSize[0]/2, self.goalPosition[1] - self.goalSize[1]/2), xsize=self.goalSize[0], ysize=self.goalSize[1])
                # 각각의 장애물 Displayable로 담는 list
                self.obstacleImage = []
                for obstacle in self.obstacles:
                    (tempXpos, tempYpos) = obstacle.position
                    (tempXsize, tempYsize) = obstacle.size
                    self.obstacleImage.append(Image(obstacle.image, pos = (tempXpos - tempXsize/2, tempYpos - tempYsize/2), xsize=tempXsize, ysize=tempYsize))
                                                   
            
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
            def drawGoal(goalPos):

                # 목표 지점 사진을 먼저 render 하고..
                goalImage = renpy.render(self.goalImage, width, height, st, at)
                
                # 위 변수에 추가로 그려줌
                newrender.blit(goalImage, (int(goalPos[0]), int(goalPos[1])))

            drawGoal(self.goalPosition)

            # 주인공의 위치를 입력 받아 새로운 프레임에 출력하는 함수
            def drawCharacter(characterPos):

                # 주인공을 먼저 render 하고..
                characterImage = renpy.render(self.characterImage, width, height, st, at)
                
                # 위 변수에 추가로 그려줌
                newrender.blit(characterImage, (int(characterPos[0]), int(characterPos[1])))

            if currentmap !=0:
                drawCharacter(self.characterPosition)

            # 장애물의 위치를 입력 받아 새로운 프레임에 출력하는 함수
            def drawObstacles(obstacle):

                # (i번째) 장애물을 먼저 render 하고..
                obstacleImage = renpy.render(self.obstacleImage[obstacle.index], width, height, st, at)
                
                # 위 변수에 추가로 그려줌
                newrender.blit(obstacleImage, (int(obstacle.position[0]), int(obstacle.position[1])))

            if currentmap !=0:
                for obstacle in self.obstacles:
                    drawObstacles(obstacle)

            # 디음 프레임과의 시간 간격 조절
            renpy.redraw(self, 0)

            # 최종적으로, 이 함수 안에서 그린 newrender 객체 return
            return newrender

        ############################### 이벤트 설정 ###############################
        def event(self, ev, x, y, st):
            import pygame
            mousePress = False

            ##### 위치 갱신 #####
            # 마우스 위치를 받아 온다
            mousePosition = renpy.get_mouse_pos()
            if pygame.mouse.get_pressed()[0]:
                mousePress = True
            
            
            """
            # 게임을 실행한 직후에 마우스가 캐릭터 위치로 이동하도록 함
            # renpy.display.draw.set_mouse_pos 이 함수 왜 이상한 데에 마우스 커서를 올려놓는거지
            if self.initializedCursorPosition == False:
                renpy.display.draw.set_mouse_pos(self.characterPosition[0] + self.characterSize[0]/2, self.characterPosition[1] + self.characterSize[0]/2)
                self.initializedCursorPosition = True

            # 마우스가 게임 시작 이후 한 번이라도 충분한 거리(화면의 두 변 중 최솟값 / 15)를 움직였는지 확인 (아니면 객체 고정)
            elif self.initialEffectiveMovement == False:
                if math.sqrt((self.characterPosition[0] - mousePosition[0])**2 + (self.characterPosition[1] - mousePosition[1])**2) > min(self.screenSize[0]/15, self.screenSize[1]/15):
                    self.initialEffectiveMovement = True
                else:
                    pass
            """
                
            # 모든 객체들의 위치 갱신
            
            if currentmap ==0:
                if mousePress and abs(mousePosition[0] - self.goalPosition[0]) < (mousePosition[0]/2 + self.goalSize[0]/2) and abs(mousePosition[1] - self.goalPosition[1]) < (mousePosition[1]/2 + self.goalSize[1]/2):
                    self.endedByReachingGoal = True
                    self.lastlocation = list(mousePosition)
                    return self.endedByReachingGoal

            
            else:
                ##### 주인공의 위치를 변경해 준다 #####
                # 속도 벡터(2-list)를 정의해 주고 단위벡터로 만들어 준다
                velocityVector = [mousePosition[0] - self.characterPosition[0], mousePosition[1] - self.characterPosition[1]]
                velocityNorm =  math.sqrt((mousePosition[0] - self.characterPosition[0])**2 + (mousePosition[1] - self.characterPosition[1])**2)
            
                if velocityNorm == 0: #0으로 나누기 회피
                    unitVelocityVector = [0, 0]
                elif velocityNorm <= self.characterAbsoluteSpeed: #캐릭터가 마우스와 너무 가까우면 이상 행동을 함
                    unitVelocityVector = [0, 0]
                else:
                    unitVelocityVector = [velocityVector[i]/velocityNorm for i in range(0, 2)]

                # 그 결과로 위치 증분을 저장
                self.characterPositionIncrement[0] = unitVelocityVector[0] * self.characterAbsoluteSpeed
                self.characterPositionIncrement[1] = unitVelocityVector[1] * self.characterAbsoluteSpeed

                # 먼저 주인공 위치 갱신
                self.characterPosition[0] += self.characterPositionIncrement[0]
                self.characterPosition[1] += self.characterPositionIncrement[1]

                ##### 장애물의 위치를 변경해 준다 #####
                for obstacle in self.obstacles:
                    obstacle.getNewPosition()

                # 스크린을 강제로 업데이트시킴
                renpy.restart_interaction()

                ##### 여러 조건 확인 #####
                # 만약 캐릭터가 화면을 벗어나면 위치 재조정
                def checkScreenCollding():
                    if self.characterPosition[0] <= self.characterSize[0]/2:
                        self.characterPosition[0] = self.characterSize[0]/2

                    if self.characterPosition[1] <= self.characterSize[1]/2:
                        self.characterPosition[1] = self.characterSize[1]/2

                    if self.characterPosition[0] >= self.screenSize[0] - self.characterSize[0]/2:
                        self.characterPosition[0] = self.screenSize[0] - self.characterSize[0]/2

                    if self.characterPosition[1] >= self.screenSize[1] - self.characterSize[1]/2:
                        self.characterPosition[1] = self.screenSize[1] - self.characterSize[1]/2
                checkScreenCollding()

                # 목표 지점 근처에 도달했는지 확인
                def is_reached():
                    return (
                        abs(self.characterPosition[0] - self.goalPosition[0]) < (self.characterSize[0]/2 + self.goalSize[0]/2) and
                        abs(self.characterPosition[1] - self.goalPosition[1]) < (self.characterSize[1]/2 + self.goalSize[1]/2)
                    )

                # 장애물과 충돌했는지 확인
                def is_collided():
                    for obstacle in self.obstacles:
                        if (
                            abs(self.characterPosition[0] - obstacle.position[0]) < (self.characterSize[0]/2 + obstacle.size[0]) and
                            abs(self.characterPosition[1] - obstacle.position[1]) < (self.characterSize[1]/2 + obstacle.size[1])
                        ):
                            return True
                    return False
                
                # 만약 목표 지점에 도달하면 게임 종료
                if is_reached():
                    self.endedByReachingGoal = True
                    self.lastlocation = self.characterPosition
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
                elif self.endedByReachingGoal:
                    return self.endedByReachingGoal

                elif self.endedByExtendedTimeLimit:
                    return self.endedByExtendedTimeLimit
                
                elif self.endedByObstacleColliding:
                    return self.endedByObstacleColliding
                
                # 종료 조건에 해당하지 않으면, 그 이벤트를 무시함
                else:
                    raise renpy.IgnoreEvent()

    #표시되는 시간은 해당 하나의 레벨에서 걸린 시간임. 이거로 나중에 이벤트 추가
    def display_s_score(st, at):
            return Text(_("소요 시간: ") + "%.3f" % game1.deltaTime, size=50, color="#40BFB7", outlines=[ (1, "#40BFB7", 0, 0) ]), None #font="gui/font/Gallagher.ttf"), .1

default game1 = Game1Diasplayable(0,[0,0])

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
    $ currentmap = 0
    $ lastlocation = [1000,300]

    # 객체의 기본값 설정(재시작 시 초기화에 사용됨)
    $ game1 = Game1Diasplayable(currentmap, lastlocation)
    call screen game1

    # 게임이 끝났으므로 다시 quick_menu 공개
label result_minigame1:

    #제한 시간과 클리어 시간을 비교함
    if game1.deltaTime <= minigame1_TimeLimits and game1.endedByObstacleColliding == False:
        if game1.last:
            "축하합니다! 게임을 클리어하셨습니다! (소요 시간: [game1.deltaTime:.3] 초)\n
            클릭을 통해 다시 스토리로 돌아갑니다"
            $ quick_menu = True
            window auto
        else:
            $ currentmap += 1
            $ lastlocation = game1.lastlocation
            $ game1 = Game1Diasplayable(currentmap, lastlocation)
            call screen game1
            call result_minigame1

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