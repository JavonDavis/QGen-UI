class InvalidConfigException(Exception):
    """Thrown when the configuration for a question is invalid"""


class EvaluationException(Exception):
    """Thrown when an excetption was thrown from either the evaluation of a code block or a user function call"""
