import os
import time
import pyautogui
from threading import Thread

 
def Async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

@Async
def runboxman():
    try:
        os.system('.\\BoxMan\\BoxMan.exe')
    except:
        print('Error!')
        exit

pyautogui.PAUSE = 0.1
pyautogui.FAILSAFE = True
CaseList = [1, 10, 30, 40, 50]
CaseTxtList = ['./cases/Case1.txt', './cases/Case2.txt', './cases/Case3.txt', './cases/Case4.txt', './cases/Case5.txt']

print('>>> Auto Testing Scripts by Karl')
print('>>> Have Fun ~\n')
print('>>> Running BoxMan...')

runboxman()

time.sleep(1)

os.remove('./TestLog.txt')

for i in range(len(CaseList)):
    if not os.path.exists(CaseTxtList[i]):
        print('Level ' + str(CaseList[i]) + ' Unsolved!')
        time.sleep(0.5)
        continue

    print('>>> Current Test Case: ' + 'Level ' + str(CaseList[i]))
    pyautogui.press('f3')
    pyautogui.typewrite(str(CaseList[i]))
    time.sleep(0.5)
    pyautogui.press('enter')
    
    print('Auto play in 3s...')
    time.sleep(1)
    print('Auto play in 2s...')
    time.sleep(1)
    print('Auto play in 1s...')
    time.sleep(1)
    print('Go!')

    steps = 0
    with open(CaseTxtList[i], 'r') as txt:
        for lines in txt.readlines():
            steps += 1
            op = lines.split()[0][6:]
            print(op)
            pyautogui.press(op)
            time.sleep(0.1)
    time.sleep(0.5)
    print('>>> Clear in %d steps.' % steps)
    print('>>> Level '+str(CaseList[i])+' Cleared.')
    with open('./TestLog.txt', 'a') as txt:
        txt.write('>>> Current Test Case: ' + 'Level ' + str(CaseList[i]) + '\n')
        txt.write('>>> Clear in %d steps.' % steps + '\n')
        txt.write('>>> Level '+str(CaseList[i])+' Cleared.\n\n')
    time.sleep(1.5)


