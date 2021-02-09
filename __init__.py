from modules.core.props import Property, StepProperty
from modules.core.step import StepBase
from modules import cbpi

@cbpi.step
class ChangeKettleTargetTemp(StepBase):
    '''
    Just put the decorator @cbpi.step on top of a method
    '''
    # Properties
    temp = Property.Number("Temperature", configurable=True, description="Target Temperature")
    kettle = StepProperty.Kettle("Kettle", description="Kettle in which the target temperature will change")

    def init(self):
        '''
        Initialize Step. This method is called once at the beginning of the step
        :return:
        '''
        # set target temp
        self.set_target_temp(self.temp, self.kettle)

    @cbpi.action("Start Timer Now")
    def start(self):
        '''
        Custom Action which can be execute form the brewing dashboard.
        All method with decorator @cbpi.action("YOUR CUSTOM NAME") will be available in the user interface
        :return:
        '''

        if self.is_timer_finished() is None:
            self.start_timer(int(self.timer))

    def reset(self):
        self.stop_timer()
        self.set_target_temp(self.temp, self.kettle)

    def finish(self):
        self.set_target_temp(self.temp, self.kettle)

    def execute(self):
        '''
        This method is execute in an interval
        :return:
        '''

        kettles = cbpi.cache["kettle"]
        kettle_name = kettles[int(self.kettle)].name
        
        self.notify("Changed target temp for %s " % (kettle_name), "New target temp is: %s C" % (self.temp), timeout=10000)
        self.next()
