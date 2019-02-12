from potnanny.extensions import db
from sqlalchemy import func


# RF Interface Settings
class RFISetting(db.Model):
    __tablename__ = 'rfi_settings'

    id = db.Column(db.Integer, primary_key=True)

    # settings for primitive rf send/rcv only
    pulse_width = db.Column(db.Integer, nullable=False, default=180)
    scan_seconds = db.Column(db.Integer, nullable=False, default=10)
    tx_pin = db.Column(db.Integer, nullable=False, default=0)
    rx_pin = db.Column(db.Integer, nullable=False, default=2)

    spi_enable = db.Column(db.Boolean, nullable=False, default=False)
    created = db.Column(db.DateTime, default=func.now())


# RF Interface Manager
class RFIManager(object):
    def __init__(self):
        obj = RFISetting.query.get(1)
        if not obj:
            obj = RFISetting()
            db.session.add(obj)
            db.session.commit()

        self.settings = obj
        self.rf_scan = '/var/www/ocats/bin/rf_scan'
        self.rf_send = '/var/www/ocats/bin/rf_send'


    def scan_code(self):
        if not self.settings.spi_enable:
            return self._primitive_scan(
                        self.settings.scan_seconds,
                        self.settings.rx_pin)
        else:
            return None


    def send_code(self, code):
        if not self.settings.spi_enable:
            return self._primitive_send(code)
        else:
            return None


    def _primitive_scan(self, seconds, pin=2, pulse_w=0):
        child = subprocess([self.rf_scan, seconds, pin, pulse_w],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE )
        output, errors = child.communicate()
        if child.returncode:
            return (child.returncode, errors)

        for line in output.splitlines():
            if re.search(r'^RF Scanner', line):
                continue

            if re.search(r'^\s*$', line):
                continue

            if re.search(r'^\d+\s+\d+\s+\d+', line):
                return (0, line)

        return (1, "unexpected failure")


    def _primitive_send(self, code):
        code, protocol, bits = code.split()
        child = subprocess(
                    [self.rf_send, code, protocol,
                        self.settings.pulse_width, self.settings.tx_pin],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE )
        output, errors = child.communicate()
        return (child.returncode, errors)


    def _spi_send(self, code):
        pass

    def _spi_scan(self):
        pass
