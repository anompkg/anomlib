## Parameters that parse args
commands = {
    'hash': {
        'options': {
            'hash': {
                'args': ['-H', '--hasher'],
                'kwargs': {
                    'help': 'Hasher in %(prog)s program',
                    'default': "md5"}
            }
        },
        'flags': {
            'source': {
                'args': ['-s'],
                'kwargs': {}
            }
        }
    },
    'pull': {
        'options': {
            'days': {
                'args': ['-D'],
                'kwargs': {
                    'help': 'Days before refresh.',
                    'default': -7,
                    'type': int
                }
            },
            'hours': {
                'args': ['-H'],
                'kwargs': {
                    'help': 'Hours before refresh.',
                    'default': +5,
                    'type': int
                }
            }
        }
    },
    'do': {
        'options': {
            'color': {
                'args': ['-c'],
                'kwargs': {
                    'help': "Set prompt's color.",
                    'default': "Yellow"
                }
            },
            'prompt': {
                'args': ['-p'],
                'kwargs': {
                    'help': 'Set prompt.',
                    'default': "with "
                }
            },
            'readline': {
                'args': ['-r', '-i', '--inputline'],
                'kwargs': {
                    'help': 'Set readline tool.',
                    'default': "rlwrap"
                }
            },
            'history': {
                'args': ['-H'],
                'kwargs': {
                    'help': 'History file for %(prog)s program',
                    'default': "test"
                }
            }
        },
    },
    'repl': {}, # will be like 4g with but for interactively working with 4g.
    'help': {},
    'install': {},
    'master': {
        'options': {
            'output': {
                'args': ['-o'],
                'kwargs': {'help': 'Write Output into a file.'}
            },
            'foo': {
                'args': [],
                'kwargs': {'help': 'foo of the %(prog)s program'}
            }
        },
        'flags': {
            'verbose': {
                'args': ['-v'],
                'kwargs': {'help': 'Verbose output.'}
            },
            'act': {
                'args': ['-a'],
                'kwargs': {'help': 'Test count.'},
            }

        }
    }
}

