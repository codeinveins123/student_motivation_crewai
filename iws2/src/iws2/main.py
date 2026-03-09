#!/usr/bin/env python
import sys
import warnings
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

from iws2.crew import Iws2

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'An individualized rescue plan for a struggling student',
    }

    try:
        Iws2().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
