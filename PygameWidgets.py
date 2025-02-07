import pygame
import numpy as np
from pathlib import Path
from collections.abc import MutableSequence
import re

def create_rect(position, size, anchor):
    """Create a pygame.Rect based on position, size, and anchor alignment."""
    position = list(position)
    r = pygame.Rect((0, 0), (size))
    setattr(r, Widget.ANCHOR_KEYWORDS[anchor], position)
    return r

class Root:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Widget(Root, pygame.sprite.Sprite):
    ANCHOR_KEYWORDS = {
        'N': 'midtop',
        'NW': 'topleft',
        'W': 'midleft',
        'SW': 'bottomleft',
        'S': 'midbottom',
        'SE': 'bottomright',
        'E': 'midright',
        'NE': 'topright',
        'C': 'center',
    }

    def __init__(self,
                *args,
                name='Widget',
                display_name=None,
                position=np.array([0, 0]),
                size_change_callbacks=None,
                position_change_callbacks=None,
                anchor='NW',
                text_color=(255, 255, 255),
                background_color=(255, 150, 150),
                font=None,
                parent=None,
                **kwargs):
        """Constructor of abstract base class for pygameW widgets.

        Args:
            *args: Parameters to pass to the parent Sprite class.
            name: Widget name (default: 'Widget').
            display_name: Display name for the widget (defaults to name).
            position: Position on screen (default: np.array([0, 0])).
            size_change_callbacks: List of zero or more callback functions to
                call when the widget size changes (default: []).
            anchor: Part of the control to align to the position.
                Possibilities: 'N', 'NW', 'W', 'SW', 'S', 'SE', 'E', 'NE', or 'C'.
                Defaults to 'NW'.
            **kwargs: Additional keyword arguments for the parent class.
        """
        super().__init__(*args, **kwargs)
        self.image = None
        self.rect = None
        self.name = name
        self.parent = parent
        if font is None:
            self.font = pygame.font.Font(Path(__file__).parent / "arial.ttf", size=14)
        else:
            self.font = font
        self.text_color = text_color
        self.background_color = background_color
        if anchor not in Widget.ANCHOR_KEYWORDS:
            print('Anchor must be one of:', ', '.join(Widget.ANCHOR_KEYWORDS.keys()))
            raise SyntaxError('Unknown anchor type: ' + anchor)
        self._anchor = anchor
        self._display_name = self.name if display_name is None else display_name
        self._position = np.array(position)
        if size_change_callbacks is None:
            self.size_change_callbacks = []
        else:
            self.size_change_callbacks = size_change_callbacks
        if position_change_callbacks is None:
            self.position_change_callbacks = []
        else:
            self.position_change_callbacks = position_change_callbacks
        self.width = None
        self.height = None
        self.t = 0

    def get_position(self):
        return self._position
    def set_position(self, new_position):
        self._position = np.array(new_position)
    def get_anchor(self):
        return self._anchor
    def set_anchor(self, new_anchor):
        self._anchor = new_anchor
    def get_display_name(self):
        return self._display_name
    def set_display_name(self, new_display_name):
        self._display_name = np.array(new_display_name)

    def update(self):
        self.t += 1

    def update_image(self):
        if self.parent is not None:
            self.parent.child_image_updated(self)

    def update_rect(self):
        anchor_key = Widget.ANCHOR_KEYWORDS[self.get_anchor()]
        kwargs = {anchor_key: self.get_position()}
        self.rect = self.image.get_rect(**kwargs)

    def handle_event(self, event):
        pass

    def size_changed(self):
        for size_change_callback in self.size_change_callbacks:
            size_change_callback(self)
    def position_changed(self):
        for position_change_callback in self.position_change_callbacks:
            position_change_callback(self)

class Label(Widget):
    def __init__(self, *args, text='', border_width=3, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = None
        self.rect = None
        self._text = None
        self.border_width = border_width
        self.set_text(text)

    def set_text(self, text):
        self._text = text
        self.update_image()
        self.size_changed()
    def get_text(self):
        return self._text

    def update_image(self):
        super().update_image()
        label_surface = self.font.render(self.get_text(), False, self.text_color)
        label_width, label_height = label_surface.get_size()

        self.width = label_width + 2 * self.border_width
        self.height = label_height + 2 * self.border_width

        self.image = pygame.Surface((self.width, self.height))

        self.image.fill((0, 0, 0))
        # pygame.draw.rect(
        #     self.image,
        #     self.background_color,
        #     [0, 0, self.width, self.height],
        #     width=width,
        #     border_radius=3
        # )
        self.image.blit(label_surface, (self.border_width, self.border_width))
        self.image.set_colorkey((0, 0, 0))

        self.update_rect()


class Control(Widget):
    def __init__(self, *args, name='Control', value=None,
                 value_change_callbacks=[], **kwargs):
        """Constructor of abstract base class for pygame control widgets.

        Args:
            *args: Parameters to pass to the parent Widget class.
            name: Control name (default: 'Control').
            value: The current control value (default: None).
            value_change_callbacks: List of zero or more callback functions to call
                when the value changes (default: []).
            **kwargs: Additional keyword arguments for the parent Widget class.
        """
        super().__init__(*args, name=name, **kwargs)
        self.value = value
        self.value_change_callbacks = value_change_callbacks

    def get_value(self):
        return self.value

    def set_value(self, value, fire_callback=True):
        self.value = value
        if fire_callback:
            self.fire_callbacks()

    def fire_callbacks(self):
        for value_change_callback in self.value_change_callbacks:
            value_change_callback(self.get_value())

    def increment_value(self, increment=None):
        if increment is None:
            increment = self.increment
        self.set_value(self.get_value() + increment)

    def decrement_value(self, decrement=None):
        if decrement is None:
            decrement = self.increment
        self.set_value(self.get_value() - decrement)

class ControlGroup(Root, pygame.sprite.Group):
    def __init__(self, *args, child_image_update_callbacks=None, **kwargs):
        super().__init__(*args, **kwargs)
        if child_image_update_callbacks is None:
            self.child_image_update_callbacks = []
        else:
            self.child_image_update_callbacks = child_image_update_callbacks

    def add(self, *controls, **kwargs):
        super().add(*controls)
        for control in controls:
            if not isinstance(control, Widget):
                raise TypeError('ControlGroup can only contain Widget objects')
            control.parent = self

    def remove(self, *controls):
        for control in controls:
            if control.parent is self:
                control.parent = None
        super().remove(*controls)

    def empty(self):
        for control in self.sprites():
            if control.parent is self:
                control.parent = None
        super().empty()

    def handle_event(self, event):
        for control in self:
            control.handle_event(event)

    def child_image_updated(self, child):
        for child_image_update_callback in self.child_image_update_callbacks:
            child_image_update_callback(child)

class ControlMenu(ControlGroup, Widget):
    def __init__(self,
                *args,
                spacing=10,
                style='column',
                column_alignment='left',
                row_alignment='top',
                background_color='darkslategray4',
                border_radius=5,
                **kwargs):
        super().__init__(*args, **kwargs)
        # ControlGroup.__init__(self, *args, **kwargs)
        # Widget.__init__(self, *args, **kwargs)
        self.spacing = spacing
        self.style = style
        self.row_alignment = row_alignment
        self.column_alignment = column_alignment
        self.background_color = background_color
        self.border_radius = border_radius
        self.background_image = None
        self.position_change_callbacks.append(lambda _:self.arrange())

    def get_position(self):
        return self._position
    def set_position(self, new_position):
        self._position = np.array(new_position)
    def get_anchor(self):
        return self._anchor
    def set_position(self, new_anchor):
        self._anchor = np.array(new_anchor)

    def draw(self, screen):
        self.update_background_image()
        screen.blit(self.background_image, self.rect)
        super().draw(screen)

    def handle_event(self, *args, **kwargs):
        for sprite in self.sprites():
            sprite.handle_event(*args, **kwargs)

    def arrange(self, update_background_image=True):
        if len(self.sprites()) == 0:
            return

        if self.style == 'column':
            # Determine total height
            total_height = (sum([control.rect.height for control in self]) +
                            self.spacing * (len(self.sprites()) + 1))
            total_width = max([control.rect.width for control in self]) + self.spacing*2
            self.rect = create_rect(self.get_position(), (total_width, total_height), self.get_anchor())
            y = self.rect.midtop[1] + self.spacing
            if self.column_alignment == 'left':
                x = self.rect.left
                anchor = 'NW'
            elif self.column_alignment == 'center':
                x = self.rect.centerx
                anchor = 'N'
            elif self.column_alignment == 'right':
                x = self.rect.right
                anchor = 'NE'
            for control in self.sprites():
                control.set_anchor(anchor)
                control.set_position((x, y))
                control.update_rect()
                y += control.rect.height + self.spacing
        elif self.style == 'row':
            # Determine total width
            total_width = (sum([control.rect.width for control in self]) +
                            self.spacing * (len(self.sprites()) + 1))
            total_height = max([control.rect.width for control in self]) + self.spacing*2
            self.rect = create_rect(self.get_position(), (total_width, total_height), self.get_anchor())

            x = self.rect.left + self.spacing
            if self.row_alignment == 'top':
                y = self.rect.top
                anchor = 'NW'
            elif self.row_alignment == 'center':
                y = self.rect.centery
                anchor = 'W'
            elif self.row_alignment == 'bottom':
                y = self.rect.bottom
                anchor = 'SW'
            for control in self.sprites():
                control.set_anchor(anchor)
                control.set_position((x, y))
                control.update_rect()
                x += control.rect.width + self.spacing
        else:
            raise TypeError('Unknown arrange style ' + self.style)

        if update_background_image:
            self.update_background_image()

    def update_background_image(self):
        if self.rect is None:
            self.arrange()
        if self.background_image is None:
            self.background_image = pygame.Surface(self.rect.size)
        self.background_image.set_colorkey('black')
        rect = self.rect.copy()
        rect.topleft = (0, 0)
        pygame.draw.rect(
            self.background_image,
            self.background_color,
            rect,
            border_radius=self.border_radius
        )

    def add(self, *sprites, rearrange=False, **kwargs):
        # Request notification when sprite changes size
        for sprite in sprites:
            if not self.has(sprite):
                sprite.size_change_callbacks.append(lambda source:self.arrange())
        super().add(*sprites, **kwargs)
        if rearrange:
            # Update arrangement
            self.arrange()

    def position_changed(self):
        for position_change_callback in self.position_change_callbacks:
            position_change_callback(self)

class TextBoxControl(Control):
    def __init__(self, *args, value='', border_width=3, resizable=False,
                    min_size=50, max_size=100, **kwargs):
        super().__init__(*args, **kwargs)
        self.border_width = border_width
        self.characters = []
        self.set_value(value, fire_callback=False, update_image=False)
        self.image = None
        self.rect = None
        self.resizable = resizable
        self.min_size = min_size
        self.max_size = max_size
        self.cursor_idx = None
        self.cursor_hitboxes = []
        self.cursor_blink_period = 10  # In game ticks
        self.allow_pattern = re.compile('[ -~]')
        self.update_image()

    def set_value(self, value, fire_callback=True, update_image=True):
        self.value = str(value)
        self.characters = list(self.value)
        if update_image:
            self.update_image()
        if fire_callback:
            self.fire_callbacks()

    def update_image(self):
        super().update_image()
        original_width = self.width
        original_height = self.height

        string = self.get_value()

        label_surface = self.font.render(string, False, self.text_color)
        label_width, label_height = label_surface.get_size()
        if self.resizable:
            self.width = max(self.min_size, label_width + 2 * self.border_width)
            self.height = label_height + 2 * self.border_width
        else:
            self.width = self.max_size
            self.height = label_height + 2 * self.border_width
        self.image = pygame.Surface((self.width, self.height))
        label_rect = create_rect(
            (self.width/2, self.height/2),
            (label_width, label_height),
            'C'
        )

        self.image.fill((0, 0, 0))
        pygame.draw.rect(
            self.image,
            self.background_color,
            [0, 0, self.width, self.height],
            width=1,
            border_radius=0
        )

        # Determine each cursor position based on text size, relative to the
        #   middle of the text box
        cursor_position = [None for k in range(len(string)+1)]
        for k in range(len(string)+1):
            cursor_position[k], cursor_height = self.font.size(string[:k])
        for k in range(len(string)+1):
            cursor_position[k] += self.width/2 - cursor_position[-1]/2
        # Update cursor hitboxes
        self.cursor_hitboxes = []
        # Establish first hitbox
        self.cursor_hitboxes = [None for k in range(len(string)+1)]
        if len(cursor_position) > 1:
            self.cursor_hitboxes[0] = create_rect(
                (0, 0),
                (cursor_position[1]/2, self.height),
                'NW'
            )
            for k in range(1, len(string)):
                last_position = cursor_position[k-1]
                this_position = cursor_position[k]
                next_position = cursor_position[k+1]
                left =  np.mean([last_position, this_position])
                right = np.mean([this_position, next_position])
                self.cursor_hitboxes[k] = create_rect(
                    (left, 0),
                    (right-left, self.height),
                    'NW'
                )
            # Establish last hitbox
            start = np.mean(cursor_position[-2:])
            self.cursor_hitboxes[len(string)] = create_rect(
                (start, 0),
                (self.width - start, self.height),
                'NW'
            )
        else:
            # String is empty
            self.cursor_hitboxes[0] = create_rect(
                (0, 0),
                (self.width, self.height),
                'NW'
            )

        if self.cursor_idx is not None:
            pygame.draw.line(
                self.image,
                self.background_color,
                [cursor_position[self.cursor_idx], self.border_width],
                [cursor_position[self.cursor_idx], self.height-2*self.border_width],
                width=1
            )

        self.image.blit(label_surface, label_rect)
        self.image.set_colorkey((0, 0, 0))

        self.update_rect()

        if self.width != original_width or self.height != original_height:
            self.size_changed()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                x, y = event.pos
                x -= self.rect.left
                y -= self.rect.top
                cursor_changed = False
                for k, hitbox in enumerate(self.cursor_hitboxes):
                    if hitbox.collidepoint((x, y)):
                        if k != self.cursor_idx:
                            self.cursor_idx = k
                            cursor_changed = True
                            break
                if cursor_changed:
                    self.update_image()
            elif self.cursor_idx is not None:
                self.cursor_idx = None
                self.update_image()
        elif event.type == pygame.KEYDOWN:
            if self.cursor_idx is not None:
                if self.allow_pattern.match(event.unicode):
                    self.characters.insert(self.cursor_idx, event.unicode)
                    self.cursor_idx += 1
                    self.set_value(''.join(self.characters))
                elif event.key == pygame.K_BACKSPACE and self.cursor_idx > 0:
                    self.characters.pop(self.cursor_idx-1)
                    self.cursor_idx -= 1
                    self.set_value(''.join(self.characters))
                elif event.key == pygame.K_RIGHT:
                    self.cursor_idx += 1
                    self.update_image()
                elif event.key == pygame.K_LEFT:
                    self.cursor_idx -= 1
                    self.update_image()

class ChoiceControl(Control, MutableSequence):
    # Abstract base class for controls where the user selects one of
    #   multiple values
    def __init__(self, *args, border_width=3, display_names=[], data=[],
                    text_alignment='center', **kwargs):
        super().__init__(*args, **kwargs)
        if type(display_names) is str:
            # Allow for a scalar display name if the user only wants to pass one
            display_names = [display_names]
        if len(data) == 0:
            # No data supplied
            data = [None for k in range(len(display_names))]
        if len(data) != len(display_names):
            raise IndexError('If data argument is supplied, it must be an iterable with the same length as display_names')
        if len(display_names) == 0:
            raise ValueError('At least one display name must be provided')
        if not all([type(name) is str for name in display_names]):
            raise ValueError('Display names must be strings')
        self.display_names = display_names
        self.data = data
        self.set_value(0, fire_callback=False)

    def __getitem__(self, idx):
        return (self.display_names[idx], self.data[idx])

    def __delitem__(self, idx):
        self.display_names.pop(idx)
        self.data.pop(idx)

    def __len__(self):
        return len(self.display_names)

    def __setitem__(self, idx, value):
        """Set an item.

        Args:
            idx (integer): Index to set
            value (type): Either a display name string, or a tuple containing
                a display name string followed by arbitrary data

        Returns:
            type: Description of returned object.

        """
        if type(value) in [tuple, list]:
            self.display_names[idx] = value[0]
            self.data[idx] = value[1:]
        else:
            self.display_names[idx] = value
            self.data[idx] = None

    def insert(self, idx, value):
        if type(value) in [tuple, list]:
            self.display_names.insert(idx, value[0])
            self.data.insert(idx, value[1:])
        else:
            self.display_names.insert(idx, value)
            self.data.insert(idx, None)

class ComboBoxControl(ChoiceControl):
    def __init__(self, *args, border_width=3, text_alignment='center',
                    **kwargs):
        super().__init__(*args, **kwargs)
        self.text_alignment = text_alignment  # 'left', 'right', or 'center'
        self.border_width = border_width
        self.expanded = False
        self.highlight_idx = None
        self.image = None
        self.rect = None
        self.element_rects = []
        self.element_images = []
        self.update_image()

    def update_image(self):
        super().update_image()
        original_width = self.width
        original_height = self.height

        # Render all text to determine necessary width and height
        label_surfaces = []
        label_rects = []
        label_width = 0
        label_height = 0
        label_widths = []
        label_heights = []
        for k, (display_name, _) in enumerate(self):
            label_surfaces.append(
                self.font.render(display_name, False, self.text_color)
            )
            label_widths.append(None)
            label_heights.append(None)
            label_widths[k], label_heights[k] = label_surfaces[k].get_size()
            label_width = max(label_width, label_widths[k])
            label_height = max(label_height, label_heights[k])

        # Determine appropriate element width/height
        element_width =  label_width +  2*self.border_width
        element_height = label_height + 2*self.border_width

        for k in range(len(self)):
            # Create label rects
            if self.text_alignment == 'center':
                new_label_rect = create_rect(
                    (element_width/2, element_height/2),
                    (label_widths[k], label_heights[k]),
                    'C')
            elif self.text_alignment == 'left':
                new_label_rect = create_rect(
                    (element_width/2 - label_width/2, element_height/2),
                    (label_width[k], label_height[k]),
                    'W')
            elif self.text_alignment == 'right':
                new_label_rect = create_rect(
                    (element_width/2 + label_width/2, element_height/2),
                    (label_width[k], label_height[k]),
                    'E')
            label_rects.append(new_label_rect)

        # Determine necessary width and height of overall image
        self.width = element_width
        if not self.expanded:
            self.height = element_height
        else:
            self.height = (len(self)+1) * label_height + (len(self)+2) * self.border_width

        # Create top (main) image
        main_image = pygame.Surface((element_width, element_height))
        pygame.draw.rect(
            main_image,
            self.background_color,
            [0, 0, element_width, element_height],
            width=1,
            border_radius=3
        )

        main_image.blit(label_surfaces[self.get_value()], label_rects[self.get_value()])

        if self.image is None or self.image.size[0] != self.width or self.image.size[1] != self.height:
            self.image = pygame.Surface((self.width, self.height))
        self.image.fill('black')
        self.image.blit(main_image, (0, 0))
        self.image.set_colorkey('black')

        if not self.expanded:
            self.element_rects = []
            self.element_images = []
        else:
            # Create dropdown list of elements
            for k, (display_name, _) in enumerate(self):
                y = (label_height + self.border_width) * (k+1)
                self.element_rects.append(
                    create_rect((0, y), (element_width, element_height), 'NW')
                )
                self.element_images.append(
                    pygame.Surface((element_width, element_height))
                )
                if self.highlight_idx == k:
                    width = 0
                else:
                    width = 1

                self.element_images[k].fill('black')
                pygame.draw.rect(
                    self.element_images[k],
                    self.background_color,
                    [0, 0, element_width, element_height],
                    width=width,
                    border_radius=0
                )
                self.element_images[k].blit(
                    label_surfaces[k],
                    label_rects[k],
                )
                self.image.blit(self.element_images[k], self.element_rects[k])

        self.update_rect()

        # If size changed, fire callback:
        # if self.width != original_width or self.height != original_height:
        #     self.size_changed()

    def get_hover_idx(self, event):
        _, y = event.pos
        y -= self.rect.top
        for k in range(len(self)):
            if self.element_rects[k].top <= y and y <= self.element_rects[k].bottom:
                return k
        return None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.expanded = True
                self.highlight_idx = self.get_value()
                self.update_image()
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.expanded:
                self.expanded = False
                self.set_value(self.highlight_idx)
                self.update_image()
        elif event.type == pygame.MOUSEMOTION:
            if self.expanded:
                new_highlight_idx = self.get_hover_idx(event)
                if new_highlight_idx is not None:
                    if self.highlight_idx != new_highlight_idx:
                        self.highlight_idx = new_highlight_idx
                        self.update_image()

class ButtonControl(Control):
    def __init__(self, *args, border_width=3, **kwargs):
        super().__init__(*args, **kwargs)
        self.border_width = border_width
        self.set_value(False, fire_callback=False)
        self.image = None
        self.rect = None
        self.update_image()

    def update_image(self):
        super().update_image()
        label_surface = self.font.render(self._display_name, False, self.text_color)
        label_width, label_height = label_surface.get_size()
        self.width = label_width + 2 * self.border_width
        self.height = label_height + 2 * self.border_width
        self.image = pygame.Surface((self.width, self.height))

        if self.get_value():
            width = 0
        else:
            width = 1

        self.image.fill((0, 0, 0))
        pygame.draw.rect(
            self.image,
            self.background_color,
            [0, 0, self.width, self.height],
            width=width,
            border_radius=3
        )
        self.image.blit(label_surface, (self.border_width, self.border_width))
        self.image.set_colorkey((0, 0, 0))

        self.update_rect()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.set_value(True)
                self.update_image()
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.get_value():
                self.set_value(False)
                self.update_image()

class RadioButtonControl(ChoiceControl):
    def __init__(self, *args, border_width=3, text_alignment='center',
                    **kwargs):
        super().__init__(*args, **kwargs)
        self.text_alignment = text_alignment  # 'left', 'right', or 'center'
        self.border_width = border_width
        self.group = ControlMenu(
            style='column',
            column_alignment='right',
            child_image_update_callbacks=[lambda child:self.update_image()]
        )
        self.rect = None
        self.update_image()

    def update_image(self):
        super().update_image()
        original_width = self.width
        original_height = self.height

        self.group.empty()
        for k, (display_name, data) in enumerate(self):
            value = (k == 0)
            self.group.add(
                CheckBoxControl(
                    name=display_name,
                    value=value
                )
            )

        self.group.arrange()
        self.group.update_background_image()

        self.image = self.group.background_image
        self.group.draw(self.image)
        self.rect = self.group.rect

    def draw(self, screen):
        self.group.draw(screen)

    def handle_event(self, event):
        try:
            # If it's a mouse event with a "pos" attribute, adjust event
            #   position relative to corner
            x, y = event.pos
            x -= self.rect.left
            y -= self.rect.top
            event.pos = (x, y)
        except AttributeError:
            # Guess it's some other event
            pass
        self.group.handle_event(event)

class CheckBoxControl(ButtonControl):
    def __init__(self, *args, value=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_value(value, fire_callback=False)
        self.update_image()

    def update_image(self):
        super().update_image()
        label_surface = self.font.render(self._display_name, False, self.text_color)
        label_width, label_height = label_surface.get_size()
        check_size = label_height
        self.width = label_width + 3 * self.border_width + check_size
        self.height = label_height + 2 * self.border_width
        self.image = pygame.Surface((self.width, self.height))

        if self.value:
            width = 0
        else:
            width = 1

        self.image.fill((0, 0, 0))
        # pygame.draw.rect(
        #     self.image,
        #     self.background_color,
        #     [0, 0, self.width, self.height],
        #     width=1,
        #     border_radius=min(3, self.height/3)
        # )
        check_x = 2*self.border_width + label_width
        check_y = self.border_width
        pygame.draw.rect(
            self.image,
            self.background_color,
            [check_x, check_y, check_size, check_size],
            width=width,
            border_radius = min(3, check_size/3)
        )
        self.image.blit(label_surface, (self.border_width, self.border_width))
        self.image.set_colorkey((0, 0, 0))

        self.update_rect()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                self.set_value(not self.get_value())
                self.update_image()

class NumericControl(Control):
    def __init__(self, *args, min=-np.inf, max=np.inf,
                 number_format='.01f', **kwargs):
        super().__init__(*args, **kwargs)
        self.max = max
        self.min = min
        if self.get_value() is None:
            self.set_value(0, fire_callback=False)
        self.number_format = "{:" + number_format + "}"

    def set_value(self, value, *args, **kwargs):
        # Coerce value to valid range
        value = pygame.math.clamp(value, self.min, self.max)
        super().set_value(value, *args, **kwargs)

class IncrementControl(NumericControl):
    def __init__(self, *args, increment=1, fast_increment=None, orientation='vertical', **kwargs):
        super().__init__(*args, **kwargs)
        self.increment = increment
        self.orientation = orientation
        if fast_increment is None:
            fast_increment = 5 * self.increment
        self.fast_increment = fast_increment
        self.increment_rect = None
        self.decrement_rect = None
        self.number_rect = None
        self.name_rect = None
        self.increment_pressed = False
        self.decrement_pressed = False
        self.update_image()

    def handle_event(self, event):
        keys = pygame.key.get_pressed()
        if event.type == pygame.MOUSEBUTTONUP:
            # Update pressed flag
            self.increment_pressed = False
            self.decrement_pressed = False
            if self.rect.collidepoint(event.pos):
                # Button is clicked somewhere in the widget
                x, y = event.pos
                x -= self.rect.left
                y -= self.rect.top
                click_increment = self.increment_rect.collidepoint((x, y))
                click_decrement = self.decrement_rect.collidepoint((x, y))
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    inc = self.fast_increment
                else:
                    inc = self.increment
                if click_increment:
                    # Mouse is on increment button
                    self.increment_value(increment=inc)
                elif click_decrement:
                    # Mouse is on decrement button
                    self.decrement_value(decrement=inc)
                # Update image
                self.update_image()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Button is clicked somewhere in the widget
            x, y = event.pos
            x -= self.rect.left
            y -= self.rect.top
            if self.increment_rect.collidepoint((x, y)):
                # Mouse is on increment button
                self.increment_pressed = True
                # Update image
                self.update_image()
            elif self.decrement_rect.collidepoint((x, y)):
                # Mouse is on decrement button
                self.decrement_pressed = True
                # Update image
                self.update_image()

    def update_image(self):
        super().update_image()
        name_surface = self.font.render(self._display_name, False, self.text_color)
        name_width, name_height = name_surface.get_size()

        value_string = self.number_format.format(self.get_value())
        number_surface = self.font.render(value_string, False, self.text_color)
        number_width, number_height = number_surface.get_size()

        arrow_height = 15
        arrow_width = 20
        if self.orientation == 'horizontal':
            arrow_width, arrow_height = arrow_height, arrow_width

        margin = 3

        increment_surface = pygame.Surface((arrow_width, arrow_height))
        decrement_surface = pygame.Surface((arrow_width, arrow_height))

        if self.orientation == 'vertical':
            increment_coords = \
                [(0,                arrow_height-1),
                (arrow_width / 2,  0),
                (arrow_width,      arrow_height-1)]
            decrement_coords = \
                [(0,                0),
                 (arrow_width / 2,  arrow_height-1),
                 (arrow_width,      0)]
        elif self.orientation == 'horizontal':
            increment_coords = \
                [(0,              0),
                 (arrow_width-1, arrow_height / 2),
                 (0,              arrow_height)]
            decrement_coords = \
                [(arrow_width-1, 0),
                (0,              arrow_height / 2),
                (arrow_width-1, arrow_height)]

        widths = [1, 0]

        pygame.draw.polygon(
            increment_surface,
            self.background_color,
            increment_coords,
            width=widths[self.increment_pressed]
        )
        pygame.draw.polygon(
            decrement_surface,
            self.background_color,
            decrement_coords,
            width=widths[self.decrement_pressed]
        )

        if self.orientation == 'vertical':
            self.width = max(arrow_width, number_width, name_width) + 2*margin
            self.height = name_height + 2 * arrow_height + number_height + 5*margin
            y = margin
            self.name_rect = create_rect((self.width // 2, y), name_surface.size, 'N')
            y += name_surface.size[1] + margin
            self.increment_rect = create_rect((self.width // 2, y), increment_surface.size, 'N')
            y += increment_surface.size[1] + margin
            self.number_rect = create_rect((self.width // 2, y), number_surface.size, 'N')
            y += number_surface.size[1] + margin
            self.decrement_rect = create_rect((self.width // 2, y), decrement_surface.size, 'N')
        elif self.orientation == 'horizontal':
            self.width = max(2 * arrow_width + number_width + 4*margin, name_width)
            self.height = max(arrow_height, number_height) + name_height + 3*margin
            y = margin
            self.name_rect = create_rect((self.width // 2, y), name_surface.size, 'N')
            x = (self.width - number_surface.size[0] - 2 * decrement_surface.size[0] - 2 * margin) // 2
            y = y + name_surface.size[1] + decrement_surface.size[1] // 2
            self.decrement_rect = create_rect((x, y), decrement_surface.size, 'W')
            x += decrement_surface.size[0] + margin
            self.number_rect = create_rect((x, y), number_surface.size, 'W')
            x += number_surface.size[0] + margin
            self.increment_rect = create_rect((x, y), increment_surface.size, 'W')

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 0, 0))

        self.image.blit(name_surface, self.name_rect)
        self.image.blit(increment_surface, self.increment_rect)
        self.image.blit(number_surface, self.number_rect)
        self.image.blit(decrement_surface, self.decrement_rect)

        self.image.set_colorkey((0, 0, 0))
        self.update_rect()


class SliderControl(NumericControl):
    def __init__(self, *args, slider_height=20, slider_width=100,
                auto_collapse=False, orientation='horizontal',
                callback_mode='mouseup', **kwargs):
        super().__init__(*args, **kwargs)
        if self.max is None or np.isinf(self.max):
            raise ValueError('max value must be set and non-infinite for a SliderControl')
        if self.min is None or np.isinf(self.min):
            raise ValueError('min value must be set and non-infinite for a SliderControl')
        self.slider_height = slider_height
        self.slider_width = slider_width
        self.auto_collapse = auto_collapse
        self.orientation = orientation
        self.mouse_inside = False
        if self.auto_collapse:
            self.current_height = 0
            self.target_height = 0
        else:
            self.current_height = self.slider_height
            self.target_height = self.slider_height
        self.callback_mode = callback_mode
        self.image = None
        self.rect = None
        self.grabbed = False
        self.grab_x_offset = 0
        self.handle_rect = None
        self.update_image()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Button is clicked somewhere in the widget
            x, y = event.pos
            x -= self.rect.left
            y -= self.rect.top
            if self.handle_rect.collidepoint((x, y)):
                # Mouse is down on handle button
                self.grabbed = True
                self.grab_x_offset = x - self.handle_rect.center[0]
                # Update image
                self.update_image()
        elif event.type == pygame.MOUSEBUTTONUP:
            # Button is up
            if self.grabbed:
                self.grabbed = False
                x, _ = event.pos
                x -= self.rect.left
                value = pygame.math.clamp(
                    (self.max - self.min) * ((x - self.grab_x_offset) / self.width) + self.min,
                    self.min,
                    self.max
                )
                self.set_value(value)
                # Update image
                self.update_image()
        elif event.type == pygame.MOUSEMOTION:
            if self.grabbed:
                # Mouse is moving and we're grabbed
                x, _ = event.pos
                x -= self.rect.left
                value = pygame.math.clamp(
                    (self.max - self.min) * ((x - self.grab_x_offset) / self.width) + self.min,
                    self.min,
                    self.max
                )
                self.set_value(value, fire_callback=(self.callback_mode=='continuous'))
                # Update image
                self.update_image()

    def update(self):
        super().update()
        delta = np.sign(round(self.target_height - self.current_height))
        self.current_height += delta

    def update_image(self):
        super().update_image()
        name_surface = self.font.render(self._display_name, False, self.text_color)
        name_width, name_height = name_surface.get_size()

        value_string = self.number_format.format(self.value)
        number_surface = self.font.render(value_string, False, self.text_color)
        number_width, number_height = number_surface.get_size()

        self.width = max(self.slider_width, name_width)

        handle_width = max(self.width / 8, self.slider_height)
        handle_surface = pygame.Surface((handle_width, self.current_height))
        widths = [1, 0]
        pygame.draw.polygon(
            handle_surface,
            self.background_color,
            (
                (handle_width/2, self.current_height),
                (0, self.current_height/2),
                (handle_width/2, 0),
                (handle_width, self.current_height/2)
            ),
            width=widths[self.grabbed]
        )
        handle_x = self.width * (self.value - self.min) / (self.max - self.min)
        self.handle_rect = create_rect((handle_x, name_height + number_height + self.current_height/2), handle_surface.size, 'C')

        slider_surface = pygame.Surface((self.width, self.current_height))
        slider_surface.set_colorkey('black')

        pygame.draw.line(
            slider_surface,
            self.background_color,
            (0, 0),
            (0, self.current_height)
        )
        pygame.draw.line(
            slider_surface,
            self.background_color,
            (0, self.current_height/2),
            (handle_x-handle_width/2, self.current_height/2)
        )
        pygame.draw.line(
            slider_surface,
            self.background_color,
            (handle_x+handle_width/2, self.current_height/2),
            (self.width, self.current_height/2)
        )
        pygame.draw.line(
            slider_surface,
            self.background_color,
            (self.width-1, 0),
            (self.width-1, self.current_height)
        )

        self.height = name_height + number_height + self.current_height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 0, 0))
        self.image.blit(name_surface, (self.width / 2 - name_width / 2, 0))
        self.image.blit(number_surface, (self.width / 2 - number_width / 2, name_height))
        self.image.blit(handle_surface, self.handle_rect)
        self.image.blit(slider_surface, (0, name_height + number_height))
        self.image.set_colorkey((0, 0, 0))
        self.update_rect()

if __name__ == '__main__':
    import sys

    pygame.init()

    clock = pygame.time.Clock()
    w = 800
    h = 600

    label = Label(text="A label!")

    button = ButtonControl(name="Button")
    button2 = ButtonControl(name=": )")
    incremental = IncrementControl(name="Incremental", orientation='horizontal')
    slider = SliderControl(name="Slider", min=0, max=10, value=5)
    combo = ComboBoxControl(name="Combo", display_names=['hi', 'yay', 'developmental', 'woot'])
    text1 = TextBoxControl(name="Text", value='hello', resizable=True)
    text2 = TextBoxControl(name="Text", value='hello2', resizable=False)
    check = CheckBoxControl(name="Check", value=False)
    radio = RadioButtonControl(name="Radio", display_names=["One", "Two", "Whee"])
    menu = ControlMenu(position=(w / 2, h / 2), anchor='C', style='row', row_alignment='center')
    menu.add(label)
    menu.add(button)
    menu.add(button2)
    menu.add(incremental)
    menu.add(slider)
    menu.add(combo)
    menu.add(text1)
    menu.add(text2)
    menu.add(check)
    menu.add(radio)
    menu.arrange()

    screen = pygame.display.set_mode((w, h))

    def main():
        while True:
            screen.fill((0, 0, 0))

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                    elif event.key == pygame.K_a:
                        label.set_text('it changed')
                menu.handle_event(event)

            menu.update()
            menu.draw(screen)

            # Display
            pygame.display.update()
            clock.tick(60)

    main()
