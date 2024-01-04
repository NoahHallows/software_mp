#EDITING IMAGES
import cv2 as cv

def blur(image_bgr, target_face_location, used_kcf, scale_factor):
    # Unpack the location
    if used_kcf == False:
        top, right, bottom, left = target_face_location
        # Scale face_location coordinates up to the original image size
        top = int(top / scale_factor)
        right = int(right / scale_factor)
        bottom = int(bottom / scale_factor)
        left = int(left / scale_factor)
        # Calculate the width and height of the bounding box
        width = right - left
        height = bottom - top
    #Because KCF returns (x, y, width, height)
    elif used_kcf == True:
        x, y, width, height = target_face_location
        top = y
        left = x
        bottom = y + height
        right = x + width
    # Increase the region slightly to make sure the entire face is covered
    top = max(top - 10, 0)
    right = min(right + 10, image_bgr.shape[1])
    bottom = min(bottom + 10, image_bgr.shape[0])
    left = max(left - 10, 0)

    # Select the region of interest (ROI) where the face is located
    face_roi = image_bgr[top:bottom, left:right]

    # Apply a Gaussian blur to the face region
    blurred_face = cv.GaussianBlur(face_roi, (99, 99), 0)

    # Replace the original image region with the blurred face
    image_bgr[top:bottom, left:right] = blurred_face

    return image_bgr

def replace(background, overlay, target_face_location, used_kcf, scale_factor):
    # Unpack the location
    if used_kcf == False:
        top, right, bottom, left = target_face_location
        # Scale face_location coordinates up to the original image size
        top = int(top / scale_factor)
        right = int(right / scale_factor)
        bottom = int(bottom / scale_factor)
        left = int(left / scale_factor)
        # Calculate the width and height of the bounding box
        width = right - left
        height = bottom - top
    #Because KCF returns (x, y, width, height)
    elif used_kcf == True:
        x, y, width, height = target_face_location
        top = y
        left = x
        bottom = y + height
        right = x + width

    # Expand the bounding box by the constant value
    top = max(0, top - 10)
    bottom = min(background.shape[0], bottom + 10)
    left = max(0, left - 10)
    right = min(background.shape[1], right + 10)
    width = width + 20
    height = height + 20

    # Ensure the width and height are positive before resizing
    if width > 0 and height > 0:
        overlay_resized = cv.resize(overlay, (width, height))
    else:
        # Handle the invalid size case, e.g., by skipping the resizing or setting a default size
        print(f"Invalid size for resize operation: width={width}, height={height}")
        return background 

    # Check if overlay image has an alpha channel (transparency)
    if overlay_resized.shape[2] == 4:
        # Split overlay into color and alpha channels
        overlay_color = overlay_resized[:, :, :3]
        alpha_mask = overlay_resized[:, :, 3] / 255.0

        # Get the ROI from the background and blend using the alpha mask
        roi = background[top:bottom, left:right]
        roi = cv.addWeighted(overlay_color, alpha_mask, roi, 1 - alpha_mask, 0, roi)

        # Put the blended ROI back into the background
        background[top:bottom, left:right] = roi
    else:
        # If no alpha channel, just replace the ROI with the resized overlay
        background[top:bottom, left:right] = overlay_resized

    return background