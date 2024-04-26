import cv2
import Utils


cap = cv2.VideoCapture('dice_roll.mp4')

if not cap.isOpened():
    print("Erro ao abrir o vídeo.")
else:

    prev_dots = 0
    prev_dots_loop = 0
    loop = 0
    prev_dices = []
    # FRAME_DELAY = 10
    FRAME_DELAY = 5
    
    while True:
        loop = loop + 1
        ret, frame = cap.read()

        if not ret:
            print("Fim do video")
            break

        frame = cv2.resize(frame, None, fx=0.3, fy=0.3, interpolation=cv2.INTER_AREA)

        img = Utils.preprocess(frame)
        all_dots, edges = Utils.get_dots(img)

        if all_dots is not None:

            dices = Utils.get_dices(all_dots)

            if len(all_dots) != prev_dots:
                if (loop - prev_dots_loop)>=FRAME_DELAY:
                    prev_dots = len(all_dots)
                    prev_dices = dices
            else:
                prev_dots_loop = loop
            # Utils.draw_dots(frame, prev_dices)
            Utils.draw_sum(frame, prev_dices)

        cv2.imshow("video", frame)
        cv2.imshow("thresh", img)
        cv2.imshow("edges", edges)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
