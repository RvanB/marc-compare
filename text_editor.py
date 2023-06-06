import wx
import wx.stc
import wx.richtext
import pymarc
import random
import grapheme

def add_styled_text(styled_text_ctrl, text, style_no, default_style_no=3):
    pos = styled_text_ctrl.GetCurrentPos()
    styled_text_ctrl.AddText(text)
    styled_text_ctrl.StartStyling(pos)
    styled_text_ctrl.SetStyling(len(text), style_no)
    styled_text_ctrl.SetStyling(pos + len(text), default_style_no)

def is_fixed_field(field):
    return field.tag in {"006", "007", "008"}

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
 
        with open("/Users/rvan/zephir-ai/rvb/data/DJH/DM.ENG.mrc", 'rb') as f:
            # Pick a random number
            n = random.randint(1, 100)
            
            n = 3
            print(n)
            reader = pymarc.MARCReader(f)
            for i in range(n):
                record = next(reader)
                        
        wx.Frame.__init__(self, parent, title=title, size=(800,600))
        self.control = wx.stc.StyledTextCtrl(self)

        self.control.SetPrintWrapMode(wx.stc.STC_WRAP_WORD)
        self.control.SetWrapMode(wx.stc.STC_WRAP_WORD)
        self.control.SetWrapVisualFlags(wx.stc.STC_WRAPVISUALFLAG_END)
        self.control.SetWrapVisualFlagsLocation(wx.stc.STC_WRAPVISUALFLAGLOC_END_BY_TEXT)

        # Set up fonts
        monospace_font = wx.Font(16, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        roman_font = wx.Font(16, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        font_string = f"face:{roman_font.GetFaceName()},size:{roman_font.GetPointSize()}"

       # self.control.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, f"face:{default_font.GetFaceName()},size:{default_font.GetPointSize()}")

        # Define styles
        # 1: Tags
        self.control.StyleSetSpec(1, f"{font_string},fore:#000000,bold")

        # 2: Indicators
        self.control.StyleSetSpec(2, f"{font_string},fore:#000000")

        # 3: Data
        self.control.StyleSetSpec(3, f"{font_string},fore:#000000")

        # 4: Subfield codes
        self.control.StyleSetSpec(4, f"{font_string},fore:#AA0022,bold")

        leader = record.leader
        add_styled_text(self.control, "LDR ", 3)
        add_styled_text(self.control, f"{str(leader)}\n", 3)
        
        for field in record:
            add_styled_text(self.control, field.tag + " ", 1)
            if field.is_control_field():
                add_styled_text(self.control, str(field.data) + "\n", 3)
                continue
                
            _ind = []
            for indicator in field.indicators:
                if indicator in (" ", "\\"):
                    _ind.append("⊔")
                else:
                    _ind.append(f"{indicator}")

            add_styled_text(self.control, ''.join(_ind) + "\t", 2)

            for i, subfield in enumerate(field.subfields):
                prefix = ' ' if i else ''
                add_styled_text(self.control, f"{prefix}|{subfield.code} ", 4)
                add_styled_text(self.control, f"{subfield.value}", 3)

            self.control.AddText("\n")

        pos = self.control.GetCurrentPos()

        self.control.SetEditable(False)
       
        # Setting up the menu.
        filemenu = wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, "&Exit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()

        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        self.Show(True)

app = wx.App(False)
frame = MainWindow(None, "Sample editor")
app.MainLoop()
