import zipfile
import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

def create_watermark(watermark_text, page_width):
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)  # Use Helvetica-Bold for bold text
    c.setFillColorRGB(0, 0, 0, 1)  # Black with transparency

    # Convert page width to float to handle arithmetic
    page_width = float(page_width)
    
    # Calculate the position for the watermark (center horizontally, bottom vertically)
    text_width = c.stringWidth(watermark_text, "Helvetica-Bold", 16)  # Width of the watermark text
    x_position = (page_width - text_width) / 2  # Center the text horizontally
    y_position = 30  # Position watermark 30 units from the bottom

    # Draw the watermark text (bold)
    c.drawString(x_position, y_position, watermark_text)
    
    # Permalink text
    permalink_text = "https://chat.whatsapp.com/J1yWn2VENBaCGOaxJKSt6F"
    permalink_x_position = (page_width - c.stringWidth(permalink_text, "Helvetica-Bold", 16)) / 2  # Center horizontally
    c.drawString(permalink_x_position, y_position - 20, permalink_text)
    
    # Draw a line under the permalink text to simulate underlining
    c.line(permalink_x_position, y_position - 25, permalink_x_position + c.stringWidth(permalink_text, "Helvetica-Bold", 16), y_position - 25)

    c.save()
    packet.seek(0)
    return packet

def add_watermark(input_pdf, watermark_text):
    try:
        # If no watermark text is provided, set a default value
        if not watermark_text:
            watermark_text = "Join For More:"

        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        # Iterate through each page
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]

            # Create watermark for the current page based on page width
            watermark_pdf = create_watermark(watermark_text, page.mediabox.width)
            watermark_reader = PdfReader(watermark_pdf)
            watermark_page = watermark_reader.pages[0]

            # Merge watermark with the page
            page.merge_page(watermark_page)
            writer.add_page(page)

        # Output the modified PDF to a BytesIO object
        output_pdf = BytesIO()
        writer.write(output_pdf)
        return output_pdf

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def process_zip(input_zip, output_zip, watermark_text):
    try:
        # Add .zip extension if missing
        if not input_zip.lower().endswith('.zip'):
            input_zip += '.zip'
        if not output_zip.lower().endswith('.zip'):
            output_zip += '.zip'

        # Create a new ZIP file to store the modified PDFs
        with zipfile.ZipFile(input_zip, 'r') as zip_ref:
            # Prepare to write the output zip file
            with zipfile.ZipFile(output_zip, 'w') as zip_output:
                # Extract all the PDFs and process them
                for file_name in zip_ref.namelist():
                    if file_name.lower().endswith('.pdf'):
                        # Extract PDF from the zip
                        pdf_data = zip_ref.read(file_name)

                        # Create a temporary file to store the extracted PDF
                        with open("temp_input.pdf", "wb") as temp_pdf:
                            temp_pdf.write(pdf_data)

                        # Add watermark to the extracted PDF
                        modified_pdf = add_watermark("temp_input.pdf", watermark_text)

                        if modified_pdf:
                            # Generate the output PDF file name with '-TechByMehdi' before the extension
                            base_name, ext = os.path.splitext(file_name)
                            modified_file_name = base_name + '-TechByMehdi' + ext

                            # Save the modified PDF to the output ZIP file with the new name
                            zip_output.writestr(modified_file_name, modified_pdf.getvalue())
                            print(f"✅ Watermark added to '{file_name}' -> saved as '{modified_file_name}'")

        # Clean up temporary file
        os.remove("temp_input.pdf")
        print(f"✅ ZIP file created successfully: {output_zip}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

# Example usage
input_zip = input("Please enter the input ZIP file name (without .zip): ")  # Input ZIP file
output_zip = input("Please enter the output ZIP file name (without .zip): ")  # Output ZIP file
watermark_text = input("Please enter Your Watermark (leave blank for default): ")  # Watermark text

process_zip(input_zip, output_zip, watermark_text)
