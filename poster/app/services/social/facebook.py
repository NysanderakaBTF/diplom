import requests

from app.services.post_service import PostService


def publish_to_facebook(user_id, post_content, images):
    """
    Publish a post to Facebook.
    :param post_content: Text content of the post.
    :param images: List of image URLs or file paths.
    """
    token = PostService.get_user_token(user_id, 'facebook')
    if not token:
        raise Exception("Facebook token not found for this user.")

    # Use the token to publish the post
    print(f"Publishing to Facebook: {post_content}")
    url = f"https://graph.facebook.com/v18.0/{token.extra.get('FACEBOOK_PAGE_ID')}/photos"
    for image in images:
        payload = {
            "url": image,  # URL of the image
            "message": post_content,
            "access_token": token,
        }
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            raise Exception(f"Failed to publish post to Facebook: {response.text}")