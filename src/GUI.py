import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QSlider, QLabel,
    QCheckBox, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer
from PyQt6 import QtGui
import qdarktheme

from common import *
from watermark import *


class FileDropLabel(QLabel):
    def __init__(self):
        super().__init__('\n\n Drop PDF or Image File Here \n\n')
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet('QLabel { border: 2px dashed #aaa; }')
        self.setAcceptDrops(True)
        self.file_paths = []

    def is_allowed_file(self, file_path):
        '''
        Check if the file is a PDF or image.
        :param file_path: Path to the file
        :return: True if the file is a PDF or image, False otherwise
        '''

        ext = file_path.lower().rsplit('.', 1)[-1]
        return f'.{ext}' in SUPPORTED_IMAGE_FORMATS

    def dragEnterEvent(self, event):
        '''
        Handle the drag enter event.
        The event contains the file paths of the dragged files.
        If the file is a PDF or image, accept the event.
        :param event: The drag enter event
        :return: None
        '''

        if event.mimeData().hasUrls():
            # Accept if at least one file is allowed
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if self.is_allowed_file(file_path):
                    event.accept()
                    return
            event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        '''
        Handle the drop event.
        The event contains the file paths of the dropped files.
        If the file is a PDF or image, display its path.
        If not, display an error message.
        :param event: The drop event
        '''

        if event.mimeData().hasUrls():
            file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
            allowed_files = [f for f in file_paths if self.is_allowed_file(f)]
            self.file_paths = allowed_files
            if allowed_files:
                self.setText('Files:\n' + '\n'.join(allowed_files))
                event.accept()
            else:
                self.setText('Only PDF or image files are allowed!')
                event.ignore()
        else:
            event.ignore()


class WatermarkWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowIcon(QtGui.QIcon(WINDOW_ICON))

        self.center()
        layout = QVBoxLayout()

        # File drag and drop widget
        self.file_drop = FileDropLabel()
        layout.addWidget(self.file_drop)

        # Text entry
        self.watermark_text_entry = QLineEdit()
        self.watermark_text_entry.setPlaceholderText('Watermark Text Here...')
        layout.addWidget(self.watermark_text_entry)

        # Spacing slider with label
        self.slider_spacing_layout = QHBoxLayout()
        self.slider_spacing = QSlider(Qt.Orientation.Horizontal)
        self.slider_spacing.setMinimum(30)  # Represents 0.3
        self.slider_spacing.setMaximum(90)  # Represents 0.9
        self.slider_spacing.setValue(60)    # Default is 0.6
        self.slider_spacing_label = QLabel(str(self.slider_spacing.value() / 100))

        def update_spacing_label(v):
            value = v / 100
            self.slider_spacing_label.setText(f'{value:.2f}')

        self.slider_spacing.valueChanged.connect(update_spacing_label)

        self.slider_spacing_layout.addWidget(QLabel('Spacing:'))
        self.slider_spacing_layout.addWidget(self.slider_spacing)
        self.slider_spacing_layout.addWidget(self.slider_spacing_label)
        layout.addLayout(self.slider_spacing_layout)

        # Options
        self.noise_checkbox_layout = QHBoxLayout()
        self.noise_checkbox_names = ['Date', 'Noise', 'Bands', 'Lock', 'Save Password']
        self.checkboxes = []

        for i in range(len(self.noise_checkbox_names)):
            label = QLabel(self.noise_checkbox_names[i])
            label.setStyleSheet('margin-right: 1px; margin-left: 10px;')  # reduce left margin
            checkbox = QCheckBox()
            checkbox.setChecked(True)
            checkbox.setStyleSheet('margin-right: 20px; margin-left: 0px;')
            self.checkboxes.append(checkbox)
            self.noise_checkbox_layout.addWidget(label)
            self.noise_checkbox_layout.addWidget(checkbox)

        self.noise_checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(self.noise_checkbox_layout)

        # Button
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.click_submit)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def center(self):
        # Set window size
        self.resize(*WINDOW_SIZE)
        # Get the screen's center point
        screen = self.screen().availableGeometry().center()
        # Get the frame geometry of the window
        fg = self.frameGeometry()
        # Move the frame geometry's center to the screen center
        fg.moveCenter(screen)
        # Move the window's top-left point to the frame geometry's top-left (centered)
        self.move(fg.topLeft())

    def click_submit(self):
        # Get the values from the widgets
        file_paths = self.file_drop.file_paths
        watermark_text = self.watermark_text_entry.text()
        spacing = self.slider_spacing.value() / 100
        options = [checkbox.isChecked() for checkbox in self.checkboxes]

        # Change button color to green
        self.submit_button.setStyleSheet('''
            QPushButton {
                background-color: green;
                color: white;
                border-radius: 5px;
                border: 1px solid #555;
                padding: 1px 4px;  /* smaller padding */
            }
        ''')

        watermark(file_paths, watermark_text, spacing, *options)
        
        # QTimer to reset color after 2 seconds (2000 ms)
        QTimer.singleShot(2000, self.reset_submit_button_color)

    def reset_submit_button_color(self):
        # Restore to default (or your preferred) style
        self.submit_button.setStyleSheet('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    qdarktheme.setup_theme('auto')
    window = WatermarkWindow()
    window.show()
    sys.exit(app.exec())
