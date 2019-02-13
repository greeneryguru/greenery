import json
import logging
from potnanny.core.models import Trigger, OutletController, ActionPluginBase
from potnanny.core.database import db_session
from potnanny.core.utils import eval_condition

logger = logging.getLogger('potnanny.plugins.onoff_action')

"""
TriggeredOnOffAction

An action that will power an outlet on when a fault threshold is crossed, and
turn the outlet back off when a normal condition threshold is crossed.

"""
class TriggeredOnOffAction(ActionPluginBase):
    action_name = 'outlet on/off'

    def __init__(self, *args, **kwargs):
        self.on_condition = None
        self.off_condition = None
        self.outlet = None

        required = ['on_condition', 'off_condition', 'outlet']
        for k, v in kwargs.items():
            if k in required:
                setattr(self, k, v)

        for r in required:
            if getattr(self, r) is None:
                raise ValueError("{} must provide value for '{}'".format(
                    self.__name__, r))


    def __repr__(self):
        return json.dumps(self.as_dict())


    def as_dict(self):
        return {
            'class': self.__class__.__name__,
            'name': self.action_name,
            'on_condition': self.on_condition,
            'off_condition': self.off_condition,
            'outlet': self.outlet,
        }


    """
    eval a measurement value, see what actions, if any, it will trigger

    params:
        - the Action instance that is our parent
        - a Measurement instance
    returns:
        a dict of action details, or None
    """
    def handle_measurement(self, parent, meas):
        logger.debug("handling measurement {}, {}".format(parent, meas))
        now = datetime.datetime.utcnow().replace(second=0, microsecond=0)
        trigger = None
        if parent.triggers:
            trigger = parent.triggers[0]


        def make_trigger():
            opts = {
                'action_id': parent.id,
                'created': now,
            }
            if parent.sleep_minutes:
                opts['closed'] = now + datetime.timedelta(minutes=parent.sleep_minutes)

            t = Trigger(**opts)
            db_session.add(t)
            db_session.commit()


        if eval_condition(meas.value, self.on_condition):
            logger.debug("turning outlet '{}' ON".format(self.outlet))
            oc = OutletController()
            result = oc.turn_on(self.outlet)
            # create a trigger only if action was successful
            if result:
                if trigger is None:
                    make_trigger()

            return

        if eval_condition(meas.value, self.off_condition):
            logger.debug("turning outlet '{}' OFF".format(self.outlet))
            oc = OutletController()
            result = oc.turn_off(self.outlet)
            if result and trigger and trigger.closed == None:
                trigger.closed = now
                db_session.commit()

            return
