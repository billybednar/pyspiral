from datetime import datetime
from time import sleep
import Tkinter

UP_ARROW = u"\u2191"
DOWN_ARROW = u"\u2193"
NO_ARROW = "|"


def tospiral(value, range_=60):
    """Scale a value to half the range with an up/down component.
    
    value -- The value to be scaled. The decimal part is considered in
             determining up/down but is not present in the output. The
             range of possible values is  (0 <= value < range_).
    range_ -- The range of valid values; must be even.
    
    Spiraling maps a value onto a smaller range, but with an up/down
    component. For the first half of the range, spiraled values
    increase from 0 to half the normal range. These are up values. For
    the second half, spiraled values decrease from (range_ / 2) to 0.
    These are down values. Exactly (range_ / 2) is neither up nor down
    and is indicated by NO_ARROW in place of an arrow. The return value
    is a tuple of the arrow character and the scaled value.
    
    """
    value %= range_
    if value == 0:
        return (NO_ARROW, 0)
    elif value < range_ / 2:
        return (UP_ARROW, int(value))
    elif value == range_ / 2:
        return (NO_ARROW, int(value))
    else:
        return (DOWN_ARROW, int(range_ - value))


def spiraltime(t, showmili=False, showspaces=False):
    """Transform a datetime into its spiraled representation"""
    ms = t.microsecond / 1000.0
    s = t.second + ms / 1000.0
    m = t.minute + s / 60.0
    h = t.hour + m / 60.0
    spiral = tospiral(h, 24) + tospiral(m, 60) + tospiral(s, 60)
    
    if showmili:
        if spiral[4] == DOWN_ARROW:
            ms = 1000 - ms
        msString = ("%#.3f" % (ms / 1000))[2:]
        if showspaces:
            return "%s%02d : %s%02d : %s%02d.%s" % (spiral + (msString,))
        else:
            return "%s%02d:%s%02d:%s%02d.%s" % (spiral + (msString,))
    else:
        if showspaces:
            return "%s%02d : %s%02d : %s%02d" % spiral
        else:
            return "%s%02d:%s%02d:%s%02d" % spiral


def spiralnow(showmili=False, showspaces=False):
    """Transform the current time into its spiraled representation"""
    return spiraltime(datetime.now(), showmili, showspaces)


class SpiralClock:
    """Displays a graphical spiral clock"""
    
    def __init__(self, height=400, barwidth=50, barspacing=20, padding=20,
                 upcolor='blue', downcolor='red'):
        """Create a graphical spiral clock"""
        self.visible = False
        
        self.height = float(height)
        self.barwidth = float(barwidth)
        self.barspacing = float(barspacing)
        self.padding = float(padding)
        self.upcolor = upcolor
        self.downcolor = downcolor
        self.ltextwidth = 12.0
        self.btextheight = 12.0
        
        self.width = (2 * padding) + (3 * barwidth) + (2 * barspacing) + (
                     self.ltextwidth)
        self.increment = (height - (2 * padding) - self.btextheight) / 30
        self.interval = int(min(500, 1000 / self.increment))
        
    def run(self):
        """Display the spiral clock window"""
        if self.visible: return
        else: self.visible = True
        
        # make window
        self.master = Tkinter.Tk()
        self.master.title('Spiral Clock')
        self.w = Tkinter.Canvas(self.master, width=self.width,
                                height=self.height)
        self.w.pack()
        
        # create time bars and labels
        self.bars = []
        self.texts = []
        for num in range(3):
            self.bars.append(self.w.create_rectangle(
                self.barx(num), self.bary(0),
                self.barx(num) + self.barwidth, self.bary(0),
                outline=''))
            self.texts.append(self.w.create_text(
                self.barx(num) + self.barwidth / 2,
                self.bary(0),
                justify='center', anchor='n'))
        
        # gridlines and labels
        for i in range(31):
            self.w.create_line(
                self.barx(0), self.bary(i),
                self.barx(2) + self.barwidth, self.bary(i))
            self.w.create_text(
                self.barx(0), self.bary(i),
                text=str(i), anchor='e', justify='right')
        
        # start updating time
        self.update()
        
        # wait until window is closed before returning
        self.master.wait_window(self.master)
    
    def update(self):
        """Update the clock display"""
        t = datetime.now()
        ms = t.microsecond / 1000.0
        s = t.second + ms / 1000.0
        m = t.minute + s / 60.0
        h = t.hour + m / 60.0
        spiral = tospiral(h, 24) + tospiral(m, 60) + tospiral(s, 60)
        
        # reverse values for fractional increments
        if spiral[4] == DOWN_ARROW:
            ms = 1000 - ms
        if spiral[2] == DOWN_ARROW:
            s *= -1
        if spiral[0] == DOWN_ARROW:
            m *= -1
        
        # adjust for those fractional increments
        values = [spiral[1], spiral[3], spiral[5]]
        values[2] += ms / 1000.0
        values[1] += s / 60.0
        values[0] += m / 60.0
        
        # update the bars
        for num in range(3):
            text = spiral[2*num] + str(spiral[2*num + 1])
            if text.startswith(UP_ARROW):
                self.setbar(num, values[num], self.upcolor, text)
            else:
                self.setbar(num, values[num], self.downcolor, text)
        
        # refresh and schedule another update
        self.master.update()
        self.master.after(self.interval, self.update)
        
    def barx(self, num):
        """Calculate the left x-coordinate of a bar"""
        return self.padding + self.ltextwidth + num * (self.barwidth +
               self.barspacing)
    
    def bary(self, height):
        """Calculate the top y-coordinate of a bar"""
        return self.height - self.padding - self.btextheight - (height *
               self.increment)
    
    def setbar(self, num, value, color, text):
        """Change a bars size, color, and text"""
        self.w.coords(
            self.bars[num],
            self.barx(num), self.bary(0),
            self.barx(num) + self.barwidth, self.bary(value))
        self.w.itemconfig(self.bars[num], fill=color)
        self.w.itemconfig(self.texts[num], text=text)


# Do some tests and show usage info when executed directly
if __name__ == "__main__":
    assert(tospiral(0, 60) == (NO_ARROW, 0))
    assert(tospiral(0.1, 60) == (UP_ARROW, 0))
    assert(tospiral(1, 60) == (UP_ARROW, 1))
    assert(tospiral(1.1, 60) == (UP_ARROW, 1))
    assert(tospiral(29, 60) == (UP_ARROW, 29))
    assert(tospiral(29.9, 60) == (UP_ARROW, 29))
    assert(tospiral(30, 60) == (NO_ARROW, 30))
    assert(tospiral(30.1, 60) == (DOWN_ARROW, 29))
    assert(tospiral(31, 60) == (DOWN_ARROW, 29))
    assert(tospiral(31.1, 60) == (DOWN_ARROW, 28))
    assert(tospiral(32, 60) == (DOWN_ARROW, 28))
    assert(tospiral(59, 60) == (DOWN_ARROW, 1))
    assert(tospiral(59.1, 60) == (DOWN_ARROW, 0))
    assert(tospiral(59.9, 60) == (DOWN_ARROW, 0))
    assert(tospiral(60, 60) == (NO_ARROW, 0))

    assert(tospiral(0, 24) == (NO_ARROW, 0))
    assert(tospiral(0.1, 24) == (UP_ARROW, 0))
    assert(tospiral(1, 24) == (UP_ARROW, 1))
    assert(tospiral(11, 24) == (UP_ARROW, 11))
    assert(tospiral(11.9, 24) == (UP_ARROW, 11))
    assert(tospiral(12, 24) == (NO_ARROW, 12))
    assert(tospiral(12.1, 24) == (DOWN_ARROW, 11))
    assert(tospiral(13, 24) == (DOWN_ARROW, 11))
    assert(tospiral(13.1, 24) == (DOWN_ARROW, 10))
    assert(tospiral(23, 24) == (DOWN_ARROW, 1))
    assert(tospiral(23.1, 24) == (DOWN_ARROW, 0))
    assert(tospiral(23.9, 24) == (DOWN_ARROW, 0))
    assert(tospiral(24, 24) == (NO_ARROW, 0))
    
    print "The current spiral time is %s\n\n" % spiralnow(),
    print "Use the spiralnow function to get the spiral time.\n",
    print "To show the graphical clock:\n"
    print "x = SpiralClock()\nx.run()\n"
    #x = SpiralClock()
    #x.run()
