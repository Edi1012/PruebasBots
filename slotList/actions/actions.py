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

class ActionAddItem(Action):  
    # Esta es la definición de una clase personalizada que hereda de `Action`, lo que significa que se trata de una acción personalizada en Rasa.

    def name(self) -> Text:
        # Define el nombre de la acción. Este nombre debe coincidir con el que se registre en `domain.yml`.
        return "action_add_item"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Este método ejecuta la lógica de la acción. 
        # `dispatcher` se utiliza para enviar mensajes al usuario.
        # `tracker` permite acceder a información de la conversación, como los slots y entidades detectadas.
        # `domain` contiene la configuración del dominio del bot.

        item = next(tracker.get_latest_entity_values("item"), None)
        # Obtiene el valor más reciente de la entidad `item` proporcionada por el usuario.
        # Si no se encuentra la entidad, devuelve `None`.

        if item:
            # Verifica si se obtuvo un valor válido para la entidad `item`.
            shopping_list = tracker.get_slot("shopping_list") or []
            # Recupera el valor actual del slot `shopping_list`. 
            # Si el slot está vacío o no tiene valor, lo inicializa como una lista vacía.

            shopping_list.append(item)
            # Agrega el elemento detectado (entidad `item`) a la lista de compras.

            dispatcher.utter_message(text=f"{item} ha sido agregado a la lista de compras.")
            # Envía un mensaje al usuario confirmando que el elemento fue agregado a la lista.

            return [{"shopping_list": shopping_list}]
            # Actualiza el valor del slot `shopping_list` con la lista actualizada 
            # y lo devuelve para que Rasa lo almacene.

        else:
            # Si no se encuentra ningún valor válido para la entidad `item`:
            dispatcher.utter_message(text="No entendí qué elemento deseas agregar.")
            # Envía un mensaje al usuario indicando que no entendió su solicitud.

            return []
            # No actualiza ningún slot, ya que no se recibió un elemento válido.


class ActionRemoveItem(Action):
    def name(self) -> Text:
        return "action_remove_item"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        item = next(tracker.get_latest_entity_values("item"), None)
        shopping_list = tracker.get_slot("shopping_list") or []
        if item and item in shopping_list:
            shopping_list.remove(item)
            dispatcher.utter_message(text=f"{item} ha sido eliminado de la lista de compras.")
            return [{"shopping_list": shopping_list}]
        else:
            dispatcher.utter_message(text="No encontré ese elemento en tu lista.")
            return []

class ActionShowList(Action):
    def name(self) -> Text:
        return "action_show_list"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        shopping_list = tracker.get_slot("shopping_list") or []
        if shopping_list:

            item_count = len(shopping_list)
            dispatcher.utter_message(text=f"Tienes {item_count} elemento(s) en tu lista.")
            dispatcher.utter_message(text=f"Esto es lo que tienes en tu lista de compras: {', '.join(shopping_list)}")
        else:
            dispatcher.utter_message(text="Tu lista de compras está vacía.")
        return []
