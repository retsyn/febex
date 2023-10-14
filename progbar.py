"""
progbar.py
Created: Friday, 13th October 2023 11:09:51 am
Matthew Riche
Last Modified: Friday, 13th October 2023 11:10:00 am
Modified By: Matthew Riche
"""

import maya.mel
import maya.cmds as cmds


def start_progbar(max_value, message="Please Wait."):
    """
    start_progbar

    Starts a breakable "main progress bar" in a Maya scene.  This allows for the breaking of loops
    by a user with ESC as well.

    usage - start_progbar([int], message=[string])
    first int is the maximum size of the progbar.
    message - the displayed status message next to the progress bar.
    """

    globals()["gMainProgressBar"] = maya.mel.eval("$tmp = $gMainProgressBar")
    cmds.progressBar(
        globals()["gMainProgressBar"],
        edit=True,
        beginProgress=True,
        isInterruptable=True,
        status=message,
        maxValue=max_value,
        minValue=0,
    )

    return


def update_progbar(step_size=1):
    """
    update_progbar

    Updates the progress bar easily.
    Won't work unless 'gMainProgressBar' is registered in globals().

    usage - update_progbar(step_size=int)
    step_size - how many units the progbar will step by.
    """

    cmds.progressBar(globals()["gMainProgressBar"], edit=True, step=step_size)

    return


def end_progbar():
    """
    end_progbar

    Ends the progress bar easily.
    There must be 'gMainProgressBar' registered in globals().

    usage - end_progbar()
    """

    cmds.progressBar(globals()["gMainProgressBar"], edit=True, endProgress=True)

    return
