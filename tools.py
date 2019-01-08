import sublime, sublime_plugin

class CursorsFromSelectionCommand(sublime_plugin.TextCommand):
    """ For a block(s) of selected text, unselect and add a cursor at the beginning of every line
    """
    def run(self, edit):

        # view.line(view.sel()[0])

        new_regions = []
        for region in self.view.sel():
            line_begs = [line_regs.begin() for line_regs in self.view.lines(region)]
            new_regions += [sublime.Region(line_beg,line_beg) for line_beg in line_begs]

        self.view.sel().clear()
        for reg in new_regions:
            self.view.sel().add(reg)

        #     line_contents = self.view.substr(line)

        #     if up:
        #       self.view.insert(edit, line.end(), "\n" + line_contents)
        #     else:
        #       self.view.insert(edit, line.begin(), line_contents + "\n")