import requests

from app.services.post_service import PostService


def publish_to_vk(user_id, post_content, images):
    """
    Publish a post to VK.
    :param post_content: Text content of the post.
    :param images: List of image URLs or file paths.
    """
    # Step 1: Upload images to VK
    token = PostService.get_user_token(user_id, 'vk')
    if not token:
        raise Exception("VK token not found for this user.")

    # Use the token to publish the post
    print(f"Publishing to VK: {post_content}")
    photo_ids = []
    for image in images:
        # Get upload server URL
        upload_url_response = requests.get(
            "https://api.vk.com/method/photos.getWallUploadServer",
            params={
                "access_token": token,
                "group_id": token.extra.get('VK_GROUP_ID'),
                "v": "5.131",  # API version
            },
        )
        upload_url = upload_url_response.json()["response"]["upload_url"]

        # Upload image
        with open(image, "rb") as file:
            upload_response = requests.post(upload_url, files={"photo": file})
        upload_data = upload_response.json()

        # Save uploaded photo
        save_response = requests.get(
            "https://api.vk.com/method/photos.saveWallPhoto",
            params={
                "access_token": token,
                "group_id": token.extra.get('VK_GROUP_ID'),
                "photo": upload_data["photo"],
                "server": upload_data["server"],
                "hash": upload_data["hash"],
                "v": "5.131",
            },
        )
        photo_ids.append(save_response.json()["response"][0]["id"])

    # Step 2: Publish the post
    attachments = ",".join([f"photo{photo_id}" for photo_id in photo_ids])
    response = requests.get(
        "https://api.vk.com/method/wall.post",
        params={
            "access_token": token,
            "owner_id": f"-{token.extra.get('VK_GROUP_ID')}",  # Group ID is negative
            "message": post_content,
            "attachments": attachments,
            "v": "5.131",
        },
    )
    if response.status_code != 200 or "error" in response.json():
        raise Exception(f"Failed to publish post to VK: {response.text}")