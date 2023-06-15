import cv2

cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("rtsp://192.168.1.109:8080/h264_pcm.sdp")

# tracker = cv2.TrackerMOSSE_create()
tracker = cv2.legacy.TrackerMOSSE_create()
# tracker = cv2.legacy.TrackerCSRT_create()
check, frame = cap.read()
bbox = cv2.selectROI("Tracking", frame, False)
tracker.init(frame, bbox)


def drawBox(frame, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3, 1)
    cv2.putText(frame, "Tracking", (75, 75),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


while True:
    timer = cv2.getTickCount()
    check, frame = cap.read()

    check, bbox = tracker.update(frame)
    if check:
        drawBox(frame, bbox)
    else:
        cv2.putText(frame, "Lost", (75, 75),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    cv2.putText(frame, str(int(fps)), (75, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Output", frame)

    if cv2.waitKey(1) & 0xFF == ord("e"):
        break

cap.release()
cv2.destroyAllWindows()
