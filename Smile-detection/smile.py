import cv2

faccascade=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') 
smilecascade=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

cap=cv2.VideoCapture(0)

while True:
    ret,frame=cap.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=faccascade.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray=gray[y:y+h,x:x+w]
        roi_color=frame[y:y+h,x:x+w]
        smiles=smilecascade.detectMultiScale(roi_gray,scaleFactor=1.8,minNeighbors=20)

        for (sx,sy,sw,sh) in smiles:
            cv2.rectangle(roi_color,(sx,sy),(sx+sw,sy+sh),(0,255,0),2)

            cv2.rectangle(roi_color,(sx,sy),(sx+sw,sy+sh),(0,255,0),2)

            cv2.putText(frame,"Smiling",(x,y+h+30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            break

    cv2.imshow("Smile Detector",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
