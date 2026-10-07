import os
from PIL import Image, ImageEnhance, ImageFilter


def enhance_image(
    input_path,
    output_path=None,
    brightness=1.0,
    contrast=1.0,
    color=1.0,
    sharpness=1.0,
    denoise=False
):
    """
    Enhance an image using Pillow.

    Enhancement factors:
        1.0 = original
        >1.0 = increase
        <1.0 = decrease

    Returns:
        output_path
    """

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Image not found: {input_path}")

    with Image.open(input_path) as image:
        # Convert to RGB/RGBA-compatible image when necessary
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGB")

        # Brightness
        if brightness != 1.0:
            image = ImageEnhance.Brightness(image).enhance(brightness)

        # Contrast
        if contrast != 1.0:
            image = ImageEnhance.Contrast(image).enhance(contrast)

        # Color / saturation
        if color != 1.0:
            image = ImageEnhance.Color(image).enhance(color)

        # Sharpness
        if sharpness != 1.0:
            image = ImageEnhance.Sharpness(image).enhance(sharpness)

        # Optional lightweight denoising
        if denoise:
            image = image.filter(ImageFilter.MedianFilter(size=3))

        # Generate output path automatically
        if output_path is None:
            filename, extension = os.path.splitext(input_path)
            output_path = f"{filename}_enhanced{extension}"

        # JPEG cannot save RGBA directly
        if output_path.lower().endswith((".jpg", ".jpeg")):
            if image.mode == "RGBA":
                image = image.convert("RGB")

        image.save(output_path)

    return output_path
