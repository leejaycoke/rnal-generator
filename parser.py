#-*- coding: utf-8 -*-

class LineParser(object):

    FILE_FINDER = re.compile(r'{file:\w+}')
    FILENAME_PATTERN = re.compile(r'')

    def __init__(self, line):
        self.line = line
        parse()

    def get_file_patterns(self):
        return FILE_FINDER.findall(self.line)

    def get_filename(self, file_pattern):
        return

    def parse(self):
        file_patterns = get_file_patterns()
        for file_pattern in file_patterns:
            pass
