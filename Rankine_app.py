import sys
from PyQt5 import QtWidgets as qtw
from Rankine_GUI import Ui_Form
from Rankine import rankine
from Calc_state import SatPropsIsobar

class MainWindow(qtw.QWidget, Ui_Form):
    def __init__(self):
        """
        MainWindow constructor
        """
        super().__init__()  #if you inherit, you generally should run the parent constructor first.
        # Main UI code goes here
        self.setupUi(self)
        self.btn_Calculate.clicked.connect(self.Calculate)
        self.rdo_Quality.clicked.connect(self.SelectQualityOrTHigh)
        self.rdo_THigh.clicked.connect(self.SelectQualityOrTHigh)
        self.rankine=rankine()  # I created a rankine object here as a member variable
        # End main ui code
        self.show()

    def Calculate(self):
        #setup the rankine object
        self.rankine.p_high= float(self.le_PHigh.text())*100  # get the high pressure isobar in kPa
        self.rankine.p_low = float(self.le_PLow.text())*100  # get the low pressure isobar in kPa
        self.rankine.t_high = None if self.rdo_Quality.isChecked() else float(self.le_TurbineInletCondition.text())
        self.rankine.turbine_eff=float(self.le_TurbineEff.text())

        #do the calculation
        eff=self.rankine.calc_efficiency()
        SatPlow=SatPropsIsobar(self.rankine.p_low)
        SatPHigh=SatPropsIsobar(self.rankine.p_high)

        #output results
        self.le_H1.setText("{:0.2f}".format(self.rankine.state1.h))
        self.le_H2.setText("{:0.2f}".format(self.rankine.state2.h))
        self.le_H3.setText("{:0.2f}".format(self.rankine.state3.h))
        self.le_H4.setText("{:0.2f}".format(self.rankine.state4.h))
        self.le_TurbineWork.setText("{:0.2f}".format(self.rankine.turbine_work))
        self.le_PumpWork.setText("{:0.2f}".format(self.rankine.pump_work))
        self.le_HeatAdded.setText("{:0.2f}".format(self.rankine.heat_added))
        self.le_Efficiency.setText("{:0.2f}".format(eff))
        self.lbl_SatPropHigh.setText(SatPHigh.txtOut)
        self.lbl_SatPropLow.setText(SatPlow.txtOut)
        pass

    def SelectQualityOrTHigh(self):
        self.lbl_TurbineInletCondition.setText(("Turbine Inlet: {} =".format('x'if self.rdo_Quality.isChecked() else 'THigh')))

#if this module is being imported, this won't run. If it is the main module, it will run.
if __name__== '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.setWindowTitle('Rankine calculator')
    sys.exit(app.exec())