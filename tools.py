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

        print('Run CursorsFromSelectionCommand')
        # view.line(view.sel()[0])

        new_regions = []
        for region in self.view.sel():
            line_begs = [line_regs.begin() for line_regs in self.view.lines(region)]
            new_regions += [sublime.Region(line_beg, line_beg) for line_beg in line_begs]

        self.view.sel().clear()
        for reg in new_regions:
            self.view.sel().add(reg)

class AddRmrfCommand(sublime_plugin.TextCommand):
    """ Add "rm -rf" at the beginning of currently selected lines"

    The command name for key-bindings etc will be add_rmrf
    """
    def run(self, edit):

        print('Run AddRmrfCommand')

        insert_points = []
        for region in self.view.sel():
            for line in self.view.lines(region):
                insert_points.append(line.begin())

        # we have to keep track of the effects of previous insertions on a
        # point's current location. (unfortunately, we can't just iterate
        # through a bunch of regions and replace them all, because of this)
        num_chars_inserted = 0
        for pt in insert_points:
            num_chars_inserted += self.view.insert(edit, pt + num_chars_inserted, 'rm -rf ')

class CursorsFromSelectionSoftBegCommand(sublime_plugin.TextCommand):
    """ For a block(s) of selected text, unselect and add a cursor at the soft beginning of every
    line (where the text starts)

    The command name for key-bindings etc will be cursors_from_selection_soft_beg
    """
    def run(self, edit):

        print('Run CursorsFromSelectionSoftBegCommand')
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

        print('Run GoToSoftBegLineCommand')

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

class SelectToSoftBegLineCommand(sublime_plugin.TextCommand):
    """ Select to the soft beginning of the line

    The command name for key-bindings etc will be  select_to_soft_beg_line
    """
    def run(self, edit):

        print('Run SelectToSoftBegLineCommand')

        new_regions = []
        for region in self.view.sel():
            first_line = self.view.lines(region)[0]
            first_line_s = self.view.substr(first_line)
            first_line_beg_indx = len(first_line_s) - len(first_line_s.lstrip())
            first_line_soft_beg = first_line.begin() + first_line_beg_indx
            new_regions += [sublime.Region(first_line_soft_beg, region.end())]

        self.view.sel().clear()
        for reg in new_regions:
            self.view.sel().add(reg)

class CustomEndLineCommand(sublime_plugin.TextCommand):
    """ Replacement for the usual ctrl-e command. Goes to the end of the line if cursor is in the
    middle of the line, otherwise will place the cursor in a useful place within the line.

    The command name for key-bindings etc will be custom_end_line
    """
    def run(self, edit):

        print('Run CustomEndLineCommand')

        new_regions = []
        for region in self.view.sel():
            end_reg = region.end()

            last_line = self.view.lines(region)[-1]
            last_line_end = last_line.end()

            if end_reg == last_line_end:
                last_line_s = self.view.substr(last_line)
                locs = []
                # the things to look for. Place cursor directly in front of the last-found of any of
                # these characters
                locs += [last_line_s.rfind(')')]
                locs += [last_line_s.rfind(']')]
                locs += [last_line_s.rfind('}')]
                locs += [last_line_s.rfind(':')]
                locs += [last_line_s.rfind("'")]

                loc = max(locs)
                if loc == -1:
                    loc = len(last_line_s)

                loc += last_line.begin()
                new_regions += [sublime.Region(loc, loc)]

            else:
                new_regions += [sublime.Region(last_line_end, last_line_end)]

        self.view.sel().clear()
        for reg in new_regions:
            self.view.sel().add(reg)


class SelectToCustomEndLineCommand(sublime_plugin.TextCommand):
    """ Select to the custom end line point

    The command name for key-bindings etc will be select_to_custom_end_line
    """
    def run(self, edit):

        print('Run SelectToCustomEndLineCommand')

        new_regions = []
        for region in self.view.sel():
            end_reg = region.end()

            last_line = self.view.lines(region)[-1]
            last_line_end = last_line.end()

            if end_reg == last_line_end:
                last_line_s = self.view.substr(last_line)
                locs = []
                # the things to look for. Place cursor directly in front of the last-found of any of
                # these characters
                locs += [last_line_s.rfind(')')]
                locs += [last_line_s.rfind(']')]
                locs += [last_line_s.rfind('}')]
                locs += [last_line_s.rfind(':')]
                locs += [last_line_s.rfind("'")]

                loc = max(locs)
                if loc == -1:
                    loc = len(last_line_s)

                loc += last_line.begin()
                new_regions += [sublime.Region(loc, loc)]

            else:
                new_regions += [sublime.Region(region.begin(), last_line_end)]

        self.view.sel().clear()
        for reg in new_regions:
            self.view.sel().add(reg)


class ChainAceJumpCommand(sublime_plugin.WindowCommand):
    def run(self, commands):
        """ Chain multiple commands together, respecting timing for the AceJump commands.

        For any AceJump commands, this function will pinch off the remaining commands after the
        AceJump and pass them to AceJump for later execution. This is necessary because we can't do
        concurrency in sublime plugins.

        Based on Chain of Command sublime package:
            - https://packagecontrol.io/packages/Chain%20of%20Command
            - https://github.com/jisaacks/ChainOfCommand/blob/master/chain.py
        Modified the vanilla AceJump to play well:
            - https://packagecontrol.io/packages/AceJump
            - https://github.com/ice9js/ace-jump-sublime/blob/master/ace_jump.py
            - See ReadMe for details on how to get the modified version.

        The command name for key-bindings etc will be chain_ace_jump
        """

        break_after = False
        window = self.window
        for i, command in enumerate(commands):
            command_name = command[0]

            # if we're doing an ace_jump command we need to pinch off the remaining commands, for
            # delegation.
            remaining_commands = []
            if 'ace_jump' in command_name:
                remaining_commands = commands[i+1:]
                break_after = True

            # Get the command args. This should be a dictionary of key value pairs where each key
            # is for each command arg, e.g. {'retries: 5', 'verbose': True}
            try:
                command_args = command[1]
            except:
                command_args = {}

            # if there was a command_args provided, make sure it's a dict
            assert isinstance(command_args, dict)

            # only add a remaining_commands arg if we're gonna do an ace_jump command
            if 'ace_jump' in command_name:
                command_args['remaining_commands'] = remaining_commands

            window.run_command(command_name, command_args)

            # if we delegated to ace jump to run the rest of the commands, we should break now.
            # Otherwise the loop will make us execute the subsequent commands again!
            if break_after:
                break

class MoveVisibleRegionBeginCommand(sublime_plugin.TextCommand):
    """ 
    Moves cursor to beginning of currently-visible region

    The command name for key-bindings etc will be move_visible_region_begin
    """

    def run(self, edit):

        print('Run MoveVisibleRegionBeginCommand')

        screenful = self.view.visible_region()

        # move to second line ... it ends up working better with incremental find and making the
        # screen less jumpy
        second_line_begin = self.view.lines(screenful)[1].begin()

        begin_region = sublime.Region(second_line_begin, second_line_begin)

        self.view.sel().clear()
        self.view.sel().add(begin_region)

class SaveLocationCommand(sublime_plugin.TextCommand):
    """ 
    Save the current cursor locations

    The command name for key-bindings etc will be save_location
    """

    def run(self, edit):

        print('Run SaveLocationCommand')

        # save all current cursor locations
        SavedLocationReturnCommand.saved_locations = []
        for reg in self.view.sel():
            SavedLocationReturnCommand.saved_locations.append(reg.begin())

class SavedLocationReturnCommand(sublime_plugin.TextCommand):
    """ 
    Returns cursors to previously-saved locations, if any

    The command name for key-bindings etc will be saved_location_return
    """

    # keeps track of the cursor location from before running this command
    # note this static member is meant to be overwritten in other places....don't assume only this
    # class can write to it!
    saved_locations = []

    def run(self, edit):

        print('Run SavedLocationReturnCommand')

        return_regions = []
        for loc in SavedLocationReturnCommand.saved_locations:
            return_regions.append(sublime.Region(loc, loc))

        self.view.sel().clear()
        for reg in return_regions:
            self.view.sel().add(reg)

class FixTextSingleLineCommand(sublime_plugin.TextCommand):
    """ 
    Fixes a single line containing a comment or prose for grammatical accuracy

    Performs fixes on individual lines of text within the selection region(s)
    
    Functionality implemented:
    - correct capitalization at the beginning of sentences

    The command name for key-bindings etc will be fix_text_single_line
    """

    def run(self, edit):

        print('Run FixTextSingleLineCommand')

        def get_edit(s):
            """ Returns a string that is a suitable replacement for s
            """
            import re
            # Find the first useful character in the string
            m = re.search("[a-zA-Z0-9]", s)
            trimmed_start = m.start()
            s_trimmed = s[trimmed_start:]
            ## now perform arbitrary string edits
            # Fix first character capitalization
            s_edited = s_trimmed.capitalize()

            return s[:trimmed_start] + s_edited

        new_regions = []
        edits = []
        for region in self.view.sel():
            for line in self.view.lines(region):
                line_s = self.view.substr(line)
                line_s_edited = get_edit(line_s)
                edits.append(line_s_edited)
                new_regions += [sublime.Region(line.begin(), line.end())]

        # self.view.sel().clear()
        for reg, edited in zip(new_regions, edits):
            self.view.replace(edit, reg, edited)
