#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from iws2.crew import Iws2Crew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'An individualized rescue plan for a struggling student',
    }

    try:
        Iws2Crew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
