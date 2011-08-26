# pyspiral

Spiral time was a 2am idea for a fancy watch and has nothing to do with spirals. Hours go from 0 up to 12 and back down to 0. Minutes and seconds go from 0 to 30 and back to 0. Pyspiral can convert to spiral time and also has a graphical clock.

## Usage
For any datetime:
```python
from datetime import datetime
from pyspiral import spiraltime
someTime = datetime.now()
print spiraltime(someTime)
```

*Output:* ```↑00:↑03:↓23``` (at 12:04:36 am)

As a shortcut for the current spiral time you can use ```spiralnow()```

To display the graphical clock:
```python
from pyspiral import SpiralClock
x = new SpiralClock()
x.run()
```