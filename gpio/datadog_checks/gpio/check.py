# Gpio Agent Check
# Add to '/etc/sudoers' to allow 'dd-agent' user to execute "sudo gpio readall" command : dd-agent ALL=NOPASSWD: /usr/bin/gpio
# wiringpi is also required (included with Raspbian)


try:
    from datadog_checks.base import AgentCheck
    from datadog_checks.base.utils.subprocess_output import get_subprocess_output
except ImportError:
    from checks import AgentCheck

__version__ = "1.0.0"

class GpioCheck(AgentCheck):

    # execute_gpio_readall runs the sub procees to obtain the output of "sudo gpio readall"
    def execute_gpio_readall(self):
        out, err, retcode = get_subprocess_output([ "sudo", "gpio", "readall"], self.log, raise_on_empty_output=True)
        if err:
            self.error("An error as occured, message:" + err)
        return out

    #  sanitize_output removes un-used lines from the output 
    def sanitize_output(output):
        lines = output.split('\n')
        del lines[0:3]
        del lines[len(lines)-4:len(lines)-1]
        pins = []
        for i in lines:
            pin_pair = i.split('||')
            pins.append(pin_pair[0])
            if(len(pin_pair) > 1):
                pins.append(pin_pair[1])
        return pins

    #  parse_pins creates a list of pin objects.
    #  The output is mirrored in two columns, this method creates a single list where all pins are in the correct orentation.
    def parse_pins(returned):
        pins = []
        LHS_set = returned[::2]
        RHS_set = returned
        RHS_set.pop(0)
        RHS_set = RHS_set[::2]
        for i in LHS_set:
            pin = i.split('|')
            if len(pin) > 2:
                pins.append(pin)
        for i in RHS_set:
            pin = i.split('|')
            pin.reverse()
            pins.append(pin)
        return pins

    # Main Method
    def check(self, instance):
        out = GpioCheck.execute_gpio_readall(self)
        returned = GpioCheck.sanitize_output(out)
        pins = GpioCheck.parse_pins(returned)
        for pin in pins:
            pin_state = pin[5].strip()
            if pin_state == '1' or pin_state =='0':
                name = pin[3].strip()
                mode = pin[4].strip()
                physical = pin[6].strip()
                BCM = pin[1].strip()
                wPi = pin[2].strip()
                self.gauge('gpio.' + name, pin_state, tags=['Physical:' + physical, 'BCM:' + BCM, 'wPi:' + wPi])