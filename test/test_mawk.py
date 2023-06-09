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


def test_outliner():
    with open("README.md", "r") as f:
        result = Outliner().run(f.read())

    assert (
        result
        == """# μ-awk
## Install
## Tutorial
## License"""
    )


def test_begin_and_eof():
    class TestEof(mawk.RuleSet):
        def on_begin(self):
            return ["hello"]
        def on_eof(self):
            return ["goodbye"]

    assert TestEof().run("") == "hello\ngoodbye"
