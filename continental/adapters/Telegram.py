import dataclasses
import json
import re

from ..Adapter import Adapter


@dataclasses.dataclass
class Telegram(Adapter):
    users: list = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self._user = None
        self._collecting_message = False
        self._skip_next_text = False

    def __call__(self):
        for line in self.text:
            if self._user:
                if self._collecting_message:
                    if '"text": ' in line and not self._skip_next_text:
                        yield json.loads(next(iter(re.finditer('"text": (".*"),?\n', line))).group(1))
                    elif '"type": "blockquote"' in line:
                        self._skip_next_text = True
                    elif re.match(r" *\]", line):
                        yield ".\n"
                        self._collecting_message = False
                        self._user = None
                elif ('"text_entities": [\n' in line) and (self._user is not None):
                    self._collecting_message = True
                elif ('"text_entities": []' in line) or ('"forwarded_from": ' in line):
                    self._user = None
            elif '"from_id": "' in line:
                candidate_user = next(iter(re.finditer('"from_id": "(.*)",\n', line))).group(1)
                if candidate_user in self.users:
                    self._user = candidate_user
                    self.collecting_message = True
