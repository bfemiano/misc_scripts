"""
    Wario is a very crude, lightweight version of Luigi's task -> target dependency model. It does not support
    external targets, Parameters, any kind of centralized scheduling, or Hadoop/S3 support. It only supports a single
    worker thread and has sub-standard logging.

    It is named after the 3rd Mario brother whom nobody really likes, and nobody really picks if there is a better
    option left in the game menu. That is a perfect reflection of this tool.
    You shouldn't use it if Luigi is available on your environment, but in case it's not and all you have is core
    python.

    See the tests under tests/unit/bdm/wario/test_wario_core.py to get a sense of which Luigi functionality
    is supported.

"""