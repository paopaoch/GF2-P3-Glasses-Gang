"""Implement the graphical user interface for the Logic Simulator.

Used in the Logic Simulator project to enable the user to run the simulation
or adjust the network properties.

Classes:
--------
MyGLCanvas - handles all canvas drawing operations.
Gui - configures the main window and all the widgets.
"""
import wx
import wx.glcanvas as wxcanvas
from OpenGL import GL, GLUT

from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner
from parse import Parser

_ = wx.GetTranslation


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
    """

    def __init__(self, parent, devices, monitors):
        """Initialise variables"""
        self.devices = devices
        self.monitors = monitors
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

    def render(self, text, cycles=0, monitors=[]):
        """Handle all drawing operations."""

        # Clear everything
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        if cycles > 0:
            self.cycles_completed = cycles
            self.monitored_monitors = monitors

        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        # Draw specified text at position (10, 10)
        self.render_text(text, 10, 10)

        # Draw a sample signal trace
        GL.glColor3f(0.0, 0.0, 1.0)  # signal trace is blue
        GL.glBegin(GL.GL_LINE_STRIP)
        for i in range(10):
            x = (i * 20) + 10
            x_next = (i * 20) + 30
            if i % 2 == 0:
                y = 75
            else:
                y = 100
            GL.glVertex2f(x, y)
            GL.glVertex2f(x_next, y)
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

        size = self.GetClientSize()
        text = "".join(["Canvas redrawn on paint event, size is ",
                        str(size.width), ", ", str(size.height)])
        self.render(text)

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
            text = "".join(["Mouse button pressed at: ", str(event.GetX()),
                            ", ", str(event.GetY())])
        if event.ButtonUp():
            text = "".join(["Mouse button released at: ", str(event.GetX()),
                            ", ", str(event.GetY())])
        if event.Leaving():
            text = "".join(["Mouse left canvas at: ", str(event.GetX()),
                            ", ", str(event.GetY())])
        if event.Dragging():
            self.pan_x += event.GetX() - self.last_mouse_x
            self.pan_y -= event.GetY() - self.last_mouse_y
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
            self.init = False
            text = "".join(["Mouse dragged to: ", str(event.GetX()),
                            ", ", str(event.GetY()), ". Pan is now: ",
                            str(self.pan_x), ", ", str(self.pan_y)])
        if event.GetWheelRotation() < 0:
            self.zoom *= (1.0 + (
                event.GetWheelRotation() / (20 * event.GetWheelDelta())))
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
            text = "".join(["Negative mouse wheel rotation. Zoom is now: ",
                            str(self.zoom)])
        if event.GetWheelRotation() > 0:
            self.zoom /= (1.0 - (
                event.GetWheelRotation() / (20 * event.GetWheelDelta())))
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
            text = "".join(["Positive mouse wheel rotation. Zoom is now: ",
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

    on_quit_button(self, event): Event handler for when the user clicks the quit
                                    button.

    on_continue_button(self, event): Event handler for when the user clicks the
                                    continue button

    switch_change(self, switch_id): Event handler for when the user set switch to
                                    the other

    on_add_monitor_button(self, event): Event handler for when the user clicks
                                        the add monitor button

    on_zap_monitor_button(self, monitor_loc): Event handler for when the user clicks
                                                the remove button

    on_help_button(self, event): Event handler for when the user clicks the help
                                 button

    on_text_box(self, event): Event handler for when the user enters text.
    """

    def __init__(self, title, path, names, devices, network, monitors):
        """Initialise GUI variables"""
        self.names = names
        self.monitors = monitors
        self.devices = devices
        self.network = network
        self.not_monitored_signal = self.monitors.get_signal_names()[1]

        """Initialise widgets and layout."""
        super().__init__(parent=None, title=title, size=(800, 600))

        # Configure the file menu
        fileMenu = wx.Menu()
        menuBar = wx.MenuBar()
        fileMenu.Append(wx.ID_ABOUT, "&About")
        fileMenu.Append(wx.ID_EXIT, "&Exit")
        menuBar.Append(fileMenu, "&File")

        # Configure the Help menu
        help_menu = wx.Menu()
        help_menu.Append(wx.ID_HELP_COMMANDS, _("&Help Commands"))
        menuBar.Append(help_menu, _("&Help"))

        self.SetMenuBar(menuBar)

        # Canvas for drawing signals
        self.canvas = MyGLCanvas(self, devices, monitors)

        # Configure sizers for layout
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.side_sizer = wx.BoxSizer(wx.VERTICAL)

        # Configure the widgets
        self.text = wx.StaticText(self, wx.ID_ANY, _(u"Cycles"))
        self.spin = wx.SpinCtrl(self, wx.ID_ANY, "10")
        self.run_button = wx.Button(self, wx.ID_ANY, _(u"Run"))
        self.continue_button = wx.Button(self, wx.ID_ANY, _(u"Continue"))
        self.quit_button = wx.Button(self, wx.ID_ANY, _(u"Quit"))
        self.text_switch = wx.StaticText(self, wx.ID_ANY, _(u"Switch: "),
                                            style=wx.TE_PROCESS_ENTER)
        self.switch_button = wx.Button(self, wx.ID_ANY, _(u"Toggle Switch"))
        self.text_monitor = wx.StaticText(self, wx.ID_ANY, _(u"Monitor: "),
                                            style=wx.TE_PROCESS_ENTER)
        self.text_box = wx.TextCtrl(self, wx.ID_ANY, "",
                                    style=wx.TE_PROCESS_ENTER)

        # configuration of sizer chirdren for side sizer
        self.sizer_cycle = wx.BoxSizer(wx.VERTICAL)
        self.sizer_run = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_switch = wx.BoxSizer(wx.VERTICAL)
        self.sizer_monitor = wx.BoxSizer(wx.VERTICAL)
        self.sizer_text_monitor = wx.BoxSizer(wx.HORIZONTAL)
        self.monitor_panel = wx.BoxSizer(wx.HORIZONTAL)

        self.main_sizer.Add(self.canvas, 5, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Add(self.side_sizer, 1, wx.ALL, 5)

        # sizer children for sizer_cycle
        self.sizer_cycle.Add(self.text, 1, wx.ALL, 5)
        self.sizer_cycle.Add(self.spin, 1, wx.ALL, 5)

        # sizer children for sizer_run
        self.sizer_run.Add(self.run_button, 1, wx.ALL, 5)
        self.sizer_run.Add(self.continue_button, 1, wx.ALL, 5)
        self.sizer_run.Add(self.quit_button, 1, wx.ALL, 5)

        # sizer children for sizer_switch
        self.sizer_switch.Add(self.text_switch, 1, wx.ALL, 5)
        self.sizer_switch.Add(self.switch_button, 1, wx.ALL, 5)

        # monitor scrollable panel -> choose option -> add/remove
        # sizer children for sizer_monitor
        self.sizer_text_monitor.Add(self.text_monitor, 1, wx.ALL, 5)

        # self.sizer_scrolled = wx.ScrolledWindow(self, style=wx.VSCROLL)
        # self.sizer_scrolled.SetSizer(self.sizer_monitor)
        # self.sizer_scrolled.SetScrollRate(0, 20)  # Adjust the scrolling speed
        # self.monitor_combo = wx.ComboBox(self.sizer_scrolled, wx.ID_ANY, choices=self.not_monitored_signal, style=wx.CB_READONLY)
        # self.monitor_add_button = wx.Button(self.sizer_scrolled, wx.ID_ANY, _(u"Add"))
        self.sizer_monitor.Add(self.sizer_text_monitor, 0, wx.ALL, 10)   
        # self.sizer_monitor.Add(self.monitor_panel, 0, wx.ALL, 10)   
        # self.monitor_panel.Add(self.monitor_combo, 0, wx.ALL, 10)
        # self.monitor_panel.Add(self.monitor_add_button, 1, wx.ALL, 10)

        # place side_sizer items
        self.side_sizer.Add(self.sizer_cycle, 1, wx.ALL, 10)
        self.side_sizer.Add(self.sizer_run, 1, wx.ALL, 5)
        self.side_sizer.Add(self.sizer_switch, 1, wx.ALL, 5)
        # self.side_sizer.Add(self.monitor_panel, 1, wx.ALL, 5)
        # self.side_sizer.Add(self.monitor_add_button, 1, wx.ALL, 5)
        self.side_sizer.Add(self.sizer_text_monitor, 1, wx.ALL, 5)
        self.side_sizer.Add(self.text_box, 1, wx.ALL, 5)
        
        # Bind events to widgets
        self.Bind(wx.EVT_MENU, self.on_menu)
        self.spin.Bind(wx.EVT_SPINCTRL, self.on_spin)
        self.run_button.Bind(wx.EVT_BUTTON, self.on_run_button)
        self.continue_button.Bind(wx.EVT_BUTTON, self.on_continue_button)
        self.quit_button.Bind(wx.EVT_BUTTON, self.on_quit_button)
        self.text_switch.Bind(wx.EVT_TEXT_ENTER, self.switch_change)
        self.switch_button.Bind(wx.EVT_BUTTON, self.switch_change)
        # self.monitor_add_button.Bind(wx.EVT_BUTTON, self.on_add_monitor_button)
        self.text_box.Bind(wx.EVT_TEXT_ENTER, self.on_text_box)

        self.SetSizeHints(1000, 600)
        self.SetSizer(self.main_sizer)

    def on_menu(self, event):
        """Handle the event when the user selects a menu item."""
        Id = event.GetId()
        if Id == wx.ID_EXIT:
            self.Close(True)
        if Id == wx.ID_ABOUT:
            wx.MessageBox("Logic Simulator\nCreated by Mojisola Agboola\n2017",
                          "About Logsim", wx.ICON_INFORMATION | wx.OK)
        if Id == wx.ID_HELP_COMMANDS:
            wx.MessageBox(_("User Commands\n"
                            "\nr  N       - run the simulation for N cycles\n"
                            "\nc  N       - continue simulation for N cycles\n"
                            "\ns  X  N    - set switch X to N (0 or 1)\n"
                            "\nm  X       - set a monitor on signal X\n"
                            "\nz  X       - zap the monior on signal X\n"
                            "\nh          - help (this command)\n"
                            "\nq          - quit the simulation"),
                            _("Help"), wx.OK | wx.ICON_INFORMATION)

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
        text = "Cycles completed."
        self.canvas.render(text)

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
            self.canvas.render(self.cycles_completed)

    def on_quit_button(self, event):
        """Event handler for when the user clicks the quit button."""
        text = "Quit button pressed."
        self.canvas.render(text)
        self.main_sizer.GetContainingWindow().close()

    def switch_change(self, event, switch_id):
        """Event handler for when the user set switch to the other."""
        if switch_id is not None:
            obj_switch = event.GetEventObject()
            if obj_switch.GetLabel() == _("LOW"):
                signal = 0
            else:
                signal = 1
            new_signal = signal^1
            self.devices.set_switch(self, switch_id, new_signal)
            if new_signal == 0:
                obj_switch.SetLabel(_("LOW"))
            elif new_signal == 1:
                obj_switch.SetLabel(_("HIGH"))
            text = "switch input is flipped."
            self.canvas.render(text)

    def on_add_monitor_button(self):
        """Event handler for when the user clicks the add monitor button"""
        monitor = self.monitor_combo.GetValue()
        if monitor is not None:
            [device_id, output_id] = self.devices.get_signal_ids(monitor)
            monitor_error = self.monitors.make_monitor(device_id, output_id,
                                                       self.cycles_completed)
            # sizer changes
            if monitor_error == self.monitors.NO_ERROR:
                # make monitor graphic
                text = "Successfully made monitor."
                self.canvas.render(text)
            else:
                text = "Error! Could not make monitor."
                self.canvas.render(text)
            self.main_sizer.Layout()

    def on_zap_monitor_button(self, monitor, event):
        """Event handler for when user clicks the remove button"""
        obj_monitor = event.GetEventObject()
        obj_panel = obj_monitor.GetContainingSizer()
        self.sizer_monitor.Hide(obj_panel)
        self.sizer_monitor.Remove(obj_panel)
        [device_id, output_id] = self.devices.get_signal_ids(monitor)
        self.monitors.remove_monitor(device_id, output_id)
        self.not_monitored_signal = self.monitors.get_signal_names()[1]
        self.sizer_monitor.Layout()
        self.main_sizer.Layout()

    def on_text_box(self, event):
        """Handle the event when the user enters text."""
        text_box_value = self.text_box.GetValue()
        text = "".join(["New text box value: ", text_box_value])
        self.canvas.render(text)
