from .engine import current_app
from .logging import logLn
from .renderer2d import Renderer2D
from .color import Color
from .entitys2d import Entity2D
from PIL import Image, ImageDraw, ImageFont
from .entitys2d import Text2D
from .assets import LoadShapes

class ConversationRenderer(Renderer2D):
    def __init__(self,text_color=Color.white,backround_color=Color.black,font_path="arial.ttf"):
        super().__init__()
        self.text_color = text_color
        self.backround_color = backround_color
        self.font_path = font_path
        self.text = ""
        self.padding_x = 20
        self.padding_y = 16
        self.max_font_size = 32
        self.min_font_size = 12
        self._last_wrapped_text = None
        self._last_font_size = None
        logLn("Conversation renderer loaded.")

    def _load_font(self, font_size):
        try:
            return ImageFont.truetype(self.font_path, font_size)
        except:
            return ImageFont.load_default()

    def _break_word(self, word, font, max_width):
        pieces = []
        current = ""
        for ch in word:
            candidate = current + ch
            if current and font.getlength(candidate) > max_width:
                pieces.append(current)
                current = ch
            else:
                current = candidate
        if current:
            pieces.append(current)
        return pieces if pieces else [word]

    def _wrap_text(self, text, font, max_width):
        if max_width <= 1:
            return text

        wrapped_lines = []
        paragraphs = str(text).split("\n")

        for paragraph in paragraphs:
            words = paragraph.split()
            if not words:
                wrapped_lines.append("")
                continue

            current_line = ""
            for word in words:
                candidate = word if not current_line else current_line + " " + word
                if font.getlength(candidate) <= max_width:
                    current_line = candidate
                    continue

                if current_line:
                    wrapped_lines.append(current_line)
                    current_line = ""

                if font.getlength(word) <= max_width:
                    current_line = word
                else:
                    pieces = self._break_word(word, font, max_width)
                    wrapped_lines.extend(pieces[:-1])
                    current_line = pieces[-1]

            if current_line:
                wrapped_lines.append(current_line)

        return "\n".join(wrapped_lines)

    def _measure_text_height(self, text, font):
        safe_text = text if text else " "
        measure_img = Image.new("RGBA", (1, 1), (0,0,0,0))
        measure_draw = ImageDraw.Draw(measure_img)
        bbox = measure_draw.multiline_textbbox((0, 0), safe_text, font=font, spacing=4)
        return max(1, bbox[3] - bbox[1])

    def _fit_wrapped_text(self, text, max_width, max_height):
        selected_text = ""
        selected_size = self.min_font_size

        for size in range(self.max_font_size, self.min_font_size - 1, -1):
            font = self._load_font(size)
            wrapped = self._wrap_text(text, font, max_width)
            text_height = self._measure_text_height(wrapped, font)
            selected_text = wrapped
            selected_size = size
            if text_height <= max_height:
                break

        return selected_text, selected_size

    def start(self): 
        from .engine import current_app
        self.backround = Entity2D(texture=LoadShapes().dot,renderer=self)
        self.text_entity = Text2D(text=self.text,font_path=self.font_path,color=self.text_color,position=(0,-current_app.window.height/2 + self.backround.scale_y),renderer=self)
    def update(self,dt):
        from .engine import current_app
        self.backround.scale_x = current_app.window.width
        self.backround.scale_y = current_app.window.height/3
        self.backround.color = self.backround_color
        self.backround.x = 0
        self.backround.y = -current_app.window.height/2 + self.backround.scale_y/2

        max_text_width = max(1, self.backround.scale_x - self.padding_x * 2)
        max_text_height = max(1, self.backround.scale_y - self.padding_y * 2)
        wrapped_text, font_size = self._fit_wrapped_text(self.text, max_text_width, max_text_height)

        if wrapped_text != self._last_wrapped_text or font_size != self._last_font_size:
            self.text_entity.font_size = font_size
            self.text_entity.set_text(wrapped_text)
            self._last_wrapped_text = wrapped_text
            self._last_font_size = font_size

        self.text_entity.color = self.text_color
        self.text_entity.x = 0
        self.text_entity.y = self.backround.y
    def add_message(self,text):
        self.text = str(text)