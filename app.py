
import os
import cv2
import numpy as np
from ultralytics import YOLO
from category_mapping import map_to_category, CATEGORY_COLORS, PLATFORMS_PER_OBJECT

CONFIDENCE_THRESHOLD = 0.35
DETECTION_MODEL_NAME = "yolov8n.pt"

WEBCAM_INDEX = 0

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
FRAME_FPS = 30

FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.6
THICKNESS = 2

ICON_SIZE = (40, 40)

def load_icon(path, size=ICON_SIZE):
    icon = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if icon is not None:
        icon = cv2.resize(icon, size, interpolation=cv2.INTER_AREA)
    return icon


TICK_ICON = load_icon("tick.png")
WARN_ICON = load_icon("warning.png")
CROSS_ICON = load_icon("cross.png")


def draw_box_and_label(img, box, label, color, conf=None):
    x1, y1, x2, y2 = map(int, box)

    cv2.rectangle(img, (x1, y1), (x2, y2), color, THICKNESS)

    text = label if conf is None else f"{label} {conf:.2f}"
    (w, h), _ = cv2.getTextSize(text, FONT, FONT_SCALE, THICKNESS)

    cv2.rectangle(img, (x1, y1 - h - 8), (x1 + w + 8, y1), color, -1)
    cv2.putText(
        img,
        text,
        (x1 + 4, y1 - 6),
        FONT,
        FONT_SCALE,
        (0, 0, 0),
        THICKNESS // 2,
        cv2.LINE_AA,
    )


def draw_platform_info(img, box, platforms, color):

    x1, y1, x2, y2 = map(int, box)

    if platforms > 4:
        text = "TOO BIG"
    else:
        text = str(platforms)

    (w, h), _ = cv2.getTextSize(text, FONT, FONT_SCALE, THICKNESS)

    bg_x1 = x1
    bg_y1 = y2 + 4
    bg_x2 = x1 + w + 8
    bg_y2 = y2 + h + 12

    bg_y2 = min(bg_y2, img.shape[0] - 1)

    cv2.rectangle(img, (bg_x1, bg_y1), (bg_x2, bg_y2), color, -1)
    cv2.putText(
        img,
        text,
        (bg_x1 + 4, bg_y2 - 4),
        FONT,
        FONT_SCALE,
        (0, 0, 0),
        THICKNESS // 2,
        cv2.LINE_AA,
    )


def estimate_damage_heuristic(crop):

    if crop is None or crop.size == 0:
        return "ok"

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 80, 160)

    edge_pixels = np.count_nonzero(edges)
    area = crop.shape[0] * crop.shape[1]
    if area == 0:
        return "ok"

    density = edge_pixels / float(area)

    if density > 0.06:
        return "cross"
    else:
        return "ok"

def overlay_icon(frame, icon, x, y):
    if icon is None:
        return frame

    h, w = icon.shape[:2]

    x1, y1 = max(0, x), max(0, y)
    x2, y2 = x1 + w, y1 + h

    if x1 >= frame.shape[1] or y1 >= frame.shape[0]:
        return frame

    if x2 > frame.shape[1]:
        w = frame.shape[1] - x1
        icon = icon[:, :w]
        x2 = frame.shape[1]

    if y2 > frame.shape[0]:
        h = frame.shape[0] - y1
        icon = icon[:h, :]
        y2 = frame.shape[0]

    if icon.ndim == 3 and icon.shape[2] == 4:
        alpha_s = icon[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(3):
            frame[y1:y2, x1:x2, c] = (
                alpha_s * icon[:, :, c]
                + alpha_l * frame[y1:y2, x1:x2, c]
            )
    else:
        frame[y1:y2, x1:x2] = icon

    return frame

def main():
    print("Loading detection model (COCO yolov8n)...")
    detector = YOLO(DETECTION_MODEL_NAME)

    cap = cv2.VideoCapture(WEBCAM_INDEX)
    if not cap.isOpened():
        print("Cannot open webcam. Check WEBCAM_INDEX.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FRAME_FPS)

    actual_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Camera resolution: {int(actual_w)}x{int(actual_h)}, FPS: {actual_fps:.1f}")

    window_name = "Object category & furniture damage (local heuristic)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1920, 1080)

    print("Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = detector.track(
            source=frame,
            persist=True,
            imgsz=320,
            conf=CONFIDENCE_THRESHOLD,
            verbose=False
        )

        r = results[0]

        if hasattr(r, "boxes") and r.boxes is not None:
            for box_obj in r.boxes:
                conf = float(box_obj.conf[0]) if hasattr(box_obj, "conf") else None
                cls_id = int(box_obj.cls[0]) if hasattr(box_obj, "cls") else None

                class_name = detector.names.get(cls_id, str(cls_id))

                category = map_to_category(class_name)
                if category is None:
                    continue

                color = CATEGORY_COLORS.get(category, (255, 255, 255))

                if hasattr(box_obj, "xyxy"):
                    xyxy = box_obj.xyxy[0].cpu().numpy()
                else:
                    xyxy = np.array([0, 0, 0, 0], dtype=float)

                draw_box_and_label(frame, xyxy, category, color, conf)

                platforms_needed = PLATFORMS_PER_OBJECT.get(class_name, 1)
                draw_platform_info(frame, xyxy, platforms_needed, color)

                if category.lower() == "furniture":
                    x1, y1, x2, y2 = map(int, xyxy)

                    x1_cl = max(0, min(x1, frame.shape[1] - 1))
                    x2_cl = max(0, min(x2, frame.shape[1]))
                    y1_cl = max(0, min(y1, frame.shape[0] - 1))
                    y2_cl = max(0, min(y2, frame.shape[0]))

                    if x2_cl > x1_cl and y2_cl > y1_cl:
                        crop = frame[y1_cl:y2_cl, x1_cl:x2_cl]

                        state = estimate_damage_heuristic(crop)
                        if state == "ok":
                            icon = TICK_ICON
                        elif state == "warning":
                            icon = WARN_ICON
                        else:
                            icon = CROSS_ICON

                        icon_y = max(y1_cl - ICON_SIZE[1] - 5, 0)
                        frame = overlay_icon(frame, icon, x1_cl, icon_y)

        cv2.imshow(window_name, frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
