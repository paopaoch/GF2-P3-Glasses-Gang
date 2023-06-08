"""Implement the graphical user interface for the Logic Simulator.

Used in the Logic Simulator project to enable the user to run the simulation
or adjust the network properties.

Classes:
--------
MyGLCanvas - handles all canvas drawing operations.
Gui - configures the main window and all the widgets.
"""
import wx
import os
import builtins
import wx.glcanvas as wxcanvas
from OpenGL import GL, GLUT
from pathlib import Path

from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner
from parse import Parser

builtins._ = wx.GetTranslation


class MyGLCanvas(wxcanvas.GLCanvas):
    """Handle all drawing operations.

    This class contains functions for drawing onto the canvas. It
    also contains handlers for events relating to the canvas.

    Parameters
    ----------
    parent: parent window.
    devices: instance of the devices.Devices() class.
    monitors: instance of the monitors.Monitors() class.

    Public methods
    --------------
    init_gl(self): Configures the OpenGL context.

    render(self, text): Handles all drawing operations.

    on_paint(self, event): Handles the paint event.

    on_size(self, event): Handles the canvas resize event.

    on_mouse(self, event): Handles mouse events.

    render_text(self, text, x_pos, y_pos): Handles text drawing
                                           operations.

    reset_view(self): Return to the initial view point

    capture_image(self): Capture the OpenGL canvas content as
                            an image

    save_image(self, file_path): Save the image on the computer
    """

    def __init__(self, parent, devices, monitors):
        """Initialise variables"""
        self.devices = devices
        self.monitors = monitors
        self.cycles_completed = 0
        """Initialise canvas properties and useful variables."""
        super().__init__(parent, -1,
                         attribList=[wxcanvas.WX_GL_RGBA,
                                     wxcanvas.WX_GL_DOUBLEBUFFER,
                                     wxcanvas.WX_GL_DEPTH_SIZE, 16, 0])
        GLUT.glutInit()
        self.init = False
        self.context = wxcanvas.GLContext(self)

        # Initialise variables for panning
        self.pan_x = 0
        self.pan_y = 0
        self.last_mouse_x = 0  # previous mouse x position
        self.last_mouse_y = 0  # previous mouse y position

        # Initialise variables for zooming
        self.zoom = 1

        # Bind events to the canvas
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse)

    def init_gl(self):
        """Configure and initialise the OpenGL context."""
        size = self.GetClientSize()
        self.SetCurrent(self.context)
        GL.glDrawBuffer(GL.GL_BACK)
        GL.glClearColor(1.0, 1.0, 1.0, 0.0)
        GL.glViewport(0, 0, size.width, size.height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(0, size.width, 0, size.height, -1, 1)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glTranslated(self.pan_x, self.pan_y, 0.0)
        GL.glScaled(self.zoom, self.zoom, self.zoom)

    def render(self, text, cycles=0, gui_monitors={}):
        """Handle all drawing operations."""

        if cycles > 0:
            self.cycles_completed = cycles
            self.gui_monitors = gui_monitors
            # gui_monitors = {monitor_string: signal_list}

        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        margin = self.monitors.get_margin()
        if not margin:
            margin = 0

        # Clear everything
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        self.render_text(text, 10, 10)

        if self.cycles_completed > 0:
            GL.glBegin(GL.GL_LINES)
            # Draw x-axis
            GL.glColor3f(1.0, 0.0, 0.0)  # Red color
            cycle_width = 20
            y_val = 50
            if margin:
                x_start = 100 + margin
            else:
                x_start = 100
            x_end = x_start + (self.cycles_completed + 1)*cycle_width
            GL.glVertex2f(x_start, y_val)
            GL.glVertex2f(x_end, y_val)

            par = 10
            for i in range(self.cycles_completed+1):
                GL.glVertex2f(x_start+i*cycle_width, y_val+par)
                GL.glVertex2f(x_start+i*cycle_width, y_val-par)
            GL.glEnd()
            # Draw arrowhead
            GL.glBegin(GL.GL_TRIANGLES)
            # Bottom-left point of arrowhead
            GL.glVertex2f(x_end - 10, y_val - 5)
            # Tip of arrowhead
            GL.glVertex2f(x_end, y_val)
            # Bottom-right point of arrowhead
            GL.glVertex2f(x_end - 10, y_val + 5)
            GL.glEnd()

            # label the axis
            self.render_text("Time", 50, y_val)
            for i in range(self.cycles_completed+1):
                self.render_text(str(i), x_start+i*cycle_width, y_val-10)

            # draw output signals at monitoring points
            for i in range(len(self.gui_monitors)):
                monitor_str_list = list(self.gui_monitors.keys())
                monitor_str = monitor_str_list[i]
                height = y_val + (i+1)*100
                self.render_text(monitor_str, 50, height)
                self.render_text("1", x_start-10, height+20)
                self.render_text("0", x_start-10, height-20)
                signal_list = self.gui_monitors[monitor_str]
                GL.glColor3f(0.0, 0.0, 1.0)  # signal trace is blue
                GL.glBegin(GL.GL_LINE_STRIP)
                for j in range(self.cycles_completed):
                    if signal_list[j] == self.devices.LOW:
                        GL.glVertex2f(x_start+j*cycle_width, height-20)
                        GL.glVertex2f(x_start+(j+1)*cycle_width, height-20)
                    elif signal_list[j] == self.devices.HIGH:
                        GL.glVertex2f(x_start+j*cycle_width, height+20)
                        GL.glVertex2f(x_start+(j+1)*cycle_width, height+20)
                    elif signal_list[j] == self.devices.RISING:
                        GL.glVertex2f(x_start+j*cycle_width, height)
                        GL.glVertex2f(x_start+(j+1)*cycle_width, height+20)
                    elif signal_list[j] == self.devices.FALLING:
                        GL.glVertex2f(x_start+j*cycle_width, height)
                        GL.glVertex2f(x_start+(j+1)*cycle_width, height-20)
                GL.glEnd()

        # We have been drawing to the back buffer, flush the graphics pipeline
        # and swap the back buffer to the front
        GL.glFlush()
        self.SwapBuffers()

    def on_paint(self, event):
        """Handle the paint event."""
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True
        self.render("")

    def on_size(self, event):
        """Handle the canvas resize event."""
        # Forces reconfiguration of the viewport, modelview and projection
        # matrices on the next paint event
        self.init = False

    def on_mouse(self, event):
        """Handle mouse events."""
        text = ""
        # Calculate object coordinates of the mouse position
        size = self.GetClientSize()
        ox = (event.GetX() - self.pan_x) / self.zoom
        oy = (size.height - event.GetY() - self.pan_y) / self.zoom
        old_zoom = self.zoom
        if event.ButtonDown():
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
            text = "".join([_(u"Mouse button pressed at: "), str(event.GetX()),
                            ", ", str(event.GetY())])
        if event.ButtonUp():
            text = "".join([_(u"Mouse button released at: "),
                            str(event.GetX()), ", ", str(event.GetY())])
        if event.Leaving():
            text = "".join([_(u"Mouse left canvas at: "), str(event.GetX()),
                            ", ", str(event.GetY())])
        if event.Dragging():
            self.pan_x += event.GetX() - self.last_mouse_x
            self.pan_y -= event.GetY() - self.last_mouse_y
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
            self.init = False
            text = "".join([_(u"Mouse dragged to: "), str(event.GetX()),
                            ", ", str(event.GetY()), _(u". Pan is now: "),
                            str(self.pan_x), ", ", str(self.pan_y)])
        if event.GetWheelRotation() < 0:
            self.zoom *= (1.0 + (
                event.GetWheelRotation() / (20 * event.GetWheelDelta())))
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
            text = "".join([_(u"Negative mouse wheel rotation. Zoom is now: "),
                            str(self.zoom)])
        if event.GetWheelRotation() > 0:
            self.zoom /= (1.0 - (
                event.GetWheelRotation() / (20 * event.GetWheelDelta())))
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
            text = "".join([_(u"Positive mouse wheel rotation. Zoom is now: "),
                            str(self.zoom)])
        if text:
            self.render(text)
        else:
            self.Refresh()  # triggers the paint event

    def render_text(self, text, x_pos, y_pos):
        """Handle text drawing operations."""
        GL.glColor3f(0.0, 0.0, 0.0)  # text is black
        GL.glRasterPos2f(x_pos, y_pos)
        font = GLUT.GLUT_BITMAP_HELVETICA_12
        for character in text:
            if character == '\n':
                y_pos = y_pos - 20
                GL.glRasterPos2f(x_pos, y_pos)
            else:
                GLUT.glutBitmapCharacter(font, ord(character))

    def reset_view(self):
        """Return to the initial view point"""
        self.zoom = 1
        self.pan_x = 0
        self.pan_y = 0
        self.init = False
        self.on_paint(0)  # Repaint the canvas

    def capture_image(self):
        """Capture and save the OpenGL canvas content as an image"""
        width, height = self.GetClientSize()
        # Synchronize OpenGL rendering
        GL.glFinish()
        pixels = GL.glReadPixels(0, 0, width, height, GL.GL_RGB,
                                 GL.GL_UNSIGNED_BYTE)
        image = wx.Image(width, height, pixels)
        image = image.Mirror(False)  # Flip horizontally
        image = image.Mirror(True)  # Flip vertically
        image = image.Mirror(True)
        return image

    def save_image(self, file_path):
        """Save the image on the computer"""
        image = self.capture_image()
        if image.SaveFile(file_path, wx.BITMAP_TYPE_PNG):
            print(f"Image saved successfully: {file_path}")
            text = "".join([_(u"Image saved successfully: "), file_path])
            self.render(text)
        else:
            print("Failed to save the image.")


class Gui(wx.Frame):
    """Configure the main window and all the widgets.

    This class provides a graphical user interface for the Logic Simulator and
    enables the user to change the circuit properties and run simulations.

    Parameters
    ----------
    title: title of the window.

    Public methods
    --------------
    on_menu(self, event): Event handler for the file menu.

    on_spin(self, event): Event handler for when the user changes the spin
                           control value.

    on_run_button(self, event): Event handler for when the user clicks the run
                                button.

    on_quit_button(self, event): Event handler for when the user clicks the
                                    quit button.

    on_continue_button(self, event): Event handler for when the user clicks the
                                    continue button

    switch_change(self, switch_id): Event handler for when the user set switc
                                    to the other

    on_add_monitor_button(self, event): Event handler for when the user clicks
                                        the add monitor button

    on_zap_monitor_button(self, monitor_loc): Event handler for when the user
                                                clicks the remove button

    on_help_button(self, event): Event handler for when the user clicks the
                                    help button

    on_reset_view(self, event): Event handler for when the user clicks the
                                reset view button

    on_save_image(self, event): Event handler for when the user clicks the
                                save button

    on_new_file(self): Event handler for when the user clicks the new file
                        button

    open_file(self): Initialise GUI for new file
    """

    def __init__(self, title, path, names, devices, network, monitors):
        """Initialise GUI variables"""
        self.names = names
        self.monitors = monitors
        self.devices = devices
        self.network = network
        self.not_monitored_signal = self.monitors.get_signal_names()[1]
        self.cycles_completed = 0

        """Initialise widgets and layout."""
        super().__init__(parent=None, title=title, size=(800, 600))

        # Configure the file menu
        fileMenu = wx.Menu()
        menuBar = wx.MenuBar()
        fileMenu.Append(wx.ID_OPEN, _(u"&New File"))
        fileMenu.Append(wx.ID_ABOUT, _(u"&About"))
        fileMenu.Append(wx.ID_EXIT, _(u"&Exit"))
        menuBar.Append(fileMenu, _(u"&File"))

        # Configure the Help menu
        help_menu = wx.Menu()
        help_menu.Append(wx.ID_HELP_COMMANDS, _(u"&Help Commands"))
        menuBar.Append(help_menu, _(u"&Help"))

        self.SetMenuBar(menuBar)

        # Canvas for drawing signals
        self.canvas = MyGLCanvas(self, devices, monitors)

        # Configure sizers for layout
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.side_sizer = wx.BoxSizer(wx.VERTICAL)

        # Configure the widgets
        self.text = wx.StaticText(self, wx.ID_ANY, _(u"Cycles"))
        self.spin = wx.SpinCtrl(self, wx.ID_ANY, "10", min=1)
        self.run_button = wx.Button(self, wx.ID_ANY, _(u"Run"))
        self.continue_button = wx.Button(self, wx.ID_ANY, _(u"Continue"))
        # self.clear_button = wx.Button(self, wx.ID_ANY, _(u"Clear"))
        self.quit_button = wx.Button(self, wx.ID_ANY, _(u"Quit"))
        self.text_switch = wx.StaticText(self, wx.ID_ANY, _(u"Switch:"),
                                         style=wx.TE_PROCESS_ENTER)
        self.text_monitor = wx.StaticText(self, wx.ID_ANY, _(u"Monitor: "),
                                          style=wx.TE_PROCESS_ENTER)
        self.reset_view_button = wx.Button(self, wx.ID_ANY, _(u"Reset View"))
        self.save_button = wx.Button(self, wx.ID_ANY, _(u"Save Image"))

        # configuration of sizer chirdren for side sizer
        self.sizer_cycle = wx.BoxSizer(wx.VERTICAL)
        self.sizer_run = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_switch = wx.BoxSizer(wx.VERTICAL)
        self.sizer_text_switch = wx.BoxSizer(wx.VERTICAL)
        self.sub_sizer_sw_state = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_monitor = wx.BoxSizer(wx.VERTICAL)
        self.sizer_text_monitor = wx.BoxSizer(wx.VERTICAL)
        self.sub_sizer_monitor = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_tool = wx.BoxSizer(wx.HORIZONTAL)

        self.main_sizer.Add(self.canvas, 5, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Add(self.side_sizer, 1, wx.ALL, 5)

        # sizer children for sizer_cycle
        self.sizer_cycle.Add(self.text, 1, wx.ALL, 5)
        self.sizer_cycle.Add(self.spin, 1, wx.ALL, 5)

        # sizer children for sizer_run
        self.sizer_run.Add(self.run_button, 1, wx.ALL, 5)
        self.sizer_run.Add(self.continue_button, 1, wx.ALL, 5)
        # self.sizer_run.Add(self.clear_button, 1, wx.ALL, 5)
        self.sizer_run.Add(self.quit_button, 1, wx.ALL, 5)

        # sizer children for sizer_tool
        self.sizer_tool.Add(self.reset_view_button, 1, wx.ALL, 5)
        self.sizer_tool.Add(self.save_button, 1, wx.ALL, 5)

        # sizer children for sizer_switch
        self.sizer_text_switch.Add(self.text_switch, 0, wx.ALL, 5)
        self.sizer_text_switch.Add(self.sub_sizer_sw_state, 0,
                                   wx.ALIGN_CENTER | wx.ALL, 5)
        self.text_sw = wx.StaticText(self, wx.ID_ANY, _(u"Switch name"),
                                     style=wx.TE_PROCESS_ENTER)
        self.text_state = wx.StaticText(self, wx.ID_ANY, _(u"Current state"),
                                        style=wx.TE_PROCESS_ENTER)
        self.sub_sizer_sw_state.Add(self.text_sw, 1, wx.ALIGN_LEFT | wx.ALL, 5)
        self.sub_sizer_sw_state.Add(self.text_state, 1,
                                    wx.ALIGN_LEFT | wx.ALL, 5)

        self.scrolled_switch = wx.ScrolledWindow(self, style=wx.VSCROLL)
        self.scrolled_switch.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.scrolled_switch.SetSizer(self.sizer_switch)
        self.scrolled_switch.SetScrollRate(0, 20)
        self.scrolled_switch.SetAutoLayout(True)
        # toggle switch
        self.sizers = {}  # Dictionary to store the sizers
        for switch_id in self.devices.find_devices(self.devices.SWITCH):
            switch_string = self.names.get_name_string(switch_id)
            sizer_name = f"sizer{switch_id}"
            # Create the horizontal sizer
            self.sub_sizer_switch = wx.BoxSizer(wx.HORIZONTAL)
            self.sizers[sizer_name] = self.sub_sizer_switch

            self.exist_text_switch = wx.StaticText(self.scrolled_switch,
                                                   wx.ID_ANY, switch_string,
                                                   style=wx.TE_PROCESS_ENTER)
            switch_state = self.devices.get_device(switch_id).switch_state
            if switch_state == 1:
                self.swt_st = wx.StaticText(self.scrolled_switch,
                                            wx.ID_ANY, _(u"ON"),
                                            style=wx.TE_PROCESS_ENTER)
                self.swt_st.SetForegroundColour(wx.Colour(0, 100, 100))
                self.tog_btn = wx.ToggleButton(self.scrolled_switch,
                                               label=_(u"Toggle Switch"))
            elif switch_state == 0:
                self.swt_st = wx.StaticText(self.scrolled_switch,
                                            wx.ID_ANY, _(u"OFF"),
                                            style=wx.TE_PROCESS_ENTER)
                self.swt_st.SetForegroundColour(wx.Colour(150, 150, 150))
                self.tog_btn = wx.ToggleButton(self.scrolled_switch,
                                               label=_(u"Toggle Switch"))
                self.tog_btn.SetValue(True)
                self.tog_btn.SetBackgroundColour(wx.Colour(80, 150, 150))

            self.sizer_switch.Add(self.sub_sizer_switch, 1, wx.ALL, 5)
            self.sub_sizer_switch.Add(self.exist_text_switch, 1,
                                      wx.ALIGN_CENTER | wx.ALL, 5)
            self.sub_sizer_switch.Add(self.swt_st, 1,
                                      wx.ALIGN_CENTER | wx.ALL, 5)
            self.sub_sizer_switch.Add(self.tog_btn, 1,
                                      wx.ALIGN_CENTER | wx.ALL, 5)

        for sizer_name, sizer in self.sizers.items():
            self.tog_btn = sizer.GetItem(2).GetWindow()
            self.tog_btn.Bind(wx.EVT_TOGGLEBUTTON, self.switch_change)
            self.tog_btn.SetId(wx.NewId())

        # monitor scrollable panel -> choose option -> add
        # sizer children for sizer_monitor
        self.sizer_text_monitor.Add(self.text_monitor, 1, wx.ALL, 5)

        self.scrolled_monitor = wx.ScrolledWindow(self, style=wx.VSCROLL)
        self.scrolled_monitor.SetSizer(self.sizer_monitor)
        self.scrolled_monitor.SetScrollRate(0, 20)
        self.scrolled_monitor.SetAutoLayout(True)
        self.scrolled_monitor.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.monitor_combo = wx.ComboBox(self.scrolled_monitor, wx.ID_ANY,
                                         choices=self.not_monitored_signal,
                                         style=wx.CB_READONLY)
        self.monitor_add_button = wx.Button(self.scrolled_monitor,
                                            wx.ID_ANY, _(u"Add"))
        self.sizer_monitor.Add(self.sub_sizer_monitor, 1,
                               wx.ALIGN_LEFT | wx.ALL, 5)
        self.sub_sizer_monitor.Add(self.monitor_combo, 1,
                                   wx.ALIGN_CENTER | wx.ALL, 5)
        self.sub_sizer_monitor.Add(self.monitor_add_button, 1,
                                   wx.ALIGN_CENTER | wx.ALL, 5)
        self.monitored_signal = self.monitors.get_signal_names()[0]
        for monitor in self.monitored_signal:
            self.sub_sizer_text_monitor = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer_monitor.Add(self.sub_sizer_text_monitor, 1, wx.ALL, 5)
            self.ext_monitor = wx.StaticText(self.scrolled_monitor,
                                             wx.ID_ANY, monitor,
                                             style=wx.TE_PROCESS_ENTER)
            self.zap_monitor_btn = wx.Button(self.scrolled_monitor,
                                             wx.ID_ANY, _(u"Remove"))
            self.zap_monitor_btn.SetBackgroundColour(wx.Colour(80, 150, 150))
            self.zap_monitor_btn.Bind(wx.EVT_BUTTON,
                                      self.on_zap_monitor_button(monitor))
            self.sub_sizer_text_monitor.Add(self.ext_monitor, 1,
                                            wx.ALL, 5)
            self.sub_sizer_text_monitor.Add(self.zap_monitor_btn, 1,
                                            wx.ALL, 5)

        # place side_sizer items
        self.side_sizer.Add(self.sizer_cycle, 0, wx.ALL, 5)
        self.side_sizer.Add(self.sizer_run, 0, wx.ALL, 5)
        self.side_sizer.Add(self.sizer_text_switch, 1, wx.ALL, 5)
        self.side_sizer.Add(self.scrolled_switch, 3, wx.EXPAND | wx.ALL, 5)
        self.side_sizer.Add(self.sizer_text_monitor, 0, wx.ALL, 5)
        self.side_sizer.Add(self.scrolled_monitor, 3, wx.EXPAND | wx.ALL, 5)
        self.side_sizer.Add(self.sizer_tool, 0, wx.ALL, 5)

        # Bind events to widgets
        self.Bind(wx.EVT_MENU, self.on_menu)
        self.spin.Bind(wx.EVT_SPINCTRL, self.on_spin)
        self.run_button.Bind(wx.EVT_BUTTON, self.on_run_button)
        self.continue_button.Bind(wx.EVT_BUTTON, self.on_continue_button)
        self.quit_button.Bind(wx.EVT_BUTTON, self.on_quit_button)
        self.monitor_add_button.Bind(wx.EVT_BUTTON, self.on_add_monitor_button)
        self.reset_view_button.Bind(wx.EVT_BUTTON, self.on_reset_view)
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save_image)

        self.SetSizeHints(1000, 600)
        self.SetSizer(self.main_sizer)

    def on_menu(self, event):
        """Handle the event when the user selects a menu item."""
        Id = event.GetId()
        if Id == wx.ID_EXIT:
            self.Close(True)
        if Id == wx.ID_ABOUT:
            wx.MessageBox(_(u"Logic Simulator\nCocreated by Amanda Ge,\n"
                          "Chulabutra Chuenchoksan, Koko Ishida\n2017"),
                          _(u"About Logsim"), wx.ICON_INFORMATION | wx.OK)
        if Id == wx.ID_OPEN:
            self.on_new_file()
        if Id == wx.ID_HELP_COMMANDS:
            wx.MessageBox(_("User Commands\n"
                            "\nRun             -> run the simulation\n"
                            "\nContinue        -> continue simulation\n"
                            "\nToggle Switch   -> change the switch state\n"
                            "\nAdd             -> set a monitor on signal\n"
                            "\nRemove          -> zap the monior on signal\n"
                            "\nHelp            -> help (this command)\n"
                            "\nQuit            -> quit the simulation"),
                          _(u"Help"), wx.OK | wx.ICON_INFORMATION)

    def on_spin(self, event):
        """Handle the event when the user changes the spin control value."""
        spin_value = self.spin.GetValue()
        text = "".join(["New spin control value: ", str(spin_value)])
        self.canvas.render(text)

    def on_run_button(self, event):
        """Handle the event when the user clicks the run button."""
        self.cycles_completed = 0
        num_cycles = self.spin.GetValue()
        self.monitored_signal = self.monitors.get_signal_names()[0]
        self.monitors.reset_monitors()
        self.devices.cold_startup()
        for _ in range(num_cycles):
            if self.network.execute_network():
                self.monitors.record_signals()
                self.cycles_completed += 1
        self.gui_monitors = self.convert_gui_monitors()
        self.canvas.render("", self.cycles_completed, self.gui_monitors)

    def on_continue_button(self, event):
        """Event handler for when the user clicks the continue button"""
        text = "Continue button pressed."
        self.canvas.render(text)
        if self.cycles_completed > 0:
            num_cycles = self.spin.GetValue()
            self.monitored_signal = self.monitors.get_signal_names()[0]
            for _ in range(num_cycles):
                if self.network.execute_network():
                    self.monitors.record_signals()
                    self.cycles_completed += 1
            self.gui_monitors = self.convert_gui_monitors()
            self.canvas.render("", self.cycles_completed, self.gui_monitors)

    def on_quit_button(self, event):
        """Event handler for when the user clicks the quit button."""
        text = "Quit button pressed."
        self.canvas.render(text)
        self.main_sizer.GetContainingWindow().Close()

    def switch_change(self, event):
        """Event handler for when the user set switch to the other."""
        self.tog_btn = event.GetEventObject()
        sizer_name = None
        sizer_ = None
        for name, sizer in self.sizers.items():
            if any(item.GetWindow() == self.tog_btn for item
                   in sizer.GetChildren()):
                sizer_name = name
                sizer_ = sizer
                break
        if sizer_name is not None:
            static_text = sizer_.GetItem(0).GetWindow()
            switch_id = self.names.query(static_text.GetLabel())
            if switch_id is not None:
                self.swt_st = sizer_.GetItem(1).GetWindow()
                if self.tog_btn.GetValue():
                    self.swt_st.SetLabel(_(u"OFF"))
                    self.swt_st.SetForegroundColour(wx.Colour(150, 150, 150))
                    new_signal = 0
                    self.tog_btn.SetBackgroundColour(wx.Colour(80, 150, 150))
                else:
                    self.swt_st.SetLabel(_(u"ON"))
                    self.swt_st.SetForegroundColour(wx.Colour(0, 100, 100))
                    new_signal = 1
                    self.tog_btn.SetBackgroundColour(wx.Colour(255, 255, 255))
                self.devices.set_switch(switch_id, new_signal)
                self.gui_monitors = self.convert_gui_monitors()
                text = "switch input is flipped."
                self.canvas.render(text)

    def on_add_monitor_button(self, event):
        """Event handler for when the user clicks the add monitor button"""
        monitor = self.monitor_combo.GetValue()
        if monitor is not None:
            [device_id, output_id] = self.devices.get_signal_ids(monitor)
            monitor_error = self.monitors.make_monitor(device_id, output_id,
                                                       self.cycles_completed)
            self.not_monitored_signal = self.monitors.get_signal_names()[1]
            # sizer changes
            if monitor_error == self.monitors.NO_ERROR:
                self.sub_sizer_text_monitor = wx.BoxSizer(wx.HORIZONTAL)
                self.sizer_monitor.Add(self.sub_sizer_text_monitor, 1,
                                       wx.ALL, 5)
                self.ext_monitor = wx.StaticText(self.scrolled_monitor,
                                                 wx.ID_ANY, monitor,
                                                 style=wx.TE_PROCESS_ENTER)
                self.zap_monitor_btn = wx.Button(self.scrolled_monitor,
                                                 wx.ID_ANY, _(u"Remove"))
                self.zap_monitor_btn.SetBackgroundColour(wx.Colour(80,
                                                                   150, 150))
                self.zap_monitor_btn.Bind(wx.EVT_BUTTON,
                                          self.on_zap_monitor_button(monitor))
                self.sub_sizer_text_monitor.Add(self.ext_monitor,
                                                1, wx.ALL, 5)
                self.sub_sizer_text_monitor.Add(self.zap_monitor_btn,
                                                1, wx.ALL, 5)
                self.monitor_combo.SetItems(self.not_monitored_signal)
                text = "Successfully made monitor."
                self.canvas.render(text)
            else:
                text = "Error! Could not make monitor."
                self.canvas.render(text)
            self.main_sizer.Layout()

    def on_zap_monitor_button(self, monitor):
        """Event handler for when user clicks the remove button"""
        def remove_pushed(event):
            obj_monitor = event.GetEventObject()
            obj_sizer = obj_monitor.GetContainingSizer()
            self.sizer_monitor.Hide(obj_sizer)
            self.sizer_monitor.Remove(obj_sizer)
            [device_id, output_id] = self.devices.get_signal_ids(monitor)
            self.monitors.remove_monitor(device_id, output_id)
            self.not_monitored_signal = self.monitors.get_signal_names()[1]
            self.monitor_combo.SetItems(self.not_monitored_signal)
            text = "Successfully removed monitor."
            self.canvas.render(text)
            self.sizer_text_monitor.Layout()
            self.sizer_monitor.Layout()
            self.main_sizer.Layout()
        return remove_pushed

    def convert_gui_monitors(self):
        """Convert the dictionary {(device_id, output_id): [signal_list]}
          to {monitor_string: [signal_list]}"""
        gui_dict = {}
        for device_id, output_id in self.monitors.monitors_dictionary:
            monitor_string = self.devices.get_signal_name(device_id,
                                                          output_id)
            signal_list = self.monitors.monitors_dictionary[(device_id,
                                                             output_id)]
            gui_dict[monitor_string] = signal_list
        return gui_dict

    def on_reset_view(self, event):
        """Event handler for when the user clicks the reset view button"""
        self.canvas.reset_view()
        text = "Reset to the origin"
        self.canvas.render(text)

    def on_save_image(self, event):
        """Event handler for when the user clicks the save button"""
        dlg = wx.FileDialog(self, "Save Image",
                            wildcard="PNG files (*.png)|*.png",
                            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            file_path = dlg.GetPath()
            self.canvas.save_image(file_path)
        dlg.Destroy()

    def on_new_file(self, file=True):
        """Event handler for when the user clicks the new file button"""
        wildcard = "Text file (*.txt)|*.txt"
        dialog = wx.FileDialog(
            self,
            message=_(u"Choose a file"),
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        )
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            # Process the selected file (e.g., open it, read data, etc.)
            print("Selected file:", path)
            if Path(path).suffix == ".txt":
                # initialise network variables
                names = Names()
                devices = Devices(names)
                network = Network(names, devices)
                monitors = Monitors(names, devices, network)
                scanner = Scanner(path, names, devices, network, monitors)
                parser = Parser(names, devices, network, monitors, scanner)
                if parser.parse_network():
                    # set up gui for new circuit
                    self.names = names
                    self.devices = devices
                    self.network = network
                    self.monitors = monitors
                    self.scanner = scanner
                    self.parser = parser
                    self.open_file()
                else:
                    wx.MessageBox(_(u"Error reading the file!"),
                                  _(u"Error"), wx.OK | wx.ICON_ERROR)
            dialog.Destroy()

    def open_file(self):
        """Initialise GUI for new file"""
        self.cycles_completed = 0
        self.monitored_signal = self.monitors.get_signal_names()[0]
        self.not_monitored_signal = self.monitors.get_signal_names()[1]

        # toggle switch initalisation
        self.sizer_switch.Clear(True)
        self.sizers = {}  # Dictionary to store the sizers
        for switch_id in self.devices.find_devices(self.devices.SWITCH):
            switch_string = self.names.get_name_string(switch_id)
            sizer_name = f"sizer{switch_id}"
            # Create the horizontal sizer
            self.sub_sizer_switch = wx.BoxSizer(wx.HORIZONTAL)
            self.sizers[sizer_name] = self.sub_sizer_switch

            self.exist_text_switch = wx.StaticText(self.scrolled_switch,
                                                   wx.ID_ANY, switch_string,
                                                   style=wx.TE_PROCESS_ENTER)
            switch_state = self.devices.get_device(switch_id).switch_state
            if switch_state == 1:
                self.swt_st = wx.StaticText(self.scrolled_switch,
                                            wx.ID_ANY, _(u"ON"),
                                            style=wx.TE_PROCESS_ENTER)
                self.swt_st.SetForegroundColour(wx.Colour(0, 100, 100))
                self.tog_btn = wx.ToggleButton(self.scrolled_switch,
                                               label=_(u"Toggle Switch"))
            elif switch_state == 0:
                self.swt_st = wx.StaticText(self.scrolled_switch,
                                            wx.ID_ANY, _(u"OFF"),
                                            style=wx.TE_PROCESS_ENTER)
                self.swt_st.SetForegroundColour(wx.Colour(150, 150, 150))
                self.tog_btn = wx.ToggleButton(self.scrolled_switch,
                                               label=_(u"Toggle Switch"))
                self.tog_btn.SetValue(True)
                self.tog_btn.SetBackgroundColour(wx.Colour(80, 150, 150))
            self.sizer_switch.Add(self.sub_sizer_switch, 1, wx.ALL, 5)
            self.sub_sizer_switch.Add(self.exist_text_switch, 1,
                                      wx.ALIGN_CENTER | wx.ALL, 5)
            self.sub_sizer_switch.Add(self.swt_st, 1,
                                      wx.ALIGN_CENTER | wx.ALL, 5)
            self.sub_sizer_switch.Add(self.tog_btn, 1,
                                      wx.ALIGN_CENTER | wx.ALL, 5)

        for sizer_name, sizer in self.sizers.items():
            self.tog_btn = sizer.GetItem(2).GetWindow()
            self.tog_btn.Bind(wx.EVT_TOGGLEBUTTON, self.switch_change)
            self.tog_btn.SetId(wx.NewId())

        # monitor initialisation
        self.monitor_combo.SetItems(self.not_monitored_signal)
        for item in self.sizer_monitor.GetChildren():
            if item.GetSizer() and item.GetSizer() != self.sub_sizer_monitor:
                item.GetSizer().Clear(True)
                self.sizer_monitor.Remove(item.GetSizer())

        for monitor in self.monitored_signal:
            self.sub_sizer_text_monitor = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer_monitor.Add(self.sub_sizer_text_monitor, 1, wx.ALL, 5)
            self.ext_monitor = wx.StaticText(self.scrolled_monitor,
                                             wx.ID_ANY, monitor,
                                             style=wx.TE_PROCESS_ENTER)
            self.zap_monitor_btn = wx.Button(self.scrolled_monitor,
                                             wx.ID_ANY, _(u"Remove"))
            self.zap_monitor_btn.SetBackgroundColour(wx.Colour(80, 150, 150))
            self.zap_monitor_btn.Bind(wx.EVT_BUTTON,
                                      self.on_zap_monitor_button(monitor))
            self.sub_sizer_text_monitor.Add(self.ext_monitor, 1,
                                            wx.ALL, 5)
            self.sub_sizer_text_monitor.Add(self.zap_monitor_btn, 1,
                                            wx.ALL, 5)

        self.main_sizer.Layout()
