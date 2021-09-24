# Predict_paper_scite_project

https://project-physicphy.herokuapp.com/

### 목표
- 머신러닝으로 만든 서비스를 웹앱으로 배포한다.


### 세부 목표
- Flask를 이용해 웹 서비스 구축
- sql-alchemy, postgresql와 arxiv-api를 이용해서 논문 데이터를 수집 후 저장
- 수집한 데이터를 기반으로 Random Forest 모델을 학습 후 저장
- 선택한 모델을 사용해 예측한 결과를 웹에서 바로 확인
- heroku를 이용해 웹앱 배포


### 구성
- main <br>
: 상단의 navbar에서 하위 페이지들에 접근 가능
- add/delete paper <br>
: id, abstract, title을 key로 arxiv에서 원하는 논문을 읽어와 db에 추가/삭제 한다. 원하는 검색 구간(날짜)을 지정할 수 있다.
- load paper <br>
: id, abstract, title을 key로 db에서 원하는 논문을 읽어와 표시한다.
- create a training model <br>
: db내에서 특정 키워드에 해당하는 논문들을 이용해 scite를 예측하는 모델을 학습시킨 후 저장한다. 학습되어 db에 저장된 모델의 목록을 확인, 특정 모델을 db에서 삭제 시킬 수 있다.
- create new prediction <br>
: id, abstract, title을 key로 arxiv에서 어제/오늘자 논문 중에서 원하는 논문을 읽어온 뒤 선택한 모델을 이용해 scite 수를 예측한다.
-  load prediction of scites <br>
: db에 저장된 최근 예측했던 결과물들을 다시 읽어와 확인할 수 있다.