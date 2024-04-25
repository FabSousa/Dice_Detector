import cv2
import Utils


cap = cv2.VideoCapture('dice_flip.mp4')

if not cap.isOpened():
    print("Erro ao abrir o vídeo.")
else:

    while True:

        ret, frame = cap.read()

        # if not ret:
        #     print("Fim do video")
            # break

        # Usar imagem no lugar do vídeo/camera
        frame = cv2.imread("dices.jpg")

        # frame = cv2.resize(frame, None, fx=0.8, fy=0.8, interpolation=cv2.INTER_AREA)

        img = Utils.preprocess(frame)
        all_dots, edges = Utils.get_dots(img)

        if all_dots is not None:

            dices = Utils.get_dices(all_dots)
            Utils.draw_dots(frame, dices)
            Utils.draw_sum(frame, dices)

        cv2.imshow("video", frame)
        # cv2.imshow("thresh", img)
        # cv2.imshow("edges", edges)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
