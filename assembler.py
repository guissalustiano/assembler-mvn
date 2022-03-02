from pprint import pprint
from typing import List, Union
import argparse
import io
from dataclasses import dataclass

mneumonic_map = {
    'JP': '0',
    'JZ': '1',
    'JN': '2',
    'LV': '3',
    'AD': '4',
    'SB': '5',
    'ML': '6',
    'DV': '7',
    'LD': '8',
    'MM': '9',
    'SC': 'A',
    'RS': 'B',
    'HM': 'C',
    'GD': 'D',
    'PD': 'E',
    'OS': 'F',
    'K': ''
}


@dataclass
class TokenAssembly:
    label: str = None
    address: int = None
    instruction: str = None
    operation: Union[str, int] = None
    comment: str = ''
    original: str = ''


def parse_assembly_file(assembly_file: io.TextIOWrapper):
    for line in assembly_file:
        line = line.rstrip()
        [commands_original, *comment] = line.split(';')

        # comment
        if len(comment) == 0:
            comment = ''
        else:
            comment = ';' + comment[0]

        commands = commands_original.split()
        if len(commands) == 0:
            yield TokenAssembly(comment=comment)
            continue

        # label
        if commands[0].endswith(':'):  # commands[0] is a label
            label = commands.pop(0).rstrip(':')
        else:
            label = None

        # address
        if commands[0].isdigit():  # commands[0] is a address
            address = int(commands.pop(0), 16)
        else:
            address = None

        # instruction
        instruction = commands.pop(0)

        # Operation
        if commands[0].startswith('['):
            operation = commands.pop(0).strip('[]')
        else:
            operation = int(commands.pop(0), 16)

        yield TokenAssembly(label, address, instruction,
                            operation, comment, commands_original)


def addressing(tokens: List[TokenAssembly]):
    address_count = 0
    for token in tokens:
        if token.instruction is None:  # only comment, continue
            continue

        if token.address is None:
            address_count += 2
            token.address = address_count
        else:
            address_count = token.address


def resolve_label(tokens: List[TokenAssembly]):
    map_label = dict()

    for token in tokens:
        if token.label is not None:
            map_label[token.label] = token.address

    for token in tokens:
        if isinstance(token.operation, str):
            token.operation = map_label[token.operation]


def to_line(token: TokenAssembly):
    if token.instruction is None:  # only comment, continue
        return token.comment
    instr_str = mneumonic_map[token.instruction]
    operation_size = 4-len(instr_str)

    return "{0:04x} {1}{2:0{3}x} ; ({4:>12}) {5}".format(
      token.address, instr_str, token.operation, operation_size, token.original, token.comment)


def to_lines(tokens: List[TokenAssembly]):
    return '\n'.join(to_line(t) for t in tokens)


def main(filename: str):
    with open(filename) as f:
        tokens = list(parse_assembly_file(f))
        addressing(tokens)
        resolve_label(tokens)
        print(to_lines(tokens))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Salustiano assembler')
    parser.add_argument('filename', type=str,
                        help='.amvn file')
    args = parser.parse_args()
    filename = args.filename
    main(filename)
