# febex

This is a quick and dirty tool to scrub rigs of non-exportable data, allowing for FBXs to better
represent rigs and animations as they are imported into Unity or Unreal.

## Installation:
Unzip the entire febex folder into something that is in your maya path.
If you'd rather put it somewhere else, you can path it like so:
```
import sys
# The path where the febex folder is (change \ to /!)
sys.path.append("install folder of febex")
```
Just make sure the folder where the code lives is called "febex" (If not, account for that in
upcoming steps).

## Running in Maya
Put the following in a script editor or shelf button-- this will work if the febex folder is pathed
correctly (see above).
```
import febex.ui as fb
ui = fb.Febex_Ui()
```

## A word on 'state'
This UI won't recall the lists of influences it just made if you close and re-open it, so try to 
perform all your operations with the window remaining open.  You may have to reload your file after
you've run a procedure on it.
