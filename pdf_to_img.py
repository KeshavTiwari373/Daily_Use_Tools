from pdf2image import convert_from_path
import os

def pdf_to_images(pdf_path, output_folder, dpi=300, output_format='png'):
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Convert PDF to images
    images = convert_from_path(pdf_path, dpi=dpi)

    # Save images
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f'page_{i+1}.{output_format}')
        image.save(image_path, output_format.upper())

    print(f"Conversion complete! Images saved in: {output_folder}")

# Example usage
pdf_file = "./res.pdf"
output_dir = "./output_images"

pdf_to_images(pdf_file, output_dir)