import wikipedia

wikipedia.set_lang('ru')
def get_wiki(query):
    try:
        if query == '/stop':
            return ("Вы вышли из раздела Wikipedia")
        else:
            result = wikipedia.summary(query)
            return result
    except:
        return '''По вашему запросу не чего не найдено.
        Введите корректное слово для поиска'''







