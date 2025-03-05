import requests

from app.services.post_service import PostService


def publish_to_instagram(user_id, post_content, images):
    token = PostService.get_user_token(user_id, 'instagram')
    if not token:
        raise Exception("Instagram token not found for this user.")

    # Use the token to publish the post
    print(f"Publishing to Instagram: {post_content}")
    """
    Publish a post to Instagram.
    :param post_content: Text content of the post.
    :param images: List of image URLs or file paths.
    """
    # Step 1: Upload image(s) to Instagram
    image_id = None
    for image in images:
        url = f"https://graph.facebook.com/v18.0/{token}/media"
        payload = {
            "image_url": image,  # URL of the image
            "caption": post_content,
            "access_token": token,
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            image_id = response.json().get("id")
        else:
            raise Exception(f"Failed to upload image to Instagram: {response.text}")

    # Step 2: Publish the post
    if image_id:
        url = f"https://graph.facebook.com/v18.0/{token}/media_publish"
        payload = {
            "creation_id": image_id,
            "access_token": token,
        }
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            raise Exception(f"Failed to publish post to Instagram: {response.text}")
    else:
        raise Exception("No image ID found for Instagram post.")