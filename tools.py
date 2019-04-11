"""Rando tools for sublime text

Author: Kit Kennedy
"""

import sublime, sublime_plugin

class CursorsFromSelectionCommand(sublime_plugin.TextCommand):
    """ For a block(s) of selected text, unselect and add a cursor at the hard beginning of every
    line (in front of whitespace)

    The command name for key-bindings etc will be cursors_from_selection
    """
    def run(self, edit):

        print('Run CursorsFromSelection')
        # view.line(view.sel()[0])

        new_regions = []
        for region in self.view.sel():
            line_begs = [line_regs.begin() for line_regs in self.view.lines(region)]
            new_regions += [sublime.Region(line_beg, line_beg) for line_beg in line_begs]

        self.view.sel().clear()
        for reg in new_regions:
            self.view.sel().add(reg)

class CursorsFromSelectionSoftBegCommand(sublime_plugin.TextCommand):
    """ For a block(s) of selected text, unselect and add a cursor at the soft beginning of every 
    line (where the text starts)

    The command name for key-bindings etc will be cursors_from_selection_soft_beg
    """
    def run(self, edit):

        print('Run CursorsFromSelection')
        # view.line(view.sel()[0])

        new_regions = []
        for region in self.view.sel():
            lines = self.view.lines(region)
            # get text
            lines_s = [self.view.substr(l) for l in lines]
            # find the first spot where there's non-whitespace
            lines_beg_indx = [len(line_s) - len(line_s.lstrip()) for line_s in lines_s]
            # calc absolute begins
            lines_soft_beg = [l.begin() + lbi for l, lbi in zip(lines, lines_beg_indx)]
            new_regions += [sublime.Region(line_beg, line_beg) for line_beg in lines_soft_beg]

        # clear currently selected
        self.view.sel().clear()
        # add new selections at line begs
        for reg in new_regions:
            self.view.sel().add(reg)

class CursorsFromCommaListCommand(sublime_plugin.TextCommand):
    """ For a block(s) of selected text, unselect and add a cursor before the first
    non-whitespace character after every comma

    The command name for key-bindings etc will be cursors_from_comma_list
    """
    def run(self, edit):
        print('Run CursorsFromCommaList')
        new_regions = []
        # for each selection region
        for region in self.view.sel():
            # get the text from the region
            the_text = self.view.substr(region)
            the_text_begins = region.begin()

            def comma_parse(dat_text, comma_parse_state='gobbling_whitespace'):
                """Parse a string, returning indices immediately following a comma+whitespace)

                start out pretending we just found a command right before the text, so that we'll
                add the beginning of the string indx as well
                                
                Args:
                    dat_text: the text
                
                Returns:
                    List of indices within the string
                    List[int]
                """
                indcs = []
                for indx, char in enumerate(dat_text):
                    if comma_parse_state == 'searching_comma':
                        if char == ',':
                            comma_parse_state = 'gobbling_whitespace'
                        else: pass
                    elif comma_parse_state == 'gobbling_whitespace':
                        if char == ' ': pass
                        else: 
                            indcs.append(indx)
                            comma_parse_state = 'searching_comma'
                return indcs

            # find the indices of all commas in the text            
            comma_indcs = comma_parse(the_text)
            comma_indcs = [indx + the_text_begins for indx in comma_indcs]
            # make a new region for each post-comma point. The region is empty because all we want
            # to do is add a cursor at the beginning
            new_regions += [sublime.Region(indx, indx) for indx in comma_indcs]

        # clear cursors
        self.view.sel().clear()
        # add a cursors at each of the discovered regions
        for reg in new_regions:
            self.view.sel().add(reg)

class DeleteToSoftBegLineCommand(sublime_plugin.TextCommand):
    """ Delete to where text begins on the current line(s)

    The command name for key-bindings etc will be  delete_to_soft_beg_line
    """
    def run(self, edit):

        print('Run DeleteToSoftBOLCommand')

        new_regions = []
        for region in self.view.sel():
            # only delete the unselected part at the beginning of the first line of the region (if
            # any)
            first_line = self.view.lines(region)[0]
            # get the text
            first_line_s = self.view.substr(first_line)
            # account for white space
            first_line_beg_indx = len(first_line_s) - len(first_line_s.lstrip())
            # account for absolute pos of line begin.
            reg = sublime.Region(first_line.begin() + first_line_beg_indx, region.a)
            # erase immediately so that ops on subsequent regions are correct
            self.view.erase(edit, reg)

class GoToSoftBegLineCommand(sublime_plugin.TextCommand):
    """ Move to where text begins on the current line(s)

    The command name for key-bindings etc will be  go_to_soft_beg_line
    """
    def run(self, edit):

        print('Run DeleteToSoftBOLCommand')

        new_regions = []
        for region in self.view.sel():
            first_line = self.view.lines(region)[0]
            first_line_s = self.view.substr(first_line)
            first_line_beg_indx = len(first_line_s) - len(first_line_s.lstrip())
            first_line_soft_beg = first_line.begin() + first_line_beg_indx
            new_regions += [sublime.Region(first_line_soft_beg, first_line_soft_beg)]

        self.view.sel().clear()
        for reg in new_regions:
            self.view.sel().add(reg)
