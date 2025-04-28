import os
import secrets
import io
from pypdf import PdfReader, PdfWriter, PaperSize
from pypdf.generic import RectangleObject
# Define a dictionary for paper sizes (dimensions in points)
PAPER_SIZES = {
    "A0":    {"width": 2383.94, "height": 3370.39},  # 841 x 1189 mm
    "A1":    {"width": 1683.78, "height": 2383.94},  # 594 x 841 mm
    "A2":    {"width": 1190.55, "height": 1683.78},  # 420 x 594 mm
    "A3":    {"width": 841.89,  "height": 1190.55},  # 297 x 420 mm
}

def resize_process_pdf(pdf_path: str, size: str, order_number: int, file_number: int):
    # Validate input file
    if not pdf_path.lower().endswith('.pdf'):
        raise ValueError("Input must be a PDF file.")
    
    # Process paper size
    size = size.upper()
    try:
        paper_size = getattr(PaperSize, size)
    except AttributeError:
        raise ValueError(f"Invalid paper size: {size}")

    # Read PDF into memory buffer
    with open(pdf_path, "rb") as f:
        pdf_data = io.BytesIO(f.read())
    
    reader = PdfReader(pdf_data)

    # Create output directory
    processed_dir = os.path.abspath("processed")
    os.makedirs(processed_dir, exist_ok=True)

    token = secrets.token_hex(8)
    pdf_page_files = []
    pdf_merger = PdfWriter()

    # Get dimensions from PaperSize
    portrait_width = paper_size.width
    portrait_height = paper_size.height

    for page_index, page in enumerate(reader.pages):
        # Get original dimensions
        current_width = float(page.mediabox.width)
        current_height = float(page.mediabox.height)

        # Determine target dimensions
        if current_width > current_height:  # landscape
            target_width = portrait_height
            target_height = portrait_width
        else:  # portrait
            target_width = portrait_width
            target_height = portrait_height

        # Calculate scaling factor
        scale = min(target_width / current_width, target_height / current_height)
        page.scale(scale, scale)
        
        # Update mediabox to target dimensions
        page.mediabox = RectangleObject([0, 0, target_width, target_height])
        
        # Add to merger
        pdf_merger.add_page(page)

        # Save individual page
        output_page_filename = f"output_{token}{size}{page_index}.pdf"
        output_page_path = os.path.join(processed_dir, output_page_filename)
        with PdfWriter() as page_writer:
            page_writer.add_page(page)
            with open(output_page_path, "wb") as f_out:
                page_writer.write(f_out)
        pdf_page_files.append(output_page_path)

    # Save merged PDF
    merged_pdf_filename = f"Order{order_number}_File{file_number}.pdf"
    merged_pdf_path = os.path.join(processed_dir, merged_pdf_filename)
    with open(merged_pdf_path, "wb") as f_out:
        pdf_merger.write(f_out)

    return merged_pdf_path, pdf_page_files

if __name__ == '__main__':
    input_dir = os.path.abspath("input")
    os.makedirs(input_dir, exist_ok=True)

    # Find all PDF files in input directory
    filelist = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    if not filelist:
        print("No PDF files found in 'input' directory.")
        exit(1)

    order_number_start = 1244
    file_number = 1

    for idx, filename in enumerate(sorted(filelist), start=0):
        input_pdf = os.path.join(input_dir, filename)
        if not os.path.isfile(input_pdf):
            print(f"Invalid file path: {input_pdf}")
            continue

        print(f"\nProcessing file: {filename} (Order #{order_number_start + idx}, File #{file_number})")

        try:
            merged_path, page_files = resize_process_pdf(
                input_pdf,
                size="A1",
                order_number=order_number_start + idx,
                file_number=file_number
            )

            print(" -> Merged PDF:", merged_path)
            print(" -> Individual pages:")
            for file in page_files:
                print("    -", os.path.basename(file))

            file_number += 1

        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")