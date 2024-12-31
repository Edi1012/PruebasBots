# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa-pro/concepts/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []



from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionSumarNumeros(Action):
    def name(self) -> Text:
        return "action_sumar_numeros"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Obtener los números del tracker
        # numero1 = tracker.get_slot("numero1")

        numero1_slot = next(tracker.get_latest_entity_values("numero1"), None)
        print (f"numero1_slot: {numero1_slot}")

        numero1 = tracker.get_slot("numero1")
        print (f"numero1: {numero1}")

        numero1 = numero1 or numero1_slot

        numero2_slot = next(tracker.get_latest_entity_values("numero2"), None)
        print (f"numero2_slot: {numero2_slot}")

        numero2 = tracker.get_slot("numero2")
        print (f"numero2: {numero2}")

        numero2 = numero2 or numero2_slot
        
        if numero1 is None:
            dispatcher.utter_message(text="No puedo realizar la suma porque me falta el número 1.")
            return []
        
        if numero2 is None:
            dispatcher.utter_message(text="No puedo realizar la suma porque me falt el número 2.")
            return []

        # Convertir a flotante y realizar la suma
        resultado = float(numero1) + float(numero2)

        # Enviar el resultado al usuario
        dispatcher.utter_message(text=f"El resultado de sumar {numero1} y {numero2} es {resultado}.")

        # Guardar el resultado en un slot (opcional)
        return [SlotSet("resultado", resultado)]
