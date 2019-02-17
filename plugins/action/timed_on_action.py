import json
import logging
import datetime
from potnanny_core.models import (Trigger, OutletController, ActionPluginBase,
    FutureOutletAction)
from potnanny_core.database import db_session
from potnanny_core.utils import eval_condition

logger = logging.getLogger('potnanny.plugins.timed_on_action')

"""
TriggeredTimedOnAction

An action that will power an outlet on when a fault threshold is crossed, and
turn the outlet back off N minutes later.

"""
class TriggeredTimedOnAction(ActionPluginBase):
    action_name = 'outlet timed-on'

    def __init__(self, *args, **kwargs):
        self.on_condition = None
        self.on_minutes = 0
        self.outlet = None

        required = ['on_condition', 'on_minutes', 'outlet']
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
            'on_minutes': self.on_minutes,
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
        now = datetime.datetime.utcnow().replace(second=0, microsecond=0)
        trigger = None
        if parent.triggers:
            trigger = parent.triggers[0]


        def make_trigger():
            closed = now + datetime.timedelta(minutes=self.on_minutes)
            if parent.sleep_minutes:
                closed = closed + datetime.timedelta(minutes=parent.sleep_minutes)

            opts = {
                'action_id': parent.id,
                'created': now,
                'closed': closed,
            }

            t = Trigger(**opts)
            db_session.add(t)
            db_session.commit()


        if not trigger and eval_condition(meas.value, self.on_condition):
            oc = OutletController()
            result = oc.turn_on(self.outlet)
            if result:
                make_trigger()
                run_time = now + datetime.timedelta(minutes=self.on_minutes)
                fa = FutureOutletAction(
                    action='off',
                    outlet=json.dumps(self.outlet),
                    run_at=run_time,
                )
                db_session.add(fa)
                db_session.commit()

            return
