import os
import tempfile
from PIL import Image
import qrcode


def generate_qr(data, qr_size=540):
    """
    generate a QR code to a tempdir and return the path
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    temp_dir = tempfile.mkdtemp()
    qr_path = os.path.join(temp_dir, "qr.png")
    qr_img.save(qr_path)
    return qr_path


def generate_qr_with_bg(data, output_path, bg_image_path="/backend/qr-bg.png", line_image_path="/backend/line.png",
                        side_block="/backend/sideblock.png", position=(322, 1035)):
    """
    生成带背景图和线条的二维码

    :param data: 二维码的数据
    :param bg_image_path: 背景图片路径
    :param output_path: 生成图片保存路径
    :param qr_size: 二维码大小（正方形边长，像素）
    :param line_image_path: 线条图片路径
    :param position: 二维码放置在背景图上的位置 (x, y)
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#06c655", back_color="white")
    qr_img = qr_img.resize((540, 540), Image.Resampling.LANCZOS)
    side_block_img = Image.open(side_block).convert("RGBA")
    side_block_img = side_block_img.resize((84, 84), Image.Resampling.LANCZOS)
    new_image = Image.new("RGB", (540, 540), "white")
    for i in range(45):
        for j in range(45):
            x1 = i * 12
            y1 = j * 12
            x2 = (i + 1) * 12
            y2 = (j + 1) * 12
            cropped_image = qr_img.crop((x1 + 2, y1 + 2, x2 - 2, y2 - 2))
            new_image.paste(cropped_image, (x1 + 2, y1 + 2))
    qr_img = new_image
    qr_img.paste(side_block_img, (4 * 12 + 1, 4 * 12 + 1), side_block_img)
    qr_img.paste(side_block_img, (34 * 12 + 1, 4 * 12 + 1), side_block_img)
    qr_img.paste(side_block_img, (4 * 12 + 1, 34 * 12 + 1), side_block_img)
    
    try:
        line_img = Image.open(line_image_path).convert("RGBA")
        # 计算线条图片的放置位置，使其位于二维码中央
        line_img = line_img.resize((156, 60), Image.Resampling.LANCZOS) # 将线条图片缩小50%
        line_x = (540 - line_img.width) // 2
        line_y = (540 - line_img.height) // 2
        qr_img.paste(line_img, (line_x, line_y), line_img)
    except FileNotFoundError:
        print(f"Warning: line image not found at {line_image_path}. Proceeding without line image.")

    bg_img = Image.open(bg_image_path).convert("RGBA")
    bg_img.paste(qr_img, position)
    bg_img.save(output_path)
