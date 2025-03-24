from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import blue, black, gray
import re

class PDFDocument:
    def __init__(self, filename, title):
        """
        Initializes the PDF document with the given filename and title.
        """
        self.canvas = canvas.Canvas(filename, pagesize=letter)
        self.canvas.setTitle(title)
        self.width, self.height = letter

    def add_page_number(self, page_num):
        """
        Adds a page number at the bottom of each page.
        """
        self.canvas.setFont('Helvetica', 10)
        self.canvas.drawRightString(self.width - inch, 0.5 * inch, f"Page {page_num}")
        self.canvas.line(inch, 0.6 * inch, self.width - inch, 0.6 * inch)

    def draw_text(self, text, x, y, size=12, line_height=14, indent=0):
        """
        Draws formatted text onto the PDF, handling bold, italic, and links.
        """
        def get_chunks(text):
            """
            Splits the text into chunks based on formatting (bold, italic, links).
            """
            patterns = [r'\*\*(.*?)\*\*', r'\*(.*?)\*', r'(https?://\S+)']
            cursor = 0
            for match in re.finditer('|'.join(patterns), text):
                if cursor < match.start():
                    yield text[cursor:match.start()], 'Helvetica', black
                if match.group().startswith('**'):
                    yield match.group()[2:-2], 'Helvetica-Bold', black
                elif match.group().startswith('*') and not match.group().startswith('**'):
                    yield match.group()[1:-1], 'Helvetica', black
                elif re.match(r'https?://', match.group()):
                    yield match.group(), 'Helvetica-Oblique', blue
                cursor = match.end()
            if cursor < len(text):
                yield text[cursor:], 'Helvetica', black

        cursor_x = x + indent
        cursor_y = y
        line_width = self.width - 2 * inch - indent

        for chunk, style, color in get_chunks(text):
            self.canvas.setFont(style, size)
            self.canvas.setFillColor(color)

            words = chunk.split()
            for word in words:
                word_width = self.canvas.stringWidth(word, style, size)
                if cursor_x + word_width > x + line_width:
                    cursor_y -= line_height
                    cursor_x = x + indent
                self.canvas.drawString(cursor_x, cursor_y, word)
                cursor_x += word_width + self.canvas.stringWidth(' ', style, size)

            self.canvas.setFillColor(black)

        return x, cursor_y - line_height

    def create_pdf(self, topic, content):
        """
        Generates a literature review PDF from the provided topic and content.
        """
        page_num = 1
        y = self.height - 1.5 * inch
        sections = content.split("\n")
        bullet = u"\u2022"  # Unicode for bullet point
        list_counter = 1

        # Add Title at the top
        self.canvas.setFont('Helvetica-Bold', 20)
        self.canvas.drawString(inch, y, f"Literature Review: {topic}")
        y -= 0.5 * inch  # Space below the title

        for section in sections:
            # Add new page if the section is a new heading and space is low
            if section.startswith("### ") and y < self.height - 2 * inch:
                self.add_page_number(page_num)
                self.canvas.showPage()
                page_num += 1
                y = self.height - inch

            # Add new page if reaching bottom of the page
            if y < 2 * inch:
                self.add_page_number(page_num)
                self.canvas.showPage()
                page_num += 1
                y = self.height - inch

            # Handle headings
            if section.startswith("### "):
                y -= 0.5 * inch
                self.canvas.setFont('Helvetica-Bold', 18)
                self.canvas.drawString(inch, y, section[4:].strip())
                y -= 0.3 * inch
                self.canvas.line(inch, y, self.width - inch, y)
                y -= 0.4 * inch
            # Handle bold text
            elif section.startswith("**"):
                y -= 0.3 * inch
                _, y = self.draw_text(section, inch, y, 14)
            # Handle numbered lists
            elif section.startswith("* "):
                section = f"**{list_counter}.** {section[2:]}"
                list_counter += 1
                _, y = self.draw_text(section, inch, y, 12, 14, 10)
            # Handle bullet points
            elif section.startswith("  + ") or section.startswith("  - "):
                section = f"{bullet} {section[4:]}"
                _, y = self.draw_text(section, inch, y, 12, 14, 20)
            # Handle normal text
            else:
                _, y = self.draw_text(section, inch, y)

            y -= 0.1 * inch  # Add slight space between sections

        # Add final page number and save PDF
        self.add_page_number(page_num)
        self.canvas.save()