from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import sessionmaker

from model.models import Contract, Employee, Event, OperationFailed


class EventModelMixin:
    """Model Mixin to manage events data."""

    Session: sessionmaker

    def get_events(self, not_signed_filter: bool, not_paid_filter: bool) -> list[dict]:
        """Retrieve events from the database and return them as a list of dictionaries."""
        with self.Session() as session:
            if not not_paid_filter and not not_signed_filter:
                result = session.query(Event)
            else:
                result = session.query(Event).filter()  # to-do : add filters
            return [row.as_dict(full=False) for row in result]

    def detail_event(self, event_id: int) -> dict:
        """Retrieve a given event from the database and return it as a dictionary."""
        with self.Session() as session:
            event = Event.get(session, event_id)
            return event.as_dict()

    def add_event(self, contract_uuid: UUID, name: str, employee_id: int) -> dict:
        """Add a new event to the database (and return it as a dictionary)."""
        with self.Session() as session:
            connected_employee = Employee.get(session, employee_id=employee_id)
            contract = Contract.get(session, contract_uuid)
            if not contract.signed:
                raise OperationFailed(f"Impossible to create an event for the unsigned contrat {contract_uuid}.")
            if contract.customer.commercial_contact != connected_employee:
                raise OperationFailed(
                    f"The employee {connected_employee} does not have the permission to add events to "
                    f"{contract.customer} contracts (linked to {contract.customer.commercial_contact})."
                )
            event = Event(contract_id=contract_uuid, name=name)
            session.add(event)
            session.commit()
            return event.as_dict()

    def set_event_support(self, event_id: int, support_username: str) -> dict:
        """Update the support associated to the event in database (and return the event as a dictionary)."""
        with self.Session() as session:
            support = Employee.get(session, username=support_username)
            if support.role.name.upper() != self.roles.SUPPORT.name.upper():  # temp
                raise OperationFailed(
                    f"The employee {support} assigned to support the event is not a support ({support.role})."
                )
            event = Event.get(session, event_id)
            event.support_contact = support
            session.add(event)
            session.commit()
            return event.as_dict()

    def update_event(
        self,
        event_id: int,
        name: Optional[str],
        start: Optional[datetime],
        end: Optional[datetime],
        attendees: Optional[int],
        location: Optional[str],
        note: Optional[str],
        employee_id: int,
    ) -> dict:
        """Update event fields in database (and return the event as a dictionary)."""
        with self.Session() as session:
            connected_employee = Employee.get(session, employee_id=employee_id)
            event = Event.get(session, event_id)
            if event.support_contact_id != connected_employee.id:
                raise OperationFailed(
                    f'The employee {connected_employee} does not have the permission manage the event "{event}" '
                    f"(linked to {event.support_contact})."
                )
            if name:
                event.name = name
            if start:
                event.start = start
            if end:
                event.end = end
            if attendees:
                event.attendees = attendees
            if location:
                event.location = location
            if note:
                event.note = note
            session.add(event)
            session.commit()
            return event.as_dict()
