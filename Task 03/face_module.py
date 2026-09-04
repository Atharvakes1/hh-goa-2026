from deepface import DeepFace
import warnings

# Suppress the Mac SSL warning so our hacker terminal stays clean
warnings.filterwarnings("ignore")

def encode_face(image_path):
    print(f"[*] Scanning face in: {image_path}...")
    try:
        # Switched to 'retinaface' backend for ultra-accurate detection
        embedding_objs = DeepFace.represent(
            img_path=image_path, 
            model_name="Facenet", 
            detector_backend="retinaface", 
            enforce_detection=True
        )
        
        # Extract the actual encoding list
        face_encoding = embedding_objs[0]["embedding"]
        print("[+] Face successfully detected and encoded!")
        print(f"[+] Encoding length: {len(face_encoding)} dimensions")
        
        return face_encoding
        
    except ValueError:
        print("[-] No face detected in the image. Try a clearer photo.")
        return None
    except Exception as e:
        print(f"[-] An error occurred: {e}")
        return None

# Test the module
if __name__ == "__main__":
    test_image = "test.jpg" 
    encoding = encode_face(test_image)
    
    if encoding:
        print("[*] Module 1 is ready for the pipeline.")