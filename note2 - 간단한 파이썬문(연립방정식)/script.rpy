# 2. 렌파이로 이전 계산 결과 저장하는 연립방정식 풀기 구현
# 이 파일에 게임 스크립트를 입력합니다.
# image 문을 사용해 이미지를 정의합니다.
# image 사진을 부를 변수명 = "이름.확장자"

# 게임에서 사용할 캐릭터를 정의합니다.
# define 이름 = Character(str, color = #RGB)
define e = Character('송붕이', color="#c8ffc8")

# 변수 선언
define x = 0.0
define y = 0.0
define a1 = 0
define b1 = 0
define c1 = 0
define a2 = 0
define b2 = 0
define c2 = 0
define flag = 'X'
define isZeroDeterminants = False
define determinant = 0

# persistent에 속하는 변수 정의
define persistent.calculated = None
define persistent.x = 0
define persistent.y = 0
define persistent.count = 0

# 여기에서부터 게임이 시작합니다.
label start:
    e "난 미지수가 2개인 연립방정식을 풀 수 있는 계산기야\n
    개발자의 능지 이슈로 계수는 아직 한 자리 정수(0~9)만 가능해\n
    현재 사용 횟수: [persistent.count]회"
    if persistent.calculated == True:
        e "최근의 계산 결과: (x = [persistent.x:.3], y = [persistent.y:.3])"

    e "순서에 맞춰 계수와 변수들을 입력해줄래?\n
    ax + by = c꼴로 공백 없이 식 2개를 입력해줘"
    $str1 = renpy.input("첫 번째 식; ax+by=c꼴로 계수들을 알려줘: ")
    $str2 = renpy.input("두 번째 식; ax+by=c꼴로 계수들을 알려줘: ")
    python:
        #일단 먼저 입력이 잘 됐는지 확인한다.
        while flag != 'Y' and flag != 'N':
            flag = renpy.input("너가 입력한 식이 이게 맞니? [str1]\n[str2]\nY/N으로 대답해줘")
            if flag == 'Y':
                break
            if flag == 'N':
                renpy.say(e, "알빠노?\n그냥 이걸로 계산할게")
                break
            renpy.say(e, "\n유효하지 않은 입력이야" )
        renpy.say(e, "계산 중이야.." )

        #각각의 스트링을 숫자로 변환한다.
        a1 = int(str1[0])
        b1 = int(str1[3])
        c1 = int(str1[6])
        a2 = int(str2[0])
        b2 = int(str2[3])
        c2 = int(str2[6])
        
        #renpy.random.randint(0, 9)를 돌려서 설정할 수도 있음
        #괄호의 값을 양 끝으로 하는 폐구간에서 수를 뽑음
        #renpy.random.choice로 list 원소 중 하나를 뽑게 할 수도 있음
        determinant = a1*b2 - a2*b1 
        if determinant == 0:
            isZeroDeterminants = True
        else:
            #Cramer's Rule 적용
            x = float(c1*b2 - c2*b1)/float(determinant)
            y = float(- c1*a2 + c2*a1)/float(determinant)
    
    if isZeroDeterminants == True:
        e "지금 이딴 걸 계산하라는 거야?\n
        넌 이따위로 눈치가 없으니까 연애를 못 하는거야."
    else:
        e "계수를 잘 입력해 줬구나!\n
        소수점 두 자리까지 답을 출력해 줄게: x = [x:.3], y = [y:.3]\n\n
        다음에 또 봐~"

        if persistent.calculated == None:
            $persistent.calculated = True;

        $persistent.x = x
        $persistent.y = y
        $persistent.count += 1
    return