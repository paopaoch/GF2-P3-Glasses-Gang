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

    def render(self, text, cycles=0, gui_monitors={}): # gui_monitors = {monitor_string: signal_list}
        """Handle all drawing operations."""

        # Clear everything
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        if cycles > 0:
            self.cycles_completed = cycles
            self.gui_monitors = gui_monitors

        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        margin = self.monitors.get_margin()
        if not margin:
            margin = 0

        self.render_text(text, 10, 10)

        if self.cycles_completed > 0:
            GL.glBegin(GL.GL_LINES)
            # Draw x-axis
            GL.glColor3f(1.0, 0.0, 0.0)  # Red color
            cycle_width = 20
            y_val = 20
            if margin:
                x_start = 100 + margin
            else:
                x_start = 100
            x_end = x_start + (self.cycles_completed + 1)*cycle_width
            GL.glVertex2f(x_start, y_val)
            GL.glVertex2f(x_end, y_val)

            par = 5
            for i in range(self.cycles_completed+1):
                GL.glVertex2f(x_start+i*cycle_width, y_val+par)
                GL.glVertex2f(x_start+i*cycle_width, y_val-par)
            
            # Draw arrowhead
            GL.glBegin(GL.GL_TRIANGLES)
            GL.glVertex2f(x_end - 10, y_val - 5)  # Bottom-left point of arrowhead
            GL.glVertex2f(x_end, y_val)                            # Tip of arrowhead
            GL.glVertex2f(x_end - 10, y_val + 5)  # Bottom-right point of arrowhead
            GL.glEnd()

            # label the axis
            self.render_text("Time", x_start, y_val)
            for i in range(self.cycles_completed+1):
                self.render_text(str(i), x_start+i*cycle_width, y_val-10)

            # draw output signals at monitoring points
            for i in range(len(self.gui_monitors)):
                monitor_str_list = [self.gui_monitors.keys()]
                monitor_str = monitor_str_list[i]
                height = y_val + i*50
                self.render_text(monitor_str, 20, height)
                self.render_text("1", x_start-10, height+10)
                self.render_text("0", x_start-10, height+10)
                signal_list = self.gui_monitors[monitor_str]
                GL.glColor3f(0.0, 0.0, 1.0)  # signal trace is blue
                GL.glBegin(GL.GL_LINE_STRIP)
                for j in range(self.cycles_completed):
                    if signal_list[j] == self.devices.LOW:
                        GL.glVertex2f(x_start+j*cycle_width, height-20)
                        GL.glVertex2f(x_start+(j+1)*cycle_width, height-20)
                    elif signal_list[j] == self.devices.HIGH:
                        GL.glVertex2f(x_start+j*cycle_width, height)
                        GL.glVertex2f(x_start+(j+1)*cycle_width, height)
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
        self.cycles_completed = 0

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
        self.text_switch = wx.StaticText(self, wx.ID_ANY, _(u"Switch:"),
                                            style=wx.TE_PROCESS_ENTER)
        self.text_monitor = wx.StaticText(self, wx.ID_ANY, _(u"Monitor: "),
                                            style=wx.TE_PROCESS_ENTER)
        self.text_box = wx.TextCtrl(self, wx.ID_ANY, "",
                                    style=wx.TE_PROCESS_ENTER)

        # configuration of sizer chirdren for side sizer
        self.sizer_cycle = wx.BoxSizer(wx.VERTICAL)
        self.sizer_run = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_switch = wx.BoxSizer(wx.VERTICAL)
        self.sub_sizer_sw_state = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_monitor = wx.BoxSizer(wx.VERTICAL)
        self.sizer_text_monitor = wx.BoxSizer(wx.VERTICAL)
        self.sub_sizer_monitor = wx.BoxSizer(wx.HORIZONTAL)

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
        self.sizer_switch.Add(self.sub_sizer_sw_state, 1, wx.ALL, 5)
        self.text_sw = wx.StaticText(self, wx.ID_ANY, 
                                     _(u"Switch name"), style=wx.TE_PROCESS_ENTER)
        self.text_state = wx.StaticText(self, wx.ID_ANY, 
                                     _(u"Current state"), style=wx.TE_PROCESS_ENTER)
        self.sub_sizer_sw_state.Add(self.text_sw, 1, wx.ALIGN_CENTER|wx.ALL, 5)
        self.sub_sizer_sw_state.Add(self.text_state, 1, wx.ALIGN_CENTER|wx.ALL, 5)

        # self.scrolled_switch = wx.ScrolledWindow(self, style=wx.VSCROLL)
        # self.scrolled_switch.SetSizer(self.sizer_switch)
        # self.scrolled_switch.SetScrollRate(0, 20)  # Adjust the scrolling speed
        # toggle switch
        for switch_id in self.devices.find_devices(self.devices.SWITCH):
            switch_string = self.names.get_name_string(switch_id)
            self.sub_sizer_switch = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer_switch.Add(self.sub_sizer_switch, 1, wx.ALL, 5)
            self.exist_text_switch = wx.StaticText(self, wx.ID_ANY, 
                                                    switch_string, style=wx.TE_PROCESS_ENTER)
            switch_state = self.devices.get_device(switch_id).switch_state
            if switch_state == 1:
                self.exist_switch_state = wx.StaticText(self, wx.ID_ANY, 
                                                    _(u"On"), style=wx.TE_PROCESS_ENTER)
                self.toggle_btn = wx.ToggleButton(self, label=_(u"Toggle Switch"))
            else:
                self.exist_switch_state = wx.StaticText(self, wx.ID_ANY, 
                                                    _(u"Off"), style=wx.TE_PROCESS_ENTER)
                self.toggle_btn = wx.ToggleButton(self, label=_(u"Toggle Switch"))
            self.toggle_btn.Bind(wx.EVT_TOGGLEBUTTON, self.switch_change)
            self.sub_sizer_switch.Add(self.exist_text_switch, 1, wx.ALIGN_CENTER|wx.ALL, 5)
            self.sub_sizer_switch.Add(self.exist_switch_state, 1, wx.ALIGN_CENTER|wx.ALL, 5)
            self.sub_sizer_switch.Add(self.toggle_btn, 1, wx.ALL, 5)

        # monitor scrollable panel -> choose option -> add
        # sizer children for sizer_monitor
        self.scrolled_monitor = wx.ScrolledWindow(self, style=wx.VSCROLL)
        self.scrolled_monitor.SetSizer(self.sizer_monitor)
        self.scrolled_monitor.SetScrollRate(0, 20)  # Adjust the scrolling speed
        self.monitor_combo = wx.ComboBox(self.scrolled_monitor, wx.ID_ANY, 
                                         choices=self.not_monitored_signal, 
                                         style=wx.CB_READONLY)
        self.monitor_add_button = wx.Button(self.scrolled_monitor, wx.ID_ANY,
                                            _(u"Add"))  
        self.sizer_monitor.Add(self.sub_sizer_monitor, 0, wx.ALL, 10)   
        self.sub_sizer_monitor.Add(self.monitor_combo, 0, wx.ALL, 10)
        self.sub_sizer_monitor.Add(self.monitor_add_button, 1, wx.ALL, 10)

        # self.scrolled_monitor = wx.ScrolledWindow(self, style=wx.VSCROLL)
        # self.scrolled_monitor.SetSizer(self.sizer_text_monitor)
        # self.scrolled_monitor.SetScrollRate(0, 20)  # Adjust the scrolling speed
        # monitor text/button -> remove
        self.monitored_signal = self.monitors.get_signal_names()[0]
        self.sizer_text_monitor.Add(self.text_monitor, 1, wx.ALL, 5)
        for monitor in self.monitored_signal:
            self.sub_sizer_text_monitor = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer_text_monitor.Add(self.sub_sizer_text_monitor, 1, wx.ALL, 5)
            self.exist_text_monitor = wx.StaticText(self.scrolled_monitor, wx.ID_ANY,
                                                    monitor, style=wx.TE_PROCESS_ENTER)
            self.remove_monitor_button = wx.Button(self.scrolled_monitor, wx.ID_ANY,
                                                    _(u"Remove"))
            self.remove_monitor_button.Bind(wx.EVT_BUTTON, self.on_zap_monitor_button(monitor))
            self.sub_sizer_text_monitor.Add(self.exist_text_monitor, 1, wx.ALL, 5)
            self.sub_sizer_text_monitor.Add(self.remove_monitor_button, 1, wx.ALL, 5)
            
        # place side_sizer items
        self.side_sizer.Add(self.sizer_cycle, 1, wx.ALL, 10)
        self.side_sizer.Add(self.sizer_run, 1, wx.ALL, 5)
        self.side_sizer.Add(self.sizer_switch, 1, wx.ALL, 5)
        self.side_sizer.Add(self.sizer_text_monitor, 1, wx.ALL, 5)
        self.side_sizer.Add(self.scrolled_monitor, 1, wx.EXPAND | wx.ALL, 5)
        self.side_sizer.Add(self.text_box, 1, wx.EXPAND | wx.ALL, 5)
        
        # Bind events to widgets
        self.Bind(wx.EVT_MENU, self.on_menu)
        self.spin.Bind(wx.EVT_SPINCTRL, self.on_spin)
        self.run_button.Bind(wx.EVT_BUTTON, self.on_run_button)
        self.continue_button.Bind(wx.EVT_BUTTON, self.on_continue_button)
        self.quit_button.Bind(wx.EVT_BUTTON, self.on_quit_button)
        self.text_switch.Bind(wx.EVT_TEXT_ENTER, self.switch_change)
        # self.switch_button.Bind(wx.EVT_BUTTON, self.switch_change)
        self.monitor_add_button.Bind(wx.EVT_BUTTON, self.on_add_monitor_button)
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
        self.gui_monitors = self.convert_gui_monitors()
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
            self.gui_monitors = self.convert_gui_monitors()
            self.canvas.render(self.cycles_completed)

    def on_quit_button(self, event):
        """Event handler for when the user clicks the quit button."""
        text = "Quit button pressed."
        self.canvas.render(text)
        self.main_sizer.GetContainingWindow().Close()

    def switch_change(self, event):
        """Event handler for when the user set switch to the other."""
        self.toggle_btn = event.GetEventObject()
        switch_id = self.toggle_btn.GetLabel()
        if switch_id is not None:
            if self.toggle_btn.GetValue():
                self.exist_switch_state.SetLabel(_(u"Off"))
                new_signal = 0
            else:
                self.exist_switch_state.SetLabel(_(u"On"))
                new_signal = 1
            self.devices.set_switch(switch_id, new_signal)
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
                self.monitor_combo.SetItems(self.not_monitored_signal)
                self.sub_sizer_text_monitor = wx.BoxSizer(wx.HORIZONTAL)
                self.sizer_text_monitor.Add(self.sub_sizer_text_monitor, 1, wx.ALL, 5)
                self.exist_text_monitor = wx.StaticText(self, wx.ID_ANY,
                                                        monitor, style=wx.TE_PROCESS_ENTER)
                self.remove_monitor_button = wx.Button(self, wx.ID_ANY,
                                                        _(u"Remove"))
                self.remove_monitor_button.Bind(wx.EVT_BUTTON, self.on_zap_monitor_button(monitor))
                self.sub_sizer_text_monitor.Add(self.exist_text_monitor, 1, wx.ALL, 5)
                self.sub_sizer_text_monitor.Add(self.remove_monitor_button, 1, wx.ALL, 5)
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
            self.sizer_text_monitor.Hide(obj_sizer)
            self.sizer_text_monitor.Remove(obj_sizer)
            [device_id, output_id] = self.devices.get_signal_ids(monitor)
            self.monitors.remove_monitor(device_id, output_id)
            self.not_monitored_signal = self.monitors.get_signal_names()[1]
            self.monitor_combo.SetItems(self.not_monitored_signal)
            text = "Successfully removed monitor."
            self.canvas.render(text)
            self.sizer_text_monitor.Layout
            self.sizer_monitor.Layout()
            self.main_sizer.Layout()
        return remove_pushed

    def convert_gui_monitors(self):
        """Convert the dictionary {(device_id, output_id): [signal_list]}
          to {monitor_string: [signal_list]}"""
        gui_dict = {}
        for device_id, output_id in self.monitors.monitors_dictionary:
            monitor_string = self.devices.get_signal_name(device_id, output_id)
            signal_list = self.monitors.monitors_dictionary[(device_id, output_id)]
            gui_dict[monitor_string] = signal_list
        return gui_dict
    
    def on_text_box(self, event):
        """Handle the event when the user enters text."""
        text_box_value = self.text_box.GetValue()
        text = "".join(["New text box value: ", text_box_value])
        self.canvas.render(text)
