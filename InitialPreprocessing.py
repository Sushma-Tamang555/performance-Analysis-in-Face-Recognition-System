import os
import cv2

def preprocess_image(image_path, face_cascade, image_size):
    img = cv2.imread(image_path)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=5)
    
    # Skip the image if no face is detected
    if len(faces) == 0:
        print("No face detected in image:", image_path)
        return None
    
    preprocessed_img = img
    
    # Apply noise reduction to the entire image
    preprocessed_img = cv2.fastNlMeansDenoisingColored(preprocessed_img, None, 3, 3, 7, 21)
    
    # Normalize color contrast of the entire image
    preprocessed_img = cv2.normalize(preprocessed_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

    return preprocessed_img


def generate_preprocessed_images(input_dir, output_dir):
    # Define parameters for face detection and image resizing
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    IMAGE_SIZE = 224

    # Loop over all the folders and images in the input directory
    for root, dirs, files in os.walk(input_dir):
        for dirname in dirs:
            # Create a new directory for the user in the output directory
            output_user_dir = os.path.join(output_dir, dirname)
            if not os.path.exists(output_user_dir):
                os.makedirs(output_user_dir)
        for filename in files:
            if filename.endswith('.jpg') or filename.endswith('.JPEG') or filename.endswith('.png'):
                # Preprocess the image and save it in the output directory
                image_path = os.path.join(root, filename)
                preprocessed_img = preprocess_image(image_path, face_cascade, IMAGE_SIZE)
                if preprocessed_img is not None:
                    # Save the preprocessed image in the user's output directory
                    user_dir = os.path.basename(root)
                    output_user_dir = os.path.join(output_dir, user_dir)
                    output_path = os.path.join(output_user_dir, filename)
                    cv2.imwrite(output_path, preprocessed_img)
                else:
                    # Skip the image if no face is detected
                    print(f"Skipping image {image_path} due to no face detected")
                    continue

    print('Done preprocessing images.')

# generate_preprocessed_images("TestImagesRaw", "TestImages")
# generate_preprocessed_images("TrainImagesRaw", "TrainImages")

