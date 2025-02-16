import win32gui
import re

class WindowMgr:
  """Encapsulates some calls to the winapi for window management"""

  def __init__ (self):
    """Constructor"""
    self._handle = None
    self._handles = []

  def find_window(self, class_name, window_name=None):
    """find a window by its class_name"""
    self._handle = win32gui.FindWindow(class_name, window_name)

  def _window_enum_callback(self, hwnd, wildcard):
    """Pass to win32gui.EnumWindows() to check all the opened windows"""
    if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
      self._handles.append(hwnd)
      self._handle = hwnd

  def find_window_wildcard(self, wildcard=""):
    """find a window whose title matches the wildcard regex"""
    self._handle = None
    self._handles = []
    win32gui.EnumWindows(self._window_enum_callback, wildcard)

    self.set_handle()

  def set_foreground(self):
    """put the window in the foreground"""
    if self._handle != None:
      win32gui.SetForegroundWindow(self._handle)
    else:
      print("No handle is selected, couldn't set focus")

  def set_handle(self):
    """get one handle to operate on from all the matched handles"""
    if len(self._handles) < 1:
      print("Matched no window")
      return False

    if len(self._handles) > 1:
      print("Selecting the first handle of multiple windows:")
    else: # len(self._handles) == 1:
      print("Matched a single window:")

    self.print_matches()
    self._handle = self._handles[0]
    return True

  def print_matches(self):
    """print the title of each matched handle"""
    blank = 0
    titles = []
    for hwnd in self._handles:
      if str(win32gui.GetWindowText(hwnd)):
        titles.append(str(win32gui.GetWindowText(hwnd)))
        #print("- " + str(win32gui.GetWindowText(hwnd)))
      else:
        blank += 1
    titles_set = set(titles)
    for title in titles_set:
      print(f"-[{titles.count(title)}] {title}")
    print(f"+ {blank} with no title")

if __name__ == "__main__":
    w = WindowMgr()
    #w.find_window_wildcard(".*OpenXcom.*")
    w.find_window_wildcard()
    #w.set_foreground()