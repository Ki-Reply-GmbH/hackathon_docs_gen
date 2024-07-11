# Author: Daniel Hummel (d.hummel@reply.de)
# Company: Ki Reply GmbH
# Version: 1.0
#
# License: This program is licensed under the GNU General Public License version 3.
# The full license can be found in the LICENSE file or at https://www.gnu.org/licenses/gpl-3.0.en.html.
#
from typing import List


class Observer:
    """
    Observer interface
    """

    def update(self, event_type: str, data):
        """
        Updates the observer with the given data.

        :param event_type: Type of the observable event
        :type event_type: str
        :param data: The data to update the observer with.
        :type data: dict
        """
        _ = event_type, data
        raise NotImplementedError("update function is not implemented")


class Observable:
    """
    Observable interface
    """

    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        """
        Attaches an observer to the observable.

        :param observer: The observer to attach.
        :type observer: Observer
        """
        self._observers.append(observer)

    def detach(self, observer: Observer):
        """
        Detaches an observer from the observable.

        :param observer: The observer to detach.
        :type observer: Observer
        """
        self._observers.remove(observer)

    def notify(self, event_type: str, data=None):
        """
        Notifies all observers of the observable.

        :param event_type: Type of the observable event
        :type event_type: str
        :param data: The data to notify the observers with.
        :type data: dict
        """
        for observer in self._observers:
            observer.update(event_type, data)