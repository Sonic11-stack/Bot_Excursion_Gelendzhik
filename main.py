from config import botExcursions
from base_commands import handles

@botExcursions.callback_query_handler(func=lambda call:True)
def response(function_call):
  if function_call.data in handles:
      handles[function_call.data](function_call.message.chat.id)
  botExcursions.answer_callback_query(function_call.id)
  
botExcursions.infinity_polling()