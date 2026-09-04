import serpapi

def find_social_match(image_path, api_key):
    print(f"[*] Initiating genuine reverse image search for: {image_path}")
    try:
        client = serpapi.Client(api_key=api_key)
        
        print("[*] Uploading image to Google Lens engine...")
        # Upload local image to get a temporary image_id
        upload = client.upload_image(image_path)
        
        print("[*] Scanning the web for exact visual matches...")
        # Run the search using the image_id
        results = client.search({
            "engine": "google_lens",
            "image_id": upload["image_id"]
        })
        
        # Parse the first real social/web match
        matches = results.get("visual_matches", [])
        
        if matches:
            best_match_url = matches[0].get("link")
            print(f"[+] SUCCESS! Found matching record:")
            print(f"    -> {best_match_url}")
            return best_match_url
        else:
            print("[-] No visual matches found.")
            return None
            
    except Exception as e:
        print(f"[-] Search API error: {e}")
        return None

# Test the module
if __name__ == "__main__":
    # Paste your free SerpApi key inside the quotes below
    SERPAPI_KEY = "a7a8fc60d40ba99808892699b523d706c64b961b414475164c249ef474e17c53"
    
    match = find_social_match("test.jpg", SERPAPI_KEY)
    if match:
        print("[*] Module 2 is ready for the pipeline.")