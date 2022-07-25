#// IMPORT
from os import cpu_count
from concurrent.futures import ThreadPoolExecutor as Executor


#// LOGIC
class ThreadLinesAdd:
    def __init__(self, refLines:int, substring:str|None=None, amount:int=0):
        """**ThreadLinesAdd** purpose is to get the amount number lines by useing the power of multi threading.

        You can not use substring and amount in the same time. Juse one of it because if substring is given,
        will use that to process the logic. Otherwise, the amount will be used instead.

        >>> my_lines:int = 1 # Your existing line numbers
        >>> my_text:str = "Your text to process"
        >>> t = ThreadLinesAdd(my_lines, my_text)
        >>> t.lines # The total line numbers found as integer
        >>> t.text  # The extra line numbers text

        :param refLines:    The reference of existing line numbers as integer.
        :param substring:   The text to process as string.
        :param amount:      The amount of addition.

        :raise ValueError:  If are no new lines and is no need to process forward."""
        # Local Variables
        self.lines:int = 0
        self.text:str = ""

        # Protected Variables
        self.__refLines = refLines
        self.__substring = substring
        self.__threads:int = cpu_count()
        self.__linesThread:int = 0

        if self.__substring is not None:
            # Count the amount of new lines
            with Executor() as executor:
                executor.map(self._lines_count, self.__substring)
                # Save the amount of available threads base on previous used threads amount
                self.__threads = len(executor._threads)

            self._check_if_is_necessary_to_go_forward()

            # Set an equal amount of lines to be processes by each thread
            self.__linesThread = self.lines // self.__threads

            # Because one line for each thread will do some useless math after like
            # multiplication by one and adding zero. Overall, the line number is:
            # lineNumber = linesPerThread * ThreadIndex + ExistingLines + 1 + threadLineIndex
            # And in this case ThreadIndex is the line number itself and the math will be:
            # lineNumber = 1 * lineNumber + ExistingLines + 1 + 0
            # If is at leas two line for each thread
            if self.__linesThread > 1:
                # Get a list of offsets base on amount of threads
                # [0, 1, 2, ..., n-1] --> n = amount of available threads
                offsets:list[int] = [ti for ti in range(self.__threads)]

                # Create the text version of the line numbers
                with Executor() as executor:
                    results = executor.map(self._lines_text, offsets)

                    # Assemble all text version of line numbers in one piece
                    for result in results: self.text += result

                # Get the lost line (the rest of lines what was not perfect divided by amount of threads)
                linesLost:int = self.lines % self.__threads
                # If we have lost lines then add them to
                if linesLost > 0: self.text += self._lines_lost_text(linesLost)

            # Otherwise, do it one by one
            else: self.text += self._lines_text_low_level()

        # Otherwise, same logic as above, but just with the provided amount
        else:
            self.lines = amount
            self._check_if_is_necessary_to_go_forward()

            self.__linesThread = self.lines // self.__threads

            if self.__linesThread > 1:
                offsets:list[int] = [ti for ti in range(self.__threads)]

                with Executor() as executor:
                    results = executor.map(self._lines_text, offsets)

                    for result in results: self.text += result

                linesLost:int = self.lines % self.__threads
                if linesLost > 0: self.text += self._lines_lost_text(linesLost)

            else:
                self.text += self._lines_text_low_level()

    def _lines_count(self, substring:str) -> None:
        """Count the amount of new lines."""
        if substring == "\n": self.lines += 1

    def _lines_text(self, offset:int) -> str:
        """Convert the line numbers in a string version of it.

        :param offset:  The offset line numbers base on thread index.
        :return:        The line numbers as a string."""
        sample:str = ""
        localOffset:int = self.__linesThread * offset + self.__refLines + 1

        for lineIndex in range(self.__linesThread):
            lineNumber = localOffset + lineIndex
            sample += f"\n{lineNumber}"

        return sample

    def _lines_lost_text(self, amount:int) -> str:
        """Convert the lost line numbers in a string version of it.

        :param amount:  The amount of lost lines.
        :return:        The line numbers as a string."""
        sample:str = ""
        localOffset:int = self.lines - amount + self.__refLines + 1

        for lineIndex in range(amount):
            lineNumber = localOffset + lineIndex
            sample += f"\n{lineNumber}"

        return sample

    def _lines_text_low_level(self) -> str:
        """The low lever of convert the line numbers in a string version of it.

        :return:        The line numbers as a string."""
        sample:str = ""
        localOffset:int = self.__refLines + 1

        for lineIndex in range(self.lines):
            lineNumber = localOffset + lineIndex
            sample += f"\n{lineNumber}"

        return sample

    def _check_if_is_necessary_to_go_forward(self) -> None:
        if self.lines == 0: raise ValueError("There are no new lines to add.")


class ThreadLinesSubstract:
    def __init__(self, refLines:str, substring:str|None=None, amount:int=0):
        """**ThreadLinesSubstract** purpose is to get the amount number lines by useing the power of multi threading.

        You can not use substring and amount in the same time. Juse one of it because if substring is given,
        will use that to process the logic. Otherwise, the amount will be used instead.

        >>> my_lines:str = "Your line number text"
        >>> my_text:str = "Your text to process"
        >>> t = ThreadLinesSubstract(my_lines, my_text)
        >>> t.lines # The total line numbers found as integer
        >>> t.text  # The new line numbers text

        :param refLines:    The reference of existing line numbers text.
        :param substring:   The text to process as string.
        :param amount:      The amount of addition.

        :raise ValueError:  If are no lines and is no need to process forward."""
        # Local Variables
        self.lines:int = 0
        self.text:str = ""

        # Protected Variables
        self.__refLines = refLines
        self.__substring = substring
        self.__index:int = 0

        if self.__substring is not None:
            # Count the amount of new lines
            with Executor() as executor:
                executor.map(self._lines_count, self.__substring)

        # Otherwise, use just the provided amount
        else: self.lines = amount

        # Get the text line numbers
        self._lines_text()

    def _lines_count(self, substring:str) -> None:
        """Count the amount of new lines."""
        self.__index += 1
        if substring == "\n": self.lines += 1

    def _lines_text(self) -> None:
        """Sample the new text line numbers."""
        if self.lines == 0: raise ValueError("There are no lines to subtract.")

        sample:list = self.__refLines.rsplit("\n", self.lines)
        self.text = sample[0]
        print(self.__refLines[:-self.__index])
        # self.text = self.__refLines[:-self.__index]



