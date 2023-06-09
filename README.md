# μ-awk
This is a tiny Python implementation of a line processor with Awk-like semantics. You write a set of regex-based rules. The program loops through the lines of some input file, running the matching functions on lines that match.

This package is too small by any margin to qualify for the status of "package", but I keep finding myself copy-pasting this code,making small improvements every time otherwise.

## Install
It is considered best practice to use a virtual environment. I recommend using [`poetry`](https://python-poetry.org/). If you do use Poetry, you can add it to your project by running:

```
poetry add mawk
```

Otherwise, using `pip`:

```
pip install mawk
```

## Tutorial
A μ-awk routine is a set of methods that are triggered on regexes. The routine will recieve the `re.Match` object and is expected to return one of three things:

* `None`: ignore that I was ever called, continue to find another rule
* `[]`: the rule completed successfully, but didn't generate any output
* `["any", "number of", "strings"]`: replace the given input line with these lines

Suppose we want to create an outline from a Markdown document, we may filter on lines starting with a `#` character.
You then write a class that derives from `mawk.RuleSet` and decorate its methods with `mawk.on_match`.

```python
from dataclasses import dataclass
import mawk
import re


@dataclass
class Outliner(mawk.RuleSet):
    ignore: bool = False

    @mawk.on_match(r"^#.*$")
    def on_header(self, m: re.Match):
        if self.ignore:
            return
        return [m[0]]

    @mawk.on_match(r"^```")
    def on_codeblock(self, _):
        self.ignore = not self.ignore
        return []

    @mawk.always
    def otherwise(self, _):
        return []


if __name__ == "__main__":
    with open("README.md", "r") as f:
        print(Outliner().run(f.read()))
```

This will output:

```
# μ-awk
## Install
## Tutorial
## License
```

Note that we had to ignore the content of code-blocks, so that the expected output above isn't included in the real output.

The `mawk.always` decorator always matches; the passed argument is therefore a `str` not `re.Match`. Rules are matched in order of definition; by default only the first match is used.

## License
Copyright 2023, the Netherlands eScience Center.
This package is distributed under the Apache 2 License, see LICENSE.
