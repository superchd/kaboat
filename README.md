## 결론:: 2021kaboat폴더가 최종 완성본 코드이므로 , 이 폴더만 보아도 무방하다.

* 2021 교내대회폴더 : gps값만 사용해서 모터를 제어했는데, 오차 때문에 실제로 사용하기 어렵다.
* gps폴더 : calcpoint.py // gps.py 두 py파일이 있을것이고, calcpoint.py를 모듈화 해서 gps.py를 사용한다.
* kaboat2021 : 대회나가서 사용한 젯슨나노를 백업한 폴더이다. **가장 중요하다** 
* lidar : 우리가 만든 알고리즘이 포함되어 있다. 여기서 ros master에 쏘는 토픽이 바로 **선회각**이다. 다만, 정확한 선회각 값은 kaboat2021에 있는 라이다 코드가 찾아 줄 것이다.  
* motor : 기본적으로 모터를 실행할때, 사용해야하는 모듈들이 저장되어 있다. 
* haemir : 아두이노로 모터를 제어할 때 사용했던 코드인데, 아두이노와 ros가 잘 호환되지 않아, 토픽을 publish 하고 subscribe하는데 에러가 많았던 코드들이다. 


## 다음은 대회영상 링크이다. 
https://drive.google.com/file/d/1APN4OoAvPmsEuWzBJlyPKRn7SXUSrTGf/view?usp=sharing
