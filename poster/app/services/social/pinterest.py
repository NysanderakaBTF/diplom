import requests

from app.services.post_service import PostService


def publish_to_pinterest(user_id, post_content, images):
    """
    Publish a post to Pinterest.
    :param post_content: Text content of the post.
    :param images: List of image URLs or file paths.
    """

    token = PostService.get_user_token(user_id, 'pinterest')
    if not token:
        raise Exception("Pinterest token not found for this user.")

    # Use the token to publish the post
    print(f"Publishing to Pinterest: {post_content}")
    for image in images:
        url = "https://api.pinterest.com/v5/pins"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        payload = {
            "title": post_content,
            "description": post_content,
            "board_id": token,
            "media_source": {
                "source_type": "image_url",
                "url": image,  # URL of the image
            },
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 201:
            raise Exception(f"Failed to publish post to Pinterest: {response.text}")