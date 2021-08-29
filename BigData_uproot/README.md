### 대용량의 데이터를 uproot 로 처리하는 패키지 입니다.
1. [selector.py](https://github.com/groupKNUPHY/Bootcamp/blob/main/BigData_uproot/selector.py)  
이벤트를 selection 하는 메인 analysis code입니다. output으로 Ntuple 만듭니다. 파일 여러개를 받아서 처리할 수 있게 Iterator method 를 사용합니다.

2. [execute.py](https://github.com/groupKNUPHY/Bootcamp/blob/main/BigData_uproot/execute.py)  
본 패키지를 실행하는 코드입니다. 여기서 batch size 는 파일 개수를 의미하고 최대 몇개의 파일을 selector 코드의 인풋으로 보낼지 정합니다.
예를 들어 1부터 100가지의 파일을 batchsize 20 으로 실행하면 1-20 21-40 41-60 61-80 81-100 총 5번의 Run을 하게되고 아웃풋으로 5개의 파일울 생성시킵니다.  
주의할점은 selector 에 concatenate 연산이 존재해서 RAM이 감당할 수 있는 만큼의 양을 잘 정해야합니다.

3. [draw.py](https://github.com/groupKNUPHY/Bootcamp/blob/main/BigData_uproot/draw.py)  
Ntuple 을 읽어서 합친 후 histogram을 그립니다.  
Ntuple 사이즈가 클 때를 대비하기위해 기존의 Ntuple concatenate -> histograming 방식이 아닌,  
histograming -> stack y axis 방식으로 최적화 하였습니다.  
이 방법을 적용하려고 matplotlib.pyplot.hist 이 아닌 mplhep.histplot 을 이용하였습니다.  
