class Figure:
    def __init__(self, figure_type, x1, y1, x2, y2, color="#9ae6b4"):
        self.id = self._generate_id()
        self.type = figure_type
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.canvas_item_id = None

    @staticmethod
    def _generate_id():
        import uuid
        return uuid.uuid4().hex[:8]

    def draw(self, canvas):
        if canvas is None:
            return None

        if self.type == "line":
            item_id = canvas.create_line(
                self.x1,
                self.y1,
                self.x2,
                self.y2,
                fill=self.color,
                width=3,
            )
        elif self.type == "circle":
            radius_x = abs(self.x2 - self.x1) / 2
            radius_y = abs(self.y2 - self.y1) / 2
            center_x = min(self.x1, self.x2) + radius_x
            center_y = min(self.y1, self.y2) + radius_y
            item_id = canvas.create_oval(
                center_x - radius_x,
                center_y - radius_y,
                center_x + radius_x,
                center_y + radius_y,
                outline=self.color,
                width=3,
                fill="",
                tags=("figure", self.id),
            )
        elif self.type == "rectangle":
            item_id = canvas.create_rectangle(
                self.x1,
                self.y1,
                self.x2,
                self.y2,
                outline=self.color,
                width=3,
                fill="",
                tags=("figure", self.id),
            )
        else:
            item_id = None

        self.canvas_item_id = item_id
        return item_id

    def erase(self, canvas):
        if canvas is not None and self.canvas_item_id is not None:
            canvas.delete(self.canvas_item_id)
        self.canvas_item_id = None

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "x1": self.x1,
            "y1": self.y1,
            "x2": self.x2,
            "y2": self.y2,
            "color": self.color,
        }

    @classmethod
    def from_dict(cls, data):
        figure = cls(
            data["type"],
            data["x1"],
            data["y1"],
            data["x2"],
            data["y2"],
            data["color"],
        )
        figure.id = data["id"]
        figure.canvas_item_id = None
        return figure
