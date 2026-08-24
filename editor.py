from figure import Figure
from action import Action
from stack import Stack


class Editor:
    def __init__(self, canvas=None):
        self.canvas = canvas
        self.figures = {}
        self.undo_stack = Stack()
        self.redo_stack = Stack()
        self.selected_figure_id = None

    def create_figure(self, figure_type):
        width = 700
        height = 500

        if self.canvas is not None:
            width = self.canvas.winfo_width() or width
            height = self.canvas.winfo_height() or height

        offset = (len(self.figures) * 25) % 200
        x1 = 80 + offset
        y1 = 80 + offset
        x2 = x1 + 120
        y2 = y1 + 80

        figure = Figure(figure_type, x1, y1, x2, y2)
        figure.draw(self.canvas)
        self.figures[figure.id] = figure
        self.selected_figure_id = figure.id

        action = Action("CREATE", figure)
        self.undo_stack.push(action)
        self.redo_stack.clear()
        return figure

    def delete_figure(self, figure_id=None):
        if figure_id is None:
            figure_id = self.selected_figure_id

        if figure_id is None:
            return False

        figure = self.figures.get(figure_id)
        if figure is None:
            return False

        figure.erase(self.canvas)
        del self.figures[figure_id]
        self.selected_figure_id = None

        action = Action("DELETE", figure)
        self.undo_stack.push(action)
        self.redo_stack.clear()
        return True

    def undo(self):
        action = self.undo_stack.pop()
        if action is None:
            return False

        if action.action_type == "CREATE":
            figure = self.figures.get(action.figure.id)
            if figure is not None:
                figure.erase(self.canvas)
                del self.figures[figure.id]
            self.redo_stack.push(action)
            return True

        if action.action_type == "DELETE":
            figure = Figure.from_dict(action.figure.to_dict())
            figure.draw(self.canvas)
            self.figures[figure.id] = figure
            self.redo_stack.push(action)
            return True

        return False

    def redo(self):
        action = self.redo_stack.pop()
        if action is None:
            return False

        if action.action_type == "CREATE":
            figure = Figure.from_dict(action.figure.to_dict())
            figure.draw(self.canvas)
            self.figures[figure.id] = figure
            self.undo_stack.push(action)
            return True

        if action.action_type == "DELETE":
            figure = self.figures.get(action.figure.id)
            if figure is not None:
                figure.erase(self.canvas)
                del self.figures[figure.id]
            self.undo_stack.push(action)
            return True

        return False

    def clear(self):
        for figure in list(self.figures.values()):
            figure.erase(self.canvas)
        self.figures.clear()
        self.selected_figure_id = None
        self.undo_stack.clear()
        self.redo_stack.clear()

    def get_history(self):
        return list(reversed(self.undo_stack.items))
