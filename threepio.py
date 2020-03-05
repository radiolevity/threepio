"""
  __  __                    _                 
 / /_/ /  _______ ___ ___  (_)__    ___  __ __
/ __/ _ \/ __/ -_) -_) _ \/ / _ \_ / _ \/ // /
\__/_//_/_/  \__/\__/ .__/_/\___(_) .__/\_, / 
                   /_/           /_/   /___/   

The helpful companion to the 40' telescope
Written with frustration by Shengjie, Isabel, and Finn

"""

from PyQt5 import QtCore, QtWidgets, QtGui, QtChart
from main_ui import Ui_MainWindow   # compiled PyQt main ui
from time_ui import Ui_Dialog     # compiled PyQt dialogue ui
from scipy import stats
# from playsound import playsound # TODO: test on Windows 
import numpy as np
import time, math, random

import tars
from precious import MyPrecious
from dialog import Dialog
from time_dialog import TimeDialog
from dec_dialog import DecDialog
from credits_dialog import CreditsDialog
from superclock import SuperClock
from observation import Observation, Survey, Scan, Spectrum, DataPoint
from alert import AlertDialog
from comm import Comm
        
class Threepio(QtWidgets.QMainWindow):
    """Main class for the app"""

    # basic time
    timer_rate = 10 # ms
    stripchart_display_ticks = 64 # how many data points to draw to stripchart
    stripchart_offset = 0

    # test data
    ticker = 0
    other_ticker = 0
    foo = 0.0
    
    # speed measurement
    tick_time = 0.0
    timing_margin = 0.995

    # stripchart
    stripchart_low = -1
    stripchart_high = 1
    
    # declination calibration
    dec_slope = 0
    dec_intercept = 0

    # palette
    BLUE = 0x2196f3
    RED = 0xff5252
    
    # tars communication interpretation
    transmission = None
    old_transmission = None

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        # use main_ui for window setup
        self.ui = Ui_MainWindow()
        self.setStyleSheet(open('stylesheet.qss').read())
        self.ui.setupUi(self)
        self.setWindowTitle("Threepio")

        # connect buttons
        self.ui.speed_faster_radio.clicked.connect(self.update_speed)
        self.ui.speed_slower_radio.clicked.connect(self.update_speed)
        self.ui.speed_default_radio.clicked.connect(self.update_speed)

        self.ui.actionInfo.triggered.connect(self.handle_credits)

        self.ui.actionScan.triggered.connect(self.handle_scan)
        self.ui.actionSurvey.triggered.connect(self.handle_survey)
        self.ui.actionSpectrum.triggered.connect(self.handle_spectrum)
        
        self.ui.actionDec.triggered.connect(self.dec_calibration)
        self.ui.actionRA.triggered.connect(self.ra_calibration)

        self.ui.chart_clear_button.clicked.connect(self.handle_clear)
        self.ui.chart_refresh_button.clicked.connect(self.handle_refresh)

        # TODO: maybe just choose one of these?
        self.ui.actionLegacy.triggered.connect(self.legacy_mode)
        self.ui.chart_legacy_button.clicked.connect(self.legacy_mode)

        # initialize stripchart
        self.stripchart_series_a = QtChart.QLineSeries()
        self.stripchart_series_b = QtChart.QLineSeries()
        self.ui.stripchart.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtGui.QColor(self.BLUE))
        pen.setWidth(3)
        self.stripchart_series_a.setPen(pen)
        pen.setColor(QtGui.QColor(self.RED))
        self.stripchart_series_b.setPen(pen)

        # DATAQ stuff
        self.tars = tars.Tars()
        self.tars.setup()
        self.tars.start()
        
        # clock
        self.clock = self.set_time()
        
        # establish observation
        self.observation = None
        
        # establish data array & most recent dec
        self.data = []
        self.current_dec = 0.0
        
        # run initial calibration
        self.declination_regression()
        
        # refresh timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.tick) # do everything
        self.timer.start(self.timer_rate) # set refresh rate

    def tick(self): # primary controller for each clock tick

        # TODO: make this use DAQ data
        self.foo += .1
        if self.foo > 90.0: self.foo = 0.0
                
        # for speed testing
        #print(time.time() - self.tick_time)
        #self.tick_time = time.time()
        
        self.update_gui() # update gui
        
        # if observation loaded -> read data
        if self.observation != None:
            
            self.update_progress_bar()
            
            period = 1/self.observation.freq
            
            if (time.time() - self.tick_time) > (period * self.timing_margin):
                
                self.tick_time = time.time()
            
                tars_data = self.tars.read_latest() # get data from DAQ
                
                self.current_dec = self.calculate_declination(tars_data[2][1])
                data_point = DataPoint(self.clock.get_sidereal_seconds(), self.current_dec, tars_data[0][1], tars_data[1][1])
                
                self.data.append(data_point)
                self.old_transmission = self.transmission
                self.transmission = self.observation.communicate(data_point, time.time())
                # print(self.transmission, time.time(), self.observation.state)
                
                if self.transmission != self.old_transmission:
                    if self.transmission == Comm.START_CAL:
                        self.alert("Set calibration switches to ON")
                        self.alert("Are the calibration switches on?")
                        self.observation.next()
                        self.message("Taking calibration data...")
                    elif self.transmission == Comm.STOP_CAL:
                        self.alert("Set calibration switches to OFF")
                        self.alert("Are the calibration switches off?")
                        self.observation.next()
                        self.message("Taking background data...")
                    elif self.transmission == Comm.NEXT:
                        self.observation.next()
                    elif self.transmission == Comm.FINISHED:
                        self.observation.next()
                        self.message("Finished.")
                    elif self.transmission == Comm.BEEP:
                        self.beep()
                    elif self.transmission == Comm.NO_ACTION:
                        pass
                    
                time_until_start = self.observation.start_RA - time.time()
                if time_until_start <= 0 and (self.observation.end_RA - time.time()) > 0:
                    self.message("Taking observation data...")
                
                # for test data
                #self.ticker += random.random()*random.randint(-1,1)
                #self.other_ticker += random.random()*random.randint(-1,1)
                #self.data.append(DataPoint(self.clock.get_sidereal_seconds(), self.ticker, self.other_ticker, self.calculate_declination(self.foo)))
                #self.observation.data_logic(DataPoint(self.clock.get_sidereal_seconds(), self.ticker, self.other_ticker, self.calculate_declination(self.foo)))
            
                self.update_strip_chart() # make the stripchart scroll #TODO: make data save/and go to gui simulataneously
        
    def legacy_mode(self):
        """lol"""
        f = open("stylesheet.qss", "w")
        f.write("background-color:#00ff00; color: #ff0000")
        self.setStyleSheet("background-color:#00ff00; color: #ff0000")
        self.setAutoFillBackground(True)
        
    def handle_credits(self):
        dialog = CreditsDialog()
        dialog.show()
        dialog.exec_()

    def set_time(self):
        new_clock = SuperClock()
        
        # TODO: abstract this better
        dialog = TimeDialog(new_clock)
        dialog.show()
        dialog.exec_()
        
        return new_clock

    def update_speed(self):
        if (self.ui.speed_faster_radio.isChecked()):
            self.stripchart_display_ticks = 32
        elif (self.ui.speed_slower_radio.isChecked()):
            self.stripchart_display_ticks = 128
        else:
            self.stripchart_display_ticks = 64
        self.handle_clear()
        
    def calculate_declination(self, input_dec):
        # calculate the true dec from input data and calibration data
        true_dec = self.dec_intercept + (self.dec_slope * input_dec)
        
        # self.ui.dec_value.setText(str(true_dec)[:5] + "deg") # for testing
        
        return true_dec
    
    def declination_regression(self):
        x = []
        y = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0]
        
        c = open("dec_cal.txt", 'r').read().splitlines() # get data from file
        for i in c:
            x.append(float(i)) # create x array
        
        if len(y) != len(x):
            # TODO: output notification
            print("Declination calibration data error, please calibrate declination")
            return 1
        
        self.dec_slope, self.dec_int, r_value, p_value, std_err = stats.linregress(x,y)

    def update_gui(self):
        self.ui.ra_value.setText(self.clock.get_sidereal_time()) # show RA
        self.ui.dec_value.setText("%.2f" % self.calculate_declination(self.current_dec)) # show dec
        
        # NOTE: this method does NOT update declination (because that needs to always be updated!)
        
        # TODO: get the input data for the stripchart and labels
        if len(self.data) > 0:
            self.ui.channelA_value.setText("%.2f" % (self.data[len(self.data) - 1].a))
            self.ui.channelB_value.setText("%.2f" % (self.data[len(self.data) - 1].b))
    
    def update_progress_bar(self):
        # this mess makes the progress bar display "T+/- XX.XX" when
        # assigned, and progress the bar when taking data
        if not self.observation.end_RA - self.observation.start_RA <= 1:
            if self.clock.get_time_until(self.observation.start_RA) > 0 and self.clock.get_time_until(self.observation.end_RA) < 0:
                self.ui.progressBar.setValue(int((self.clock.get_time_until(self.observation.end_RA) / (self.observation.end_RA - self.observation.start_RA)) * 100 % 100))
            else:
                self.ui.progressBar.setValue(0)
            self.ui.progressBar.setFormat("T%+.1fs" % (self.clock.get_time_until(self.observation.start_RA)))
        else:
            self.ui.progressBar.setFormat("n/a")
            self.ui.progressBar.setValue(0)
            
    def display_info(self, message):
        self.ui.message_label.setText(message)
    
    def update_strip_chart(self):
        new_a = self.data[len(self.data) - 1].a
        new_b = self.data[len(self.data) - 1].b
        self.stripchart_series_a.append(new_a, len(self.data))
        self.stripchart_series_b.append(new_b, len(self.data))

        while (len(self.data) - self.stripchart_offset > self.stripchart_display_ticks):
            self.stripchart_series_a.remove(0)
            self.stripchart_series_b.remove(0)
            self.stripchart_offset += 1

        # TODO: make the stripchart fill in old data when slowed down

        chart = QtChart.QChart()
        chart.addSeries(self.stripchart_series_a)
        chart.addSeries(self.stripchart_series_b)
        
        
        axisX = QtChart.QValueAxis()

        if (new_a < new_b):
            if (new_a < self.stripchart_low):
                self.stripchart_low = new_a
            if (new_b > self.stripchart_high):
                self.stripchart_high = new_b
        else:
            if (new_b < self.stripchart_low):
                self.stripchart_low = new_b
            if (new_a > self.stripchart_high):
                self.stripchart_high = new_a
                
        axisX.setRange(self.stripchart_low, self.stripchart_high)
        
        # axisX.setLabelFormat("%g")
        chart.setAxisX(axisX)

        self.stripchart_series_a.attachAxis(axisX)
        self.stripchart_series_b.attachAxis(axisX)
        
        # chart.createDefaultAxes()
        chart.legend().hide()

        self.ui.stripchart.setChart(chart)
        
    def handle_clear(self):
        self.stripchart_offset += self.stripchart_series_a.count()
        self.stripchart_series_a.clear()
        self.stripchart_series_b.clear()
    
    def handle_refresh(self):
        self.stripchart_low = 32767
        self.stripchart_high = -32768

    def handle_survey(self):
        obs = Survey()
        self.new_observation(obs)

    def handle_scan(self):
        obs = Scan()
        self.new_observation(obs)

    def handle_spectrum(self):
        obs = Spectrum()
        self.new_observation(obs)

    def new_observation(self, obs):
        dialog = Dialog(self, self.clock.get_sidereal_time(), obs, self.clock)
        dialog.setWindowTitle("New " + obs.obs_type)
        dialog.show()
        dialog.exec_()
        
    def dec_calibration(self):
        dialog = DecDialog(self.tars)
        dialog.show()
        dialog.exec_()
        self.declination_regression() # calculate a new regression
        
    def ra_calibration(self):
        self.clock = self.set_time()
        
    def message(self, message):
        self.ui.message_label.setText(message)
        
    def alert(self, message):
        alert = AlertDialog(message)
        alert.show()
        alert.exec_()
        
    def beep(self):
        print("beep! ", time.time())

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Threepio()
    window.setMinimumSize(800,600)
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':   
    main()