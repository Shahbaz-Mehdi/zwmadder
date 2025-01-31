from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO
import decimal
import os

def create_watermark(watermark_text, page_width):
    packet = BytesIO()
    c = canvas.Canvas(packet)
    
    # Set the font to bold
    c.setFont("Helvetica-Bold", 16)  # Use "Helvetica-Bold" for bold text
    c.setFillColorRGB(0, 0, 0)  # Fully black (no transparency)

    # Convert page width to float to handle arithmetic
    page_width = float(page_width)
    
    # Calculate the position for the watermark (center horizontally, bottom vertically)
    text_width = c.stringWidth(watermark_text, "Helvetica-Bold", 16)  # Width of the watermark text
    x_position = (page_width - text_width) / 2  # Center the text horizontally
    y_position = 30  # Position watermark 30 units from the bottom

    c.drawString(x_position, y_position, watermark_text)

    # Underline the permalink (if present)
    if "https://" in watermark_text:
        # Extract URL part and calculate its position
        url_start = watermark_text.find("https://")
        url_text = watermark_text[url_start:]
        url_text_width = c.stringWidth(url_text, "Helvetica-Bold", 16)
        
        # Draw a line to underline the URL
        c.setStrokeColorRGB(0, 0, 0)  # Black color for the underline
        c.setLineWidth(1)
        c.line(x_position + c.stringWidth(watermark_text[:url_start], "Helvetica-Bold", 16), 
               y_position - 2, 
               x_position + c.stringWidth(watermark_text[:url_start], "Helvetica-Bold", 16) + url_text_width, 
               y_position - 2)
    
    c.save()
    packet.seek(0)
    return packet

def add_watermark(input_pdf, output_pdf, watermark_text):
    try:
        # Add '.pdf' if it's missing from the input/output file names
        if not input_pdf.lower().endswith('.pdf'):
            input_pdf += '.pdf'
        
        # If no output PDF name is provided, use the input PDF name with '-TechByMehdi' suffix
        if not output_pdf:
            output_pdf = input_pdf.replace('.pdf', '-TechByMehdi.pdf')
        elif not output_pdf.lower().endswith('.pdf'):
            output_pdf += '-TechByMehdi.pdf'

        # If no watermark text is provided, set a default value
        if not watermark_text:
            watermark_text = "Join For More: https://chat.whatsapp.com/J1yWn2VENBaCGOaxJKSt6F"

        # Open the input PDF
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

        # Save the output PDF
        with open(output_pdf, "wb") as output_file:
            writer.write(output_file)

        print(f"✅ Watermark added successfully. Output saved to '{output_pdf}'")

    except Exception as e:
        print(f"❌ Error: {e}")

# Example usage
input_pdf = input("Please enter Your input Name (without .pdf): ")  # Replace with your input PDF file
output_pdf = input("Please enter Your output Name (without .pdf): ")  # Leave blank to use input PDF name
watermark_text = input("Please enter Your Watermark (leave blank for default): ")  # Replace with your group link or leave blank

add_watermark(input_pdf, output_pdf, watermark_text)
