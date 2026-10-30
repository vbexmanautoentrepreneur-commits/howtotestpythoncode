import re, sys, subprocess
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTextBrowser, QTableWidget, QTableWidgetItem, QSplitter, QProgressBar,)


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        self.setWindowTitle("PyTest Dashboard")
        self.resize(1200, 800)
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        self.btn_run = QPushButton("🚀 Run Tests")
        self.btn_run.clicked.connect(self.run_tests)
        layout.addWidget(self.btn_run)
        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)
        splitter = QSplitter(Qt.Vertical)
        layout.addWidget(splitter)
        self.summary = QTextBrowser()
        self.test_table = QTableWidget()
        self.test_table.setColumnCount(2)
        self.test_table.setHorizontalHeaderLabels(["Test", "Status"])
        self.test_table.setColumnWidth(0, 800)
        self.test_table.horizontalHeader().setStretchLastSection(True)
        self.coverage = QTextBrowser()
        splitter.addWidget(self.summary)
        splitter.addWidget(self.test_table)
        splitter.addWidget(self.coverage)
        splitter.setSizes([200, 450, 250])
        self.setup_dark_theme()

    def setup_dark_theme(self):

        self.setStyleSheet("""
                QMainWindow { background-color: #1e1e1e; }
                QWidget { background-color: #1e1e1e; color: #dcdcdc; font-size: 10pt; }
                QPushButton { background-color: #0078d7; color: white; border: none; border-radius: 6px; padding: 8px; font-weight: bold; }
                QPushButton:hover { background-color: #2893ff; }
                QPushButton:pressed { background-color: #005a9e; }
                QTextBrowser { background-color: #252526; border: 1px solid #3c3c3c; border-radius: 6px; color: white; }
                QTableWidget { background-color: #252526; color: white; border: 1px solid #3c3c3c; gridline-color: #3c3c3c; }
                QHeaderView::section { background-color: #333333; color: white; padding: 6px; border: none; }
                QProgressBar { border: 1px solid #3c3c3c; border-radius: 6px; text-align: center; background-color: #252526; }
                QProgressBar::chunk { background-color: #28a745; }
                """)

    def run_tests(self):

        self.btn_run.setText("⏳ Running Tests...")
        self.btn_run.setEnabled(False)
        QApplication.processEvents()
        try:
            result = subprocess.run([sys.executable, "-m", "pytest", "-v", "--cov=src", "--cov-report=term-missing",],
                                    capture_output=True, text=True, encoding="utf-8", errors="replace" )

            output = result.stdout + "\n" + result.stderr
            self.parse_summary(output)
            self.parse_tests(output)
            self.parse_coverage(output)

        except Exception as e:
            self.summary.setHtml(
                f"<h2 style='color:red'>Error</h2>"
                f"<pre>{str(e)}</pre>"
            )
        self.btn_run.setText("🚀 Run Tests")
        self.btn_run.setEnabled(True)

    def parse_summary(self, text):
        passed = len(re.findall(r"\bPASSED\b", text))
        failed = len(re.findall(r"\bFAILED\b", text))
        tests = passed + failed
        success_rate = int(passed * 100 / tests) if tests else  0
        self.progress.setValue(success_rate)
        if success_rate == 100:
            self.progress.setStyleSheet("""
            QProgressBar { border: 1px solid #3c3c3c; border-radius: 6px; text-align: center; background-color: #252526; }
            QProgressBar::chunk { background-color: #28a745; }
            """)
            status = "✅ SUCCESS"
        else:
            self.progress.setStyleSheet("""
            QProgressBar { border: 1px solid #3c3c3c; border-radius: 6px; text-align: center; background-color: #252526; }
            QProgressBar::chunk { background-color: #dc3545; }
            """)
            status = "❌ FAILED"

        html = f"""
        <div style=" background:#252526; padding:15px; border-radius:10px; ">
        <h2>{status}</h2>
            <table width="100%">
                <tr>
                    <td><b>Tests</b></td>
                    <td>{tests}</td>
                </tr>
                <tr>
                    <td><b>Passed</b></td>
                    <td style="color:#28a745;">{passed}</td>
                </tr>
                <tr>
                    <td><b>Failed</b></td>
                    <td style="color:#dc3545;">{failed}</td>
                </tr>
                <tr>
                    <td><b>Reliability</b></td>
                    <td>{success_rate}%</td>
                </tr>
            </table>
        </div>
        """

        self.summary.setHtml(html)

    def parse_tests(self, text):
        tests = re.findall(r"([^\s]+::[^\s]+)\s+(PASSED|FAILED)", text)
        self.test_table.setRowCount(len(tests))
        for row, (name, status) in enumerate(tests):
            item_name = QTableWidgetItem(name)
            if status == "PASSED":
                item_status = QTableWidgetItem("✅ PASSED")
                item_status.setTextAlignment(Qt.AlignCenter)
                item_status.setBackground(QColor("#1e4620"))
            else:
                item_status = QTableWidgetItem("❌ FAILED")
                item_status.setTextAlignment(Qt.AlignCenter)
                item_status.setBackground(QColor("#5c1f1f"))
            item_status.setForeground(QColor("white"))
            self.test_table.setItem(row, 0, item_name)
            self.test_table.setItem(row, 1, item_status)
        self.test_table.resizeColumnsToContents()
        self.test_table.setColumnWidth(0, 800)

    def parse_coverage(self, text):
        rows = []
        start = False
        for line in text.splitlines():
            if "Name" in line and "Cover" in line:
                start = True
                continue
            if not start:
                continue
            if not line.strip():
                continue
            m = re.match(r"(.+?)\s+(\d+)\s+(\d+)\s+(\d+%)", line.strip())
            if m:
                rows.append(m.groups())
        html = """
        <div style=" background:#252526; padding:15px; border-radius:10px; ">
            <h2 style="color:white;">📊 Coverage Report</h2>
            <table width="100%" cellspacing="0" cellpadding="6" style=" border-collapse:collapse; color:white; ">
                <tr style=" background-color:#333333; font-weight:bold; ">
                    <th align="left">File</th>
                    <th>Statements</th>
                    <th>Miss</th>
                    <th>Coverage</th>
                </tr>
        """

        for name, stmts, miss, cover in rows:
            color = "#28a745"
            if cover != "100%": color = "#ffc107"
            if cover and int(cover.replace("%", "")) < 80: color = "#dc3545"
            html += f"""
            <tr>
                <td>{name}</td>
                <td align="center">{stmts}</td>
                <td align="center">{miss}</td>
                <td align="center">
                    <span style=" color:{color}; font-weight:bold; ">
                        {cover}
                    </span>
                </td>
            </tr>
            """
        html += """ </table> </div> """
        self.coverage.setHtml(html)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())