import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from PIL import Image
import matplotlib.pyplot as plt

def encrypt_bmp_ecb(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        bmp_data = f.read()

    # BMP szerkezet: a header resz, amely 54 bajtos + a pixel resz
    header = bmp_data[:54]
    pixel_data = bmp_data[54:]

    # titkositas ecb-vel
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_pixels = cipher.encrypt(pad(pixel_data, AES.block_size))

    # a BMP szerkezet visszaallitasa, a titkositott pixelekkel
    encrypted_bmp = header + encrypted_pixels

    with open(output_file, 'wb') as f:
        f.write(encrypted_bmp)
    return encrypted_bmp


def encrypt_bmp_cbc(input_file, output_file, key):
    # ugyanaz, csak most cbc-vel titkositunk
    with open(input_file, 'rb') as f:
        bmp_data = f.read()

    header = bmp_data[:54]
    pixel_data = bmp_data[54:]

    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_pixels = cipher.encrypt(pad(pixel_data, AES.block_size))

    encrypted_bmp = header + encrypted_pixels

    with open(output_file, 'wb') as f:
        f.write(encrypted_bmp)
    return encrypted_bmp


def display_images(original_file, ecb_file, cbc_file=None):
    # az eredeti es titkositott kepek megjelenitese
    fig, axes = plt.subplots(1, 3 if cbc_file else 2, figsize=(15, 5))

    # eredeti kep
    original_img = Image.open(original_file)
    axes[0].imshow(original_img)
    axes[0].set_title('Az eredeti BMP')
    axes[0].axis('off')

    # ECB-vel titkositott kep
    ecb_img = Image.open(ecb_file)
    axes[1].imshow(ecb_img)
    axes[1].set_title('ECB titkositas')
    axes[1].axis('off')

    # CBC-vel titkositott kep
    if cbc_file:
        cbc_img = Image.open(cbc_file)
        axes[2].imshow(cbc_img)
        axes[2].set_title('CBC titkositas')
        axes[2].axis('off')

    plt.tight_layout()
    plt.show()


def demonstrate_with_real_image():
    key = os.urandom(16)
    encrypt_bmp_ecb('penguin.bmp', 'penguin_ecb.bmp', key)
    encrypt_bmp_cbc('penguin.bmp', 'penguin_cbc.bmp', key)

    display_images('penguin.bmp', 'penguin_ecb.bmp', 'penguin_cbc.bmp')


demonstrate_with_real_image()
